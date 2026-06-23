#!/usr/bin/env python3
"""Generate Ascendant gear balance outlier and rarity consistency reports."""

from __future__ import annotations

import json
import pathlib
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "config/ascendant_balance"
DOCS_DIR = ROOT / "docs"

GEAR_COLLECTIONS = ("weapons", "armor", "shields", "magic_items", "spells", "accessories_relics")
COMBAT_COLLECTIONS = {"weapons", "armor", "shields", "magic_items", "accessories_relics"}

RARITY_ORDER = {
    "common": 0,
    "uncommon": 1,
    "rare": 2,
    "epic": 3,
    "legendary": 4,
    "mythic": 5,
    "ascendant": 6,
}

RARITY_PROGRESSIONS = {
    "common": ("unranked", "tier_0_baseline", "center"),
    "uncommon": ("e_rank", "tier_1_early", "center_to_inner"),
    "rare": ("d_rank", "tier_2_regional", "inner_to_middle"),
    "epic": ("c_rank_to_b_rank", "tier_3_advanced", "middle"),
    "legendary": ("b_rank_to_a_rank", "tier_4_boss", "outer"),
    "mythic": ("a_rank_to_s_rank", "tier_5_dragon", "outer_to_edge"),
    "ascendant": ("s_rank", "tier_6_ascendant", "edge"),
}

OUTLIER_CLASSES = (
    "underpowered_for_rarity",
    "overpowered_for_rarity",
    "missing_stat_data",
    "missing_loot_context",
    "missing_recipe_context",
    "boss_reward_candidate",
    "rank_gate_candidate",
    "manual_review_required",
)

SPECIAL_ABILITY_TERMS = (
    "ability",
    "ancient",
    "ascendant",
    "boss",
    "capstone",
    "chase",
    "combat-defining",
    "dragon",
    "effect",
    "legendary",
    "major",
    "mythic",
    "relic",
    "soulslike",
    "spell",
    "summon",
    "unique",
    "utility",
)

HIGH_POWER_TERMS = (
    "annihilator",
    "ancient",
    "ascendant",
    "boss",
    "cataclysm",
    "chaos",
    "dead_king",
    "dragon",
    "dread",
    "elder",
    "legendary",
    "lord",
    "moonlight",
    "mythic",
    "netherite",
    "phylactery",
    "soul",
    "wither",
)

ABILITY_FLAG_TERMS = {
    "mobility": (
        "boots",
        "dash",
        "dashers",
        "elytra",
        "flamingo",
        "flippers",
        "hook",
        "jump",
        "piston",
        "running",
        "shoes",
        "slippers",
        "speed",
        "step",
        "umbrella",
        "wing",
        "wings",
    ),
    "survival": (
        "antidote",
        "beef",
        "charm",
        "heart",
        "necklace",
        "obsidian_skull",
        "panic",
        "pendant",
        "scarf",
        "skull",
        "steak",
        "totem",
        "vessel",
    ),
    "stealth_or_vision": (
        "goggles",
        "invisibility",
        "night_vision",
        "scarf_of_invisibility",
    ),
    "resource_or_utility": (
        "claws",
        "compass",
        "forge",
        "glove",
        "ink",
        "pouch",
        "ring",
        "scroll",
        "spell_book",
        "talisman",
        "wand",
    ),
}

STAT_POLICY = {
    "status": "audit_control_scaffold_only_no_stat_changes",
    "rules": [
        "Do not nerf blindly.",
        "Prefer rank, loot, and recipe placement before stat edits.",
        "Powerful iconic items should move later in progression before losing identity.",
        "Weak but flavorful items can stay early, cosmetic, collector, or story loot.",
        "Missing stat exposure is a review finding, not proof that an item is weak.",
    ],
    "thresholds": {
        "low_rarity_high_stat": {
            "rarities": ["common", "uncommon"],
            "weapon_damage_at_least": 8.0,
            "weapon_range_at_least": 5.0,
            "weapon_multiplier_at_least": 1.5,
            "armor_score_at_least": 10.0,
            "shield_durability_at_least": 1500.0,
        },
        "rare_high_stat": {
            "rarities": ["rare"],
            "weapon_damage_at_least": 10.0,
            "weapon_range_at_least": 5.0,
            "weapon_multiplier_at_least": 1.7,
            "armor_score_at_least": 14.0,
            "shield_durability_at_least": 2500.0,
        },
        "high_rarity_low_stat": {
            "rarities": ["legendary", "mythic", "ascendant"],
            "weapon_damage_at_most": 5.0,
            "weapon_multiplier_at_most": 1.2,
            "weapon_range_at_most": 3.0,
            "armor_score_at_most": 5.0,
            "shield_durability_at_most": 400.0,
        },
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: pathlib.Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def parse_number(value: Any) -> float | None:
    if value in (None, "", {}, []):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value)
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else None


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, "", {}, []):
        return []
    return [value]


