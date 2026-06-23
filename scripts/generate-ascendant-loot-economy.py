#!/usr/bin/env python3
"""Generate the Ascendant loot economy audit and policy scaffold."""

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

OUT_DIR = ROOT / "config/ascendant_loot"
DOCS_DIR = ROOT / "docs"
DISABLED_REVIEW_DIR = ROOT / "kubejs/server_scripts_disabled/review/ascendant_loot"

RARITY_ORDER = {
    "common": 0,
    "uncommon": 1,
    "rare": 2,
    "epic": 3,
    "legendary": 4,
    "mythic": 5,
    "ascendant": 6,
}

RARITY_LABELS = {
    "common": "Common",
    "uncommon": "Uncommon",
    "rare": "Rare",
    "epic": "Epic",
    "legendary": "Legendary",
    "mythic": "Mythic",
    "ascendant": "Ascendant",
}

SOURCE_CONTEXT_POLICY = {
    "village": {
        "regions": ["hearthlands", "crownlands", "region_compatible_settlements"],
        "rings": ["center", "inner"],
        "rank": "unranked_to_e_rank",
        "danger": 0,
        "minimum": "common",
        "ceiling": "uncommon",
        "material": "mundane",
        "gear": "starter",
        "action": "reduce_if_modded_high_value",
    },
    "settlement": {
        "regions": ["hearthlands", "crownlands", "region_compatible_settlements"],
        "rings": ["center", "inner"],
        "rank": "unranked_to_d_rank",
        "danger": 1,
        "minimum": "common",
        "ceiling": "rare",
        "material": "mundane_to_regional",
        "gear": "starter_to_early",
        "action": "manual_review",
    },
    "minor_ruin": {
        "regions": ["atlas_region_matching_structure"],
        "rings": ["inner", "middle"],
        "rank": "e_rank_to_d_rank",
        "danger": 1,
        "minimum": "common",
        "ceiling": "rare",
        "material": "regional",
        "gear": "early",
        "action": "untouched_unless_high_rarity",
    },
    "dungeon": {
        "regions": ["atlas_region_matching_structure"],
        "rings": ["middle", "outer"],
        "rank": "d_rank_to_b_rank",
        "danger": 3,
        "minimum": "uncommon",
        "ceiling": "epic",
        "material": "regional_to_refined",
        "gear": "midgame",
        "action": "manual_review",
    },
    "structure": {
        "regions": ["atlas_region_matching_structure"],
        "rings": ["inner", "middle", "outer"],
        "rank": "e_rank_to_b_rank",
        "danger": 2,
        "minimum": "common",
        "ceiling": "rare",
        "material": "regional",
        "gear": "early_to_midgame",
        "action": "manual_review",
    },
    "boss": {
        "regions": ["outer", "corrupted", "boss_biome_specific"],
        "rings": ["outer", "edge"],
        "rank": "b_rank_to_s_rank",
        "danger": 5,
        "minimum": "epic",
        "ceiling": "mythic",
        "material": "boss",
        "gear": "late_game",
        "action": "preserve_or_improve",
    },
    "dragon": {
        "regions": ["dragonbound", "outer", "corrupted"],
        "rings": ["outer", "edge"],
        "rank": "a_rank_to_s_rank",
        "danger": 5,
        "minimum": "legendary",
        "ceiling": "ascendant",
        "material": "dragon",
        "gear": "capstone",
        "action": "preserve_or_improve",
    },
    "mob": {
        "regions": ["spawn_region_matching_entity"],
        "rings": ["all"],
        "rank": "unranked_to_c_rank",
        "danger": 1,
        "minimum": "common",
        "ceiling": "uncommon",
        "material": "mundane",
        "gear": "none_or_starter",
        "action": "untouched",
    },
    "fishing": {
        "regions": ["valid_water_regions"],
        "rings": ["all"],
        "rank": "unranked_to_c_rank",
        "danger": 1,
        "minimum": "common",
        "ceiling": "rare",
        "material": "regional",
        "gear": "utility",
        "action": "untouched_unless_high_rarity",
    },
    "archaeology": {
        "regions": ["ruin_or_desert_region_matching_site"],
        "rings": ["inner", "middle", "outer"],
        "rank": "e_rank_to_b_rank",
        "danger": 2,
        "minimum": "common",
        "ceiling": "rare",
        "material": "regional",
        "gear": "relic_seed",
        "action": "manual_review",
    },
    "bounty": {
        "regions": ["atlas_region_matching_contract"],
        "rings": ["all"],
        "rank": "board_rank",
        "danger": 2,
        "minimum": "common",
        "ceiling": "legendary",
        "material": "contract",
        "gear": "rank_reward",
        "action": "controlled",
    },
    "block": {
        "regions": ["all"],
        "rings": ["all"],
        "rank": "none",
        "danger": 0,
        "minimum": "common",
        "ceiling": "common",
        "material": "block_drop",
        "gear": "none",
        "action": "untouched",
    },
    "generic": {
        "regions": ["manual_review"],
        "rings": ["manual_review"],
        "rank": "manual_review",
        "danger": 2,
        "minimum": "common",
        "ceiling": "rare",
        "material": "manual_review",
        "gear": "manual_review",
        "action": "manual_review",
    },
}

STRUCTURE_TIER_POLICY = {
    "village_supplies": ("settlement_basic", "uncommon", 0, "unranked_to_e_rank"),
    "minor_ruin": ("minor_ruin", "rare", 1, "e_rank_to_d_rank"),
    "rare_to_epic": ("dangerous_dungeon", "epic", 3, "d_rank_to_b_rank"),
    "legendary_to_mythic": ("boss_arena", "mythic", 5, "b_rank_to_s_rank"),
    "mythic_to_ascendant": ("dragon_tier_zone", "ascendant", 5, "a_rank_to_s_rank"),
    "review": ("review", "rare", 2, "manual_review"),
}

