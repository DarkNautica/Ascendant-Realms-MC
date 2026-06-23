#!/usr/bin/env python3
"""Generate Ascendant structure tier, region, density, and loot-linkage policy files."""

from __future__ import annotations

import json
import pathlib
import re
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "config/ascendant_structures"
DOCS_DIR = ROOT / "docs"

STRUCTURE_REGISTRY_PATH = ROOT / "config/ascendant_index/structure_registry.json"
WORLDGEN_AUDIT_PATH = ROOT / "docs/generated/worldgen_content_audit.json"
STRUCTURE_LOOT_TIERS_PATH = ROOT / "config/ascendant_loot/structure_loot_tiers.json"
MANUAL_OBSERVATIONS_PATH = ROOT / "config/ascendant_structures/manual_structure_observations.json"

BEGINNER_REGIONS = {"hearthlands", "crownlands", "center"}
BOSS_OR_DUNGEON_CATEGORIES = {"dangerous_dungeon", "boss_arena", "dragon_tier_zone"}
VILLAGE_OR_TOWN_CATEGORIES = {"settlement", "town", "village"}
WATER_REGION_HINTS = {
    "verdant_coast",
    "coastal_only",
    "frostmarch_if_frozen",
    "frozen_ocean_only",
    "frostmarch",
    "north_east_marches",
    "south_east_wilds",
}
LAND_FIRST_REGION_HINTS = {
    "hearthlands",
    "crownlands",
    "sunreach",
    "south_west_wilds",
    "stoneback_highlands",
    "north_west_marches",
}

CLASS_POLICY = {
    "settlement": {
        "category": "settlement",
        "regions": ["hearthlands", "crownlands", "region_compatible_settlement"],
        "biome_families": ["plains", "forest", "savanna", "taiga", "desert_if_native"],
        "rings": ["center", "inner"],
        "danger": 0,
        "rank": "unranked_to_e_rank",
        "loot": "settlement_basic",
        "rarity_ceiling": "uncommon",
    },
    "landmark_or_ruin": {
        "category": "ruin",
        "regions": ["atlas_region_matching_biome_tag"],
        "biome_families": ["native_palette"],
        "rings": ["inner", "middle"],
        "danger": 1,
        "rank": "e_rank_to_d_rank",
        "loot": "minor_ruin",
        "rarity_ceiling": "rare",
    },
    "dangerous_dungeon": {
        "category": "dungeon",
        "regions": ["atlas_region_matching_biome_tag"],
        "biome_families": ["native_palette", "underground_if_step_matches"],
        "rings": ["middle", "outer"],
        "danger": 3,
        "rank": "d_rank_to_b_rank",
        "loot": "dangerous_dungeon",
        "rarity_ceiling": "epic",
    },
    "boss_arena": {
        "category": "boss",
        "regions": ["outer", "corrupted", "boss_theme_region"],
        "biome_families": ["boss_theme_specific"],
        "rings": ["outer", "edge"],
        "danger": 5,
        "rank": "b_rank_to_s_rank",
        "loot": "boss_arena",
        "rarity_ceiling": "mythic",
    },
    "dragon_tier_zone": {
        "category": "dragon",
        "regions": ["outer", "dragonbound", "boss_theme_region"],
        "biome_families": ["dragon_theme_specific"],
        "rings": ["outer", "edge"],
        "danger": 5,
        "rank": "a_rank_to_s_rank",
        "loot": "dragon_tier",
        "rarity_ceiling": "ascendant",
    },
    "end_landmark": {
        "category": "end_landmark",
        "regions": ["end_only"],
        "biome_families": ["end"],
        "rings": ["dimension_locked"],
        "danger": 4,
        "rank": "b_rank_to_a_rank",
        "loot": "end_landmark",
        "rarity_ceiling": "mythic",
    },
    "nether_landmark": {
        "category": "nether_landmark",
        "regions": ["nether_only"],
        "biome_families": ["nether"],
        "rings": ["dimension_locked"],
        "danger": 4,
        "rank": "b_rank_to_a_rank",
        "loot": "nether_landmark",
        "rarity_ceiling": "legendary",
    },
    "uncategorized_structure": {
        "category": "ambient",
        "regions": ["atlas_region_matching_biome_tag"],
        "biome_families": ["native_palette"],
        "rings": ["inner", "middle", "outer"],
        "danger": 2,
        "rank": "manual_review",
        "loot": "review",
        "rarity_ceiling": "rare",
    },
}

LOOT_TIER_POLICY = {
    "village_supplies": ("settlement_basic", "uncommon", 0, "unranked_to_e_rank"),
    "minor_ruin": ("minor_ruin", "rare", 1, "e_rank_to_d_rank"),
    "rare_to_epic": ("dangerous_dungeon", "epic", 3, "d_rank_to_b_rank"),
    "legendary_to_mythic": ("boss_arena", "mythic", 5, "b_rank_to_s_rank"),
    "mythic_to_ascendant": ("dragon_tier", "ascendant", 5, "a_rank_to_s_rank"),
    "epic_to_mythic": ("end_landmark", "mythic", 4, "b_rank_to_a_rank"),
    "rare_to_legendary": ("nether_landmark", "legendary", 4, "b_rank_to_a_rank"),
    "review": ("review", "rare", 2, "manual_review"),
}

SOURCE_MOD_BY_JAR_TOKEN = {
    "aquamirae": "Aquamirae",
    "YungsBetterDungeons": "YUNG's Better Dungeons",
    "YungsBetterMineshafts": "YUNG's Better Mineshafts",
    "YungsBetterStrongholds": "YUNG's Better Strongholds",
    "YungsBridges": "YUNG's Bridges",
    "YungsExtras": "YUNG's Extras",
    "idas": "Integrated Dungeons and Structures",
    "integrated_villages": "Integrated Villages",
    "Towns-and-Towers": "Towns and Towers",
    "Structory": "Structory",
    "MoogsVoyagerStructures": "Moog's Voyager Structures",
    "MoogsSoaringStructures": "Moog's Soaring Structures",
    "MoogsEndStructures": "Moog's End Structures",
    "create_structures_arise": "Create: Structures Arise",
    "L_Enders_Cataclysm": "L_Ender's Cataclysm",
    "IceAndFireCE": "Ice And Fire Community Edition",
    "mowziesmobs": "Mowzie's Mobs",
    "block_factorys_bosses": "Bosses'Rise",
    "soulslike": "Marium's Soulslike Weaponry",
    "irons_spellbooks": "Iron's Spells 'n Spellbooks",
    "born_in_chaos": "Born in Chaos",
    "Terralith": "Terralith",
    "minecraft-1.20.1": "Minecraft",
}

WEAK_HINT_TOKENS = {
    "water": ["ocean", "ship", "shipwreck", "boat", "kraken", "siren", "sunken", "water", "beach", "coast", "lighthouse"],
    "frozen": ["ice", "frozen", "frost", "snow", "snowy", "yeti"],
    "arid": ["desert", "badlands", "mesa", "sand", "pyramid", "terracotta", "sandworm"],
    "wet_lush": ["jungle", "lush", "mangrove", "swamp", "moss", "azalea"],
    "mountain": ["mountain", "highland", "hills", "peaks", "spire", "gorgon", "cyclops"],
    "forest": ["forest", "taiga", "spruce", "dark_oak", "oak", "birch"],
    "settlement": ["village", "town", "market", "camp", "house", "inn", "lumber"],
    "dungeon": ["dungeon", "mineshaft", "stronghold", "catacomb", "crypt", "temple", "tower", "spawner"],
    "boss": ["boss", "arena", "acropolis", "cataclysm", "champion"],
    "dragon": ["dragon", "hydra", "cyclops", "gorgon", "siren", "dread"],
    "sky": ["airship", "floating", "sky", "soaring", "airdrop"],
    "nether": ["nether", "bastion", "fortress", "crimson", "warped", "underworld"],
    "end": ["end", "ender", "end_city"],
}

OCEAN_BIOME_TAGS = {
    "minecraft:is_ocean",
    "minecraft:is_deep_ocean",
    "c:is_ocean",
    "forge:is_ocean",
}
COAST_BIOME_TAGS = {
    "minecraft:is_beach",
    "forge:is_beach",
}
RIVER_BIOME_TAGS = {
    "minecraft:is_river",
    "forge:is_river",
}
WATER_BIOME_TAGS = OCEAN_BIOME_TAGS | COAST_BIOME_TAGS | RIVER_BIOME_TAGS
FROZEN_BIOME_TAGS = {
    "minecraft:is_snowy",
    "c:climate_cold",
    "forge:is_cold",
}
NETHER_BIOME_TAGS = {"minecraft:is_nether"}
END_BIOME_TAGS = {"minecraft:is_end"}
FOREST_BIOME_TAGS = {"minecraft:is_forest", "minecraft:is_taiga", "forge:is_forest", "forge:is_taiga"}
SAVANNA_BIOME_TAGS = {"minecraft:is_savanna", "forge:is_savanna"}
MOUNTAIN_BIOME_TAGS = {"minecraft:is_mountain", "forge:is_mountain", "c:is_mountain"}
JUNGLE_WET_BIOME_TAGS = {"minecraft:is_jungle", "forge:is_jungle", "minecraft:is_swamp", "forge:is_swamp"}


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


def slug_text(*parts: object) -> str:
    return " ".join(str(part or "").lower() for part in parts)


def source_mod_from_audit(audit_entry: dict[str, Any]) -> str:
    source = str(audit_entry.get("source") or "")
    for token, label in SOURCE_MOD_BY_JAR_TOKEN.items():
        if token.lower() in source.lower():
            return label
    if source.endswith(".jar"):
        return source.removesuffix(".jar")
    return source or "unknown"


def is_registry_policy_structure(entry: dict[str, Any]) -> bool:
    structure_id = str(entry.get("structure_id") or "")
    return bool(structure_id) and not structure_id.startswith("data/")


def is_audit_policy_structure(entry: dict[str, Any]) -> bool:
    if not isinstance(entry, dict):
        return False
    return bool(entry.get("type") or entry.get("start_pool") or entry.get("structure_sets"))


def normalize_tag_value(raw: Any) -> str | None:
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict):
        value = raw.get("id")
        return str(value) if value else None
    return None


def tag_id_from_archive_name(name: str) -> str | None:
    match = re.match(r"data/([^/]+)/tags/worldgen/biome/(.+)\.json$", name)
    if not match:
        return None
    namespace, path = match.groups()
    return f"{namespace}:{path}"


def tag_id_from_openloader_path(path: pathlib.Path, data_root: pathlib.Path) -> str | None:
    try:
        parts = path.relative_to(data_root).parts
    except ValueError:
        return None
    if len(parts) < 7 or parts[1] != "data" or parts[3:6] != ("tags", "worldgen", "biome"):
        return None
    namespace = parts[2]
    tag_path = "/".join(parts[6:]).removesuffix(".json")
    return f"{namespace}:{tag_path}"


