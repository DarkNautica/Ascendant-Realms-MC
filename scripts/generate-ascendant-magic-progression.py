#!/usr/bin/env python3
"""Generate the Ascendant magic progression audit and policy scaffold."""

from __future__ import annotations

import json
import os
import pathlib
import re
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
ACTIVE_INSTANCE = pathlib.Path(
    os.environ.get(
        "ASCENDANT_ACTIVE_INSTANCE",
        r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)",
    )
)
ACTIVE_MODS = ACTIVE_INSTANCE / "mods"

OUT_DIR = ROOT / "config/ascendant_magic"
DOCS_DIR = ROOT / "docs"
DISABLED_REVIEW_DIR = ROOT / "kubejs/server_scripts_disabled/review/ascendant_magic"

RARITY_ORDER = {
    "common": 0,
    "uncommon": 1,
    "rare": 2,
    "epic": 3,
    "legendary": 4,
    "mythic": 5,
    "ascendant": 6,
}

RARITY_POLICY = {
    "common": {
        "rank": "unranked",
        "loot_tier": "tier_0_baseline",
        "recipe_tier": "tier_0_baseline",
        "progression": "early",
        "ring": "center",
    },
    "uncommon": {
        "rank": "e_rank",
        "loot_tier": "tier_1_early",
        "recipe_tier": "tier_1_early",
        "progression": "early",
        "ring": "center_to_inner",
    },
    "rare": {
        "rank": "d_rank",
        "loot_tier": "tier_2_regional",
        "recipe_tier": "tier_2_regional",
        "progression": "mid",
        "ring": "inner_to_middle",
    },
    "epic": {
        "rank": "c_rank_to_b_rank",
        "loot_tier": "tier_3_advanced",
        "recipe_tier": "tier_3_advanced",
        "progression": "mid",
        "ring": "middle",
    },
    "legendary": {
        "rank": "b_rank_to_a_rank",
        "loot_tier": "tier_4_boss",
        "recipe_tier": "tier_4_boss",
        "progression": "late",
        "ring": "outer",
    },
    "mythic": {
        "rank": "a_rank_to_s_rank",
        "loot_tier": "tier_5_dragon",
        "recipe_tier": "tier_5_dragon",
        "progression": "endgame",
        "ring": "outer_to_edge",
    },
    "ascendant": {
        "rank": "s_rank",
        "loot_tier": "tier_6_ascendant",
        "recipe_tier": "tier_6_ascendant",
        "progression": "endgame",
        "ring": "edge",
    },
}

SCHOOL_POLICY = {
    "fire": {
        "atlas_region_affinity": ["sunreach", "south_east_wilds", "nether_front"],
        "theme": "Fire, sun, heat, ash, desert, blaze, and infernal pressure.",
        "progression_note": "Fire magic can appear early as basic utility but high-damage fire spells belong in Sunreach, Nether, boss, or high-rank routes.",
    },
    "ice": {
        "atlas_region_affinity": ["frostmarch", "north_west_marches", "north_east_marches"],
        "theme": "Ice, frost, snow, cold control, frozen movement, and winter summons.",
        "progression_note": "Frost magic should lean north and stay away from warm starter-region snow logic.",
    },
    "lightning": {
        "atlas_region_affinity": ["verdant_coast", "stoneback_highlands", "south_east_wilds"],
        "theme": "Storms, electricity, speed, charge, and volatile ranged damage.",
        "progression_note": "Lightning fits stormy coastal/eastern regions and highland storms; strong chain effects need mid-game or better sources.",
    },
    "nature": {
        "atlas_region_affinity": ["verdant_coast", "south_east_wilds", "hearthlands"],
        "theme": "Roots, vines, poison, animals, healing growth, and wild utility.",
        "progression_note": "Nature magic can be accessible early through Verdant/Hearthlands utility, with poison and control escalating into mid-game.",
    },
    "holy": {
        "atlas_region_affinity": ["hearthlands", "crownlands", "outer_rim"],
        "theme": "Healing, protection, light, support, warding, and radiant judgment.",
        "progression_note": "Basic support should be discoverable, while major healing and radiant combat should be rank-gated.",
    },
    "blood": {
        "atlas_region_affinity": ["outer_rim", "south_west_wilds", "nether_front"],
        "theme": "Blood cost, sacrifice, life-drain, dangerous martial magic, and taboo power.",
        "progression_note": "Blood magic should be rare outside dangerous mobs, cult sites, bosses, or high-rank contracts.",
    },
    "ender": {
        "atlas_region_affinity": ["end_expanse", "outer_rim", "stoneback_highlands"],
        "theme": "Teleportation, planar movement, void-adjacent mobility, and unstable utility.",
        "progression_note": "Mobility-breaking spells should arrive after players have proven exploration and rank progress.",
    },
    "eldritch": {
        "atlas_region_affinity": ["outer_rim", "end_expanse", "north_east_marches"],
        "theme": "Ancient, forbidden, abyssal, mind-bending, or corruption-linked magic.",
        "progression_note": "Eldritch magic is late-game by tone even when individual utility spells are low rarity.",
    },
    "evocation": {
        "atlas_region_affinity": ["stoneback_highlands", "outer_rim", "hearthlands"],
        "theme": "Summoned force, spectral weapons, fangs, arcane projectiles, and battle-control.",
        "progression_note": "Basic evocation is a beginner combat route, but summoning/weapon swarms should move into mid/high ranks.",
    },
    "void": {
        "atlas_region_affinity": ["outer_rim", "end_expanse", "nether_front"],
        "theme": "Void, black holes, abyssal pulls, corruption, and reality-breaking effects.",
        "progression_note": "Void magic should be high-rank, dangerous-structure, or boss-tier unless it is a small utility spell.",
    },
    "arcane": {
        "atlas_region_affinity": ["hearthlands", "crownlands", "outer_rim"],
        "theme": "General spellcraft, runes, books, mage gear, force, utility, and neutral magic.",
        "progression_note": "Arcane is the bridge school: starter-safe in basic forms, but late-game when tied to ancient knowledge or rare materials.",
    },
    "utility": {
        "atlas_region_affinity": ["hearthlands", "crownlands", "all_regions"],
        "theme": "Spellcraft infrastructure, inscriptions, wands, books, crafting devices, and non-combat tools.",
        "progression_note": "Utility items can be broad, but progression-critical crafting stations and rare books must respect rank and material tiers.",
    },
}