def first_nonempty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", {}, []):
            return value
    return None


def local_id(item_id: str) -> str:
    return item_id.split(":", 1)[-1]


def has_special_ability_note(entry: dict[str, Any]) -> bool:
    text_parts = [
        str(entry.get("id") or ""),
        str(entry.get("name") or ""),
        str(entry.get("rarity_reason") or ""),
        json.dumps(entry.get("tags", ""), sort_keys=True),
        json.dumps(entry.get("evidence", ""), sort_keys=True),
        json.dumps(entry.get("notes", ""), sort_keys=True),
    ]
    text = " ".join(text_parts).lower()
    return any(term in text for term in SPECIAL_ABILITY_TERMS)


def high_power_theme(entry: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(entry.get("id") or ""),
            str(entry.get("name") or ""),
            str(entry.get("source_mod") or ""),
            str(entry.get("rarity_reason") or ""),
        ]
    ).lower()
    return any(term in text for term in HIGH_POWER_TERMS)


def ability_flags(entry: dict[str, Any]) -> list[str]:
    text = " ".join(
        [
            str(entry.get("id") or ""),
            str(entry.get("name") or ""),
            str(entry.get("rarity_reason") or ""),
            json.dumps(entry.get("tags", ""), sort_keys=True),
        ]
    ).lower()
    flags = [
        flag
        for flag, terms in ABILITY_FLAG_TERMS.items()
        if any(term in text for term in terms)
    ]
    return sorted(flags)


def stat_snapshot(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "damage": entry.get("damage"),
        "damage_number": parse_number(entry.get("damage")),
        "attack_speed": entry.get("attack_speed"),
        "attack_speed_number": parse_number(entry.get("attack_speed")),
        "armor": entry.get("armor"),
        "armor_number": parse_number(entry.get("armor")),
        "armor_toughness": entry.get("armor_toughness"),
        "armor_toughness_number": parse_number(entry.get("armor_toughness")),
        "durability": entry.get("durability"),
        "durability_number": parse_number(entry.get("durability")),
        "attack_range": entry.get("attack_range"),
        "attack_range_number": parse_number(entry.get("attack_range")),
        "max_damage_multiplier": entry.get("max_damage_multiplier"),
        "max_damage_multiplier_number": parse_number(entry.get("max_damage_multiplier")),
        "damage_status": entry.get("damage_status"),
    }


def armor_score(snapshot: dict[str, Any]) -> float | None:
    armor = snapshot.get("armor_number")
    toughness = snapshot.get("armor_toughness_number")
    if armor is None and toughness is None:
        return None
    return float(armor or 0) + float(toughness or 0) * 2


def has_exposed_power_stat(snapshot: dict[str, Any], collections: set[str]) -> bool:
    if "spells" in collections:
        return True
    keys = ["damage_number", "attack_range_number", "max_damage_multiplier_number"]
    if collections & {"armor", "magic_items", "accessories_relics"}:
        keys.extend(["armor_number", "armor_toughness_number"])
    if "shields" in collections:
        keys.append("durability_number")
    return any(snapshot.get(key) is not None for key in keys)


def expected_stat_missing(snapshot: dict[str, Any], collections: set[str]) -> bool:
    if "spells" in collections:
        return False
    if "weapons" in collections and snapshot.get("damage_number") is None and snapshot.get("max_damage_multiplier_number") is None:
        return True
    if "armor" in collections and snapshot.get("armor_number") is None and snapshot.get("armor_toughness_number") is None:
        return True
    if "shields" in collections and snapshot.get("durability_number") is None and snapshot.get("max_damage_multiplier_number") is None:
        return True
    if collections & {"magic_items", "accessories_relics"}:
        return not has_exposed_power_stat(snapshot, collections)
    return False


def is_low_rarity_high_stat(rarity: str, snapshot: dict[str, Any], collections: set[str]) -> bool:
    order = RARITY_ORDER.get(rarity, 0)
    damage = snapshot.get("damage_number")
    attack_range = snapshot.get("attack_range_number")
    multiplier = snapshot.get("max_damage_multiplier_number")
    durability = snapshot.get("durability_number")
    score = armor_score(snapshot)
    if order <= RARITY_ORDER["uncommon"]:
        return any(
            [
                damage is not None and damage >= 8,
                attack_range is not None and attack_range >= 5,
                multiplier is not None and multiplier >= 1.5,
                score is not None and score >= 10,
                "shields" in collections and durability is not None and durability >= 1500,
            ]
        )
    if order == RARITY_ORDER["rare"]:
        return any(
            [
                damage is not None and damage >= 10,
                attack_range is not None and attack_range >= 5 and multiplier is not None and multiplier >= 1.5,
                multiplier is not None and multiplier >= 1.7,
                score is not None and score >= 14,
                "shields" in collections and durability is not None and durability >= 2500,
            ]
        )
    return False