def load_biome_tag_map(audit: dict[str, Any]) -> dict[str, list[str]]:
    tag_map: dict[str, list[str]] = {}

    def ingest(tag_id: str, raw: bytes) -> None:
        try:
            payload = json.loads(raw.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return
        values = payload.get("values", []) if isinstance(payload, dict) else []
        if not isinstance(values, list):
            return
        normalized = [value for value in (normalize_tag_value(item) for item in values) if value]
        if normalized:
            tag_map.setdefault(tag_id, [])
            tag_map[tag_id].extend(str(value) for value in normalized)

    for source in audit.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_path = pathlib.Path(str(source.get("path") or ""))
        if not source_path.exists() or source_path.suffix.lower() != ".jar":
            continue
        try:
            with zipfile.ZipFile(source_path) as archive:
                for name in archive.namelist():
                    tag_id = tag_id_from_archive_name(name)
                    if tag_id:
                        ingest(tag_id, archive.read(name))
        except (OSError, zipfile.BadZipFile):
            continue

    openloader_root = ROOT / "config/openloader/data"
    if openloader_root.exists():
        for tag_path in openloader_root.rglob("data/*/tags/worldgen/biome/*.json"):
            tag_id = tag_id_from_openloader_path(tag_path, openloader_root)
            if tag_id:
                ingest(tag_id, tag_path.read_bytes())

    return {tag: sorted(dict.fromkeys(values)) for tag, values in sorted(tag_map.items())}


def load_structure_json_map(audit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    structure_json: dict[str, dict[str, Any]] = {}

    def structure_id_from_archive_name(name: str) -> str | None:
        match = re.match(r"data/([^/]+)/worldgen/structure/(.+)\.json$", name)
        if not match:
            return None
        namespace, path = match.groups()
        return f"{namespace}:{path}"

    def structure_id_from_openloader_path(path: pathlib.Path, data_root: pathlib.Path) -> str | None:
        try:
            parts = path.relative_to(data_root).parts
        except ValueError:
            return None
        if len(parts) < 6 or parts[1] != "data" or parts[3:5] != ("worldgen", "structure"):
            return None
        namespace = parts[2]
        structure_path = "/".join(parts[5:]).removesuffix(".json")
        return f"{namespace}:{structure_path}"

    def ingest(structure_id: str, raw: bytes) -> None:
        try:
            payload = json.loads(raw.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return
        if isinstance(payload, dict):
            structure_json[structure_id] = payload

    for source in audit.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_path = pathlib.Path(str(source.get("path") or ""))
        if not source_path.exists() or source_path.suffix.lower() != ".jar":
            continue
        try:
            with zipfile.ZipFile(source_path) as archive:
                for name in archive.namelist():
                    structure_id = structure_id_from_archive_name(name)
                    if structure_id:
                        ingest(structure_id, archive.read(name))
        except (OSError, zipfile.BadZipFile):
            continue

    openloader_root = ROOT / "config/openloader/data"
    if openloader_root.exists():
        for structure_path in openloader_root.rglob("data/*/worldgen/structure/*.json"):
            structure_id = structure_id_from_openloader_path(structure_path, openloader_root)
            if structure_id:
                ingest(structure_id, structure_path.read_bytes())

    return structure_json


def resolve_biome_selector(selector: Any, tag_map: dict[str, list[str]], max_depth: int = 10) -> dict[str, Any]:
    pending: list[str] = []
    if isinstance(selector, list):
        pending.extend(str(item) for item in selector if item)
    elif selector:
        pending.append(str(selector))

    resolved_biomes: set[str] = set()
    tag_refs: set[str] = set()
    unresolved_tags: set[str] = set()
    seen_tags: set[str] = set()

    def visit(value: str, depth: int) -> None:
        if not value:
            return
        if value.startswith("#"):
            tag_id = value[1:]
            tag_refs.add(tag_id)
            if tag_id in seen_tags:
                return
            seen_tags.add(tag_id)
            tag_values = tag_map.get(tag_id)
            if not tag_values or depth >= max_depth:
                unresolved_tags.add(tag_id)
                return
            for child in tag_values:
                visit(str(child), depth + 1)
        else:
            resolved_biomes.add(value)

    for item in pending:
        visit(item, 0)

    return {
        "selector": selector,
        "tag_refs": sorted(tag_refs),
        "allowed_biome_ids": sorted(resolved_biomes),
        "unresolved_tags": sorted(unresolved_tags),
    }


def weak_name_hints(structure_id: str, audit_entry: dict[str, Any], source_mod: str) -> dict[str, list[str]]:
    text = slug_text(
        structure_id,
        audit_entry.get("biomes"),
        audit_entry.get("start_pool"),
        audit_entry.get("type"),
        audit_entry.get("step"),
        source_mod,
    )
    hints: dict[str, list[str]] = {}
    for family, tokens in WEAK_HINT_TOKENS.items():
        matched = sorted(token for token in tokens if token in text)
        if matched:
            hints[family] = matched
    return hints


def default_manual_observations() -> list[dict[str, Any]]:
    return [
        {
            "requested_structure_id": "iceandfire:*_dragon_roost",
            "actual_structure_id_seen": "iceandfire:*_dragon_roost",
            "locate_command": "/locate structure iceandfire:<dragon_roost_variant>",
            "coordinates": None,
            "atlas_region": None,
            "biome": None,
            "visual_issue_tags": ["water_island", "wet_terrain_mismatch", "land_structure"],
            "player_notes": "Dragon roosts were reported spawning as islands in water like oceans or lakes.",
            "screenshot_reference": None,
            "decision": "candidate_land_placement_review",
            "timestamp_or_session_note": "Jayden first Structure Director visual pass, 2026-06-17",
        },
        {
            "requested_structure_id": "idas:abandoned_vineyard",
            "actual_structure_id_seen": "idas:abandoned_vineyard",
            "locate_command": "/locate structure idas:abandoned_vineyard",
            "coordinates": {"x": 9568, "z": 9264},
            "atlas_region": "south_east_wilds",
            "biome": "terralith:hot_shrubland",
            "visual_issue_tags": ["water_island", "wet_terrain_mismatch", "region_fit_mismatch", "land_structure"],
            "player_notes": "Abandoned vineyard spawned as an island in water and in an odd region context.",
            "screenshot_reference": None,
            "decision": "candidate_land_and_region_lock_review",
            "timestamp_or_session_note": "Jayden first Structure Director visual pass, latest.log locate evidence",
        },
        {
            "requested_structure_id": "iceandfire:gorgon_temple",
            "actual_structure_id_seen": "idas:labyrinth",
            "locate_command": "/locate structure iceandfire:gorgon_temple then /locate structure idas:labyrinth",
            "coordinates": {"x": 2704, "z": 14816},
            "atlas_region": "sunreach",
            "biome": "terralith:desert_canyon",
            "visual_issue_tags": ["idas_replacement_override", "looked_good"],
            "player_notes": "IDAS overrides this Ice and Fire structure with idas:labyrinth; Jayden said the labyrinth looked good.",
            "screenshot_reference": None,
            "decision": "acceptable_mod_override_document_only",
            "timestamp_or_session_note": "Jayden first Structure Director visual pass, latest.log override evidence",
        },
        {
            "requested_structure_id": "iceandfire:graveyard",
            "actual_structure_id_seen": "idas:haunted_manor",
            "locate_command": "/locate structure iceandfire:graveyard then /locate structure idas:haunted_manor",
            "coordinates": None,
            "atlas_region": None,
            "biome": None,
            "visual_issue_tags": ["idas_replacement_override", "needs_followup"],
            "player_notes": "IDAS overrides this Ice and Fire structure with idas:haunted_manor; placement still needs follow-up if it looks bad.",
            "screenshot_reference": None,
            "decision": "needs_followup",
            "timestamp_or_session_note": "Jayden first Structure Director visual pass, latest.log override evidence",
        },
    ]


def load_manual_observations() -> list[dict[str, Any]]:
    if not MANUAL_OBSERVATIONS_PATH.exists():
        return default_manual_observations()
    try:
        data = read_json(MANUAL_OBSERVATIONS_PATH)
    except json.JSONDecodeError:
        return default_manual_observations()
    observations = data.get("observations", []) if isinstance(data, dict) else []
    loaded = [entry for entry in observations if isinstance(entry, dict)]
    return loaded or default_manual_observations()


def observation_matches(structure_id: str, observation: dict[str, Any]) -> bool:
    ids = [
        str(observation.get("requested_structure_id") or ""),
        str(observation.get("actual_structure_id_seen") or ""),
    ]
    for raw in ids:
        if not raw:
            continue
        pattern = "^" + re.escape(raw).replace("\\*", ".*") + "$"
        if re.match(pattern, structure_id):
            return True
    return False


def start_height_value(start_height: Any) -> int | None:
    if isinstance(start_height, dict):
        if "absolute" in start_height and isinstance(start_height.get("absolute"), int):
            return int(start_height["absolute"])
        for key in ("min_inclusive", "max_inclusive"):
            child = start_height.get(key)
            if isinstance(child, dict) and isinstance(child.get("absolute"), int):
                return int(child["absolute"])
    return None


def biome_families_from_evidence(
    resolved_biomes: list[str],
    tag_refs: list[str],
    biome_audit: dict[str, Any],
) -> list[str]:
    families: set[str] = set()
    tag_set = set(tag_refs)

    if tag_set & NETHER_BIOME_TAGS:
        families.add("nether")
    if tag_set & END_BIOME_TAGS:
        families.add("end")
    if tag_set & OCEAN_BIOME_TAGS:
        families.add("ocean")
    if tag_set & RIVER_BIOME_TAGS:
        families.add("river_wetland")
    if tag_set & COAST_BIOME_TAGS:
        families.add("coastline")
    if tag_set & FROZEN_BIOME_TAGS:
        families.add("frost_cold")
    if tag_set & FOREST_BIOME_TAGS:
        families.add("forest_taiga")
    if tag_set & SAVANNA_BIOME_TAGS:
        families.add("plains_savanna")
    if tag_set & MOUNTAIN_BIOME_TAGS:
        families.add("mountain_highland")
    if tag_set & JUNGLE_WET_BIOME_TAGS:
        families.add("jungle_wet")

    known_biome_count = 0
    water_biome_count = 0
    frozen_water_biome_count = 0
    cold_biome_count = 0
    arid_biome_count = 0
    wet_biome_count = 0
    highland_biome_count = 0
    for biome_id in resolved_biomes:
        biome_info = biome_audit.get(biome_id, {}) if isinstance(biome_audit.get(biome_id), dict) else {}
        if not biome_info:
            continue
        known_biome_count += 1
        bucket = biome_info.get("bucket", {}) if isinstance(biome_info.get("bucket"), dict) else {}
        climate_bucket = str(bucket.get("climate_bucket") or "")
        terrain_bucket = str(bucket.get("terrain_bucket") or "")
        flags = set(str(flag) for flag in bucket.get("flags", []) if flag)
        temperature = biome_info.get("temperature")
        downfall = biome_info.get("downfall")

        if terrain_bucket == "water_or_sea" or "aquatic_features" in flags or "oceanic_noise" in flags:
            water_biome_count += 1
            if climate_bucket == "frozen_or_snow" or "freezing" in flags:
                frozen_water_biome_count += 1
        if climate_bucket == "frozen_or_snow" or "freezing" in flags or "snow_precipitation" in flags:
            cold_biome_count += 1
        if climate_bucket == "hot_arid" or "desert_features" in flags:
            arid_biome_count += 1
        if "wet" in flags or (isinstance(downfall, (int, float)) and downfall >= 0.75):
            wet_biome_count += 1
        if terrain_bucket == "mountain_or_highland":
            highland_biome_count += 1
        if isinstance(temperature, (int, float)) and temperature <= 0.15:
            cold_biome_count += 1
        if isinstance(temperature, (int, float)) and temperature >= 1.0 and (
            not isinstance(downfall, (int, float)) or downfall <= 0.35
        ):
            arid_biome_count += 1

    if known_biome_count:
        if water_biome_count / known_biome_count >= 0.6:
            families.add("ocean")
            if frozen_water_biome_count and frozen_water_biome_count / max(water_biome_count, 1) >= 0.75 and tag_set & FROZEN_BIOME_TAGS:
                families.add("frozen_ocean")
        if cold_biome_count / known_biome_count >= 0.35 or tag_set & FROZEN_BIOME_TAGS:
            families.add("frost_cold")
        if arid_biome_count / known_biome_count >= 0.35:
            families.add("desert_badlands")
        if wet_biome_count / known_biome_count >= 0.35:
            families.add("jungle_wet")
        if highland_biome_count / known_biome_count >= 0.45 and not families.intersection({"ocean", "jungle_wet"}):
            families.add("mountain_highland")

    if not families:
        families.add("native_palette")
    return sorted(families)


def build_structure_evidence(
    structure_id: str,
    registry_entry: dict[str, Any] | None,
    audit_entry: dict[str, Any],
    source_mod: str,
    structure_sets: list[dict[str, Any]],
    loot_entry: dict[str, Any],
    tag_map: dict[str, list[str]],
    structure_json_map: dict[str, dict[str, Any]],
    biome_audit: dict[str, Any],
    manual_observations: list[dict[str, Any]],
) -> dict[str, Any]:
    structure_json = structure_json_map.get(structure_id, {})
    resolved = resolve_biome_selector(audit_entry.get("biomes") or structure_json.get("biomes"), tag_map)
    block_profile = audit_entry.get("block_profile", {}) if isinstance(audit_entry.get("block_profile"), dict) else {}
    material_counts = block_profile.get("material_counts", {}) if isinstance(block_profile.get("material_counts"), dict) else {}
    top_blocks = block_profile.get("top_blocks", {}) if isinstance(block_profile.get("top_blocks"), dict) else {}
    total_blocks = int(block_profile.get("total_blocks_sampled") or 0)
    fluid_blocks = sum(
        int(count)
        for block, count in top_blocks.items()
        if isinstance(count, int) and any(token in str(block) for token in ["water", "kelp", "seagrass", "coral", "bubble_column"])
    )
    matched_observations = [
        observation
        for observation in manual_observations
        if observation_matches(structure_id, observation)
    ]

    evidence_sources: list[dict[str, Any]] = []
    if matched_observations:
        evidence_sources.append({"source": "manual_live_observation", "strength": "strong", "count": len(matched_observations)})
    if resolved["allowed_biome_ids"] or resolved["tag_refs"]:
        evidence_sources.append(
            {
                "source": "biome_tag_or_selector",
                "strength": "strong",
                "resolved_biome_count": len(resolved["allowed_biome_ids"]),
                "tag_ref_count": len(resolved["tag_refs"]),
            }
        )
    if structure_sets:
        evidence_sources.append({"source": "structure_set_rules", "strength": "strong", "count": len(structure_sets)})
    if structure_json:
        evidence_sources.append({"source": "structure_json", "strength": "strong"})
    if audit_entry.get("start_pool") or audit_entry.get("templates_sampled"):
        evidence_sources.append(
            {
                "source": "template_pool_or_nbt",
                "strength": "strong",
                "templates_sampled": audit_entry.get("templates_sampled") or 0,
            }
        )
    if total_blocks > 100:
        evidence_sources.append({"source": "block_palette", "strength": "strong", "total_blocks_sampled": total_blocks})
    if registry_entry and registry_entry.get("structure_class"):
        evidence_sources.append({"source": "structure_registry_class", "strength": "medium"})
    if registry_entry and registry_entry.get("integration_hooks"):
        evidence_sources.append({"source": "registry_integration_hooks", "strength": "medium"})
    if loot_entry:
        evidence_sources.append({"source": "loot_policy_linkage", "strength": "medium"})
    if audit_entry.get("type") or audit_entry.get("step"):
        evidence_sources.append({"source": "worldgen_structure_type_or_step", "strength": "medium"})

    hints = weak_name_hints(structure_id, audit_entry, source_mod)
    if hints:
        evidence_sources.append({"source": "name_path_mod_label_hints", "strength": "weak", "hints": hints})

    families = biome_families_from_evidence(resolved["allowed_biome_ids"], resolved["tag_refs"], biome_audit)
    height_value = start_height_value(structure_json.get("start_height"))
    evidence = {
        "structure_id": structure_id,
        "source_mod": source_mod,
        "dimension": "nether" if "nether" in families else "end" if "end" in families else "overworld",
        "biome_tag_or_selector": audit_entry.get("biomes") or structure_json.get("biomes"),
        "allowed_biome_ids": resolved["allowed_biome_ids"],
        "biome_tag_refs": resolved["tag_refs"],
        "unresolved_biome_tags": resolved["unresolved_tags"],
        "template_pool_ids": [value for value in [audit_entry.get("start_pool"), structure_json.get("start_pool")] if value],
        "template_nbt_ids": audit_entry.get("template_ids", []) if isinstance(audit_entry.get("template_ids"), list) else [],
        "templates_sampled": audit_entry.get("templates_sampled") or 0,
        "block_palette_evidence": {
            "available": total_blocks > 100,
            "fluid_or_water_block_count": fluid_blocks,
            "fluid_or_water_ratio": round(fluid_blocks / total_blocks, 4) if total_blocks else 0.0,
            "common_block_families": sorted(material_counts.keys()),
            "dominant_materials": block_profile.get("dominant_materials", []),
            "top_blocks_preview": dict(list(top_blocks.items())[:20]),
            "total_blocks_sampled": total_blocks,
        },
        "loot_table_ids": sorted(set(str(item) for item in audit_entry.get("loot_tables", []) if item))
        if isinstance(audit_entry.get("loot_tables"), list)
        else [],
        "terrain_adaptation": structure_json.get("terrain_adaptation") or audit_entry.get("terrain_adaptation"),
        "placement_type": structure_json.get("type") or audit_entry.get("type"),
        "heightmap": structure_json.get("project_start_to_heightmap"),
        "start_height": structure_json.get("start_height"),
        "start_height_absolute_hint": height_value,
        "processor_lists": audit_entry.get("processor_lists", []) if isinstance(audit_entry.get("processor_lists"), list) else [],
        "structure_sets": structure_sets,
        "manual_live_evidence": matched_observations,
        "name_hints_weak_only": hints,
        "evidence_sources": evidence_sources,
        "biome_families_from_evidence": families,
    }
    return evidence


def classify_structure_from_evidence(
    structure_id: str,
    registry_entry: dict[str, Any] | None,
    audit_entry: dict[str, Any],
    evidence: dict[str, Any],
) -> tuple[str, list[str]]:
    raw_class = str((registry_entry or {}).get("structure_class") or "")
    integration_hooks = set(str(value) for value in (registry_entry or {}).get("integration_hooks", []) if value)
    families = set(evidence.get("biome_families_from_evidence", []))
    placement_type = str(evidence.get("placement_type") or "")
    reasons: list[str] = []

    if "nether" in families:
        return "nether_landmark", ["Biome tag/selector evidence places this in Nether biome context."]
    if "end" in families:
        return "end_landmark", ["Biome tag/selector evidence places this in End biome context."]
    if raw_class in CLASS_POLICY:
        reasons.append(f"Registry class `{raw_class}` is used as medium evidence.")
        return raw_class, reasons
    if "dragonbound" in integration_hooks:
        return "dragon_tier_zone", ["Registry integration hook `dragonbound` marks this as dragon-tier content."]
    if "boss_bounty" in integration_hooks:
        return "boss_arena", ["Registry integration hook `boss_bounty` marks this as boss-tier content."]
    if placement_type in {"minecraft:mineshaft", "minecraft:stronghold", "minecraft:ancient_city"}:
        return "dangerous_dungeon", [f"Worldgen structure type `{placement_type}` is dungeon-like medium evidence."]
    if evidence.get("loot_table_ids") or int((evidence.get("block_palette_evidence") or {}).get("fluid_or_water_block_count") or 0) == 0:
        return "landmark_or_ruin", ["Block/loot evidence exists but no stronger category evidence was found."]
    return "uncategorized_structure", ["No non-name evidence supports a narrower final category."]


def confidence_from_evidence(evidence: dict[str, Any], sensitive: bool) -> tuple[int, str, dict[str, int]]:
    counts = {"strong": 0, "medium": 0, "weak": 0}
    score = 0
    for source in evidence.get("evidence_sources", []):
        strength = str(source.get("strength") or "weak")
        if strength not in counts:
            strength = "weak"
        counts[strength] += 1
        score += {"strong": 18, "medium": 9, "weak": 1}[strength]
        if source.get("source") == "manual_live_observation":
            score += 14
        if source.get("source") == "block_palette" and source.get("total_blocks_sampled", 0) >= 1000:
            score += 5
        if source.get("source") == "biome_tag_or_selector" and source.get("resolved_biome_count", 0) > 0:
            score += 5
    if sensitive and counts["strong"] == 0:
        score = min(score, 39)
    score = min(score, 100)
    tier = "strong" if score >= 70 else "medium" if score >= 45 else "weak"
    return score, tier, counts


def infer_regions_from_evidence(structure_class: str, biome_families: list[str]) -> list[str]:
    families = set(biome_families)
    regions: list[str] = []
    if "nether" in families:
        return ["nether_only"]
    if "end" in families:
        return ["end_only"]
    if structure_class == "settlement":
        regions.extend(["hearthlands", "crownlands", "region_compatible_settlement"])
    if "frozen_ocean" in families:
        regions.extend(["frostmarch", "north_east_marches", "frozen_ocean_only"])
    elif "frost_cold" in families:
        regions.extend(["frostmarch", "north_east_marches"])
    if "ocean" in families:
        regions.extend(["verdant_coast", "frostmarch_if_frozen", "coastal_only"])
    if "coastline" in families:
        regions.extend(["verdant_coast", "coastal_only", "frostmarch_if_frozen"])
    if "river_wetland" in families:
        regions.extend(["verdant_coast", "south_east_wilds"])
    if "desert_badlands" in families:
        regions.extend(["sunreach", "south_west_wilds"])
    if "jungle_wet" in families:
        regions.extend(["verdant_coast", "south_east_wilds"])
    if "mountain_highland" in families:
        regions.extend(["stoneback_highlands", "north_west_marches", "south_west_wilds"])
    if "forest_taiga" in families:
        regions.extend(["hearthlands", "crownlands", "frostmarch_if_snowy", "stoneback_if_taiga"])
    if "plains_savanna" in families:
        regions.extend(["hearthlands", "crownlands", "sunreach_if_savanna"])
    if structure_class in {"boss_arena", "dragon_tier_zone"}:
        regions = [region for region in regions if region not in BEGINNER_REGIONS]
        regions.extend(["outer", "boss_theme_region"])
    if not regions:
        regions = CLASS_POLICY.get(structure_class, CLASS_POLICY["uncategorized_structure"])["regions"].copy()
    return sorted(dict.fromkeys(regions))


def infer_layer_policy_from_evidence(
    structure_class: str,
    biome_families: list[str],
    regions: list[str],
    density_class: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    families = set(biome_families)
    tag_refs = set(evidence.get("biome_tag_refs", []))
    block_evidence = evidence.get("block_palette_evidence", {}) if isinstance(evidence.get("block_palette_evidence"), dict) else {}
    water_blocks_sampled = int(block_evidence.get("fluid_or_water_block_count") or 0)
    water_ratio = float(block_evidence.get("fluid_or_water_ratio") or 0.0)
    start_height = evidence.get("start_height_absolute_hint")

    vertical_layers: list[str] = []
    if "nether" in families or "nether_only" in regions:
        vertical_layers.append("nether")
    if "end" in families or "end_only" in regions:
        vertical_layers.append("end")

    if isinstance(start_height, int) and start_height >= 150:
        vertical_layers.append("sky_high")
    elif isinstance(start_height, int) and start_height >= 100:
        vertical_layers.append("sky_low")

    water_role = "none"
    explicit_ocean_evidence = bool(tag_refs & OCEAN_BIOME_TAGS) or water_ratio >= 0.05
    explicit_deep_ocean_evidence = "minecraft:is_deep_ocean" in tag_refs and "minecraft:is_ocean" not in tag_refs
    explicit_frozen_ocean_evidence = "frozen_ocean" in families and bool(tag_refs & FROZEN_BIOME_TAGS)
    if explicit_ocean_evidence:
        if explicit_frozen_ocean_evidence:
            water_role = "frozen_ocean"
        elif explicit_deep_ocean_evidence:
            water_role = "sea_floor"
        elif "river_wetland" in families or tag_refs & RIVER_BIOME_TAGS:
            water_role = "river_or_wetland"
        else:
            water_role = "ocean"

    if water_role == "sea_floor":
        vertical_layers.append("sea_floor")
    elif water_role in {"ocean", "frozen_ocean"}:
        vertical_layers.append("sea_surface")
    elif water_role == "river_or_wetland":
        vertical_layers.append("river_or_wetland")
    elif "coastline" in families or tag_refs & COAST_BIOME_TAGS:
        vertical_layers.append("coastal_surface")

    if not vertical_layers:
        vertical_layers.append("surface_land")

    sky_role = "none"
    if "sky_high" in vertical_layers:
        sky_role = "rare_high_sky"
    elif "sky_low" in vertical_layers:
        sky_role = "rare_low_sky"

    required_terrain = "native_surface"
    if water_role == "sea_floor":
        required_terrain = "deep_water_or_ocean_floor"
    elif water_role in {"ocean", "frozen_ocean"}:
        required_terrain = "ocean_or_coast"
    elif water_role == "coastline":
        required_terrain = "coastal_land_or_beach"
    elif water_role == "river_or_wetland":
        required_terrain = "river_lake_swamp_or_wetland"
    elif sky_role != "none":
        required_terrain = "airspace_above_safe_surface"
    elif "underground" in vertical_layers:
        required_terrain = "underground_or_cave_layer"

    risk_flags: list[str] = []
    if water_role != "none" and not any(region in WATER_REGION_HINTS for region in regions):
        risk_flags.append("water_structure_without_water_region_rule")
    if water_role in {"sea_floor", "ocean", "frozen_ocean"} and any(region in LAND_FIRST_REGION_HINTS for region in regions):
        risk_flags.append("water_structure_can_overlap_land_first_region")
    if sky_role != "none" and density_class == "common":
        risk_flags.append("sky_structure_too_common")
    if structure_class in {"boss_arena", "dragon_tier_zone"} and any(region in BEGINNER_REGIONS for region in regions):
        risk_flags.append("boss_or_dragon_near_beginner_region")
    if structure_class == "settlement" and water_role != "none" and "coastal_only" not in regions:
        risk_flags.append("settlement_water_context_needs_manual_review")
    for observation in evidence.get("manual_live_evidence", []):
        tags = set(str(tag) for tag in observation.get("visual_issue_tags", []) if tag)
        if tags & {"water_island", "ocean_island", "lake_island", "wet_terrain_mismatch"}:
            risk_flags.append("manual_water_island_placement_issue")
        if str(observation.get("decision") or "") == "needs_followup":
            risk_flags.append("manual_followup_required")

    return {
        "vertical_layers": sorted(dict.fromkeys(vertical_layers)),
        "water_role": water_role,
        "sky_role": sky_role,
        "required_terrain": required_terrain,
        "water_blocks_sampled": water_blocks_sampled,
        "water_block_ratio_sampled": water_ratio,
        "risk_flags": sorted(dict.fromkeys(risk_flags)),
    }


def infer_density_class(spacing: int | None, separation: int | None) -> tuple[str, str]:
    if spacing is None:
        return "unknown", "missing_spacing_data"
    if spacing <= 12 or separation == 0:
        return "common", "dangerously_dense"
    if spacing <= 24:
        return "common", "dense"
    if spacing <= 40:
        return "uncommon", "moderate"
    if spacing <= 72:
        return "rare", "controlled"
    if spacing <= 128:
        return "very_rare", "controlled"
    return "unique", "controlled"


def strongest_density(structure_sets: list[dict[str, Any]]) -> tuple[str, str, int | None, int | None]:
    spacings = [
        (entry.get("spacing"), entry.get("separation"))
        for entry in structure_sets
        if isinstance(entry, dict)
    ]
    numeric = [
        (int(spacing), int(separation) if separation is not None else None)
        for spacing, separation in spacings
        if isinstance(spacing, int)
    ]
    if not numeric:
        density, risk = infer_density_class(None, None)
        return density, risk, None, None
    spacing, separation = min(numeric, key=lambda row: row[0])
    density, risk = infer_density_class(spacing, separation)
    return density, risk, spacing, separation


def merge_structure_sets(registry_entry: dict[str, Any] | None, audit_entry: dict[str, Any]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for raw in (audit_entry.get("structure_sets") or []):
        if not isinstance(raw, dict):
            continue
        key = str(raw.get("structure_set") or "")
        if not key:
            continue
        merged[key] = {
            "structure_set": key,
            "spacing": raw.get("spacing"),
            "separation": raw.get("separation"),
            "salt": raw.get("salt"),
            "source": raw.get("source"),
        }
    if registry_entry:
        for raw in (registry_entry.get("structure_sets") or []):
            if not isinstance(raw, dict):
                continue
            key = str(raw.get("structure_set") or "")
            if not key or key in merged:
                continue
            merged[key] = {
                "structure_set": key,
                "spacing": raw.get("spacing"),
                "separation": raw.get("separation"),
                "salt": raw.get("salt"),
                "source": registry_entry.get("jar"),
            }
    return sorted(merged.values(), key=lambda entry: str(entry.get("structure_set")))


def recommended_action(
    structure_class: str,
    regions: list[str],
    density_risk: str,
    spacing: int | None,
    source_mod: str,
    structure_id: str,
) -> str:
    text = slug_text(source_mod, structure_id)
    if "ascendant_atlas" in text:
        return "should_keep_debug_only"
    if "ascendant_guild" in text:
        return "defer_until_guild_phase"
    if structure_class in {"boss_arena", "dragon_tier_zone"} and (spacing is None or spacing < 48):
        return "should_reduce"
    if structure_class == "dangerous_dungeon" and any(region in BEGINNER_REGIONS for region in regions):
        return "should_region_lock"
    if density_risk == "dangerously_dense":
        return "should_reduce"
    if density_risk == "missing_spacing_data":
        return "needs_test"
    if source_mod in {"Towns and Towers", "Integrated Villages", "Integrated Dungeons and Structures", "Structory"}:
        return "needs_test"
    if "Moog" in source_mod:
        return "needs_test"
    if "Aquamirae" in source_mod and ("frozen_ocean_only" not in regions and "frostmarch" not in regions):
        return "should_region_lock"
    return "should_keep"


def review_priority(structure_class: str, density_risk: str, action: str, source_mod: str) -> str:
    if action in {"should_reduce", "should_region_lock", "should_disable"}:
        return "high"
    if structure_class in {"boss_arena", "dragon_tier_zone"}:
        return "high"
    if density_risk in {"dangerously_dense", "dense"}:
        return "high"
    if source_mod in {"Towns and Towers", "Integrated Villages", "Integrated Dungeons and Structures", "Structory"} or "Moog" in source_mod:
        return "medium"
    if action == "needs_test":
        return "medium"
    return "low"


def load_loot_linkage() -> dict[str, dict[str, Any]]:
    if not STRUCTURE_LOOT_TIERS_PATH.exists():
        return {}
    data = read_json(STRUCTURE_LOOT_TIERS_PATH)
    entries = data.get("entries", []) if isinstance(data, dict) else []
    return {
        str(entry.get("structure_id")): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("structure_id")
    }


def build_entries() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    registry = read_json(STRUCTURE_REGISTRY_PATH)
    audit = read_json(WORLDGEN_AUDIT_PATH)
    raw_registry_entries = [
        entry
        for entry in registry.get("structures", [])
        if isinstance(entry, dict) and entry.get("structure_id")
    ]
    registry_entries = {
        str(entry.get("structure_id")): entry
        for entry in raw_registry_entries
        if is_registry_policy_structure(entry)
    }
    raw_audit_entries = audit.get("structures", {}) if isinstance(audit.get("structures"), dict) else {}
    audit_entries = {
        str(structure_id): entry
        for structure_id, entry in raw_audit_entries.items()
        if isinstance(entry, dict) and is_audit_policy_structure(entry)
    }
    loot_linkage = load_loot_linkage()
    tag_map = load_biome_tag_map(audit)
    structure_json_map = load_structure_json_map(audit)
    biome_audit = audit.get("biomes", {}) if isinstance(audit.get("biomes"), dict) else {}
    manual_observations = load_manual_observations()

    all_ids = sorted(set(registry_entries) | set(audit_entries))
    entries: list[dict[str, Any]] = []
    structure_set_index: dict[str, dict[str, Any]] = {}

    for structure_id in all_ids:
        registry_entry = registry_entries.get(structure_id)
        audit_entry = audit_entries.get(structure_id, {}) if isinstance(audit_entries.get(structure_id, {}), dict) else {}
        source_mod = str((registry_entry or {}).get("source_mod") or source_mod_from_audit(audit_entry)).strip()
        structure_sets = merge_structure_sets(registry_entry, audit_entry)
        loot_entry = loot_linkage.get(structure_id, {})
        evidence = build_structure_evidence(
            structure_id,
            registry_entry,
            audit_entry,
            source_mod,
            structure_sets,
            loot_entry,
            tag_map,
            structure_json_map,
            biome_audit,
            manual_observations,
        )
        structure_class, classification_reasons = classify_structure_from_evidence(
            structure_id,
            registry_entry,
            audit_entry,
            evidence,
        )
        policy = CLASS_POLICY.get(structure_class, CLASS_POLICY["uncategorized_structure"])
        loot_tier = str((registry_entry or {}).get("loot_tier") or "review")
        reward_tier, rarity_ceiling, danger_tier, guild_rank = LOOT_TIER_POLICY.get(
            loot_tier,
            (policy["loot"], policy["rarity_ceiling"], policy["danger"], policy["rank"]),
        )
        if structure_class in {"boss_arena", "dragon_tier_zone"}:
            danger_tier = max(int(danger_tier), 5)
        biome_families = evidence.get("biome_families_from_evidence", ["native_palette"])
        regions = infer_regions_from_evidence(structure_class, biome_families)
        density_class, density_risk, min_spacing, min_separation = strongest_density(structure_sets)
        layer_policy = infer_layer_policy_from_evidence(
            structure_class,
            biome_families,
            regions,
            density_class,
            evidence,
        )
        action = recommended_action(structure_class, regions, density_risk, min_spacing, source_mod, structure_id)
        priority = review_priority(structure_class, density_risk, action, source_mod)
        linked_reward_tier = str(loot_entry.get("reward_tier") or reward_tier)
        if linked_reward_tier == "review" and reward_tier != "review":
            linked_reward_tier = reward_tier

        block_profile = audit_entry.get("block_profile", {}) if isinstance(audit_entry.get("block_profile"), dict) else {}
        material_counts = block_profile.get("material_counts", {}) if isinstance(block_profile.get("material_counts"), dict) else {}
        sensitive_role = (
            structure_class in {"settlement", "dangerous_dungeon", "boss_arena", "dragon_tier_zone"}
            or layer_policy["water_role"] != "none"
            or layer_policy["sky_role"] != "none"
        )
        confidence_score, confidence_tier, evidence_strength_counts = confidence_from_evidence(evidence, sensitive_role)
        manual_review_required = (
            confidence_tier == "weak"
            or bool(layer_policy["risk_flags"])
            or (sensitive_role and evidence_strength_counts["strong"] == 0)
        )
        name_only_classification = sensitive_role and evidence_strength_counts["strong"] == 0 and evidence_strength_counts["medium"] == 0
        reason_summary = " ".join(classification_reasons)
        if layer_policy["water_role"] != "none":
            reason_summary += f" Water role comes from biome/block evidence: {layer_policy['water_role']}."
        if layer_policy["sky_role"] != "none":
            reason_summary += f" Sky role comes from structure height evidence: {evidence.get('start_height')}."
        evidence["final_classification"] = {
            "structure_class": structure_class,
            "category": policy["category"],
            "biome_families": biome_families,
            "atlas_allowed_regions": regions,
            "vertical_layers": layer_policy["vertical_layers"],
            "water_role": layer_policy["water_role"],
            "sky_role": layer_policy["sky_role"],
            "confidence_score": confidence_score,
            "confidence_tier": confidence_tier,
            "manual_review_required": manual_review_required,
            "name_only_classification": name_only_classification,
            "reason_summary": reason_summary.strip(),
        }
        entry = {
            "structure_id": structure_id,
            "source_mod": source_mod,
            "source_file": (registry_entry or {}).get("jar") or audit_entry.get("source"),
            "category": policy["category"],
            "structure_class": structure_class,
            "biome_tag_or_selector": audit_entry.get("biomes"),
            "biome_families": biome_families,
            "atlas_allowed_regions": regions,
            "vertical_layers": layer_policy["vertical_layers"],
            "water_role": layer_policy["water_role"],
            "sky_role": layer_policy["sky_role"],
            "required_terrain": layer_policy["required_terrain"],
            "distance_ring": policy["rings"] if structure_class not in {"boss_arena", "dragon_tier_zone"} else ["outer", "edge"],
            "danger_tier": danger_tier,
            "guild_rank_tier": guild_rank,
            "loot_tier": linked_reward_tier,
            "allowed_rarity_ceiling": str(loot_entry.get("allowed_rarity_ceiling") or rarity_ceiling),
            "density_class": density_class,
            "density_risk": density_risk,
            "minimum_spacing": min_spacing,
            "minimum_separation": min_separation,
            "generation_step": audit_entry.get("step"),
            "structure_sets": structure_sets,
            "start_pool": audit_entry.get("start_pool"),
            "templates_sampled": audit_entry.get("templates_sampled"),
            "block_profile": {
                "dominant_materials": block_profile.get("dominant_materials", []),
                "material_counts": material_counts,
                "chest_blocks_sampled": material_counts.get("chest", 0),
                "total_blocks_sampled": block_profile.get("total_blocks_sampled", 0),
                "water_blocks_sampled": layer_policy["water_blocks_sampled"],
                "water_block_ratio_sampled": layer_policy["water_block_ratio_sampled"],
            },
            "spawn_override_groups": audit_entry.get("spawn_override_groups", []),
            "can_generate_near_spawn": any(region in BEGINNER_REGIONS for region in regions)
            and structure_class not in BOSS_OR_DUNGEON_CATEGORIES,
            "should_region_restrict": action == "should_region_lock" or structure_class in {"boss_arena", "dragon_tier_zone"},
            "should_rank_tier": structure_class in BOSS_OR_DUNGEON_CATEGORIES or linked_reward_tier not in {"settlement_basic", "minor_ruin"},
            "manual_review_priority": priority,
            "recommended_action": action,
            "risk_flags": layer_policy["risk_flags"],
            "evidence_source": [
                f"{item.get('source')}:{item.get('strength')}"
                for item in evidence.get("evidence_sources", [])
            ],
            "confidence": confidence_score,
            "classification_confidence": confidence_tier,
            "evidence_strength_counts": evidence_strength_counts,
            "classification_reason": reason_summary.strip(),
            "manual_review_required": manual_review_required,
            "name_only_classification": name_only_classification,
            "evidence": {
                "classification_inputs": [
                    "config/ascendant_index/structure_registry.json",
                    "docs/generated/worldgen_content_audit.json",
                    "config/ascendant_loot/structure_loot_tiers.json",
                    "mod/datapack biome tags and structure JSONs",
                    "config/ascendant_structures/manual_structure_observations.json",
                ],
                "not_name_only": not name_only_classification,
                "uses_biome_tag": audit_entry.get("biomes") is not None,
                "uses_block_palette": bool(block_profile),
                "uses_structure_set_spacing": min_spacing is not None,
                "detail": evidence,
            },
            "notes": "Control scaffold only. Do not enable region locks, village injections, or live density rewrites without explicit review.",
        }
        entries.append(entry)

        for structure_set in structure_sets:
            set_id = str(structure_set.get("structure_set") or "")
            if not set_id:
                continue
            policy_entry = structure_set_index.setdefault(
                set_id,
                {
                    "structure_set": set_id,
                    "source": structure_set.get("source"),
                    "spacing": structure_set.get("spacing"),
                    "separation": structure_set.get("separation"),
                    "salt": structure_set.get("salt"),
                    "structures": [],
                    "density_class": None,
                    "density_risk": None,
                    "recommended_action": "should_keep",
                    "overlap_risk": False,
                    "notes": [],
                },
            )
            policy_entry["structures"].append(structure_id)
            spacing = structure_set.get("spacing")
            separation = structure_set.get("separation")
            set_density, set_risk = infer_density_class(
                int(spacing) if isinstance(spacing, int) else None,
                int(separation) if isinstance(separation, int) else None,
            )
            policy_entry["density_class"] = set_density
            policy_entry["density_risk"] = set_risk
            if set_risk == "dangerously_dense":
                policy_entry["recommended_action"] = "should_reduce"
            elif source_mod in {"Towns and Towers", "Integrated Villages"} and isinstance(spacing, int) and spacing <= 64:
                policy_entry["recommended_action"] = "needs_test"
                policy_entry["overlap_risk"] = True
                policy_entry["notes"].append("Village/town family should be checked for overlap and settlement crowding.")
            elif structure_class in {"boss_arena", "dragon_tier_zone"} and (not isinstance(spacing, int) or spacing < 48):
                policy_entry["recommended_action"] = "should_reduce"
                policy_entry["notes"].append("Boss or dragon content should not be near-spawn/common.")
            if source_mod == "Aquamirae":
                policy_entry["notes"].append("Keep ocean/frozen-ocean themed; current surface override is spacing 20/separation 8.")

    audit["policy_filter_counts"] = {
        "registry_rows_skipped_as_tags": len(raw_registry_entries) - len(registry_entries),
        "audit_rows_skipped_as_tags": len(raw_audit_entries) - len(audit_entries),
    }
    return entries, structure_set_index, audit


def build_validation(entries: list[dict[str, Any]], density_entries: list[dict[str, Any]], known_ids: set[str]) -> dict[str, Any]:
    no_tier = [entry["structure_id"] for entry in entries if not entry.get("danger_tier") and entry.get("danger_tier") != 0]
    no_loot = [
        entry["structure_id"]
        for entry in entries
        if not entry.get("loot_tier") or entry.get("loot_tier") == "review"
    ]
    no_region = [
        entry["structure_id"]
        for entry in entries
        if not entry.get("atlas_allowed_regions")
    ]
    boss_dungeon_beginner = [
        entry["structure_id"]
        for entry in entries
        if entry.get("structure_class") in BOSS_OR_DUNGEON_CATEGORIES
        and any(region in BEGINNER_REGIONS for region in entry.get("atlas_allowed_regions", []))
    ]
    dangerous_dense = [
        {
            "structure_id": entry["structure_id"],
            "structure_sets": [set_entry.get("structure_set") for set_entry in entry.get("structure_sets", [])],
            "spacing": entry.get("minimum_spacing"),
            "separation": entry.get("minimum_separation"),
            "density_risk": entry.get("density_risk"),
        }
        for entry in entries
        if entry.get("density_risk") in {"dangerously_dense", "dense"}
    ]
    overlap_risks = [
        {
            "structure_set": entry.get("structure_set"),
            "spacing": entry.get("spacing"),
            "separation": entry.get("separation"),
            "structures": entry.get("structures", [])[:12],
        }
        for entry in density_entries
        if entry.get("overlap_risk") is True
    ]
    missing_policy_ids = [
        entry["structure_id"]
        for entry in entries
        if entry["structure_id"] not in known_ids
    ]
    water_wrong_region = [
        entry["structure_id"]
        for entry in entries
        if entry.get("water_role") != "none"
        and not any(region in WATER_REGION_HINTS for region in entry.get("atlas_allowed_regions", []))
    ]
    sea_floor_missing_rule = [
        entry["structure_id"]
        for entry in entries
        if entry.get("water_role") == "sea_floor"
        and "sea_floor" not in entry.get("vertical_layers", [])
    ]
    sky_common_near_spawn = [
        entry["structure_id"]
        for entry in entries
        if entry.get("sky_role") != "none"
        and (entry.get("density_class") == "common" or entry.get("can_generate_near_spawn") is True)
    ]
    village_overlap_without_policy = [
        entry.get("structure_set")
        for entry in density_entries
        if entry.get("overlap_risk") is True and not entry.get("notes")
    ]
    name_only_classifications = [
        entry["structure_id"]
        for entry in entries
        if entry.get("name_only_classification") is True
    ]
    low_confidence_sensitive_classifications = [
        {
            "structure_id": entry["structure_id"],
            "classification_confidence": entry.get("classification_confidence"),
            "confidence": entry.get("confidence"),
            "structure_class": entry.get("structure_class"),
            "water_role": entry.get("water_role"),
            "sky_role": entry.get("sky_role"),
        }
        for entry in entries
        if entry.get("manual_review_required") is True
    ]
    water_without_non_name_evidence = [
        entry["structure_id"]
        for entry in entries
        if entry.get("water_role") != "none"
        and not any("biome_tag_or_selector:strong" in source or "block_palette:strong" in source or "manual_live_observation:strong" in source for source in entry.get("evidence_source", []))
    ]
    frozen_without_cold_evidence = [
        entry["structure_id"]
        for entry in entries
        if entry.get("water_role") == "frozen_ocean"
        and "frost_cold" not in entry.get("biome_families", [])
        and "frozen_ocean" not in entry.get("biome_families", [])
    ]
    sky_without_height_evidence = [
        entry["structure_id"]
        for entry in entries
        if entry.get("sky_role") != "none"
        and not any("structure_json:strong" in source for source in entry.get("evidence_source", []))
    ]
    return {
        "no_tier_assignment": no_tier,
        "boss_or_dungeon_in_beginner_regions": boss_dungeon_beginner,
        "no_loot_tier": no_loot,
        "no_atlas_region_rules": no_region,
        "dangerously_dense_or_dense_spacing": dangerous_dense,
        "village_town_overlap_risks": overlap_risks,
        "policy_references_missing_structure_ids": missing_policy_ids,
        "water_structures_outside_water_regions": water_wrong_region,
        "sea_floor_structures_without_deep_water_rule": sea_floor_missing_rule,
        "sky_structures_common_or_near_spawn": sky_common_near_spawn,
        "village_overlap_risks_without_policy_notes": village_overlap_without_policy,
        "name_only_classifications": name_only_classifications,
        "low_confidence_or_manual_review_classifications": low_confidence_sensitive_classifications,
        "water_roles_without_non_name_evidence": water_without_non_name_evidence,
        "frozen_ocean_without_cold_or_frozen_evidence": frozen_without_cold_evidence,
        "sky_roles_without_height_evidence": sky_without_height_evidence,
    }


def counter_dict(values: list[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def make_markdown_table(headers: list[str], rows: list[list[object]], limit: int | None = None) -> str:
    visible = rows[:limit] if limit is not None else rows
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in visible:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    if limit is not None and len(rows) > limit:
        lines.append(f"| ... | {len(rows) - limit} more rows in JSON |  |  |  |")
    return "\n".join(lines)


def proposed_spacing_for_set(entry: dict[str, Any], related_structures: list[dict[str, Any]]) -> tuple[int | None, int | None, str]:
    spacing = entry.get("spacing")
    separation = entry.get("separation")
    if not isinstance(spacing, int):
        return None, None, "missing_spacing_data_manual_review"
    structure_classes = {str(row.get("structure_class")) for row in related_structures}
    water_roles = {str(row.get("water_role")) for row in related_structures}
    sky_roles = {str(row.get("sky_role")) for row in related_structures}
    if structure_classes & {"boss_arena", "dragon_tier_zone"}:
        proposed_spacing = max(spacing, 96)
        proposed_separation = max(int(separation or 0), 48)
        return proposed_spacing, proposed_separation, "boss_or_dragon_should_be_rare"
    if "dangerous_dungeon" in structure_classes:
        proposed_spacing = max(spacing, 32)
        proposed_separation = max(int(separation or 0), 12)
        return proposed_spacing, proposed_separation, "dungeon_density_review"
    if water_roles & {"sea_floor", "ship_or_ocean_surface", "ocean", "frozen_ocean"}:
        proposed_spacing = max(spacing, 36)
        proposed_separation = max(int(separation or 0), 12)
        return proposed_spacing, proposed_separation, "water_structure_density_review"
    if sky_roles - {"none"}:
        proposed_spacing = max(spacing, 96)
        proposed_separation = max(int(separation or 0), 48)
        return proposed_spacing, proposed_separation, "sky_structure_should_be_rare"
    proposed_spacing = max(spacing, 28)
    proposed_separation = max(int(separation or 0), 10)
    return proposed_spacing, proposed_separation, "general_visible_density_review"


def build_override_candidates(entries: list[dict[str, Any]], density_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_set: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        for structure_set in entry.get("structure_sets", []):
            set_id = str(structure_set.get("structure_set") or "")
            if set_id:
                by_set[set_id].append(entry)
    candidates: list[dict[str, Any]] = []
    for density_entry in density_entries:
        set_id = str(density_entry.get("structure_set") or "")
        related = by_set.get(set_id, [])
        action = str(density_entry.get("recommended_action") or "")
        risk = str(density_entry.get("density_risk") or "")
        if action not in {"should_reduce", "needs_test"} and risk not in {"dangerously_dense", "dense"}:
            continue
        proposed_spacing, proposed_separation, fix_type = proposed_spacing_for_set(density_entry, related)
        candidate = {
            "structure_set": set_id,
            "source": density_entry.get("source"),
            "current_spacing": density_entry.get("spacing"),
            "current_separation": density_entry.get("separation"),
            "current_salt": density_entry.get("salt"),
            "proposed_spacing": proposed_spacing,
            "proposed_separation": proposed_separation,
            "structures": sorted(set(str(value) for value in density_entry.get("structures", []))),
            "density_risk": risk,
            "suggested_fix_type": fix_type,
            "review_status": "candidate_disabled_pending_manual_review",
            "live_enabled": False,
            "notes": [
                "Review-only candidate. Do not copy into OpenLoader until Jayden approves this specific structure set.",
                "If accepted, recreate the original structure_set JSON with only spacing/separation adjusted unless a region lock is also approved.",
            ],
        }
        candidates.append(candidate)
    return sorted(candidates, key=lambda entry: (str(entry.get("suggested_fix_type")), str(entry.get("structure_set"))))


def compact_evidence_fields(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_source": entry.get("evidence_source", []),
        "confidence": entry.get("confidence"),
        "classification_confidence": entry.get("classification_confidence"),
        "classification_reason": entry.get("classification_reason"),
        "manual_review_required": entry.get("manual_review_required"),
        "name_only_classification": entry.get("name_only_classification"),
    }


def build_policy_outputs(entries: list[dict[str, Any]], density_entries: list[dict[str, Any]]) -> dict[str, Any]:
    water_entries = [entry for entry in entries if entry.get("water_role") != "none"]
    sky_entries = [entry for entry in entries if entry.get("sky_role") != "none"]
    sea_floor_entries = [entry for entry in water_entries if entry.get("water_role") == "sea_floor"]
    ship_entries = [entry for entry in water_entries if entry.get("water_role") == "ship_or_ocean_surface" or "sea_surface" in entry.get("vertical_layers", [])]
    dungeon_entries = [entry for entry in entries if entry.get("structure_class") == "dangerous_dungeon"]
    boss_entries = [entry for entry in entries if entry.get("structure_class") in {"boss_arena", "dragon_tier_zone"}]
    village_entries = [entry for entry in entries if entry.get("structure_class") == "settlement"]
    override_candidates = build_override_candidates(entries, density_entries)
    return {
        "structure_registry": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "category": entry["category"],
                "structure_class": entry["structure_class"],
                "vertical_layers": entry["vertical_layers"],
                "water_role": entry["water_role"],
                "sky_role": entry["sky_role"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "distance_ring": entry["distance_ring"],
                "danger_tier": entry["danger_tier"],
                "guild_rank_tier": entry["guild_rank_tier"],
                "loot_tier": entry["loot_tier"],
                "density_class": entry["density_class"],
                "density_risk": entry["density_risk"],
                "recommended_action": entry["recommended_action"],
                "manual_review_priority": entry["manual_review_priority"],
                "risk_flags": entry["risk_flags"],
                **compact_evidence_fields(entry),
            }
            for entry in entries
        ],
        "vertical_layer_rules": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "vertical_layers": entry["vertical_layers"],
                "required_terrain": entry["required_terrain"],
                "water_role": entry["water_role"],
                "sky_role": entry["sky_role"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "distance_ring": entry["distance_ring"],
                "density_class": entry["density_class"],
                "risk_flags": entry["risk_flags"],
                "recommended_action": entry["recommended_action"],
                **compact_evidence_fields(entry),
            }
            for entry in entries
        ],
        "structure_set_overrides": override_candidates,
        "water_structure_policy": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "water_role": entry["water_role"],
                "vertical_layers": entry["vertical_layers"],
                "required_terrain": entry["required_terrain"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "density_class": entry["density_class"],
                "water_block_ratio_sampled": entry["block_profile"]["water_block_ratio_sampled"],
                "risk_flags": entry["risk_flags"],
                "recommended_action": entry["recommended_action"],
                **compact_evidence_fields(entry),
            }
            for entry in water_entries
        ],
        "sky_structure_policy": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "sky_role": entry["sky_role"],
                "vertical_layers": entry["vertical_layers"],
                "required_terrain": entry["required_terrain"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "density_class": entry["density_class"],
                "minimum_spacing": entry["minimum_spacing"],
                "risk_flags": entry["risk_flags"],
                "recommended_action": entry["recommended_action"],
                **compact_evidence_fields(entry),
            }
            for entry in sky_entries
        ],
        "sea_floor_structure_policy": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "required_terrain": entry["required_terrain"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "density_class": entry["density_class"],
                "loot_tier": entry["loot_tier"],
                "recommended_action": entry["recommended_action"],
                **compact_evidence_fields(entry),
            }
            for entry in sea_floor_entries
        ],
        "ship_structure_policy": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "required_terrain": entry["required_terrain"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "density_class": entry["density_class"],
                "loot_tier": entry["loot_tier"],
                "recommended_action": entry["recommended_action"],
                **compact_evidence_fields(entry),
            }
            for entry in ship_entries
        ],
        "dungeon_structure_policy": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "vertical_layers": entry["vertical_layers"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "distance_ring": entry["distance_ring"],
                "danger_tier": entry["danger_tier"],
                "guild_rank_tier": entry["guild_rank_tier"],
                "loot_tier": entry["loot_tier"],
                "density_class": entry["density_class"],
                "recommended_action": entry["recommended_action"],
                "manual_review_priority": entry["manual_review_priority"],
                **compact_evidence_fields(entry),
            }
            for entry in dungeon_entries
        ],
        "boss_structure_policy": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "vertical_layers": entry["vertical_layers"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "distance_ring": entry["distance_ring"],
                "danger_tier": entry["danger_tier"],
                "guild_rank_tier": entry["guild_rank_tier"],
                "loot_tier": entry["loot_tier"],
                "density_class": entry["density_class"],
                "recommended_action": entry["recommended_action"],
                "risk_flags": entry["risk_flags"],
                **compact_evidence_fields(entry),
            }
            for entry in boss_entries
        ],
        "village_structure_policy": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "vertical_layers": entry["vertical_layers"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "distance_ring": entry["distance_ring"],
                "danger_tier": entry["danger_tier"],
                "loot_tier": entry["loot_tier"],
                "density_class": entry["density_class"],
                "recommended_action": entry["recommended_action"],
                "risk_flags": entry["risk_flags"],
                **compact_evidence_fields(entry),
            }
            for entry in village_entries
        ],
    }