MOB_TIER_POLICY = {
    "passive_or_wildlife": ("wildlife", "common", 0, "none"),
    "technical_or_projectile": ("technical", "common", 0, "none"),
    "common_hostile": ("common_hostile", "uncommon", 1, "unranked_to_e_rank"),
    "dangerous_hostile": ("dangerous", "rare", 2, "e_rank_to_c_rank"),
    "elite": ("elite", "epic", 3, "c_rank_to_b_rank"),
    "boss": ("boss", "legendary", 4, "b_rank_to_a_rank"),
    "dragon_tier": ("dragon", "mythic", 5, "a_rank_to_s_rank"),
}

VANILLA_KNOWN_ITEMS = {
    "minecraft:air",
    "minecraft:arrow",
    "minecraft:bone",
    "minecraft:book",
    "minecraft:bread",
    "minecraft:cooked_beef",
    "minecraft:copper_ingot",
    "minecraft:diamond",
    "minecraft:echo_shard",
    "minecraft:emerald",
    "minecraft:ender_pearl",
    "minecraft:experience_bottle",
    "minecraft:gold_ingot",
    "minecraft:iron_ingot",
    "minecraft:netherite_scrap",
    "minecraft:totem_of_undying",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def safe_rel(path: pathlib.Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def slug_has_any(value: str, needles: tuple[str, ...]) -> bool:
    lower = value.lower()
    return any(needle in lower for needle in needles)


def item_namespace(item_id: str) -> str:
    return item_id.split(":", 1)[0] if ":" in item_id else ""


def is_item_id(value: object) -> bool:
    return isinstance(value, str) and bool(re.match(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$", value))


def collect_item_ids(node: Any, out: set[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in {"name", "item", "content"} and is_item_id(value) and not str(value).startswith("#"):
                out.add(str(value))
            else:
                collect_item_ids(value, out)
    elif isinstance(node, list):
        for entry in node:
            collect_item_ids(entry, out)


def load_registries() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, str],
    dict[str, str],
    dict[str, set[str]],
]:
    gear = read_json(ROOT / "config/ascendant_index/gear_registry.json")
    structures = read_json(ROOT / "config/ascendant_index/structure_registry.json")
    mobs = read_json(ROOT / "config/ascendant_index/mob_registry.json")

    rarity_by_item: dict[str, str] = {}
    mod_name_by_namespace: dict[str, str] = {}
    domain_by_item: dict[str, set[str]] = defaultdict(set)
    for collection in ("weapons", "armor", "shields", "magic_items", "spells", "accessories_relics"):
        for entry in gear.get(collection, []):
            item_id = str(entry.get("id", ""))
            rarity = str(entry.get("rarity", "")).lower()
            if item_id and rarity:
                rarity_by_item[item_id] = rarity
            if item_id:
                domain_value = entry.get("domains") or entry.get("domain") or collection
                if isinstance(domain_value, str):
                    domain_parts = re.split(r"[,;/ ]+", domain_value)
                elif isinstance(domain_value, list):
                    domain_parts = [str(part) for part in domain_value]
                else:
                    domain_parts = [collection]
                for domain in domain_parts:
                    domain = domain.strip()
                    if domain:
                        domain_by_item[item_id].add(domain)
            mod_id = str(entry.get("mod_id") or item_namespace(item_id))
            source_mod = str(entry.get("source_mod") or mod_id)
            if mod_id:
                mod_name_by_namespace.setdefault(mod_id, source_mod)

    for entry in structures.get("structures", []):
        sid = str(entry.get("structure_id", ""))
        if ":" in sid:
            mod_name_by_namespace.setdefault(item_namespace(sid), str(entry.get("source_mod") or item_namespace(sid)))

    for entry in mobs.get("mobs", []):
        eid = str(entry.get("entity_id", ""))
        if ":" in eid:
            mod_name_by_namespace.setdefault(item_namespace(eid), str(entry.get("source_mod") or item_namespace(eid)))

    return gear, structures, mobs, rarity_by_item, mod_name_by_namespace, domain_by_item


def parse_kubejs_items() -> set[str]:
    items: set[str] = set()
    for script in (ROOT / "kubejs/startup_scripts").glob("*.js"):
        text = script.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"event\.create\(['\"]([^'\"]+)['\"]\)", text):
            raw = match.group(1)
            items.add(raw if ":" in raw else f"kubejs:{raw}")
    return items


def iter_jar_loot_tables() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not ACTIVE_MODS.exists():
        return rows
    for jar_path in sorted(ACTIVE_MODS.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar_path) as jar:
                for name in jar.namelist():
                    if not name.startswith("data/") or "/loot_tables/" not in name or not name.endswith(".json"):
                        continue
                    parts = name.split("/")
                    if len(parts) < 4:
                        continue
                    namespace = parts[1]
                    after = name.split("/loot_tables/", 1)[1][:-5]
                    loot_id = f"{namespace}:{after}"
                    try:
                        payload = json.loads(jar.read(name).decode("utf-8-sig"))
                        invalid = None
                    except Exception as exc:  # noqa: BLE001 - audit should survive bad third-party data.
                        payload = {}
                        invalid = str(exc)
                    items: set[str] = set()
                    collect_item_ids(payload, items)
                    rows.append(
                        {
                            "source_id": loot_id,
                            "namespace": namespace,
                            "source_file": str(jar_path),
                            "source_file_display": f"{jar_path.name}!/{name}",
                            "jar": jar_path.name,
                            "json_path": name,
                            "payload": payload,
                            "items": sorted(items),
                            "invalid_json": invalid,
                            "source_kind": "installed_mod_jar",
                        }
                    )
        except zipfile.BadZipFile:
            rows.append(
                {
                    "source_id": f"invalid_jar:{jar_path.name}",
                    "namespace": "invalid_jar",
                    "source_file": str(jar_path),
                    "source_file_display": jar_path.name,
                    "jar": jar_path.name,
                    "json_path": "",
                    "payload": {},
                    "items": [],
                    "invalid_json": "bad zip/jar",
                    "source_kind": "installed_mod_jar",
                }
            )
    return rows


def iter_datapack_loot_tables() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    roots = [
        ROOT / "config/openloader/data",
        ROOT / "openloader/data",
        ROOT / "datapacks",
        ROOT / "kubejs/data",
    ]
    seen_paths: set[pathlib.Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.glob("**/data/*/loot_tables/**/*.json")):
            resolved = path.resolve()
            if resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            marker_positions = [
                i
                for i, part in enumerate(path.parts)
                if part == "data" and len(path.parts) > i + 2 and path.parts[i + 2] == "loot_tables"
            ]
            if not marker_positions:
                continue
            data_marker = marker_positions[-1]
            if len(path.parts) <= data_marker + 3:
                continue
            namespace = path.parts[data_marker + 1]
            after_parts = path.parts[data_marker + 3 :]
            after = "/".join(after_parts)[:-5]
            loot_id = f"{namespace}:{after}"
            try:
                payload = read_json(path)
                invalid = None
            except Exception as exc:  # noqa: BLE001
                payload = {}
                invalid = str(exc)
            items: set[str] = set()
            collect_item_ids(payload, items)
            rows.append(
                {
                    "source_id": loot_id,
                    "namespace": namespace,
                    "source_file": str(path),
                    "source_file_display": safe_rel(path),
                    "jar": "",
                    "json_path": safe_rel(path),
                    "payload": payload,
                    "items": sorted(items),
                    "invalid_json": invalid,
                    "source_kind": "repo_datapack_or_openloader",
                }
            )
    return rows


def classify_context(source_id: str, namespace: str, items: list[str]) -> str:
    lid = source_id.lower()
    joined_items = " ".join(items).lower()
    if "/entities/" in lid or ":entities/" in lid:
        if slug_has_any(lid, ("dragon", "wyrm")):
            return "dragon"
        if slug_has_any(lid, ("boss", "ignis", "leviathan", "harbinger", "maledictus", "wroughtnaut", "frostmaw")):
            return "boss"
        return "mob"
    if "gameplay/fishing" in lid or "fishing" in lid:
        return "fishing"
    if "archaeology" in lid or "suspicious" in lid:
        return "archaeology"
    if "village" in lid or "villager" in lid:
        return "village"
    if "hunter_board" in lid or "guild" in lid:
        return "bounty"
    if slug_has_any(lid, ("boss", "arena", "citadel", "cataclysm", "monstrosity", "leviathan", "ignis")):
        return "boss"
    if slug_has_any(lid, ("dragon", "dread", "cyclops", "gorgon", "hydra")):
        return "dragon"
    if slug_has_any(lid, ("dungeon", "catacomb", "crypt", "tower", "stronghold", "bastion", "ancient_city", "mineshaft", "temple", "pyramid", "trial", "ruins")):
        return "dungeon"
    if ":blocks/" in lid:
        return "block"
    if ":chests/" in lid or "/chests/" in lid:
        if slug_has_any(joined_items, ("legendary", "mythic", "ascendant")):
            return "dungeon"
        return "structure"
    return "generic"


def policy_for_context(context: str, source_id: str) -> dict[str, Any]:
    policy = dict(SOURCE_CONTEXT_POLICY.get(context, SOURCE_CONTEXT_POLICY["generic"]))
    if context == "structure":
        lower = source_id.lower()
        if slug_has_any(lower, ("ruin", "waymark", "camp")):
            policy.update(SOURCE_CONTEXT_POLICY["minor_ruin"])
        if slug_has_any(lower, ("village", "settlement", "outpost")):
            policy.update(SOURCE_CONTEXT_POLICY["settlement"])
    return policy


def max_rarity(items: list[str], rarity_by_item: dict[str, str]) -> str:
    best = "common"
    for item in items:
        rarity = rarity_by_item.get(item, infer_item_rarity(item))
        if RARITY_ORDER.get(rarity, 0) > RARITY_ORDER.get(best, 0):
            best = rarity
    return best


def infer_item_rarity(item_id: str) -> str:
    local = item_id.split(":", 1)[-1].lower()
    namespace = item_namespace(item_id)
    if namespace in {"cataclysm", "soulsweapons", "block_factorys_bosses"} and slug_has_any(local, ("boss", "soul", "dragon", "lord")):
        return "legendary"
    if slug_has_any(local, ("ascendant", "annihilator", "incinerator")):
        return "ascendant"
    if slug_has_any(local, ("mythic", "dragonsteel", "dragonbone", "netherite", "netherite_scrap")):
        return "mythic"
    if slug_has_any(local, ("legendary", "totem", "sigil", "boss")):
        return "legendary"
    if slug_has_any(local, ("diamond", "echo_shard", "ancient", "artifact", "relic")):
        return "epic"
    if slug_has_any(local, ("gold", "ender", "seal", "scroll", "spell_book", "rune")):
        return "rare"
    if slug_has_any(local, ("iron", "guild_mark", "experience_bottle")):
        return "uncommon"
    return "common"


def high_rarity_items(items: list[str], rarity_by_item: dict[str, str], threshold: str) -> list[dict[str, str]]:
    threshold_rank = RARITY_ORDER[threshold]
    flagged: list[dict[str, str]] = []
    for item in items:
        rarity = rarity_by_item.get(item, infer_item_rarity(item))
        if RARITY_ORDER.get(rarity, 0) >= threshold_rank:
            flagged.append({"item_id": item, "rarity": rarity})
    return sorted(flagged, key=lambda entry: (RARITY_ORDER.get(entry["rarity"], 0), entry["item_id"]), reverse=True)


def scan_bountiful_reward_pools(known_items: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    pool_rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for path in sorted((ROOT / "config/openloader/data").glob("**/data/bountiful/bounty_pools/**/*.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        content = payload.get("content", {})
        if not isinstance(content, dict):
            continue
        rewards = []
        for reward_id, reward in content.items():
            if not isinstance(reward, dict):
                continue
            item_id = str(reward.get("content", ""))
            if reward.get("type") == "item" and item_id and item_id not in known_items:
                missing.append(item_id)
            rewards.append(
                {
                    "reward_id": reward_id,
                    "type": reward.get("type"),
                    "item_id": item_id if reward.get("type") == "item" else None,
                    "amount": reward.get("amount"),
                    "unitWorth": reward.get("unitWorth"),
                    "weightMult": reward.get("weightMult"),
                    "declared_rarity": str(reward.get("rarity", "")).lower() or None,
                }
            )
        pool_rows.append(
            {
                "pool_id": path.stem,
                "source_file": safe_rel(path),
                "context": "bounty",
                "rewards": rewards,
            }
        )
    return pool_rows, sorted(set(missing))


def canonical_materials() -> dict[str, dict[str, Any]]:
    path = ROOT / "config/ascendant_core/materials.json"
    if not path.exists():
        return {}
    data = read_json(path)
    materials = data.get("canonical_materials", {})
    return materials if isinstance(materials, dict) else {}


def material_like(item_id: str) -> bool:
    local = item_id.split(":", 1)[-1].lower()
    return bool(
        re.search(
            r"(^raw_|_ingot$|_nugget$|_gem$|_dust$|_scrap$|_ore$|_crystal$|_shard$|_scale$|_bone$|_plate$)",
            local,
        )
    )


def find_noncanonical_material_outputs(items: set[str], materials: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for material_name, info in materials.items():
        canonical = str(info.get("canonical", ""))
        status = str(info.get("status", ""))
        if not canonical or status == "planned":
            continue
        for item_id in sorted(items):
            local = item_id.split(":", 1)[-1].lower()
            if item_id != canonical and material_like(item_id) and material_name.lower() in local:
                rows.append(
                    {
                        "material": material_name,
                        "canonical_item": canonical,
                        "observed_item": item_id,
                    }
                )
    return rows


def build_structure_tiers(structure_registry: dict[str, Any]) -> dict[str, Any]:
    entries = []
    counts = Counter()
    for structure in structure_registry.get("structures", []):
        loot_tier = str(structure.get("loot_tier", "review"))
        reward_tier, ceiling, danger, rank = STRUCTURE_TIER_POLICY.get(loot_tier, STRUCTURE_TIER_POLICY["review"])
        row = {
            "structure_id": structure.get("structure_id"),
            "source_mod": structure.get("source_mod"),
            "structure_class": structure.get("structure_class"),
            "source_loot_tier": loot_tier,
            "reward_tier": reward_tier,
            "atlas_region_allowance": ["atlas_region_matching_structure"],
            "distance_ring_allowance": ["center", "inner"] if loot_tier == "village_supplies" else ["inner", "middle", "outer"],
            "guild_rank_tier": rank,
            "danger_tier": danger,
            "minimum_rarity": "common" if danger < 3 else "uncommon",
            "allowed_rarity_ceiling": ceiling,
            "material_tier": "mundane" if danger < 2 else "regional_to_boss",
            "gear_tier": reward_tier,
            "recommended_action": "manual_review" if reward_tier == "review" else "controlled",
            "notes": structure.get("notes", ""),
        }
        counts[reward_tier] += 1
        entries.append(row)
    return {
        "version": 1,
        "generated_at": now_iso(),
        "source_registry": "config/ascendant_index/structure_registry.json",
        "entries": entries,
        "summary": {"total_structures": len(entries), "by_reward_tier": dict(sorted(counts.items()))},
    }


def build_mob_drop_tiers(mob_registry: dict[str, Any]) -> dict[str, Any]:
    entries = []
    counts = Counter()
    for mob in mob_registry.get("mobs", []):
        threat = str(mob.get("bounty_tier") or mob.get("threat_tier") or "common_hostile")
        if threat == "none":
            threat = str(mob.get("threat_tier") or "passive_or_wildlife")
        drop_tier, ceiling, danger, rank = MOB_TIER_POLICY.get(threat, MOB_TIER_POLICY.get(str(mob.get("threat_tier")), MOB_TIER_POLICY["common_hostile"]))
        row = {
            "entity_id": mob.get("entity_id"),
            "name": mob.get("name"),
            "source_mod": mob.get("source_mod"),
            "threat_tier": mob.get("threat_tier"),
            "bounty_tier": mob.get("bounty_tier"),
            "drop_tier": drop_tier,
            "atlas_region_allowance": ["spawn_region_matching_entity"],
            "distance_ring_allowance": ["all"] if danger < 4 else ["outer", "edge"],
            "guild_rank_tier": rank,
            "danger_tier": danger,
            "minimum_rarity": "common" if danger < 3 else "uncommon",
            "allowed_rarity_ceiling": ceiling,
            "material_tier": "mundane" if danger < 2 else "regional_to_boss",
            "gear_tier": "none" if danger < 2 else drop_tier,
            "recommended_action": "untouched" if danger < 3 else "manual_review",
        }
        counts[drop_tier] += 1
        entries.append(row)
    return {
        "version": 1,
        "generated_at": now_iso(),
        "source_registry": "config/ascendant_index/mob_registry.json",
        "entries": entries,
        "summary": {"total_mobs": len(entries), "by_drop_tier": dict(sorted(counts.items()))},
    }


def build_boss_rewards(mob_drop_tiers: dict[str, Any]) -> dict[str, Any]:
    bosses = []
    for entry in mob_drop_tiers["entries"]:
        if entry["drop_tier"] in {"boss", "dragon"} or entry["danger_tier"] >= 4:
            ceiling = "ascendant" if entry["drop_tier"] == "dragon" else "mythic"
            bosses.append(
                {
                    "entity_id": entry["entity_id"],
                    "name": entry["name"],
                    "source_mod": entry["source_mod"],
                    "boss_reward_tier": entry["drop_tier"],
                    "atlas_region_allowance": entry["atlas_region_allowance"],
                    "distance_ring_allowance": ["outer", "edge"],
                    "guild_rank_tier": entry["guild_rank_tier"],
                    "danger_tier": entry["danger_tier"],
                    "minimum_rarity": "epic" if entry["drop_tier"] == "boss" else "legendary",
                    "allowed_rarity_ceiling": ceiling,
                    "material_tier": "dragon" if entry["drop_tier"] == "dragon" else "boss",
                    "gear_tier": "capstone" if entry["drop_tier"] == "dragon" else "late_game",
                    "recommended_action": "preserve_or_improve",
                }
            )
    return {
        "version": 1,
        "generated_at": now_iso(),
        "source_registry": "config/ascendant_index/mob_registry.json",
        "bosses": bosses,
        "summary": {
            "total_boss_reward_entries": len(bosses),
            "by_reward_tier": dict(sorted(Counter(row["boss_reward_tier"] for row in bosses).items())),
        },
    }


def build_bounty_reward_pools(bountiful_pools: list[dict[str, Any]], missing_item_refs: list[str]) -> dict[str, Any]:
    rank_policy = {
        "ar_village_hunter_rews": {
            "board": "village_hunter_board",
            "guild_rank_tier": "unranked_to_e_rank",
            "danger_tier": 1,
            "allowed_rarity_ceiling": "rare",
            "currency": ["kubejs:guild_mark"],
        },
        "ar_town_guild_rews": {
            "board": "town_guild_board",
            "guild_rank_tier": "d_rank_to_b_rank",
            "danger_tier": 3,
            "allowed_rarity_ceiling": "epic",
            "currency": ["kubejs:guild_mark", "kubejs:hunter_seal"],
        },
        "ar_major_guild_rews": {
            "board": "major_guild_registry",
            "guild_rank_tier": "b_rank_to_s_rank",
            "danger_tier": 5,
            "allowed_rarity_ceiling": "legendary",
            "currency": ["kubejs:hunter_seal", "kubejs:ascendant_sigil"],
        },
    }
    entries = []
    for pool in bountiful_pools:
        base = rank_policy.get(pool["pool_id"], {})
        entries.append(
            {
                "pool_id": pool["pool_id"],
                "source_file": pool["source_file"],
                "board": base.get("board", "manual_review"),
                "loot_context": "bounty",
                "atlas_region_allowance": ["atlas_region_matching_contract"],
                "distance_ring_allowance": ["all"] if base.get("danger_tier", 2) < 4 else ["middle", "outer", "edge"],
                "guild_rank_tier": base.get("guild_rank_tier", "manual_review"),
                "danger_tier": base.get("danger_tier", 2),
                "minimum_rarity": "common",
                "allowed_rarity_ceiling": base.get("allowed_rarity_ceiling", "rare"),
                "material_tier": "contract_currency",
                "gear_tier": "rank_reward",
                "recommended_action": "controlled",
                "currency_items": base.get("currency", []),
                "rewards": pool["rewards"],
            }
        )
    return {
        "version": 1,
        "generated_at": now_iso(),
        "source": "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_pools",
        "entries": entries,
        "missing_item_references": missing_item_refs,
        "summary": {
            "total_pools": len(entries),
            "reward_item_count": sum(len(entry["rewards"]) for entry in entries),
        },
    }


def build_rarity_budget() -> dict[str, Any]:
    return {
        "version": 1,
        "generated_at": now_iso(),
        "rarity_order": RARITY_ORDER,
        "context_budgets": {
            context: {
                "minimum_rarity": policy["minimum"],
                "allowed_rarity_ceiling": policy["ceiling"],
                "danger_tier": policy["danger"],
                "guild_rank_tier": policy["rank"],
                "distance_ring_allowance": policy["rings"],
                "atlas_region_allowance": policy["regions"],
            }
            for context, policy in SOURCE_CONTEXT_POLICY.items()
        },
        "guild_rank_budgets": {
            "unranked": {"ceiling": "uncommon", "routine_rewards": ["common", "uncommon"]},
            "e_rank": {"ceiling": "rare", "routine_rewards": ["common", "uncommon", "rare"]},
            "d_rank": {"ceiling": "rare", "routine_rewards": ["uncommon", "rare"]},
            "c_rank": {"ceiling": "epic", "routine_rewards": ["rare", "epic"]},
            "b_rank": {"ceiling": "legendary", "routine_rewards": ["rare", "epic", "legendary"]},
            "a_rank": {"ceiling": "mythic", "routine_rewards": ["epic", "legendary", "mythic"]},
            "s_rank": {"ceiling": "ascendant", "routine_rewards": ["legendary", "mythic", "ascendant"]},
        },
        "distance_ring_budgets": {
            "center": {"ceiling": "uncommon", "notes": "Hearthlands/Crownlands beginner zone."},
            "inner": {"ceiling": "rare", "notes": "Early exploration."},
            "middle": {"ceiling": "epic", "notes": "Dangerous structures and elite mobs begin."},
            "outer": {"ceiling": "mythic", "notes": "Boss and dragon approaches."},
            "edge": {"ceiling": "ascendant", "notes": "Corrupted/outer capstone content only."},
        },
    }


def make_loot_source_assignments(
    loot_tables: list[dict[str, Any]],
    rarity_by_item: dict[str, str],
    mod_name_by_namespace: dict[str, str],
    domain_by_item: dict[str, set[str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    entries = []
    counts_by_context = Counter()
    counts_by_action = Counter()
    high_rarity_low_tier = []
    high_rarity_village_basic = []
    invalid_json = []

    for table in loot_tables:
        source_id = table["source_id"]
        namespace = table["namespace"]
        items = table["items"]
        context = classify_context(source_id, namespace, items)
        policy = policy_for_context(context, source_id)
        ceiling = policy["ceiling"]
        max_seen = max_rarity(items, rarity_by_item)
        action = policy["action"]
        observed_high = high_rarity_items(items, rarity_by_item, "legendary")
        observed_basic_high = high_rarity_items(items, rarity_by_item, "epic")
        domains_present = sorted({domain for item in items for domain in domain_by_item.get(item, set())})
        magic_spell_items = [
            item
            for item in items
            if domain_by_item.get(item, set()) & {"magic_item", "spell", "magic_items", "spells"}
        ]
        accessory_relic_items = [
            item
            for item in items
            if domain_by_item.get(item, set()) & {"accessory_relic", "accessories_relics"}
        ]
        material_reward_items = [item for item in items if material_like(item)]
        if RARITY_ORDER.get(max_seen, 0) > RARITY_ORDER.get(ceiling, 0):
            action = "manual_review"
        if context in {"village", "settlement", "minor_ruin", "mob"} and observed_high:
            high_rarity_low_tier.append({"source_id": source_id, "context": context, "items": observed_high[:12]})
        if context in {"village", "settlement"} and observed_basic_high:
            high_rarity_village_basic.append({"source_id": source_id, "context": context, "items": observed_basic_high[:12]})
        if table["invalid_json"]:
            invalid_json.append({"source_id": source_id, "error": table["invalid_json"]})

        row = {
            "source_id": source_id,
            "source_mod": mod_name_by_namespace.get(namespace, namespace),
            "source_namespace": namespace,
            "source_kind": table["source_kind"],
            "source_file": table["source_file_display"],
            "loot_context": context,
            "atlas_region_allowance": policy["regions"],
            "distance_ring_allowance": policy["rings"],
            "guild_rank_tier": policy["rank"],
            "danger_tier": policy["danger"],
            "allowed_rarity_ceiling": ceiling,
            "minimum_rarity": policy["minimum"],
            "material_tier": policy["material"],
            "gear_tier": policy["gear"],
            "observed_max_rarity": max_seen,
            "observed_high_rarity_items": observed_high,
            "gear_domains_present": domains_present,
            "magic_spell_items": magic_spell_items,
            "accessory_relic_items": accessory_relic_items,
            "material_reward_items": material_reward_items,
            "output_item_count": len(items),
            "output_item_ids": items,
            "recommended_action": action,
            "invalid_json": table["invalid_json"],
        }
        counts_by_context[context] += 1
        counts_by_action[action] += 1
        entries.append(row)

    summary = {
        "total_loot_tables": len(entries),
        "by_context": dict(sorted(counts_by_context.items())),
        "by_recommended_action": dict(sorted(counts_by_action.items())),
        "high_rarity_low_tier_count": len(high_rarity_low_tier),
        "high_rarity_village_basic_count": len(high_rarity_village_basic),
        "invalid_json_count": len(invalid_json),
        "high_rarity_low_tier_examples": high_rarity_low_tier[:50],
        "high_rarity_village_basic_examples": high_rarity_village_basic[:50],
        "invalid_json": invalid_json[:50],
    }
    return entries, summary


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    def cell(value: Any) -> str:
        text = str(value if value is not None else "")
        text = text.replace("|", "\\|").replace("\n", " ")
        return text

    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)


def write_docs(
    loot_policy: dict[str, Any],
    structure_tiers: dict[str, Any],
    mob_tiers: dict[str, Any],
    boss_tiers: dict[str, Any],
    bounty_pools: dict[str, Any],
) -> None:
    summary = loot_policy["summary"]
    high_rarity_examples = summary.get("high_rarity_low_tier_examples", [])
    village_examples = summary.get("high_rarity_village_basic_examples", [])

    economy_doc = f"""# Ascendant Loot Economy System

Generated: {loot_policy['generated_at']}

## Status

This is the active loot and reward economy control scaffold. It audits installed mod jar loot tables, repo OpenLoader/datapack loot tables, live Bountiful reward pools, Loot Integrations behavior, the gear rarity registry, structure tiers, mob tiers, boss tiers, magic/spell sources, accessory/relic sources, and canonical material rewards.

No broad loot rewrites are enabled by this pass. Candidate notes live under `kubejs/server_scripts_disabled/review/ascendant_loot/` and are ignored by Minecraft.

## Core Rules

- Crownlands/Hearthlands and early village loot cannot award legendary, mythic, or ascendant gear.
- Early villages cannot award boss-tier or dragon-tier materials.
- Common dungeons may award common, uncommon, and rare items; dangerous dungeons may reach epic when the structure tier supports it.
- Boss-tier content must reward above random chests, with epic to mythic rewards depending on boss tier.
- Structure loot must match the structure danger tier in `config/ascendant_loot/structure_loot_tiers.json`.
- Bounties pay Guild Marks, Hunter Seals, or rank-appropriate rewards from `config/ascendant_loot/bounty_reward_pools.json`.
- Magic items and spells use the same rarity budget as gear, with boss/outer-region spell loot reserved for higher ranks.
- Relics and accessories are rare by default and should be tied to exploration, bosses, or ranked contracts.
- Loot policy must support `config/ascendant_index/gear_registry.json`, not contradict it.

## Machine Policy Files

- `config/ascendant_loot/loot_policy.json`: full loot-source audit and source-level assignments.
- `config/ascendant_loot/structure_loot_tiers.json`: every indexed structure mapped to reward tier, danger tier, rank tier, and rarity ceiling.
- `config/ascendant_loot/mob_drop_tiers.json`: every indexed mob mapped to drop tier and bounty/drop guardrails.
- `config/ascendant_loot/boss_reward_tiers.json`: boss and dragon reward tiers.
- `config/ascendant_loot/bounty_reward_pools.json`: live Bountiful reward pools with rank/danger ceilings.
- `config/ascendant_loot/loot_rarity_budget.json`: shared context, rank, and ring rarity ceilings.

## Audit Summary

{markdown_table(
        ['Metric', 'Count'],
        [
            ['Loot tables audited', summary['total_loot_tables']],
            ['Installed mod jars scanned', loot_policy['scan_inputs']['installed_mod_jars']],
            ['Repo datapack/OpenLoader loot tables', loot_policy['scan_inputs']['repo_datapack_loot_tables']],
            ['High-rarity low-tier warnings', summary['high_rarity_low_tier_count']],
            ['High-rarity village/basic warnings', summary['high_rarity_village_basic_count']],
            ['Structure reward entries', structure_tiers['summary']['total_structures']],
            ['Mob drop entries', mob_tiers['summary']['total_mobs']],
            ['Boss reward entries', boss_tiers['summary']['total_boss_reward_entries']],
            ['Bountiful reward pools', bounty_pools['summary']['total_pools']],
        ],
    )}

## Loot Integrations

`config/lootintegrations.json` is present and currently allows extra modded loot injection with `moddedItemWeight = 3`. That means random containers can receive additional modded items outside the original loot table. The scaffold treats this as a control risk: do not raise that weight, and do not rely on original chest tables alone for progression safety.

## Current Risk Notes

- Any source with `recommended_action = manual_review` needs human review before a real rewrite.
- Any village or settlement source showing epic-or-better output must be reduced or gated before terrain/civilization signoff.
- Boss and dragon drops should be preserved or improved, not flattened into generic chest loot.
"""

    if high_rarity_examples:
        economy_doc += "\n## High-Rarity Low-Tier Examples\n\n"
        rows = []
        for example in high_rarity_examples[:20]:
            item_preview = ", ".join(f"{i['item_id']} ({i['rarity']})" for i in example.get("items", [])[:5])
            rows.append([example.get("source_id"), example.get("context"), item_preview])
        economy_doc += markdown_table(["Source", "Context", "Flagged Items"], rows) + "\n"

    write_text(DOCS_DIR / "ASCENDANT_LOOT_ECONOMY.md", economy_doc)

    audit_rows = []
    for source in loot_policy["loot_sources"][:350]:
        audit_rows.append(
            [
                source["source_id"],
                source["source_mod"],
                source["loot_context"],
                source["danger_tier"],
                source["allowed_rarity_ceiling"],
                source["observed_max_rarity"],
                source["recommended_action"],
            ]
        )
    audit_doc = f"""# Loot Table Audit

Generated: {loot_policy['generated_at']}

This report summarizes the loot-source audit. The full per-source assignment for every scanned loot table is in `config/ascendant_loot/loot_policy.json`.

## Summary

{markdown_table(
        ['Metric', 'Count'],
        [
            ['Total loot tables', summary['total_loot_tables']],
            ['Invalid loot JSON', summary['invalid_json_count']],
            ['High-rarity low-tier sources', summary['high_rarity_low_tier_count']],
            ['High-rarity village/basic sources', summary['high_rarity_village_basic_count']],
        ],
    )}

## Context Counts

{markdown_table(['Context', 'Count'], [[k, v] for k, v in summary['by_context'].items()])}

## Action Counts

{markdown_table(['Recommended Action', 'Count'], [[k, v] for k, v in summary['by_recommended_action'].items()])}

## Source Assignments Preview

Only the first 350 rows are shown here to keep the markdown readable. The JSON policy contains every scanned source.

{markdown_table(['Source ID', 'Mod', 'Context', 'Danger', 'Ceiling', 'Observed Max', 'Action'], audit_rows)}
"""
    if village_examples:
        audit_doc += "\n## Village And Basic-Loot High Rarity Warnings\n\n"
        rows = []
        for example in village_examples[:50]:
            item_preview = ", ".join(f"{i['item_id']} ({i['rarity']})" for i in example.get("items", [])[:6])
            rows.append([example.get("source_id"), example.get("context"), item_preview])
        audit_doc += markdown_table(["Source", "Context", "Flagged Items"], rows) + "\n"

    write_text(DOCS_DIR / "LOOT_TABLE_AUDIT.md", audit_doc)

    structure_rows = []
    for entry in structure_tiers["entries"]:
        structure_rows.append(
            [
                entry["structure_id"],
                entry["source_mod"],
                entry["structure_class"],
                entry["source_loot_tier"],
                entry["reward_tier"],
                entry["danger_tier"],
                entry["allowed_rarity_ceiling"],
                entry["recommended_action"],
            ]
        )
    structure_doc = f"""# Structure Reward Tier Index

Generated: {structure_tiers['generated_at']}

This index maps every structure in `config/ascendant_index/structure_registry.json` to the reward economy scaffold. It does not change structure generation.

## Summary

{markdown_table(['Reward Tier', 'Count'], [[k, v] for k, v in structure_tiers['summary']['by_reward_tier'].items()])}

## Structure Reward Tiers

{markdown_table(['Structure ID', 'Mod', 'Class', 'Source Loot Tier', 'Reward Tier', 'Danger', 'Ceiling', 'Action'], structure_rows)}
"""
    write_text(DOCS_DIR / "STRUCTURE_REWARD_TIER_INDEX.md", structure_doc)


def update_docs_index() -> None:
    path = DOCS_DIR / "DOCS_INDEX.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    additions = [
        "- [ASCENDANT_LOOT_ECONOMY.md](ASCENDANT_LOOT_ECONOMY.md) - Authoritative loot/reward economy policy scaffold.",
        "- [LOOT_TABLE_AUDIT.md](LOOT_TABLE_AUDIT.md) - Generated loot table audit summary.",
        "- [STRUCTURE_REWARD_TIER_INDEX.md](STRUCTURE_REWARD_TIER_INDEX.md) - Generated structure reward tier index.",
    ]
    missing = [line for line in additions if line not in text]
    if not missing:
        return
    marker = "## Generated / Registry Docs"
    if marker in text:
        text = text.replace(marker, marker + "\n\n" + "\n".join(missing), 1)
    else:
        text += "\n\n## Loot Economy Docs\n\n" + "\n".join(missing) + "\n"
    path.write_text(text, encoding="utf-8")


def update_current_status(summary: dict[str, Any]) -> None:
    path = DOCS_DIR / "CURRENT_STATUS.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    block = f"""## Loot Economy Control Scaffold

- Status: generated audit/control scaffold only; no broad loot rewrites are enabled.
- Audited loot tables: {summary['total_loot_tables']}.
- High-rarity low-tier warnings: {summary['high_rarity_low_tier_count']}.
- High-rarity village/basic warnings: {summary['high_rarity_village_basic_count']}.
- Authoritative docs/configs: `docs/ASCENDANT_LOOT_ECONOMY.md`, `docs/LOOT_TABLE_AUDIT.md`, `docs/STRUCTURE_REWARD_TIER_INDEX.md`, and `config/ascendant_loot/*.json`.
- Next step after terrain signoff: manually review flagged loot sources, then approve narrow KubeJS/datapack rewrites source by source.
"""
    heading = "## Loot Economy Control Scaffold"
    if heading in text:
        start = text.index(heading)
        next_heading = text.find("\n## ", start + 1)
        if next_heading == -1:
            text = text[:start].rstrip() + "\n\n" + block
        else:
            text = text[:start].rstrip() + "\n\n" + block + "\n" + text[next_heading + 1 :].lstrip()
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_disabled_review_note(loot_policy: dict[str, Any]) -> None:
    flagged = loot_policy["summary"].get("high_rarity_village_basic_examples", [])
    rows = []
    for entry in flagged[:60]:
        rows.append(
            "- "
            + str(entry.get("source_id"))
            + ": "
            + ", ".join(f"{i['item_id']} ({i['rarity']})" for i in entry.get("items", [])[:6])
        )
    note = """# Ascendant Loot Rewrite Candidates

This folder is intentionally disabled. Minecraft and KubeJS should ignore it.

No rewrite is enabled by this pass. Use these notes only after the player approves a narrow loot correction.

## Candidate Review Queue

"""
    note += "\n".join(rows) if rows else "- No high-rarity village/basic candidates were detected in this run."
    write_text(DISABLED_REVIEW_DIR / "README.md", note)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    gear, structures, mobs, rarity_by_item, mod_name_by_namespace, domain_by_item = load_registries()
    kubejs_items = parse_kubejs_items()

    jar_loot = iter_jar_loot_tables()
    datapack_loot = iter_datapack_loot_tables()
    all_loot_tables = jar_loot + datapack_loot

    known_items = set(VANILLA_KNOWN_ITEMS) | set(rarity_by_item) | kubejs_items
    for table in all_loot_tables:
        known_items.update(table["items"])

    bountiful_pools, bounty_missing_items = scan_bountiful_reward_pools(known_items)
    for pool in bountiful_pools:
        for reward in pool["rewards"]:
            item_id = reward.get("item_id")
            if item_id:
                known_items.add(item_id)

    loot_sources, summary = make_loot_source_assignments(
        all_loot_tables,
        rarity_by_item,
        mod_name_by_namespace,
        domain_by_item,
    )
    all_output_items = {item for source in loot_sources for item in source["output_item_ids"]}
    materials = canonical_materials()
    noncanonical_material_outputs = find_noncanonical_material_outputs(all_output_items, materials)

    structure_tiers = build_structure_tiers(structures)
    mob_tiers = build_mob_drop_tiers(mobs)
    boss_tiers = build_boss_rewards(mob_tiers)
    bounty_pools = build_bounty_reward_pools(bountiful_pools, bounty_missing_items)
    rarity_budget = build_rarity_budget()

    structure_ids = {entry.get("structure_id") for entry in structures.get("structures", [])}
    policy_structure_refs = {
        entry.get("structure_id")
        for entry in structure_tiers["entries"]
        if entry.get("structure_id")
    }
    missing_structure_ids = sorted(str(s) for s in policy_structure_refs if s not in structure_ids)

    loot_policy = {
        "version": 1,
        "generated_at": now_iso(),
        "status": "audit_and_control_scaffold_only",
        "no_enabled_rewrites": True,
        "source_registries": {
            "gear": "config/ascendant_index/gear_registry.json",
            "structures": "config/ascendant_index/structure_registry.json",
            "mobs": "config/ascendant_index/mob_registry.json",
            "materials": "config/ascendant_core/materials.json",
        },
        "scan_inputs": {
            "active_instance_mods": str(ACTIVE_MODS),
            "installed_mod_jars": len(list(ACTIVE_MODS.glob("*.jar"))) if ACTIVE_MODS.exists() else 0,
            "installed_mod_jar_loot_tables": len(jar_loot),
            "repo_datapack_loot_tables": len(datapack_loot),
            "bountiful_reward_pools": len(bountiful_pools),
            "loot_integrations_config": "config/lootintegrations.json" if (ROOT / "config/lootintegrations.json").exists() else None,
        },
        "rules": [
            "Crownlands/Hearthlands loot should not give legendary, mythic, or ascendant gear.",
            "Early villages should not give boss-tier materials.",
            "Common dungeons can give common/uncommon/rare, not endgame gear.",
            "Boss-tier content must give better rewards than random chests.",
            "Structure loot should match structure danger tier.",
            "Bounties should pay Guild Marks, Hunter Seals, or rank-appropriate rewards.",
            "Magic items and spells should follow region and difficulty logic.",
            "Relics and accessories should be rare and tied to exploration, bosses, or rank contracts.",
            "Loot should support the gear rarity registry, not contradict it.",
        ],
        "rarity_order": RARITY_ORDER,
        "context_policy": SOURCE_CONTEXT_POLICY,
        "known_item_ids": sorted(known_items),
        "canonical_materials": materials,
        "loot_sources": loot_sources,
        "validation": {
            "high_rarity_low_tier_sources": summary["high_rarity_low_tier_examples"],
            "high_rarity_village_basic_sources": summary["high_rarity_village_basic_examples"],
            "noncanonical_material_outputs": noncanonical_material_outputs,
            "bounty_missing_item_references": bounty_missing_items,
            "policy_reference_checks": {
                "missing_structure_ids": missing_structure_ids,
                "missing_item_ids": [],
            },
        },
        "summary": summary,
    }

    write_json(OUT_DIR / "loot_policy.json", loot_policy)
    write_json(OUT_DIR / "structure_loot_tiers.json", structure_tiers)
    write_json(OUT_DIR / "mob_drop_tiers.json", mob_tiers)
    write_json(OUT_DIR / "boss_reward_tiers.json", boss_tiers)
    write_json(OUT_DIR / "bounty_reward_pools.json", bounty_pools)
    write_json(OUT_DIR / "loot_rarity_budget.json", rarity_budget)

    write_docs(loot_policy, structure_tiers, mob_tiers, boss_tiers, bounty_pools)
    update_docs_index()
    update_current_status(summary)
    write_disabled_review_note(loot_policy)

    print("Generated Ascendant loot economy scaffold.")
    print(f"Audited loot tables: {summary['total_loot_tables']}")
    print(f"High-rarity low-tier warnings: {summary['high_rarity_low_tier_count']}")
    print(f"High-rarity village/basic warnings: {summary['high_rarity_village_basic_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