SCHOOL_KEYWORDS = [
    ("fire", ("fire", "flame", "flaming", "blaze", "burn", "burning", "scorch", "magma", "cinder", "pyro", "sun", "heat", "infernal", "ember")),
    ("ice", ("ice", "frost", "frostbite", "frostwave", "frostward", "snow", "snowball", "blizzard", "cold", "boreal", "cryo", "frozen", "icicle")),
    ("lightning", ("lightning", "thunder", "storm", "electro", "volt", "shock", "charge", "static", "ball_lightning")),
    ("nature", ("nature", "natural", "root", "vine", "oak", "oakskin", "poison", "venom", "spider", "fang", "druid", "druidic", "firefly", "wisp")),
    ("holy", ("holy", "divine", "heal", "healing", "bless", "angel", "paladin", "light", "guiding", "radiant", "priest", "protection")),
    ("blood", ("blood", "bloody", "vampiric", "sacrifice", "siphon", "heartstop", "bloodline")),
    ("ender", ("ender", "end_", "enderman", "teleport", "portal", "recall", "planar", "pocket_dimension")),
    ("eldritch", ("eldritch", "ancient", "abyss", "abyssal", "dead_king", "necro", "necronomicon", "lich", "dread", "shadow", "cursed", "cultist")),
    ("void", ("void", "black_hole", "dark", "darkness", "ray_of_siphoning", "soul", "raise_dead", "summon_vex", "withering", "wither")),
    ("evocation", ("evocation", "evoker", "archevoker", "fang", "spectral", "summon", "magic_arrow", "magic_missile", "arrow_volley", "shackle", "telekinesis", "throw", "shockwave", "stomp")),
    ("arcane", ("arcane", "rune", "runestone", "scroll", "spell_book", "spellbook", "spell", "mana", "amethyst", "mithril", "wand", "staff", "artificer", "inscription", "resonance")),
]

LOW_TIER_LOOT_CONTEXTS = {"village", "settlement", "minor_ruin", "mob", "block"}
LOW_TIER_RANK_MARKERS = {"unranked", "unranked_to_e_rank", "unranked_to_c_rank", "e_rank", "e_rank_to_d_rank"}
REVIEW_STATUSES = {"bypass", "too_cheap", "duplicate", "needs_manual_review"}
NONCANONICAL_RECIPE_STATUSES = {"duplicate"}


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


def namespace(item_id: str) -> str:
    return item_id.split(":", 1)[0] if ":" in item_id else ""


def local_id(item_id: str) -> str:
    return item_id.split(":", 1)[-1]


def clean_label(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("§6", "").replace("§r", "")).strip()


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def load_registry() -> dict[str, Any]:
    registry = read_json(ROOT / "config/ascendant_index/gear_registry.json", {})
    if not isinstance(registry, dict):
        raise RuntimeError("config/ascendant_index/gear_registry.json must be a JSON object")
    return registry