def build_test_points(entries: list[dict[str, Any]], policy_outputs: dict[str, Any]) -> dict[str, Any]:
    def locate_rows(source_entries: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
        rows = []
        for entry in source_entries[:limit]:
            structure_id = str(entry.get("structure_id"))
            rows.append(
                {
                    "structure_id": structure_id,
                    "command": f"/locate structure {structure_id}",
                    "inspection_focus": [
                        "Does it match Atlas region identity?",
                        "Does it overlap nearby structures, roads, villages, water, cliffs, or terrain seams?",
                        "Does loot/danger feel correct for the ring?",
                    ],
                }
            )
        return rows

    high_priority = [entry for entry in entries if entry.get("manual_review_priority") == "high"]
    high_priority.sort(key=lambda entry: (str(entry.get("recommended_action")), str(entry.get("structure_id"))))
    water_entries = [entry for entry in entries if entry.get("water_role") != "none"]
    sky_entries = [entry for entry in entries if entry.get("sky_role") != "none"]
    boss_entries = [entry for entry in entries if entry.get("structure_class") in {"boss_arena", "dragon_tier_zone"}]
    village_entries = [entry for entry in entries if entry.get("structure_class") == "settlement"]
    dungeon_entries = [entry for entry in entries if entry.get("structure_class") == "dangerous_dungeon"]
    return {
        "version": 1,
        "status": "manual_locate_test_plan_no_live_generation_changes",
        "fresh_world_required": True,
        "global_rules": [
            "Use a fresh validation world or ungenerated chunks.",
            "Do not judge structure density in old chunks.",
            "Record coordinates, biome, Atlas region, structure ID, nearby structures, and screenshots for failures.",
            "Use spectator/creative flight for review; do not enable region locks or live overrides from this file directly.",
        ],
        "priority_locate_commands": locate_rows(high_priority, 40),
        "water_structure_locate_commands": locate_rows(water_entries, 30),
        "sky_structure_locate_commands": locate_rows(sky_entries, 20),
        "boss_structure_locate_commands": locate_rows(boss_entries, 30),
        "dungeon_structure_locate_commands": locate_rows(dungeon_entries, 30),
        "village_or_town_locate_commands": locate_rows(village_entries, 30),
        "candidate_override_sets_to_review": [
            {
                "structure_set": entry.get("structure_set"),
                "current_spacing": entry.get("current_spacing"),
                "proposed_spacing": entry.get("proposed_spacing"),
                "suggested_fix_type": entry.get("suggested_fix_type"),
            }
            for entry in policy_outputs.get("structure_set_overrides", [])[:40]
        ],
    }


def write_docs(
    generated_at: str,
    entries: list[dict[str, Any]],
    density_entries: list[dict[str, Any]],
    validation: dict[str, Any],
    audit: dict[str, Any],
    policy_outputs: dict[str, Any],
) -> None:
    category_counts = counter_dict([entry.get("structure_class") for entry in entries])
    source_counts = Counter(str(entry.get("source_mod")) for entry in entries)
    action_counts = counter_dict([entry.get("recommended_action") for entry in entries])
    priority_counts = counter_dict([entry.get("manual_review_priority") for entry in entries])
    density_counts = counter_dict([entry.get("density_class") for entry in entries])
    high_priority = [
        entry
        for entry in entries
        if entry.get("manual_review_priority") == "high"
    ]
    high_priority.sort(key=lambda entry: (str(entry.get("recommended_action")), str(entry.get("structure_id"))))

    tier_rows = [
        [
            entry["structure_id"],
            entry["source_mod"],
            entry["structure_class"],
            ",".join(entry["atlas_allowed_regions"][:4]),
            "/".join(entry["distance_ring"]),
            entry["danger_tier"],
            entry["loot_tier"],
            entry["density_class"],
            entry["recommended_action"],
        ]
        for entry in entries
    ]
    tier_doc = f"""# Ascendant Structure Tiering

Generated: {generated_at}

This is a control scaffold for structure authorship. It does not add structure mods, does not inject village pools, and does not rewrite live structure sets. Classifications use `docs/generated/worldgen_content_audit.json` first, including biome tags, structure sets, sampled block palettes, start pools, and generation steps, with `config/ascendant_index/structure_registry.json` as the fallback index.

## Summary

- Structures classified: {len(entries)}
- Structure sets with density policy: {len(density_entries)}
- Worldgen audit structures: {audit.get("counts", {}).get("structures", "unknown")}
- Structure templates indexed by audit: {audit.get("counts", {}).get("templates", "unknown")}
- Structure/tag rows skipped because they were not direct generated structures: {sum(audit.get("policy_filter_counts", {}).values())}
- High-priority manual review entries: {len(high_priority)}
- Dense or dangerously dense entries: {len(validation.get("dangerously_dense_or_dense_spacing", []))}
- Boss/dungeon entries allowed in beginner regions: {len(validation.get("boss_or_dungeon_in_beginner_regions", []))}
- Untiered loot review entries: {len(validation.get("no_loot_tier", []))}

## Counts

- Structure classes: `{category_counts}`
- Recommended actions: `{action_counts}`
- Manual review priorities: `{priority_counts}`
- Density classes: `{density_counts}`

## Policy Rules

- Hearthlands and Crownlands are beginner-friendly. Boss arenas, dragon zones, and high-tier dungeons should be middle, outer, edge, dimension-locked, or tightly region-themed.
- Aquamirae content stays ocean, cold ocean, frozen ocean, and Frostmarch themed. Its surface set is already widened and should not be treated as inland clutter.
- Towns and Towers, Integrated Villages, IDAS, Structory, and Moog structures are kept for authored variety, but their density and overlap risks need review before more structure volume is added.
- Region locking is preferred over blanket disabling. Density reduction is preferred when a good structure is simply too frequent.
- Village injection remains untouched in this pass.

## High Priority Review

{make_markdown_table(["Structure", "Mod", "Class", "Regions", "Spacing", "Loot", "Action"], [[entry["structure_id"], entry["source_mod"], entry["structure_class"], ",".join(entry["atlas_allowed_regions"][:4]), entry.get("minimum_spacing"), entry.get("loot_tier"), entry.get("recommended_action")] for entry in high_priority], limit=80)}

## Full Tier Preview

{make_markdown_table(["Structure", "Mod", "Class", "Regions", "Rings", "Danger", "Loot", "Density", "Action"], tier_rows, limit=160)}

Full machine-readable policy:

- `config/ascendant_structures/structure_tier_registry.json`
- `config/ascendant_structures/structure_region_rules.json`
- `config/ascendant_structures/structure_density_policy.json`
- `config/ascendant_structures/structure_loot_linkage.json`
"""
    write_text(DOCS_DIR / "ASCENDANT_STRUCTURE_TIERING.md", tier_doc)

    dense_entries = [
        entry
        for entry in entries
        if entry.get("density_risk") in {"dangerously_dense", "dense", "missing_spacing_data"}
    ]
    dense_entries.sort(key=lambda entry: (
        999 if entry.get("minimum_spacing") is None else int(entry.get("minimum_spacing")),
        str(entry.get("structure_id")),
    ))
    density_rows = [
        [
            entry["structure_id"],
            entry["source_mod"],
            entry.get("minimum_spacing"),
            entry.get("minimum_separation"),
            entry.get("density_risk"),
            entry.get("recommended_action"),
        ]
        for entry in dense_entries
    ]
    density_doc = f"""# Structure Density And Region Audit

Generated: {generated_at}

This report reviews live structure-set spacing from the generated worldgen audit. It is documentation and policy only. No live structure set was rewritten by this generator.

## Summary

- Structure sets with policy rows: {len(density_entries)}
- Entries marked dense, dangerously dense, or missing spacing data: {len(dense_entries)}
- Structure/tag rows skipped because they were not direct generated structures: {sum(audit.get("policy_filter_counts", {}).values())}
- Village/town overlap risks: {len(validation.get("village_town_overlap_risks", []))}
- Recommended reductions: {sum(1 for entry in entries if entry.get("recommended_action") == "should_reduce")}
- Recommended region locks: {sum(1 for entry in entries if entry.get("recommended_action") == "should_region_lock")}
- Needs test entries: {sum(1 for entry in entries if entry.get("recommended_action") == "needs_test")}

## Density Policy

- `common`: appears often or has a low spacing value. Good only for tiny ambient pieces, buried/underground features, or intentional structure families.
- `uncommon`: moderate overworld landmarks.
- `rare`: major dungeons, towns, and larger ruins.
- `very_rare`: boss arenas, dragons, and large regional anchors.
- `unique`: reserved for dimension or capstone anchors.

## Dense Or Missing-Spacing Entries

{make_markdown_table(["Structure", "Mod", "Spacing", "Separation", "Risk", "Action"], density_rows, limit=140)}

## Source Family Notes

- Moog structures are high-volume. Keep the best ambient finds, but test clutter before raising global density.
- YUNG mineshafts use very low structure-set spacing by design. Treat underground density separately from visible surface clutter.
- IDAS common structures are varied but numerous; region locks and loot tiering matter more than adding more packs.
- Integrated Villages and Towns and Towers should be tested for village/town overlap before any settlement work.
- Aquamirae surface structures are already widened through the world-integration datapack and should remain frozen-ocean themed.
"""
    write_text(DOCS_DIR / "STRUCTURE_DENSITY_AND_REGION_AUDIT.md", density_doc)

    conflict_rows = [
        [
            entry.get("structure_set"),
            entry.get("spacing"),
            entry.get("separation"),
            ", ".join(entry.get("structures", [])[:8]),
            entry.get("recommended_action"),
        ]
        for entry in density_entries
        if entry.get("overlap_risk") or entry.get("density_risk") in {"dangerously_dense", "dense"}
    ]
    conflict_doc = f"""# Structure Conflicts And Overlaps

Generated: {generated_at}

This is the current overlap-risk register for structure families. It records risks only; it does not disable, region-lock, or inject structures.

## Summary

- Potential conflict rows: {len(conflict_rows)}
- Village/town overlap risks: {len(validation.get("village_town_overlap_risks", []))}
- Structure/tag rows skipped because they were not direct generated structures: {sum(audit.get("policy_filter_counts", {}).values())}
- Boss/dungeon beginner-region conflicts: {len(validation.get("boss_or_dungeon_in_beginner_regions", []))}
- Unknown policy IDs: {len(validation.get("policy_references_missing_structure_ids", []))}

## Conflict Rows

{make_markdown_table(["Structure Set", "Spacing", "Separation", "Structures", "Action"], conflict_rows, limit=140)}

## Open Issues

- Some template-pool children are sampled only through the direct start pool. Major settlements and IDAS structures still need spot checks in-game.
- Structure loot linkage is now represented, but loot rewrites remain disabled until source-by-source approval.
- Region locking is documented only. A future pass can translate approved rows into datapack or helper behavior after terrain signoff.
"""
    write_text(DOCS_DIR / "STRUCTURE_CONFLICTS_AND_OVERLAPS.md", conflict_doc)

    water_entries = policy_outputs.get("water_structure_policy", [])
    sky_entries = policy_outputs.get("sky_structure_policy", [])
    sea_floor_entries = policy_outputs.get("sea_floor_structure_policy", [])
    ship_entries = policy_outputs.get("ship_structure_policy", [])
    dungeon_entries = policy_outputs.get("dungeon_structure_policy", [])
    boss_entries = policy_outputs.get("boss_structure_policy", [])
    village_entries = policy_outputs.get("village_structure_policy", [])
    override_candidates = policy_outputs.get("structure_set_overrides", [])
    layer_counts = counter_dict(
        [
            layer
            for entry in entries
            for layer in entry.get("vertical_layers", [])
        ]
    )
    region_rows = [
        [
            entry["structure_id"],
            ",".join(entry["atlas_allowed_regions"][:5]),
            ",".join(entry["vertical_layers"]),
            entry["required_terrain"],
            entry["recommended_action"],
        ]
        for entry in entries
    ]
    water_rows = [
        [
            entry["structure_id"],
            entry["source_mod"],
            entry["water_role"],
            ",".join(entry["vertical_layers"]),
            ",".join(entry["atlas_allowed_regions"][:4]),
            entry["recommended_action"],
        ]
        for entry in water_entries
    ]
    sky_rows = [
        [
            entry["structure_id"],
            entry["source_mod"],
            entry["sky_role"],
            ",".join(entry["atlas_allowed_regions"][:4]),
            entry.get("minimum_spacing"),
            entry["recommended_action"],
        ]
        for entry in sky_entries
    ]
    override_rows = [
        [
            entry["structure_set"],
            entry.get("current_spacing"),
            entry.get("current_separation"),
            entry.get("proposed_spacing"),
            entry.get("proposed_separation"),
            entry.get("suggested_fix_type"),
        ]
        for entry in override_candidates
    ]
    danger_rows = [
        [
            entry["structure_id"],
            entry["source_mod"],
            entry["structure_class"],
            entry["danger_tier"],
            entry["guild_rank_tier"],
            entry["loot_tier"],
            entry["density_class"],
            entry["recommended_action"],
        ]
        for entry in entries
        if entry["structure_class"] in BOSS_OR_DUNGEON_CATEGORIES or entry.get("loot_tier") not in {"minor_ruin", "settlement_basic"}
    ]

    director_doc = f"""# Ascendant Structure Director

Generated: {generated_at}

This is the v1 Structure Director control pass. It does not add mods, does not place NPCs, does not inject villages, does not add Hunter Boards or Guild Halls, and does not enable broad live structure rewrites. It turns the existing worldgen audit into a single pack-owned map for region fit, vertical layer, water/sky placement, density risk, danger tier, loot tier, and review priority.

## Status

- Mode: audit/control scaffold with disabled candidates only.
- Structures classified: {len(entries)}.
- Structure sets classified: {len(density_entries)}.
- Water structures: {len(water_entries)}.
- Sky structures: {len(sky_entries)}.
- Sea-floor structures: {len(sea_floor_entries)}.
- Ship/ocean-surface structures: {len(ship_entries)}.
- Dungeons: {len(dungeon_entries)}.
- Boss/dragon structures: {len(boss_entries)}.
- Village/town/settlement structures: {len(village_entries)}.
- Review-only density candidates: {len(override_candidates)}.
- Classification confidence: {counter_dict([entry.get("classification_confidence") for entry in entries])}.
- Manual-review rows: {sum(1 for entry in entries if entry.get("manual_review_required") is True)}.
- Name-only final classifications: {sum(1 for entry in entries if entry.get("name_only_classification") is True)}.

## Authority Files

- `config/ascendant_structures/structure_registry.json`
- `config/ascendant_structures/structure_evidence_registry.json`
- `config/ascendant_structures/structure_classification_confidence.json`
- `config/ascendant_structures/manual_structure_observations.json`
- `config/ascendant_structures/structure_region_rules.json`
- `config/ascendant_structures/structure_vertical_layer_rules.json`
- `config/ascendant_structures/structure_density_policy.json`
- `config/ascendant_structures/structure_set_overrides.json`
- `config/ascendant_structures/water_structure_policy.json`
- `config/ascendant_structures/sky_structure_policy.json`
- `config/ascendant_structures/sea_floor_structure_policy.json`
- `config/ascendant_structures/ship_structure_policy.json`
- `config/ascendant_structures/dungeon_structure_policy.json`
- `config/ascendant_structures/boss_structure_policy.json`
- `config/ascendant_structures/village_structure_policy.json`
- `config/ascendant_structures/structure_test_points.json`

## Director Rules

- Names, namespace/path words, template-pool words, and mod labels are weak hints only. They must never be the only evidence for water, frozen-ocean, sky, sea-floor, village/town, boss, or dungeon classifications.
- Crownlands/Hearthlands stay beginner-friendly. Bosses, dragons, and high-danger dungeons must not become common starter landmarks.
- Sunreach and Stoneback are land-first. Ocean/ship/sea-floor structures need explicit coastline, ocean, frozen-ocean, or wetland context.
- Verdant Coast owns most lush/coastal/oceanic structure identity. Frostmarch owns frozen-ocean and ice-themed water content.
- Sky structures must be rare and manually reviewed for visual noise before any density increase.
- Village/town structures are not injected into new village pools in this pass. Existing generation is only audited for overlap, density, and region fit.
- Structure loot and danger tier are policy-only here. No loot rewrites or rank gates are enabled.

## Current Blockers

- Dense structure families still need manual review before any live spacing changes.
- Some IDAS, Moog, Integrated Villages, and Towns and Towers structures have broad biome selectors and need in-game spot checks.
- Live region locks require a later approved datapack/helper implementation. This pass only creates the map and disabled candidates.
"""
    write_text(DOCS_DIR / "ASCENDANT_STRUCTURE_DIRECTOR.md", director_doc)

    region_layer_doc = f"""# Structure Region And Layer Index

Generated: {generated_at}

This index maps structures to Atlas regions and vertical placement layers. It uses biome tags/selectors, start pools, structure sets, generation steps, and sampled block palettes where available.

## Summary

- Structures indexed: {len(entries)}.
- Layer counts: `{layer_counts}`.
- Water-region warning candidates: {len(validation.get("water_structures_outside_water_regions", []))}.
- Sky common/near-spawn warning candidates: {len(validation.get("sky_structures_common_or_near_spawn", []))}.

## Region And Layer Preview

{make_markdown_table(["Structure", "Regions", "Layers", "Required Terrain", "Action"], region_rows, limit=180)}
"""
    write_text(DOCS_DIR / "STRUCTURE_REGION_AND_LAYER_INDEX.md", region_layer_doc)

    density_impl_doc = f"""# Structure Density Implementation Report

Generated: {generated_at}

This report converts the density audit into review-only implementation candidates. No candidate is live. No OpenLoader structure-set override was written by this generator.

## Summary

- Structure sets with density policy: {len(density_entries)}.
- Dense/dangerously dense structure entries: {len(validation.get("dangerously_dense_or_dense_spacing", []))}.
- Village/town overlap-risk structure sets: {len(validation.get("village_town_overlap_risks", []))}.
- Disabled candidate override rows: {len(override_candidates)}.

## Candidate Overrides

{make_markdown_table(["Structure Set", "Current Spacing", "Current Separation", "Candidate Spacing", "Candidate Separation", "Fix Type"], override_rows, limit=160)}

## Implementation Boundary

- Candidate files live under `config/ascendant_structures/candidates/` and are not loaded by Minecraft.
- A future live override must be copied into `config/openloader/data/ascendant_structure_overrides/` only after manual review.
- First approved changes should be small spacing/separation adjustments for obvious spam families, not broad disables.
"""
    write_text(DOCS_DIR / "STRUCTURE_DENSITY_IMPLEMENTATION_REPORT.md", density_impl_doc)

    water_sky_doc = f"""# Water And Sky Structures

Generated: {generated_at}

This separates structures that need water, coast, sea-floor, wetland, or sky rules. These should never be judged as ordinary land structures.

## Summary

- Water structures: {len(water_entries)}.
- Sea-floor structures: {len(sea_floor_entries)}.
- Ship/ocean-surface structures: {len(ship_entries)}.
- Sky structures: {len(sky_entries)}.
- Water structures outside explicit water-region policy: {len(validation.get("water_structures_outside_water_regions", []))}.
- Sky structures common or near spawn: {len(validation.get("sky_structures_common_or_near_spawn", []))}.

## Water Structures

{make_markdown_table(["Structure", "Mod", "Water Role", "Layers", "Regions", "Action"], water_rows, limit=140)}

## Sky Structures

{make_markdown_table(["Structure", "Mod", "Sky Role", "Regions", "Spacing", "Action"], sky_rows, limit=80)}
"""
    write_text(DOCS_DIR / "WATER_AND_SKY_STRUCTURES.md", water_sky_doc)

    danger_doc = f"""# Structure Loot And Danger Tiers

Generated: {generated_at}

This links major structure categories to danger tier, Guild rank tier, and loot tier. It is policy-only; no loot tables, bounty rewards, recipes, magic gates, or rank gates are enabled here.

## Summary

- Boss/dragon structures: {len(boss_entries)}.
- Dangerous dungeons: {len(dungeon_entries)}.
- Review-only loot tiers: {len(validation.get("no_loot_tier", []))}.
- Boss/dungeon beginner-region warnings: {len(validation.get("boss_or_dungeon_in_beginner_regions", []))}.

## Danger And Loot Preview

{make_markdown_table(["Structure", "Mod", "Class", "Danger", "Guild Rank", "Loot Tier", "Density", "Action"], danger_rows, limit=180)}

## Reward Rules

- Beginner regions should not hand out boss-tier loot from random nearby structures.
- Boss structures must beat common dungeons in reward quality, but must also be rarer and farther from safe center play.
- Dungeon loot linkage remains a control scaffold until the loot economy pass approves exact table rewrites.
"""
    write_text(DOCS_DIR / "STRUCTURE_LOOT_AND_DANGER_TIERS.md", danger_doc)

    testing_doc = f"""# Structure Testing Checklist

Generated: {generated_at}

Use this after Jayden accepts the current Atlas terrain enough to test structures. Always use a fresh world or ungenerated chunks.

## Setup

1. Create a fresh creative validation world.
2. Keep the current Atlas terrain validation reports for reference.
3. Use `/locate structure <id>` from `config/ascendant_structures/structure_test_points.json`.
4. For each find, record coordinates, Atlas region, visible biome, structure ID, nearby structures, and a screenshot if it fails.

## What To Check

- Region fit: structure palette and biome should match Frostmarch, Sunreach, Verdant Coast, Stoneback, Crownlands, or outer-region identity.
- Density: one structure can be exciting; repeated fields of similar landmarks are clutter.
- Water fit: ships, sea-floor ruins, ocean monuments, Aquamirae, sirens, and sunken structures should be water/coast/frozen-ocean content, not inland spam.
- Sky fit: floating islands and airships should feel rare and intentional.
- Settlement fit: villages/towns should not overlap, stack, or erase wilderness gaps.
- Danger fit: bosses, dragons, and high-tier dungeons should not dominate starter regions.
- Loot fit: chest/reward tier should match danger tier; do not judge exact loot rewrites yet.

## Do Not Do During This Test

- Do not add new structure mods.
- Do not inject villages, Hunter Boards, Guild Halls, or NPC placement.
- Do not enable all candidate overrides.
- Do not rewrite loot or recipes.
"""
    write_text(DOCS_DIR / "STRUCTURE_TESTING_CHECKLIST.md", testing_doc)


def write_manual_observation_file(generated_at: str) -> None:
    write_json(
        MANUAL_OBSERVATIONS_PATH,
        {
            "version": 1,
            "generated_at": generated_at,
            "status": "review_only_live_observation_import_no_generation_changes",
            "schema": {
                "requested_structure_id": "Structure ID the player asked /locate for; may contain a narrow wildcard only for grouped player reports.",
                "actual_structure_id_seen": "Actual generated structure if a mod redirected or replaced the locate result.",
                "locate_command": "Command or command chain used.",
                "coordinates": "Object with x/y/z if known, otherwise null.",
                "atlas_region": "Atlas region from /ascatlas here if known.",
                "biome": "Actual biome from /ascatlas here or debug screen if known.",
                "visual_issue_tags": "Short tags such as water_island, region_fit_mismatch, looked_good, needs_followup.",
                "player_notes": "Jayden's note or condensed exact field observation.",
                "screenshot_reference": "Optional screenshot path.",
                "decision": "review decision; never a live override by itself.",
                "timestamp_or_session_note": "Session marker for traceability.",
            },
            "observations": default_manual_observations(),
        },
    )


def build_evidence_registry(entries: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    strength_counts = Counter()
    for entry in entries:
        for source in entry.get("evidence", {}).get("detail", {}).get("evidence_sources", []):
            strength_counts[str(source.get("strength") or "weak")] += 1
    rows = []
    for entry in entries:
        detail = entry.get("evidence", {}).get("detail", {})
        rows.append(
            {
                "structure_id": entry["structure_id"],
                "structure_set_ids": [item.get("structure_set") for item in entry.get("structure_sets", []) if item.get("structure_set")],
                "source_mod": entry["source_mod"],
                "dimension": detail.get("dimension"),
                "biome_tags_from_structure": detail.get("biome_tag_refs", []),
                "allowed_biome_ids_if_resolved": detail.get("allowed_biome_ids", []),
                "unresolved_biome_tags": detail.get("unresolved_biome_tags", []),
                "template_pool_ids": detail.get("template_pool_ids", []),
                "template_nbt_ids": detail.get("template_nbt_ids", []),
                "block_palette_evidence": detail.get("block_palette_evidence", {}),
                "loot_table_ids": detail.get("loot_table_ids", []),
                "terrain_adaptation": detail.get("terrain_adaptation"),
                "placement_type": detail.get("placement_type"),
                "heightmap": detail.get("heightmap"),
                "start_height": detail.get("start_height"),
                "processor_lists": detail.get("processor_lists", []),
                "live_locate_or_manual_evidence": detail.get("manual_live_evidence", []),
                "name_hints_weak_only": detail.get("name_hints_weak_only", {}),
                "final_classification": detail.get("final_classification", {}),
                "confidence_score": entry.get("confidence"),
                "confidence_tier": entry.get("classification_confidence"),
                "evidence_source": entry.get("evidence_source", []),
                "reason_summary": entry.get("classification_reason"),
            }
        )
    return {
        "version": 1,
        "generated_at": generated_at,
        "status": "evidence_registry_no_live_generation_changes",
        "evidence_strength_summary": dict(sorted(strength_counts.items())),
        "structure_count": len(rows),
        "structures": rows,
    }


def build_confidence_registry(entries: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    rows = [
        {
            "structure_id": entry["structure_id"],
            "source_mod": entry["source_mod"],
            "structure_class": entry["structure_class"],
            "water_role": entry["water_role"],
            "sky_role": entry["sky_role"],
            "confidence": entry["confidence"],
            "classification_confidence": entry["classification_confidence"],
            "evidence_strength_counts": entry.get("evidence_strength_counts", {}),
            "manual_review_required": entry["manual_review_required"],
            "name_only_classification": entry["name_only_classification"],
            "classification_reason": entry["classification_reason"],
            "name_hints_weak_only": entry.get("evidence", {}).get("detail", {}).get("name_hints_weak_only", {}),
        }
        for entry in entries
    ]
    return {
        "version": 1,
        "generated_at": generated_at,
        "status": "classification_confidence_no_live_generation_changes",
        "summary": {
            "strong": sum(1 for entry in rows if entry["classification_confidence"] == "strong"),
            "medium": sum(1 for entry in rows if entry["classification_confidence"] == "medium"),
            "weak": sum(1 for entry in rows if entry["classification_confidence"] == "weak"),
            "manual_review_required": sum(1 for entry in rows if entry["manual_review_required"] is True),
            "name_only_classification": sum(1 for entry in rows if entry["name_only_classification"] is True),
        },
        "structures": rows,
    }


def build_review_candidate_files(entries: list[dict[str, Any]], policy_outputs: dict[str, Any], generated_at: str) -> dict[str, Any]:
    land_candidates = []
    region_candidates = []
    for entry in entries:
        risk_flags = set(entry.get("risk_flags", []))
        if "manual_water_island_placement_issue" in risk_flags or (
            entry.get("water_role") == "none"
            and entry.get("manual_review_required") is True
            and set((entry.get("evidence", {}).get("detail", {}).get("name_hints_weak_only") or {}).keys()) & {"dragon", "settlement"}
        ):
            land_candidates.append(
                {
                    "structure_id": entry["structure_id"],
                    "structure_sets": [item.get("structure_set") for item in entry.get("structure_sets", []) if item.get("structure_set")],
                    "current_water_role": entry.get("water_role"),
                    "current_required_terrain": entry.get("required_terrain"),
                    "evidence_source": entry.get("evidence_source", []),
                    "confidence": entry.get("confidence"),
                    "reported_or_detected_issue": entry.get("risk_flags", []),
                    "candidate_fix": "Review biome/tag or region-lock options that keep this land structure off ocean-scale water basins without changing all structures in its source mod.",
                    "live_enabled": False,
                }
            )
        if entry.get("recommended_action") == "should_region_lock" or "manual_water_island_placement_issue" in risk_flags:
            region_candidates.append(
                {
                    "structure_id": entry["structure_id"],
                    "structure_sets": [item.get("structure_set") for item in entry.get("structure_sets", []) if item.get("structure_set")],
                    "atlas_allowed_regions": entry.get("atlas_allowed_regions", []),
                    "biome_tag_or_selector": entry.get("biome_tag_or_selector"),
                    "evidence_source": entry.get("evidence_source", []),
                    "confidence": entry.get("confidence"),
                    "candidate_fix": "Review a narrow per-structure region/biome tag rule. Avoid broad structure-set locks unless every member is reviewed.",
                    "live_enabled": False,
                }
            )

    common = {
        "version": 1,
        "generated_at": generated_at,
        "status": "disabled_review_only_not_loaded_by_minecraft",
        "do_not_move_to_openloader_without_approval": True,
    }
    return {
        "land": {
            **common,
            "candidate_scope": "land structures with manual water-island evidence or low-confidence land placement evidence",
            "candidates": land_candidates,
        },
        "region": {
            **common,
            "candidate_scope": "structures that may need narrow Atlas region or biome-tag locks after visual review",
            "candidates": region_candidates,
        },
        "density": {
            **common,
            "candidate_scope": "spacing/density candidates generated from structure-set evidence; still disabled",
            "candidates": policy_outputs.get("structure_set_overrides", []),
        },
    }


def write_evidence_docs(
    generated_at: str,
    entries: list[dict[str, Any]],
    evidence_registry: dict[str, Any],
    confidence_registry: dict[str, Any],
    validation: dict[str, Any],
) -> None:
    weak_rows = [
        entry
        for entry in entries
        if entry.get("manual_review_required") is True
    ][:60]
    iceandfire_rows = [
        entry
        for entry in entries
        if str(entry.get("structure_id", "")).startswith("iceandfire:")
    ]
    idas_override_notes = [
        "iceandfire:gorgon_temple locate evidence is recorded as IDAS replacement idas:labyrinth; the active generated result looked good.",
        "iceandfire:graveyard locate evidence is recorded as IDAS replacement idas:haunted_manor; placement still needs follow-up if it looks wrong.",
    ]
    rules_doc = f"""# Structure Classification Evidence Rules

Generated: {generated_at}

This is the evidence contract for the Ascendant Structure Director. It fixes the previous bad inference where English words in mod labels or structure IDs were treated as placement truth.

## Evidence Strength

- Strong: manual/live locate evidence, resolved biome tags or biome IDs, structure-set rules, structure JSON placement fields, template pool/NBT evidence, and sampled block palettes.
- Medium: registry class, registry integration hooks, loot/policy linkage, and worldgen type/step.
- Weak: structure ID words, namespace/path words, template-pool words, mod display names, and English labels such as ice, ocean, ship, water, desert, cave, village, dragon, sky, or boss.

## Hard Rules

- Weak hints are recorded in `name_hints_weak_only` and must never be the only evidence for a final sensitive classification.
- Water, frozen-ocean, ocean, sky, sea-floor, village/town, boss, and dungeon classifications must carry non-name evidence and a confidence score.
- If evidence is weak or conflicting, the row must set `manual_review_required=true`.
- IDAS replacement cases are classified from the active generated structure, not only the requested Ice and Fire locate name.
- Candidate overrides stay disabled until Jayden approves a specific live change after in-game review.
"""
    audit_doc = f"""# Structure Classification Audit Report

Generated: {generated_at}

## Summary

- Structures with evidence rows: {evidence_registry.get('structure_count')}.
- Strong confidence rows: {confidence_registry['summary']['strong']}.
- Medium confidence rows: {confidence_registry['summary']['medium']}.
- Weak confidence rows: {confidence_registry['summary']['weak']}.
- Manual-review rows: {confidence_registry['summary']['manual_review_required']}.
- Name-only final classifications: {confidence_registry['summary']['name_only_classification']}.
- Water roles without non-name evidence: {len(validation.get('water_roles_without_non_name_evidence', []))}.
- Frozen-ocean roles without cold/frozen evidence: {len(validation.get('frozen_ocean_without_cold_or_frozen_evidence', []))}.
- Sky roles without height evidence: {len(validation.get('sky_roles_without_height_evidence', []))}.

## Ice And Fire Correction

{make_markdown_table(["Structure", "Class", "Water Role", "Regions", "Confidence", "Manual Review", "Reason"], [[entry["structure_id"], entry["structure_class"], entry["water_role"], ",".join(entry["atlas_allowed_regions"][:4]), entry["confidence"], entry["manual_review_required"], entry["classification_reason"]] for entry in iceandfire_rows], limit=30)}

## IDAS Override Handling

{"".join(f"- {note}\n" for note in idas_override_notes)}

## Manual Review Queue Preview

{make_markdown_table(["Structure", "Class", "Water", "Sky", "Confidence", "Risk Flags"], [[entry["structure_id"], entry["structure_class"], entry["water_role"], entry["sky_role"], entry["confidence"], ",".join(entry["risk_flags"][:5])] for entry in weak_rows], limit=60)}
"""
    write_text(DOCS_DIR / "STRUCTURE_CLASSIFICATION_EVIDENCE_RULES.md", rules_doc)
    write_text(DOCS_DIR / "STRUCTURE_CLASSIFICATION_AUDIT_REPORT.md", audit_doc)


def main() -> int:
    generated_at = now_iso()
    entries, structure_set_index, audit = build_entries()
    known_ids = {str(entry.get("structure_id")) for entry in entries if entry.get("structure_id")}
    density_entries = sorted(structure_set_index.values(), key=lambda entry: str(entry.get("structure_set")))
    validation = build_validation(entries, density_entries, known_ids)
    policy_outputs = build_policy_outputs(entries, density_entries)
    test_points = build_test_points(entries, policy_outputs)

    summary = {
        "generated_at": generated_at,
        "structure_count": len(entries),
        "structure_set_count": len(density_entries),
        "structure_class_counts": counter_dict([entry.get("structure_class") for entry in entries]),
        "classification_confidence_counts": counter_dict([entry.get("classification_confidence") for entry in entries]),
        "manual_review_required_count": sum(1 for entry in entries if entry.get("manual_review_required") is True),
        "name_only_classification_count": sum(1 for entry in entries if entry.get("name_only_classification") is True),
        "source_mod_counts": dict(sorted(Counter(str(entry.get("source_mod")) for entry in entries).items())),
        "density_class_counts": counter_dict([entry.get("density_class") for entry in entries]),
        "recommended_action_counts": counter_dict([entry.get("recommended_action") for entry in entries]),
        "manual_review_priority_counts": counter_dict([entry.get("manual_review_priority") for entry in entries]),
        "policy_filter_counts": audit.get("policy_filter_counts", {}),
    }

    common_header = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_live_structure_rewrites",
        "sources": [
            "config/ascendant_index/structure_registry.json",
            "docs/generated/worldgen_content_audit.json",
            "config/ascendant_loot/structure_loot_tiers.json",
            "mod/datapack biome tags and structure JSONs",
            "config/ascendant_structures/manual_structure_observations.json",
        ],
        "constraints": [
            "Do not add new structure mods.",
            "Do not add Hunter Boards or Guild Halls.",
            "Do not inject anything into village pools.",
            "Do not rewrite live structure sets unless a later approved change is a safe spacing/density reduction.",
        ],
    }

    tier_registry = {
        **common_header,
        "summary": summary,
        "validation": validation,
        "structures": entries,
    }
    region_rules = {
        **common_header,
        "summary": summary,
        "region_rules": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "category": entry["category"],
                "atlas_allowed_regions": entry["atlas_allowed_regions"],
                "biome_families": entry["biome_families"],
                "biome_tag_or_selector": entry.get("biome_tag_or_selector"),
                "distance_ring": entry["distance_ring"],
                "should_region_restrict": entry["should_region_restrict"],
                "recommended_action": entry["recommended_action"],
                "evidence": entry["evidence"],
            }
            for entry in entries
        ],
        "validation": {
            "no_atlas_region_rules": validation["no_atlas_region_rules"],
            "boss_or_dungeon_in_beginner_regions": validation["boss_or_dungeon_in_beginner_regions"],
            "policy_references_missing_structure_ids": validation["policy_references_missing_structure_ids"],
        },
    }
    density_policy = {
        **common_header,
        "summary": summary,
        "structure_sets": density_entries,
        "structures": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "structure_class": entry["structure_class"],
                "density_class": entry["density_class"],
                "density_risk": entry["density_risk"],
                "minimum_spacing": entry["minimum_spacing"],
                "minimum_separation": entry["minimum_separation"],
                "structure_sets": entry["structure_sets"],
                "manual_review_priority": entry["manual_review_priority"],
                "recommended_action": entry["recommended_action"],
            }
            for entry in entries
        ],
        "validation": {
            "dangerously_dense_or_dense_spacing": validation["dangerously_dense_or_dense_spacing"],
            "village_town_overlap_risks": validation["village_town_overlap_risks"],
        },
    }
    loot_linkage = {
        **common_header,
        "summary": summary,
        "structure_loot_linkage": [
            {
                "structure_id": entry["structure_id"],
                "source_mod": entry["source_mod"],
                "category": entry["category"],
                "danger_tier": entry["danger_tier"],
                "guild_rank_tier": entry["guild_rank_tier"],
                "loot_tier": entry["loot_tier"],
                "allowed_rarity_ceiling": entry["allowed_rarity_ceiling"],
                "chest_blocks_sampled": entry["block_profile"]["chest_blocks_sampled"],
                "should_rank_tier": entry["should_rank_tier"],
                "recommended_action": entry["recommended_action"],
            }
            for entry in entries
        ],
        "validation": {
            "no_loot_tier": validation["no_loot_tier"],
            "no_tier_assignment": validation["no_tier_assignment"],
        },
    }

    write_json(OUT_DIR / "structure_tier_registry.json", tier_registry)
    write_json(
        OUT_DIR / "structure_registry.json",
        {
            **common_header,
            "summary": summary,
            "structures": policy_outputs["structure_registry"],
            "validation": validation,
        },
    )
    write_json(OUT_DIR / "structure_region_rules.json", region_rules)
    write_json(
        OUT_DIR / "structure_vertical_layer_rules.json",
        {
            **common_header,
            "summary": summary,
            "vertical_layer_rules": policy_outputs["vertical_layer_rules"],
            "validation": {
                "water_structures_outside_water_regions": validation["water_structures_outside_water_regions"],
                "sea_floor_structures_without_deep_water_rule": validation["sea_floor_structures_without_deep_water_rule"],
                "sky_structures_common_or_near_spawn": validation["sky_structures_common_or_near_spawn"],
            },
        },
    )
    write_json(OUT_DIR / "structure_density_policy.json", density_policy)
    write_json(
        OUT_DIR / "structure_set_overrides.json",
        {
            **common_header,
            "status": "disabled_candidates_only_no_live_openloader_overrides",
            "summary": {
                **summary,
                "candidate_override_count": len(policy_outputs["structure_set_overrides"]),
            },
            "candidate_overrides": policy_outputs["structure_set_overrides"],
        },
    )
    write_json(OUT_DIR / "structure_loot_linkage.json", loot_linkage)
    for policy_name in [
        "water_structure_policy",
        "sky_structure_policy",
        "sea_floor_structure_policy",
        "ship_structure_policy",
        "dungeon_structure_policy",
        "boss_structure_policy",
        "village_structure_policy",
    ]:
        write_json(
            OUT_DIR / f"{policy_name}.json",
            {
                **common_header,
                "summary": summary,
                policy_name: policy_outputs[policy_name],
                "validation": validation,
            },
        )
    write_json(OUT_DIR / "structure_test_points.json", test_points)

    evidence_registry = build_evidence_registry(entries, generated_at)
    confidence_registry = build_confidence_registry(entries, generated_at)
    write_json(OUT_DIR / "structure_evidence_registry.json", evidence_registry)
    write_json(OUT_DIR / "structure_classification_confidence.json", confidence_registry)
    write_manual_observation_file(generated_at)

    candidates_dir = OUT_DIR / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    write_text(
        candidates_dir / "README.md",
        """# Disabled Structure Override Candidates

This folder is intentionally not an OpenLoader datapack. It contains review-only structure-set spacing candidates generated from the worldgen audit.

Do not copy any candidate into `config/openloader/data/ascendant_structure_overrides/` until Jayden approves that specific structure set after fresh-world testing.
""",
    )
    write_json(
        candidates_dir / "structure_set_override_candidates.json",
        {
            "version": 1,
            "generated_at": generated_at,
            "status": "disabled_review_only",
            "candidate_overrides": policy_outputs["structure_set_overrides"],
        },
    )
    review_candidate_files = build_review_candidate_files(entries, policy_outputs, generated_at)
    write_json(candidates_dir / "structure_land_placement_candidates.json", review_candidate_files["land"])
    write_json(candidates_dir / "structure_region_lock_candidates.json", review_candidate_files["region"])
    write_json(candidates_dir / "structure_density_candidates.json", review_candidate_files["density"])
    write_docs(generated_at, entries, density_entries, validation, audit, policy_outputs)
    write_evidence_docs(generated_at, entries, evidence_registry, confidence_registry, validation)
    print(f"Generated {len(entries)} structure tier rows and {len(density_entries)} structure-set density rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