def is_high_rarity_low_stat_without_note(rarity: str, snapshot: dict[str, Any], collections: set[str], entry: dict[str, Any]) -> bool:
    if RARITY_ORDER.get(rarity, 0) < RARITY_ORDER["legendary"]:
        return False
    if not has_exposed_power_stat(snapshot, collections):
        return False
    if has_special_ability_note(entry):
        return False
    if "weapons" in collections or "magic_items" in collections or "accessories_relics" in collections:
        damage = snapshot.get("damage_number")
        multiplier = snapshot.get("max_damage_multiplier_number")
        attack_range = snapshot.get("attack_range_number")
        if damage is not None:
            return damage <= 5 and (multiplier is None or multiplier <= 1.2) and (attack_range is None or attack_range <= 3)
    if "armor" in collections:
        score = armor_score(snapshot)
        if score is not None:
            return score <= 5
    if "shields" in collections:
        durability = snapshot.get("durability_number")
        if durability is not None:
            return durability <= 400
    return False


def load_gear_entries(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for collection in GEAR_COLLECTIONS:
        for entry in registry.get(collection, []):
            if not isinstance(entry, dict) or not entry.get("id"):
                continue
            item_id = str(entry["id"])
            merged = by_id.setdefault(
                item_id,
                {
                    "id": item_id,
                    "collections": [],
                    "entries": [],
                },
            )
            merged["collections"].append(collection)
            merged["entries"].append(entry)
    for item_id, merged in by_id.items():
        entries = merged["entries"]
        primary = entries[0]
        merged["primary_collection"] = merged["collections"][0]
        merged["name"] = first_nonempty(*(entry.get("name") for entry in entries)) or item_id
        merged["source_mod"] = first_nonempty(*(entry.get("source_mod") for entry in entries)) or item_id.split(":", 1)[0]
        merged["mod_id"] = first_nonempty(*(entry.get("mod_id") for entry in entries)) or item_id.split(":", 1)[0]
        merged["rarity"] = str(first_nonempty(*(entry.get("rarity") for entry in entries)) or "common").lower()
        merged["rarity_color"] = first_nonempty(*(entry.get("rarity_color") for entry in entries))
        merged["rarity_reason"] = first_nonempty(*(entry.get("rarity_reason") for entry in entries)) or ""
        merged["tags"] = first_nonempty(*(entry.get("tags") for entry in entries))
        merged["evidence"] = first_nonempty(*(entry.get("evidence") for entry in entries))
        merged["notes"] = first_nonempty(*(entry.get("notes") for entry in entries))
        merged["stat_entry"] = choose_stat_entry(entries)
        merged["stat_snapshot"] = stat_snapshot(merged["stat_entry"])
        merged["registry_link"] = {
            "gear_registry_id": item_id,
            "collections": merged["collections"],
            "primary_collection": merged["primary_collection"],
        }
        if not primary.get("rarity") or not primary.get("rarity_color"):
            merged["missing_rarity_or_border"] = True
        else:
            merged["missing_rarity_or_border"] = False
    return by_id


def choose_stat_entry(entries: list[dict[str, Any]]) -> dict[str, Any]:
    best = entries[0]
    best_score = -1
    for entry in entries:
        snapshot = stat_snapshot(entry)
        score = sum(1 for key, value in snapshot.items() if key.endswith("_number") and value is not None)
        if score > best_score:
            best = entry
            best_score = score
    return best


def build_recipe_maps(recipe_policy: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    recipes_by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    indexed_policy: dict[str, dict[str, Any]] = {}
    for entry in recipe_policy.get("major_recipe_entries", []) if isinstance(recipe_policy, dict) else []:
        if isinstance(entry, dict) and entry.get("item_id"):
            recipes_by_item[str(entry["item_id"])].append(entry)
    for entry in recipe_policy.get("indexed_item_policy", []) if isinstance(recipe_policy, dict) else []:
        if isinstance(entry, dict) and entry.get("item_id"):
            indexed_policy[str(entry["item_id"])] = entry
    return recipes_by_item, indexed_policy


def build_loot_map(loot_policy: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    loot_by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source in loot_policy.get("loot_sources", []) if isinstance(loot_policy, dict) else []:
        if not isinstance(source, dict):
            continue
        for item_id in source.get("output_item_ids", []) or []:
            if item_id:
                loot_by_item[str(item_id)].append(source)
    return loot_by_item


def build_magic_progression() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path, key in [
        (ROOT / "config/ascendant_magic/spell_progression_registry.json", "spells"),
        (ROOT / "config/ascendant_magic/magic_item_progression_registry.json", "magic_items"),
    ]:
        data = read_json(path, {})
        if not isinstance(data, dict):
            continue
        for entry in data.get(key, []):
            if isinstance(entry, dict) and entry.get("id"):
                rows[str(entry["id"])] = entry
    return rows


def progression_for(
    item_id: str,
    rarity: str,
    recipe_indexed_policy: dict[str, dict[str, Any]],
    magic_progression: dict[str, dict[str, Any]],
) -> tuple[str, str, str, str]:
    magic = magic_progression.get(item_id)
    if magic:
        return (
            str(magic.get("guild_rank_tier") or RARITY_PROGRESSIONS.get(rarity, RARITY_PROGRESSIONS["common"])[0]),
            str(magic.get("allowed_loot_tier") or RARITY_PROGRESSIONS.get(rarity, RARITY_PROGRESSIONS["common"])[1]),
            str(magic.get("atlas_distance_ring") or RARITY_PROGRESSIONS.get(rarity, RARITY_PROGRESSIONS["common"])[2]),
            "ascendant_magic_policy",
        )
    recipe = recipe_indexed_policy.get(item_id)
    if recipe:
        return (
            str(recipe.get("intended_guild_rank") or RARITY_PROGRESSIONS.get(rarity, RARITY_PROGRESSIONS["common"])[0]),
            str(recipe.get("intended_recipe_tier") or RARITY_PROGRESSIONS.get(rarity, RARITY_PROGRESSIONS["common"])[1]),
            str(recipe.get("intended_atlas_distance_ring") or RARITY_PROGRESSIONS.get(rarity, RARITY_PROGRESSIONS["common"])[2]),
            "ascendant_recipe_policy",
        )
    rank, tier, ring = RARITY_PROGRESSIONS.get(rarity, RARITY_PROGRESSIONS["common"])
    return rank, tier, ring, "derived_from_current_rarity"


def classify_entry(
    item: dict[str, Any],
    recipes: list[dict[str, Any]],
    loot_sources: list[dict[str, Any]],
) -> tuple[list[str], list[str], str]:
    classes: set[str] = set()
    reasons: list[str] = []
    collections = set(item["collections"])
    rarity = str(item["rarity"])
    snapshot = item["stat_snapshot"]

    if item.get("missing_rarity_or_border"):
        classes.add("manual_review_required")
        reasons.append("Missing rarity or Item Borders color in gear_registry.")

    if expected_stat_missing(snapshot, collections):
        classes.add("missing_stat_data")
        reasons.append("Relevant combat/defense stats are not exposed in scanned registry data.")

    if is_low_rarity_high_stat(rarity, snapshot, collections):
        classes.add("overpowered_for_rarity")
        classes.add("rank_gate_candidate")
        reasons.append("Exposed stat value exceeds current low-rarity policy threshold.")

    if is_high_rarity_low_stat_without_note(rarity, snapshot, collections, item):
        classes.add("underpowered_for_rarity")
        reasons.append("High-rarity item has weak exposed stats and no obvious special ability note.")

    if RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"] and not loot_sources:
        classes.add("missing_loot_context")
        reasons.append("High-rarity item has no scanned direct loot source; acquisition placement needs review.")

    if RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"] and not recipes:
        classes.add("missing_recipe_context")
        reasons.append("High-rarity item has no scanned recipe context; confirm it is intentionally loot/drop/boss-only.")

    risky_recipes = [recipe for recipe in recipes if str(recipe.get("recipe_status") or "") in {"bypass", "too_cheap", "needs_manual_review"}]
    if risky_recipes and RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["epic"]:
        classes.add("rank_gate_candidate")
        classes.add("manual_review_required")
        reasons.append("Recipe audit marks one or more recipes as bypass, too cheap, or needing manual review.")

    low_tier_loot = [
        source
        for source in loot_sources
        if str(source.get("loot_context") or "") in {"village", "settlement", "minor_ruin", "mob"}
        and RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"]
    ]
    if low_tier_loot:
        classes.add("rank_gate_candidate")
        classes.add("manual_review_required")
        reasons.append("High-rarity item appears in low-tier loot context.")

    if RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"] and high_power_theme(item):
        classes.add("boss_reward_candidate")
        reasons.append("High-rarity item has boss, dragon, soul, ancient, or capstone identity.")

    flags = ability_flags(item)
    if flags and collections & {"accessories_relics", "magic_items"}:
        classes.add("manual_review_required")
        reasons.append(f"Potential high-impact ability flags detected: {', '.join(flags)}.")
        if RARITY_ORDER.get(rarity, 0) <= RARITY_ORDER["rare"] and any(
            flag in flags for flag in ("mobility", "survival", "stealth_or_vision")
        ):
            classes.add("rank_gate_candidate")
            reasons.append("Low/mid-rarity mobility, survival, or stealth utility may need rank or loot placement review.")

    if classes and "manual_review_required" not in classes:
        classes.add("manual_review_required")

    if not classes:
        return [], [], "keep_current_rarity_and_stats"
    action = "prefer_progression_placement_review_before_stat_changes"
    if "missing_stat_data" in classes and len(classes) == 2 and "manual_review_required" in classes:
        action = "improve_stat_exposure_or_manual_verify"
    return sorted(classes, key=lambda value: OUTLIER_CLASSES.index(value)), reasons, action


def build_reports() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    registry = read_json(ROOT / "config/ascendant_index/gear_registry.json", {})
    if not isinstance(registry, dict):
        raise RuntimeError("config/ascendant_index/gear_registry.json must be a JSON object")

    gear_by_id = load_gear_entries(registry)
    recipe_policy = read_json(ROOT / "config/ascendant_recipes/recipe_progression_policy.json", {})
    recipes_by_item, recipe_indexed_policy = build_recipe_maps(recipe_policy if isinstance(recipe_policy, dict) else {})
    loot_policy = read_json(ROOT / "config/ascendant_loot/loot_policy.json", {})
    loot_by_item = build_loot_map(loot_policy if isinstance(loot_policy, dict) else {})
    magic_progression = build_magic_progression()

    balance_entries: list[dict[str, Any]] = []
    outliers: list[dict[str, Any]] = []
    review_entries: list[dict[str, Any]] = []

    for item_id in sorted(gear_by_id):
        item = gear_by_id[item_id]
        rarity = str(item["rarity"])
        recipes = recipes_by_item.get(item_id, [])
        loot_sources = loot_by_item.get(item_id, [])
        rank, progression_tier, atlas_ring, progression_source = progression_for(
            item_id,
            rarity,
            recipe_indexed_policy,
            magic_progression,
        )
        classes, reasons, action = classify_entry(item, recipes, loot_sources)
        recipe_statuses = sorted({str(recipe.get("recipe_status") or "unknown") for recipe in recipes})
        loot_contexts = sorted({str(source.get("loot_context") or "unknown") for source in loot_sources})
        entry = {
            "item_id": item_id,
            "name": item["name"],
            "source_mod": item["source_mod"],
            "collections": item["collections"],
            "primary_collection": item["primary_collection"],
            "rarity": rarity,
            "rarity_color": item.get("rarity_color"),
            "rarity_reason": item.get("rarity_reason"),
            "guild_rank_tier": rank,
            "progression_tier": progression_tier,
            "atlas_distance_ring": atlas_ring,
            "progression_source": progression_source,
            "stat_snapshot": item["stat_snapshot"],
            "ability_flags": ability_flags(item),
            "has_special_ability_note": has_special_ability_note(item),
            "loot_contexts": loot_contexts,
            "loot_source_count": len(loot_sources),
            "recipe_statuses": recipe_statuses,
            "recipe_count": len(recipes),
            "outlier_classes": classes,
            "recommended_action": action,
            "registry_link": item["registry_link"],
        }
        balance_entries.append(entry)
        if classes:
            outlier = {
                "outlier_id": f"gear_balance/{re.sub(r'[^a-z0-9_./-]+', '_', item_id.lower())}",
                "item_id": item_id,
                "name": item["name"],
                "source_mod": item["source_mod"],
                "collections": item["collections"],
                "rarity": rarity,
                "classifications": classes,
                "reasons": reasons,
                "stat_snapshot": item["stat_snapshot"],
                "ability_flags": ability_flags(item),
                "guild_rank_tier": rank,
                "progression_tier": progression_tier,
                "atlas_distance_ring": atlas_ring,
                "loot_contexts": loot_contexts,
                "recipe_statuses": recipe_statuses,
                "recommended_action": action,
                "registry_link": item["registry_link"],
            }
            outliers.append(outlier)
            if any(cls in classes for cls in ("underpowered_for_rarity", "overpowered_for_rarity", "rank_gate_candidate", "boss_reward_candidate")):
                review_entries.append(
                    {
                        "item_id": item_id,
                        "name": item["name"],
                        "current_rarity": rarity,
                        "collections": item["collections"],
                        "review_reasons": classes,
                        "review_direction": rarity_review_direction(classes),
                        "preferred_first_fix": "rank_loot_recipe_placement_before_stats",
                        "registry_link": item["registry_link"],
                    }
                )

    outliers.sort(key=outlier_sort_key)
    review_entries.sort(key=review_sort_key)

    known_ids = set(gear_by_id)
    policy_ids = {entry["item_id"] for entry in balance_entries}
    high_stat_low = [entry for entry in balance_entries if "overpowered_for_rarity" in entry["outlier_classes"]]
    low_stat_high = [entry for entry in balance_entries if "underpowered_for_rarity" in entry["outlier_classes"]]
    missing_progression = [entry for entry in balance_entries if not entry.get("progression_tier")]

    stat_policy = {
        "version": 1,
        "generated_at": now_iso(),
        **STAT_POLICY,
        "source": {
            "gear_registry": "config/ascendant_index/gear_registry.json",
            "loot_policy": "config/ascendant_loot/loot_policy.json",
            "recipe_policy": "config/ascendant_recipes/recipe_progression_policy.json",
            "magic_policy": "config/ascendant_magic/*.json",
        },
        "balance_policy_entries": balance_entries,
        "validation": {
            "gear_registry_generated_at": registry.get("generated_at"),
            "gear_registry_entry_count": sum(len(registry.get(collection, [])) for collection in GEAR_COLLECTIONS),
            "gear_registry_unique_item_ids": len(known_ids),
            "balance_policy_item_ids": len(policy_ids),
            "gear_index_missing_balance_policy": sorted(known_ids - policy_ids),
            "balance_policy_unknown_item_ids": sorted(policy_ids - known_ids),
            "items_without_progression_tier": [entry["item_id"] for entry in missing_progression],
            "high_stat_low_rarity": [entry["item_id"] for entry in high_stat_low],
            "low_stat_high_rarity_no_special_ability_note": [entry["item_id"] for entry in low_stat_high],
            "outlier_list_stale": False,
        },
        "summary": {
            "balance_policy_entries": len(balance_entries),
            "outlier_items": len(outliers),
            "rarity_review_queue": len(review_entries),
            "by_rarity": dict(Counter(entry["rarity"] for entry in balance_entries)),
            "by_collection_membership": dict(Counter(collection for entry in balance_entries for collection in entry["collections"])),
            "by_outlier_class": dict(Counter(cls for entry in balance_entries for cls in entry["outlier_classes"])),
        },
    }

    gear_outliers = {
        "version": 1,
        "generated_at": now_iso(),
        "status": "audit_outlier_report_only_no_stat_changes",
        "source": stat_policy["source"],
        "outlier_classes": list(OUTLIER_CLASSES),
        "outliers": outliers,
        "validation": {
            "gear_registry_unique_item_ids": len(known_ids),
            "outlier_item_ids": sorted({entry["item_id"] for entry in outliers}),
            "outlier_list_stale": False,
            "unknown_item_ids": sorted({entry["item_id"] for entry in outliers} - known_ids),
        },
        "summary": {
            "outlier_items": len(outliers),
            "by_classification": dict(Counter(cls for entry in outliers for cls in entry["classifications"])),
            "by_rarity": dict(Counter(entry["rarity"] for entry in outliers)),
            "by_primary_collection": dict(Counter(entry["collections"][0] for entry in outliers)),
        },
    }

    rarity_review_queue = {
        "version": 1,
        "generated_at": now_iso(),
        "status": "audit_review_queue_only_no_rarity_regeneration",
        "rules": [
            "Do not regenerate rarity blindly.",
            "Use this queue to review item placement, loot, recipes, and rank before changing rarity labels.",
            "Any rarity change must preserve Item Borders color and tooltip consistency.",
        ],
        "review_entries": review_entries,
        "validation": {
            "gear_registry_unique_item_ids": len(known_ids),
            "review_item_ids": sorted({entry["item_id"] for entry in review_entries}),
            "unknown_item_ids": sorted({entry["item_id"] for entry in review_entries} - known_ids),
            "outlier_list_stale": False,
        },
        "summary": {
            "review_entries": len(review_entries),
            "by_current_rarity": dict(Counter(entry["current_rarity"] for entry in review_entries)),
            "by_review_direction": dict(Counter(entry["review_direction"] for entry in review_entries)),
        },
    }

    return gear_outliers, rarity_review_queue, stat_policy


def rarity_review_direction(classes: list[str]) -> str:
    if "overpowered_for_rarity" in classes:
        return "check_if_rarity_or_rank_should_increase"
    if "underpowered_for_rarity" in classes:
        return "check_if_rarity_should_decrease_or_item_should_be_collector_cosmetic"
    if "boss_reward_candidate" in classes:
        return "keep_or_raise_progression_placement_before_stats"
    if "rank_gate_candidate" in classes:
        return "keep_rarity_but_move_later_or_gate"
    return "manual_review"


def outlier_sort_key(entry: dict[str, Any]) -> tuple[int, int, str]:
    classes = set(entry.get("classifications", []))
    if "overpowered_for_rarity" in classes:
        severity = 0
    elif "underpowered_for_rarity" in classes:
        severity = 1
    elif "rank_gate_candidate" in classes and "boss_reward_candidate" in classes:
        severity = 2
    elif "rank_gate_candidate" in classes:
        severity = 3
    elif "boss_reward_candidate" in classes:
        severity = 4
    elif "missing_loot_context" in classes or "missing_recipe_context" in classes:
        severity = 5
    else:
        severity = 6
    rarity_score = -RARITY_ORDER.get(str(entry.get("rarity") or "common"), 0)
    return (severity, rarity_score, str(entry.get("item_id") or ""))


def review_sort_key(entry: dict[str, Any]) -> tuple[int, int, str]:
    direction = str(entry.get("review_direction") or "")
    if direction == "check_if_rarity_or_rank_should_increase":
        severity = 0
    elif direction == "keep_rarity_but_move_later_or_gate":
        severity = 1
    elif direction == "keep_or_raise_progression_placement_before_stats":
        severity = 2
    else:
        severity = 3
    rarity_score = -RARITY_ORDER.get(str(entry.get("current_rarity") or "common"), 0)
    return (severity, rarity_score, str(entry.get("item_id") or ""))


def markdown_table(rows: list[list[Any]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return "\n".join(out)


def write_docs(gear_outliers: dict[str, Any], rarity_review_queue: dict[str, Any], stat_policy: dict[str, Any]) -> None:
    outliers = gear_outliers["outliers"]
    balance_entries = stat_policy["balance_policy_entries"]
    review_entries = rarity_review_queue["review_entries"]
    summary_rows = [
        ["Balance policy entries", stat_policy["summary"]["balance_policy_entries"]],
        ["Outlier items", gear_outliers["summary"]["outlier_items"]],
        ["Rarity review queue", rarity_review_queue["summary"]["review_entries"]],
        ["High-stat low-rarity items", len(stat_policy["validation"]["high_stat_low_rarity"])],
        ["Low-stat high-rarity items without ability note", len(stat_policy["validation"]["low_stat_high_rarity_no_special_ability_note"])],
        ["Items without progression tier", len(stat_policy["validation"]["items_without_progression_tier"])],
    ]
    outlier_rows = [
        [
            f"`{entry['item_id']}`",
            entry["rarity"],
            ", ".join(entry["collections"]),
            ", ".join(entry["classifications"]),
            entry["recommended_action"],
        ]
        for entry in outliers[:80]
    ]
    class_rows = [[key, value] for key, value in gear_outliers["summary"]["by_classification"].items()]
    write_text(
        DOCS_DIR / "GEAR_BALANCE_OUTLIER_REPORT.md",
        f"""# Gear Balance Outlier Report

Generated: {now_iso()}

## Status

This is a balance audit and outlier report only. It does not change item stats, regenerate rarity, edit loot, edit recipes, or enable gates.

## Summary

{markdown_table(summary_rows, ["Metric", "Count"])}

## Outlier Class Counts

{markdown_table(class_rows, ["Classification", "Count"])}

## Top Outlier Preview

{markdown_table(outlier_rows or [["None", "", "", "", ""]], ["Gear Registry ID", "Rarity", "Collections", "Classifications", "Preferred Action"])}

## Interpretation

- `missing_stat_data` means the registry could not expose enough numeric stats to judge the item safely.
- `overpowered_for_rarity` and `underpowered_for_rarity` are review flags, not automatic stat changes.
- `boss_reward_candidate` and `rank_gate_candidate` prefer placement changes before stat edits.
- All rows link back to `config/ascendant_index/gear_registry.json` by item ID.
""",
    )

    high_stat_rows = [
        [
            f"`{entry['item_id']}`",
            entry["rarity"],
            ", ".join(entry["collections"]),
            stat_brief(entry["stat_snapshot"]),
            entry["recommended_action"],
        ]
        for entry in balance_entries
        if "overpowered_for_rarity" in entry["outlier_classes"]
    ][:80]
    low_stat_rows = [
        [
            f"`{entry['item_id']}`",
            entry["rarity"],
            ", ".join(entry["collections"]),
            stat_brief(entry["stat_snapshot"]),
            entry["recommended_action"],
        ]
        for entry in balance_entries
        if "underpowered_for_rarity" in entry["outlier_classes"]
    ][:80]
    review_rows = [
        [
            f"`{entry['item_id']}`",
            entry["current_rarity"],
            ", ".join(entry["collections"]),
            entry["review_direction"],
        ]
        for entry in review_entries[:120]
    ]
    write_text(
        DOCS_DIR / "RARITY_CONSISTENCY_AUDIT.md",
        f"""# Rarity Consistency Audit

Generated: {now_iso()}

This audit compares current rarity labels against exposed stats and progression context. It does not regenerate rarity. Review current rarity, loot placement, recipe cost, and rank tier together before changing any label.

## Summary

{markdown_table(summary_rows, ["Metric", "Count"])}

## High-Stat Low-Rarity Items

{markdown_table(high_stat_rows or [["None", "", "", "", ""]], ["Gear Registry ID", "Rarity", "Collections", "Exposed Stats", "Preferred Action"])}

## Low-Stat High-Rarity Items Without Ability Note

{markdown_table(low_stat_rows or [["None", "", "", "", ""]], ["Gear Registry ID", "Rarity", "Collections", "Exposed Stats", "Preferred Action"])}

## Rarity Review Queue Preview

{markdown_table(review_rows or [["None", "", "", ""]], ["Gear Registry ID", "Current Rarity", "Collections", "Review Direction"])}
""",
    )

    risk_rows = [
        [
            f"`{entry['item_id']}`",
            entry["rarity"],
            entry["guild_rank_tier"],
            entry["progression_tier"],
            ", ".join(entry["loot_contexts"]) or "none",
            ", ".join(entry["recipe_statuses"]) or "none",
            ", ".join(entry["outlier_classes"]),
        ]
        for entry in balance_entries
        if entry["outlier_classes"]
    ][:120]
    write_text(
        DOCS_DIR / "GEAR_PROGRESSion_RISK_REGISTER.md",
        f"""# Gear Progression Risk Register

Generated: {now_iso()}

This register focuses on progression risk, not nerfs. If an item is powerful but iconic, move it later in rank, loot, recipe, boss, or bounty progression before changing its stats.

## Summary

{markdown_table(summary_rows, ["Metric", "Count"])}

## Progression Risk Preview

{markdown_table(risk_rows or [["None", "", "", "", "", "", ""]], ["Gear Registry ID", "Rarity", "Guild Rank", "Progression Tier", "Loot Contexts", "Recipe Statuses", "Risk Classes"])}

## Current Rule

Terrain is still not signed off. Balance reports are safe to review, but do not turn this into live loot, recipe, rank, or stat enforcement until Atlas land/water acceptance is complete.
""",
    )


def stat_brief(snapshot: dict[str, Any]) -> str:
    parts = []
    for key, label in [
        ("damage_number", "damage"),
        ("attack_speed_number", "speed"),
        ("armor_number", "armor"),
        ("armor_toughness_number", "toughness"),
        ("durability_number", "durability"),
        ("attack_range_number", "range"),
        ("max_damage_multiplier_number", "mult"),
    ]:
        value = snapshot.get(key)
        if value is not None:
            parts.append(f"{label}={value:g}")
    return ", ".join(parts) if parts else "not exposed"


def main() -> int:
    gear_outliers, rarity_review_queue, stat_policy = build_reports()
    write_json(OUT_DIR / "gear_outliers.json", gear_outliers)
    write_json(OUT_DIR / "rarity_review_queue.json", rarity_review_queue)
    write_json(OUT_DIR / "stat_policy.json", stat_policy)
    write_docs(gear_outliers, rarity_review_queue, stat_policy)
    print(f"Balance policy entries: {stat_policy['summary']['balance_policy_entries']}")
    print(f"Outlier items: {gear_outliers['summary']['outlier_items']}")
    print(f"Rarity review queue: {rarity_review_queue['summary']['review_entries']}")
    print(f"High-stat low-rarity: {len(stat_policy['validation']['high_stat_low_rarity'])}")
    print(f"Low-stat high-rarity without ability note: {len(stat_policy['validation']['low_stat_high_rarity_no_special_ability_note'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