def load_spell_school_terms_from_jar() -> dict[str, str]:
    schools: dict[str, str] = {}
    if not ACTIVE_MODS.exists():
        return schools
    for jar_path in ACTIVE_MODS.glob("irons_spellbooks-*.jar"):
        try:
            with zipfile.ZipFile(jar_path) as jar:
                lang_names = [
                    name
                    for name in jar.namelist()
                    if name == "assets/irons_spellbooks/lang/en_us.json"
                ]
                if not lang_names:
                    continue
                lang = json.loads(jar.read(lang_names[0]).decode("utf-8"))
                for key, value in lang.items():
                    if key.startswith("school.irons_spellbooks."):
                        schools[key.rsplit(".", 1)[-1]] = str(value)
        except Exception:
            continue
    return schools


def rank_policy_for_rarity(rarity: str) -> dict[str, str]:
    return RARITY_POLICY.get(str(rarity).lower(), RARITY_POLICY["common"])


def infer_school(entry: dict[str, Any], fallback_collection: str) -> tuple[str, str]:
    item_id = str(entry.get("id") or "")
    name = clean_label(str(entry.get("name") or item_id))
    haystack = f"{item_id} {name} {entry.get('rarity_reason') or ''}".lower()
    for school, terms in SCHOOL_KEYWORDS:
        if any(term in haystack for term in terms):
            return school, "keyword_from_id_name_or_registry_reason"
    if fallback_collection == "magic_items":
        domains = " ".join(str(part).lower() for part in as_list(entry.get("domains")))
        if "weapon" in domains and ("staff" in haystack or "wand" in haystack):
            return "arcane", "magic_weapon_staff_or_wand"
        if "ring" in haystack or "amulet" in haystack or "charm" in haystack:
            return "utility", "magic_accessory_utility"
    return "arcane", "default_arcane_review"


def acquisition_methods_for(
    item_id: str,
    rarity: str,
    recipes_by_item: dict[str, list[dict[str, Any]]],
    loot_by_item: dict[str, list[dict[str, Any]]],
) -> list[str]:
    methods: set[str] = set()
    if recipes_by_item.get(item_id):
        methods.add("crafting")
    for source in loot_by_item.get(item_id, []):
        context = str(source.get("loot_context") or "loot")
        if context == "boss":
            methods.add("boss")
        elif context == "dragon":
            methods.add("dragon_or_mythic_structure")
        elif context == "bounty":
            methods.add("bounty")
        elif context in {"dungeon", "structure"}:
            methods.add("structure_loot")
        elif context == "mob":
            methods.add("mob_drop")
        elif context in {"village", "settlement"}:
            methods.add("settlement_loot_review")
        else:
            methods.add(context)
    if not methods:
        if RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"]:
            methods.add("boss_or_dangerous_structure_recommended")
        elif RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["epic"]:
            methods.add("structure_or_rank_contract_recommended")
        else:
            methods.add("loot_or_vendor_recommended")
    return sorted(methods)


def recipe_summary_for(item_id: str, rarity: str, recipes_by_item: dict[str, list[dict[str, Any]]]) -> tuple[str, list[dict[str, Any]]]:
    recipes = recipes_by_item.get(item_id, [])
    if not recipes:
        return "not_craftable_or_not_found", []
    status_order = {"bypass": 0, "too_cheap": 1, "duplicate": 2, "needs_manual_review": 3, "okay": 4}
    sorted_recipes = sorted(recipes, key=lambda entry: status_order.get(str(entry.get("recipe_status") or ""), 9))
    first = sorted_recipes[0]
    return str(first.get("intended_recipe_tier") or rank_policy_for_rarity(rarity)["recipe_tier"]), [
        {
            "recipe_id": recipe.get("recipe_id"),
            "recipe_type": recipe.get("recipe_type"),
            "current_ingredients": recipe.get("current_ingredients", []),
            "output_count": recipe.get("output_count", 1),
            "recipe_status": recipe.get("recipe_status"),
            "proposed_replacement": recipe.get("proposed_replacement"),
        }
        for recipe in sorted_recipes[:8]
    ]


def build_recipe_maps(recipe_policy: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    recipes_by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    magic_recipe_entries: list[dict[str, Any]] = []
    for recipe in recipe_policy.get("major_recipe_entries", []) if isinstance(recipe_policy, dict) else []:
        if not isinstance(recipe, dict):
            continue
        item_id = str(recipe.get("item_id") or "")
        if not item_id:
            continue
        recipes_by_item[item_id].append(recipe)
        if recipe.get("output_domain") == "magic_or_spell" or item_id.startswith("irons_spellbooks:"):
            magic_recipe_entries.append(recipe)
    return recipes_by_item, magic_recipe_entries


def build_loot_maps(loot_policy: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    loot_by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    magic_sources: list[dict[str, Any]] = []
    for source in loot_policy.get("loot_sources", []) if isinstance(loot_policy, dict) else []:
        if not isinstance(source, dict):
            continue
        item_ids = [str(item_id) for item_id in source.get("output_item_ids", []) if item_id]
        magic_items = [str(item_id) for item_id in source.get("magic_spell_items", []) if item_id]
        if magic_items or any(item_id.startswith("irons_spellbooks:") for item_id in item_ids):
            magic_sources.append(source)
        for item_id in item_ids:
            loot_by_item[item_id].append(source)
    return loot_by_item, magic_sources


def progression_entry(
    entry: dict[str, Any],
    collection: str,
    recipes_by_item: dict[str, list[dict[str, Any]]],
    loot_by_item: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    item_id = str(entry.get("id") or "")
    rarity = str(entry.get("rarity") or "common").lower()
    policy = rank_policy_for_rarity(rarity)
    school, school_evidence = infer_school(entry, collection)
    school_policy = SCHOOL_POLICY[school]
    recipe_tier, recipe_sources = recipe_summary_for(item_id, rarity, recipes_by_item)
    methods = acquisition_methods_for(item_id, rarity, recipes_by_item, loot_by_item)
    loot_sources = [
        {
            "source_id": source.get("source_id"),
            "loot_context": source.get("loot_context"),
            "guild_rank_tier": source.get("guild_rank_tier"),
            "danger_tier": source.get("danger_tier"),
            "allowed_rarity_ceiling": source.get("allowed_rarity_ceiling"),
            "recommended_action": source.get("recommended_action"),
        }
        for source in loot_by_item.get(item_id, [])[:8]
    ]
    notes = [
        f"School/type assignment evidence: {school_evidence}.",
        "Audit-only policy; no hard gate or spell rewrite is enabled.",
    ]
    if RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"]:
        notes.append("High-tier magic should require boss, dangerous-structure, rare-material, or rank-contract proof.")
    if not recipe_sources and not loot_sources:
        notes.append("No direct recipe or loot source found in current scans; acquisition needs manual placement review.")
    return {
        "id": item_id,
        "name": clean_label(str(entry.get("name") or item_id)),
        "source_mod": entry.get("source_mod") or namespace(item_id) or "unknown",
        "source_mod_id": entry.get("mod_id") or namespace(item_id) or None,
        "type": "spell" if collection == "spells" else "magic_item",
        "school": school,
        "rarity": rarity,
        "guild_rank_tier": policy["rank"],
        "atlas_region_affinity": school_policy["atlas_region_affinity"],
        "atlas_distance_ring": policy["ring"],
        "allowed_loot_tier": policy["loot_tier"],
        "recipe_tier_if_craftable": recipe_tier,
        "intended_acquisition_method": methods,
        "progression_band": policy["progression"],
        "loot_sources": loot_sources,
        "recipe_sources": recipe_sources,
        "notes": notes,
    }


def high_tier_low_tier_loot(policy_entries: list[dict[str, Any]], loot_by_item: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for entry in policy_entries:
        rarity = str(entry.get("rarity") or "common")
        if RARITY_ORDER.get(rarity, 0) < RARITY_ORDER["legendary"]:
            continue
        for source in loot_by_item.get(str(entry.get("id")), []):
            context = str(source.get("loot_context") or "")
            rank = str(source.get("guild_rank_tier") or "")
            ceiling = str(source.get("allowed_rarity_ceiling") or "common")
            low_ceiling = RARITY_ORDER.get(ceiling, 0) < RARITY_ORDER.get(rarity, 0)
            if context in LOW_TIER_LOOT_CONTEXTS or rank in LOW_TIER_RANK_MARKERS or low_ceiling:
                issues.append(
                    {
                        "id": entry.get("id"),
                        "rarity": rarity,
                        "source_id": source.get("source_id"),
                        "loot_context": context,
                        "guild_rank_tier": rank,
                        "allowed_rarity_ceiling": ceiling,
                    }
                )
    return issues


def recipe_review_issues(policy_entries: list[dict[str, Any]], recipes_by_item: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    high_tier_low: list[dict[str, Any]] = []
    noncanonical: list[dict[str, Any]] = []
    policy_by_id = {str(entry.get("id")): entry for entry in policy_entries}
    for item_id, recipes in recipes_by_item.items():
        policy_entry = policy_by_id.get(item_id)
        if not policy_entry:
            continue
        rarity = str(policy_entry.get("rarity") or "common")
        for recipe in recipes:
            status = str(recipe.get("recipe_status") or "")
            if RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"] and status in REVIEW_STATUSES:
                high_tier_low.append(
                    {
                        "id": item_id,
                        "rarity": rarity,
                        "recipe_id": recipe.get("recipe_id"),
                        "recipe_status": status,
                        "current_ingredients": recipe.get("current_ingredients", []),
                        "proposed_replacement": recipe.get("proposed_replacement"),
                    }
                )
            if status in NONCANONICAL_RECIPE_STATUSES or recipe.get("canonical_material_conflicts"):
                noncanonical.append(
                    {
                        "id": item_id,
                        "recipe_id": recipe.get("recipe_id"),
                        "recipe_status": status,
                        "canonical_material_conflicts": recipe.get("canonical_material_conflicts", []),
                    }
                )
    return high_tier_low, noncanonical


def build_school_region_policy(spells: list[dict[str, Any]], magic_items: list[dict[str, Any]], jar_schools: dict[str, str]) -> dict[str, Any]:
    all_entries = spells + magic_items
    entries_by_school: dict[str, list[str]] = defaultdict(list)
    for entry in all_entries:
        entries_by_school[str(entry.get("school") or "arcane")].append(str(entry.get("id")))
    schools = []
    for school_id, policy in SCHOOL_POLICY.items():
        schools.append(
            {
                "school": school_id,
                "source_label": jar_schools.get(school_id),
                "atlas_region_affinity": policy["atlas_region_affinity"],
                "theme": policy["theme"],
                "progression_note": policy["progression_note"],
                "spells": sorted([item_id for item_id in entries_by_school.get(school_id, []) if item_id in {str(e.get("id")) for e in spells}]),
                "magic_items": sorted([item_id for item_id in entries_by_school.get(school_id, []) if item_id in {str(e.get("id")) for e in magic_items}]),
            }
        )
    known_ids = {str(entry.get("id")) for entry in all_entries}
    referenced_ids = {
        item_id
        for school in schools
        for item_id in list(school.get("spells", [])) + list(school.get("magic_items", []))
    }
    return {
        "version": 1,
        "generated_at": now_iso(),
        "status": "audit_control_scaffold_only_no_hard_gates",
        "source": {
            "gear_registry": "config/ascendant_index/gear_registry.json",
            "iron_spell_school_labels_from_active_jar": bool(jar_schools),
            "spell_school_assignment_note": "Iron's Spells 1.20.1 jar exposes school labels but not per-spell school JSON in this scan, so per-spell school rows are audit heuristics and manual-review candidates.",
        },
        "schools": schools,
        "validation": {
            "policy_references_missing_spells_or_items": sorted(referenced_ids - known_ids),
            "unassigned_spells_or_items": sorted(known_ids - referenced_ids),
            "missing_jar_school_labels": sorted(set(SCHOOL_POLICY) - set(jar_schools)),
        },
    }


def build_magic_loot_policy(policy_entries: list[dict[str, Any]], magic_sources: list[dict[str, Any]], loot_by_item: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    high_tier_low = high_tier_low_tier_loot(policy_entries, loot_by_item)
    source_rows = []
    for source in magic_sources:
        source_rows.append(
            {
                "source_id": source.get("source_id"),
                "source_mod": source.get("source_mod"),
                "loot_context": source.get("loot_context"),
                "atlas_region_allowance": source.get("atlas_region_allowance", []),
                "distance_ring_allowance": source.get("distance_ring_allowance", []),
                "guild_rank_tier": source.get("guild_rank_tier"),
                "danger_tier": source.get("danger_tier"),
                "allowed_rarity_ceiling": source.get("allowed_rarity_ceiling"),
                "magic_spell_items": source.get("magic_spell_items", []),
                "recommended_action": source.get("recommended_action"),
            }
        )
    return {
        "version": 1,
        "generated_at": now_iso(),
        "status": "audit_control_scaffold_only_no_loot_rewrites",
        "rules": [
            "Spell loot must not bypass Atlas region, Guild rank, danger tier, or rarity budget.",
            "Beginner magic can be discoverable through low-risk loot, but high-impact spells must move to bosses, dangerous structures, rare materials, or rank contracts.",
            "High-tier magic found in low-tier loot remains review-only until a specific rewrite is approved.",
        ],
        "magic_loot_sources": source_rows,
        "validation": {
            "high_tier_spell_in_low_tier_loot": high_tier_low,
            "missing_magic_loot_sources": [
                entry["id"]
                for entry in policy_entries
                if "loot" in " ".join(entry.get("intended_acquisition_method", []))
                and not loot_by_item.get(entry["id"])
            ],
        },
        "summary": {
            "magic_loot_sources": len(source_rows),
            "high_tier_spell_low_tier_loot_warnings": len(high_tier_low),
            "by_context": dict(Counter(str(source.get("loot_context") or "unknown") for source in magic_sources)),
        },
    }


def build_magic_recipe_policy(policy_entries: list[dict[str, Any]], recipes_by_item: dict[str, list[dict[str, Any]]], magic_recipe_entries: list[dict[str, Any]]) -> dict[str, Any]:
    high_tier_low, noncanonical = recipe_review_issues(policy_entries, recipes_by_item)
    rows = []
    for recipe in magic_recipe_entries:
        rows.append(
            {
                "item_id": recipe.get("item_id"),
                "recipe_id": recipe.get("recipe_id"),
                "source_mod": recipe.get("source_mod"),
                "recipe_type": recipe.get("recipe_type"),
                "current_ingredients": recipe.get("current_ingredients", []),
                "output_count": recipe.get("output_count", 1),
                "rarity": recipe.get("gear_material_rarity"),
                "intended_guild_rank": recipe.get("intended_guild_rank"),
                "intended_atlas_distance_ring": recipe.get("intended_atlas_distance_ring"),
                "intended_recipe_tier": recipe.get("intended_recipe_tier"),
                "recipe_status": recipe.get("recipe_status"),
                "canonical_material_conflicts": recipe.get("canonical_material_conflicts", []),
                "proposed_replacement": recipe.get("proposed_replacement"),
            }
        )
    return {
        "version": 1,
        "generated_at": now_iso(),
        "status": "audit_candidate_scaffold_only_no_hard_gates",
        "rules": [
            "High-tier spells and magic items cannot be craftable from basic vanilla-only materials.",
            "Spellbooks, scrolls, and rare magic components should require region, structure, boss, or rank proof at higher rarities.",
            "Recipe rewrite candidates remain disabled until manually approved.",
        ],
        "magic_recipe_entries": rows,
        "validation": {
            "high_tier_spell_low_tier_recipes": high_tier_low,
            "spell_recipe_noncanonical_materials": noncanonical,
            "unreviewed_magic_recipe_candidates": [
                entry
                for entry in rows
                if str(entry.get("recipe_status") or "") in REVIEW_STATUSES
            ],
        },
        "summary": {
            "magic_recipe_entries": len(rows),
            "high_tier_low_tier_recipe_warnings": len(high_tier_low),
            "noncanonical_recipe_warnings": len(noncanonical),
            "by_status": dict(Counter(str(row.get("recipe_status") or "unknown") for row in rows)),
        },
    }


def build_item_registry(entries: list[dict[str, Any]], collection_name: str) -> dict[str, Any]:
    missing_rank_region = [
        entry["id"]
        for entry in entries
        if not entry.get("guild_rank_tier") or not entry.get("atlas_region_affinity")
    ]
    missing_acquisition = [
        entry["id"]
        for entry in entries
        if not entry.get("intended_acquisition_method")
    ]
    return {
        "version": 1,
        "generated_at": now_iso(),
        "status": "audit_control_scaffold_only_no_hard_gates",
        "source": {
            "gear_registry": "config/ascendant_index/gear_registry.json",
            "collection": collection_name,
        },
        collection_name: entries,
        "validation": {
            "missing_rank_or_region_tier": missing_rank_region,
            "missing_acquisition_method": missing_acquisition,
        },
        "summary": {
            "entries": len(entries),
            "by_rarity": dict(Counter(str(entry.get("rarity") or "unknown") for entry in entries)),
            "by_school": dict(Counter(str(entry.get("school") or "unknown") for entry in entries)),
            "by_progression_band": dict(Counter(str(entry.get("progression_band") or "unknown") for entry in entries)),
        },
    }


def markdown_table(rows: list[list[Any]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return "\n".join(out)


def write_docs(
    spell_registry: dict[str, Any],
    item_registry: dict[str, Any],
    school_policy: dict[str, Any],
    loot_policy: dict[str, Any],
    recipe_policy: dict[str, Any],
) -> None:
    spells = spell_registry["spells"]
    magic_items = item_registry["magic_items"]
    all_entries = spells + magic_items
    rarity_counts = Counter(entry["rarity"] for entry in all_entries)
    school_counts = Counter(entry["school"] for entry in all_entries)
    high_tier_loot = loot_policy["validation"]["high_tier_spell_in_low_tier_loot"]
    high_tier_recipes = recipe_policy["validation"]["high_tier_spell_low_tier_recipes"]
    unreviewed_recipes = recipe_policy["validation"]["unreviewed_magic_recipe_candidates"]

    overview_rows = [
        ["Indexed spells", len(spells)],
        ["Indexed magic items", len(magic_items)],
        ["Magic loot sources", loot_policy["summary"]["magic_loot_sources"]],
        ["Magic recipe entries", recipe_policy["summary"]["magic_recipe_entries"]],
        ["High-tier low-tier loot warnings", len(high_tier_loot)],
        ["High-tier low-tier recipe warnings", len(high_tier_recipes)],
        ["Unreviewed magic recipe candidates", len(unreviewed_recipes)],
    ]
    school_rows = [
        [
            school["school"],
            ", ".join(school["atlas_region_affinity"]),
            len(school["spells"]),
            len(school["magic_items"]),
            school["progression_note"],
        ]
        for school in school_policy["schools"]
    ]
    write_text(
        DOCS_DIR / "ASCENDANT_MAGIC_PROGRESSION.md",
        f"""# Ascendant Magic Progression

Generated: {now_iso()}

## Status

This is the active magic progression audit/control scaffold. It does not add new magic mods, does not rewrite spells, and does not enable hard gates.

The goal is to make Iron's Spells and all indexed magic items obey the same Atlas region, Guild rank, rarity, loot, recipe, and material logic used by weapons, armor, loot, and recipes.

## Summary

{markdown_table(overview_rows, ["Metric", "Count"])}

## Core Rules

- Frost and ice magic lean Frostmarch and cold northern regions.
- Fire, sun, blaze, and desert heat magic lean Sunreach, southern arid regions, and Nether-adjacent routes.
- Nature, poison, water, and storm magic lean Verdant Coast and eastern wet regions.
- Earth, force, gravity, metal, and battle evocation lean Stoneback/highland or dangerous structure routes.
- Dark, void, eldritch, ancient, necromantic, and blood magic lean outer, corrupted, Nether, End, or high-rank content.
- Beginner magic should be discoverable, but it should not drown the player in every school at once.
- High-tier spells should require dangerous structures, bosses, rare materials, or Guild rank progress.
- Spell loot must not bypass the rarity budget or recipe progression scaffold.

## Machine Policy Files

- `config/ascendant_magic/spell_progression_registry.json`
- `config/ascendant_magic/magic_item_progression_registry.json`
- `config/ascendant_magic/school_region_policy.json`
- `config/ascendant_magic/magic_loot_policy.json`
- `config/ascendant_magic/magic_recipe_policy.json`

## School And Region Policy

{markdown_table(school_rows, ["School", "Atlas Affinity", "Spells", "Magic Items", "Progression Note"])}

## Current Risk Notes

- Per-spell school assignment is an audit heuristic where the Iron's Spells jar exposes school labels but not per-spell school JSON in this scan.
- Any high-tier spell or magic item in low-tier loot remains a warning until a narrow loot rewrite is approved.
- Magic recipe candidates remain disabled review notes only.
- This scaffold should be reviewed alongside `docs/ASCENDANT_LOOT_ECONOMY.md` and `docs/RECIPE_PROGRESSION_AUDIT.md` before enabling gates.
""",
    )

    spell_rows = [
        [
            f"`{entry['id']}`",
            entry["name"],
            entry["school"],
            entry["rarity"],
            entry["guild_rank_tier"],
            ", ".join(entry["atlas_region_affinity"]),
            entry["progression_band"],
            ", ".join(entry["intended_acquisition_method"]),
        ]
        for entry in spells
    ]
    write_text(
        DOCS_DIR / "SPELL_REGION_AND_RANK_INDEX.md",
        f"""# Spell Region And Rank Index

Generated: {now_iso()}

This generated index maps every indexed spell to a school, Atlas region affinity, Guild rank tier, rarity, loot tier, and acquisition route. It is policy scaffolding only; it does not change spell behavior.

## Summary

{markdown_table([[key, value] for key, value in rarity_counts.items()], ["Rarity", "Spell/Magic Count"])}

## Spells

{markdown_table(spell_rows, ["Spell ID", "Name", "School", "Rarity", "Guild Rank", "Atlas Affinity", "Progression", "Acquisition"])}
""",
    )

    loot_preview = [
        [
            issue["id"],
            issue["rarity"],
            issue["source_id"],
            issue["loot_context"],
            issue["guild_rank_tier"],
            issue["allowed_rarity_ceiling"],
        ]
        for issue in high_tier_loot[:50]
    ]
    recipe_preview = [
        [
            issue["id"],
            issue["rarity"],
            issue["recipe_id"],
            issue["recipe_status"],
            issue.get("proposed_replacement") or "manual review",
        ]
        for issue in high_tier_recipes[:50]
    ]
    write_text(
        DOCS_DIR / "MAGIC_LOOT_AND_RECIPE_AUDIT.md",
        f"""# Magic Loot And Recipe Audit

Generated: {now_iso()}

This audit links indexed spells and magic items to the current loot economy and recipe progression scaffolds. It is intentionally review-only: no KubeJS recipe rewrites, loot rewrites, spell edits, or rank gates are enabled.

## Summary

{markdown_table(overview_rows, ["Metric", "Count"])}

## Rarity Distribution

{markdown_table([[key, value] for key, value in rarity_counts.items()], ["Rarity", "Count"])}

## School Distribution

{markdown_table([[key, value] for key, value in school_counts.items()], ["School", "Count"])}

## High-Tier Magic In Low-Tier Loot

{markdown_table(loot_preview or [["None", "", "", "", "", ""]], ["Item/Spell", "Rarity", "Source", "Context", "Source Rank", "Source Ceiling"])}

## High-Tier Or Review Magic Recipes

{markdown_table(recipe_preview or [["None", "", "", "", ""]], ["Item/Spell", "Rarity", "Recipe", "Status", "Proposed Replacement"])}

## Candidate Output

Candidate guidance is written to `kubejs/server_scripts_disabled/review/ascendant_magic/magic_progression_candidates.js`. It is disabled by path and contains comments only, so it cannot change live recipes or loot.
""",
    )


def write_candidate_file(recipe_policy: dict[str, Any], loot_policy: dict[str, Any]) -> None:
    lines = [
        "// Ascendant Magic progression candidate notes.",
        "// Disabled review-only file. It lives under kubejs/server_scripts_disabled and is not loaded by Minecraft.",
        "// Do not move this into kubejs/server_scripts until Jayden approves narrow, source-specific magic gates or rewrites.",
        "",
        "// High-tier magic in low-tier loot candidates:",
    ]
    for issue in loot_policy["validation"]["high_tier_spell_in_low_tier_loot"][:80]:
        lines.append(
            f"// - Review loot source {issue.get('source_id')} exposing {issue.get('id')} ({issue.get('rarity')}) in {issue.get('loot_context')} / {issue.get('guild_rank_tier')}."
        )
    lines.append("")
    lines.append("// High-tier or risky magic recipe candidates:")
    for issue in recipe_policy["validation"]["high_tier_spell_low_tier_recipes"][:80]:
        lines.append(
            f"// - Review recipe {issue.get('recipe_id')} for {issue.get('id')} ({issue.get('rarity')}): {issue.get('proposed_replacement') or 'manual review'}"
        )
    write_text(DISABLED_REVIEW_DIR / "magic_progression_candidates.js", "\n".join(lines))


def main() -> int:
    registry = load_registry()
    recipe_policy = read_json(ROOT / "config/ascendant_recipes/recipe_progression_policy.json", {})
    loot_policy = read_json(ROOT / "config/ascendant_loot/loot_policy.json", {})
    recipes_by_item, magic_recipe_entries = build_recipe_maps(recipe_policy if isinstance(recipe_policy, dict) else {})
    loot_by_item, magic_sources = build_loot_maps(loot_policy if isinstance(loot_policy, dict) else {})
    jar_schools = load_spell_school_terms_from_jar()

    spells = [
        progression_entry(entry, "spells", recipes_by_item, loot_by_item)
        for entry in registry.get("spells", [])
        if isinstance(entry, dict) and entry.get("id")
    ]
    magic_items = [
        progression_entry(entry, "magic_items", recipes_by_item, loot_by_item)
        for entry in registry.get("magic_items", [])
        if isinstance(entry, dict) and entry.get("id")
    ]
    all_policy_entries = spells + magic_items

    spell_registry = build_item_registry(spells, "spells")
    magic_item_registry = build_item_registry(magic_items, "magic_items")
    school_region_policy = build_school_region_policy(spells, magic_items, jar_schools)
    magic_loot_policy = build_magic_loot_policy(all_policy_entries, magic_sources, loot_by_item)
    magic_recipe_policy = build_magic_recipe_policy(all_policy_entries, recipes_by_item, magic_recipe_entries)

    write_json(OUT_DIR / "spell_progression_registry.json", spell_registry)
    write_json(OUT_DIR / "magic_item_progression_registry.json", magic_item_registry)
    write_json(OUT_DIR / "school_region_policy.json", school_region_policy)
    write_json(OUT_DIR / "magic_loot_policy.json", magic_loot_policy)
    write_json(OUT_DIR / "magic_recipe_policy.json", magic_recipe_policy)
    write_docs(spell_registry, magic_item_registry, school_region_policy, magic_loot_policy, magic_recipe_policy)
    write_candidate_file(magic_recipe_policy, magic_loot_policy)

    print(f"Wrote {len(spells)} spell policy rows and {len(magic_items)} magic item policy rows.")
    print(f"Magic loot sources: {magic_loot_policy['summary']['magic_loot_sources']}")
    print(f"Magic recipe entries: {magic_recipe_policy['summary']['magic_recipe_entries']}")
    print(f"High-tier loot warnings: {magic_loot_policy['summary']['high_tier_spell_low_tier_loot_warnings']}")
    print(f"High-tier recipe warnings: {magic_recipe_policy['summary']['high_tier_low_tier_recipe_warnings']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
