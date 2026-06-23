#!/usr/bin/env python3
"""Generate Ascendant Atlas control contracts, audits, docs, and debug waymark assets."""

from __future__ import annotations

import json
import pathlib
import zipfile
from dataclasses import dataclass
from typing import Any

import nbtlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_VERSION_1_20_1 = 3465
PACK_NAMES = [
    "config/openloader/data/ascendant_realms_atlas",
    "openloader/data/ascendant_realms_atlas",
]


VANILLA_BIOMES = [
    "minecraft:plains",
    "minecraft:sunflower_plains",
    "minecraft:forest",
    "minecraft:birch_forest",
    "minecraft:old_growth_birch_forest",
    "minecraft:dark_forest",
    "minecraft:flower_forest",
    "minecraft:meadow",
    "minecraft:cherry_grove",
    "minecraft:taiga",
    "minecraft:old_growth_pine_taiga",
    "minecraft:old_growth_spruce_taiga",
    "minecraft:snowy_taiga",
    "minecraft:snowy_plains",
    "minecraft:ice_spikes",
    "minecraft:frozen_river",
    "minecraft:frozen_ocean",
    "minecraft:deep_frozen_ocean",
    "minecraft:savanna",
    "minecraft:savanna_plateau",
    "minecraft:windswept_savanna",
    "minecraft:desert",
    "minecraft:badlands",
    "minecraft:wooded_badlands",
    "minecraft:eroded_badlands",
    "minecraft:jungle",
    "minecraft:sparse_jungle",
    "minecraft:bamboo_jungle",
    "minecraft:swamp",
    "minecraft:mangrove_swamp",
    "minecraft:river",
    "minecraft:beach",
    "minecraft:ocean",
    "minecraft:deep_ocean",
    "minecraft:warm_ocean",
    "minecraft:lukewarm_ocean",
    "minecraft:cold_ocean",
    "minecraft:windswept_hills",
    "minecraft:windswept_forest",
    "minecraft:stony_peaks",
    "minecraft:jagged_peaks",
    "minecraft:frozen_peaks",
    "minecraft:snowy_slopes",
    "minecraft:dripstone_caves",
    "minecraft:lush_caves",
    "minecraft:deep_dark",
    "minecraft:nether_wastes",
    "minecraft:crimson_forest",
    "minecraft:warped_forest",
    "minecraft:soul_sand_valley",
    "minecraft:basalt_deltas",
    "minecraft:the_end",
    "minecraft:end_highlands",
    "minecraft:end_midlands",
    "minecraft:small_end_islands",
    "minecraft:end_barrens",
]


PROGRESSION_TIERS = [
    {
        "id": "tier_0_hearthlands",
        "tier": 0,
        "rank_band": ["Unranked", "E-Rank"],
        "distance_blocks": [0, 1500],
        "loot_rarities": ["common", "uncommon"],
        "world_role": "Starter Crownlands and safe settlement learning loop.",
    },
    {
        "id": "tier_1_inner_wilds",
        "tier": 1,
        "rank_band": ["E-Rank", "D-Rank"],
        "distance_blocks": [1200, 3500],
        "loot_rarities": ["common", "uncommon", "rare"],
        "world_role": "First real roads, camps, minor ruins, and licensed hunter work.",
    },
    {
        "id": "tier_2_outer_marches",
        "tier": 2,
        "rank_band": ["D-Rank", "C-Rank"],
        "distance_blocks": [3000, 6500],
        "loot_rarities": ["uncommon", "rare", "epic"],
        "world_role": "Climate identity, harder structures, regional materials, and ranked contracts.",
    },
    {
        "id": "tier_3_ancient_frontiers",
        "tier": 3,
        "rank_band": ["C-Rank", "B-Rank"],
        "distance_blocks": [6000, 10000],
        "loot_rarities": ["rare", "epic", "legendary"],
        "world_role": "Major dungeons, elite mobs, frontier guild outposts, and boss leads.",
    },
    {
        "id": "tier_4_dragon_scars",
        "tier": 4,
        "rank_band": ["B-Rank", "A-Rank"],
        "distance_blocks": [9000, 14000],
        "loot_rarities": ["epic", "legendary", "mythic"],
        "world_role": "Dragon, Cataclysm, Marium, and realm-threat content.",
    },
    {
        "id": "tier_5_corrupted_rim",
        "tier": 5,
        "rank_band": ["A-Rank", "S-Rank"],
        "distance_blocks": [12000, 30000000],
        "loot_rarities": ["legendary", "mythic", "ascendant"],
        "world_role": "Ascendant-tier outer danger, capstone structures, and mythic rewards.",
    },
]


REGIONS = [
    {
        "id": "crownlands",
        "display_name": "The Crownlands",
        "tier": 0,
        "sector": "center",
        "coordinate_hint": "near world spawn",
        "biome_keywords": ["plains", "forest", "meadow", "cherry", "river"],
        "settlement_bias": ["hamlet", "village", "large_village"],
        "structure_bias": ["starter_waymark", "hunter_board", "farmstead", "safe_road"],
        "loot_ceiling": "uncommon",
    },
    {
        "id": "frostmarch",
        "display_name": "The Frostmarch",
        "tier": 2,
        "sector": "north",
        "coordinate_hint": "negative Z direction in the long-term Atlas module",
        "biome_keywords": ["snow", "frozen", "ice", "cold", "taiga"],
        "settlement_bias": ["village", "frontier_camp", "cold_port"],
        "structure_bias": ["frost_waymark", "aquamirae", "snow_ruin", "cold_outpost"],
        "loot_ceiling": "legendary",
    },
    {
        "id": "sunreach",
        "display_name": "Sunreach",
        "tier": 2,
        "sector": "south",
        "coordinate_hint": "positive Z direction in the long-term Atlas module",
        "biome_keywords": ["savanna", "desert", "badlands", "scorched", "hot"],
        "settlement_bias": ["market_town", "oasis_village", "road_camp"],
        "structure_bias": ["sunreach_waymark", "desert_ruin", "mowzie_encounter"],
        "loot_ceiling": "legendary",
    },
    {
        "id": "verdant_coast",
        "display_name": "The Verdant Coast",
        "tier": 2,
        "sector": "east",
        "coordinate_hint": "positive X direction in the long-term Atlas module",
        "biome_keywords": ["jungle", "swamp", "mangrove", "ocean", "coast", "river"],
        "settlement_bias": ["fishing_village", "river_market", "frontier_camp"],
        "structure_bias": ["verdant_crossing", "shipwreck", "wetland_ruin"],
        "loot_ceiling": "epic",
    },
    {
        "id": "stoneback_highlands",
        "display_name": "The Stoneback Highlands",
        "tier": 2,
        "sector": "west",
        "coordinate_hint": "negative X direction in the long-term Atlas module",
        "biome_keywords": ["mountain", "peak", "slope", "stony", "windswept"],
        "settlement_bias": ["mining_village", "guild_town", "watch_post"],
        "structure_bias": ["stoneback_waystation", "mine", "bridge", "mountain_ruin"],
        "loot_ceiling": "legendary",
    },
    {
        "id": "deep_wilds",
        "display_name": "The Deep Wilds",
        "tier": 3,
        "sector": "outer_wilds",
        "coordinate_hint": "farther from spawn after the first frontier",
        "biome_keywords": ["dark", "ancient", "deep", "lush", "dripstone"],
        "settlement_bias": ["frontier_camp", "ruined_settlement"],
        "structure_bias": ["idas", "yung_major", "moog_major", "rival_camp"],
        "loot_ceiling": "mythic",
    },
    {
        "id": "dragon_scars",
        "display_name": "The Dragon Scars",
        "tier": 4,
        "sector": "outer_highlands",
        "coordinate_hint": "remote mountain, volcanic, badlands, and dragon routes",
        "biome_keywords": ["dragon", "volcanic", "charred", "peak", "badlands"],
        "settlement_bias": ["ruined_settlement", "guild_outpost"],
        "structure_bias": ["dragon_scar_warning", "iceandfire", "cataclysm", "soulsweapons"],
        "loot_ceiling": "ascendant",
    },
    {
        "id": "nether_front",
        "display_name": "The Nether Front",
        "tier": 4,
        "sector": "nether",
        "dimension": "minecraft:the_nether",
        "biome_keywords": ["nether", "crimson", "warped", "basalt", "soul"],
        "settlement_bias": ["none", "fortified_outpost"],
        "structure_bias": ["nether_ruin", "cataclysm", "medieval_nether"],
        "loot_ceiling": "mythic",
    },
    {
        "id": "end_expanse",
        "display_name": "The End Expanse",
        "tier": 5,
        "sector": "end",
        "dimension": "minecraft:the_end",
        "biome_keywords": ["end"],
        "settlement_bias": ["none"],
        "structure_bias": ["mes", "end_ruin", "capstone"],
        "loot_ceiling": "ascendant",
    },
]


CLIMATE_SECTORS = [
    {
        "id": "center",
        "display_name": "Crownlands",
        "coordinate_rule": "near spawn; no hard biome-source lock yet",
        "primary_regions": ["crownlands"],
        "biome_keywords": ["plains", "forest", "meadow", "cherry", "river"],
    },
    {
        "id": "north",
        "display_name": "Frostmarch",
        "coordinate_rule": "future Atlas module: negative Z",
        "primary_regions": ["frostmarch"],
        "biome_keywords": ["snow", "frozen", "ice", "cold", "taiga"],
    },
    {
        "id": "south",
        "display_name": "Sunreach",
        "coordinate_rule": "future Atlas module: positive Z",
        "primary_regions": ["sunreach"],
        "biome_keywords": ["desert", "badlands", "savanna", "scorched", "hot"],
    },
    {
        "id": "east",
        "display_name": "Verdant Coast",
        "coordinate_rule": "future Atlas module: positive X",
        "primary_regions": ["verdant_coast"],
        "biome_keywords": ["jungle", "swamp", "mangrove", "ocean", "coast", "river"],
    },
    {
        "id": "west",
        "display_name": "Stoneback Highlands",
        "coordinate_rule": "future Atlas module: negative X",
        "primary_regions": ["stoneback_highlands"],
        "biome_keywords": ["mountain", "peak", "slope", "stony", "windswept"],
    },
]


ATLAS_STRUCTURES = [
    {
        "id": "crownlands_waymark",
        "display_name": "Crownlands Waymark",
        "region": "crownlands",
        "size": (7, 6, 5),
        "spacing": 180,
        "separation": 72,
        "salt": 2831101,
        "biomes": [
            "minecraft:plains",
            "minecraft:sunflower_plains",
            "minecraft:forest",
            "minecraft:birch_forest",
            "minecraft:flower_forest",
            "minecraft:meadow",
            "minecraft:cherry_grove",
        ],
        "banner": "minecraft:yellow_banner",
        "base": "minecraft:mossy_cobblestone",
        "wood": "minecraft:spruce_planks",
        "note_lines": ["Crownlands", "E/D work", "Roads stay lit", "Report threats"],
    },
    {
        "id": "frostmarch_waymark",
        "display_name": "Frostmarch Waymark",
        "region": "frostmarch",
        "size": (7, 6, 5),
        "spacing": 220,
        "separation": 88,
        "salt": 2831102,
        "biomes": [
            "minecraft:snowy_plains",
            "minecraft:snowy_taiga",
            "minecraft:ice_spikes",
            "minecraft:frozen_river",
            "minecraft:frozen_ocean",
            "minecraft:deep_frozen_ocean",
            "minecraft:frozen_peaks",
            "minecraft:snowy_slopes",
        ],
        "banner": "minecraft:light_blue_banner",
        "base": "minecraft:snow_block",
        "wood": "minecraft:spruce_planks",
        "note_lines": ["Frostmarch", "Cold kills slow", "Silver sightings", "Travel in pairs"],
    },
    {
        "id": "sunreach_waymark",
        "display_name": "Sunreach Waymark",
        "region": "sunreach",
        "size": (7, 6, 5),
        "spacing": 220,
        "separation": 88,
        "salt": 2831103,
        "biomes": [
            "minecraft:desert",
            "minecraft:savanna",
            "minecraft:savanna_plateau",
            "minecraft:windswept_savanna",
            "minecraft:badlands",
            "minecraft:wooded_badlands",
            "minecraft:eroded_badlands",
        ],
        "banner": "minecraft:orange_banner",
        "base": "minecraft:smooth_red_sandstone",
        "wood": "minecraft:acacia_planks",
        "note_lines": ["Sunreach", "Heat and raiders", "Gold routes", "Water before pride"],
    },
    {
        "id": "verdant_crossing",
        "display_name": "Verdant Crossing",
        "region": "verdant_coast",
        "size": (7, 6, 5),
        "spacing": 240,
        "separation": 96,
        "salt": 2831104,
        "biomes": [
            "minecraft:jungle",
            "minecraft:sparse_jungle",
            "minecraft:bamboo_jungle",
            "minecraft:swamp",
            "minecraft:mangrove_swamp",
            "minecraft:river",
            "minecraft:beach",
            "minecraft:warm_ocean",
            "minecraft:lukewarm_ocean",
        ],
        "banner": "minecraft:green_banner",
        "base": "minecraft:moss_block",
        "wood": "minecraft:jungle_planks",
        "note_lines": ["Verdant Coast", "Water hides teeth", "Storm routes", "Poison reports due"],
    },
    {
        "id": "stoneback_waystation",
        "display_name": "Stoneback Waystation",
        "region": "stoneback_highlands",
        "size": (7, 6, 5),
        "spacing": 240,
        "separation": 96,
        "salt": 2831105,
        "biomes": [
            "minecraft:windswept_hills",
            "minecraft:windswept_forest",
            "minecraft:stony_peaks",
            "minecraft:jagged_peaks",
            "minecraft:frozen_peaks",
            "minecraft:snowy_slopes",
            "minecraft:dripstone_caves",
        ],
        "banner": "minecraft:gray_banner",
        "base": "minecraft:stone_bricks",
        "wood": "minecraft:dark_oak_planks",
        "note_lines": ["Stoneback", "Mines and bridges", "Steel permits", "Watch the cliffs"],
    },
]


def write_json(relative_path: str, data: Any) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_text(relative_path: str, text: str) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n").strip() + "\n", encoding="utf-8")


def clear_pack(relative_path: str) -> None:
    path = ROOT / relative_path
    if not path.exists():
        return
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            child.rmdir()


def latest_client_mods() -> pathlib.Path | None:
    instances = pathlib.Path(r"C:\Users\Jayden\curseforge\minecraft\Instances")
    if not instances.exists():
        return None
    candidates = [
        path / "mods"
        for path in instances.iterdir()
        if path.is_dir() and path.name.startswith("Ascendant Realms") and (path / "mods").exists()
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.parent.stat().st_mtime, reverse=True)[0]


def scan_biomes() -> list[str]:
    ids = set(VANILLA_BIOMES)
    mods = latest_client_mods()
    if not mods:
        return sorted(ids)
    for jar in mods.glob("*.jar"):
        try:
            with zipfile.ZipFile(jar) as archive:
                for name in archive.namelist():
                    if not name.startswith("data/") or "/worldgen/biome/" not in name or not name.endswith(".json"):
                        continue
                    parts = name.split("/")
                    if len(parts) < 5:
                        continue
                    namespace = parts[1]
                    biome_path = "/".join(parts[4:])[:-5]
                    ids.add(f"{namespace}:{biome_path}")
        except zipfile.BadZipFile:
            continue
    return sorted(ids)


def assign_biome(biome_id: str) -> dict[str, Any]:
    text = biome_id.lower()
    if any(piece in text for piece in ["end_", "the_end", ":end", "ender"]):
        return {"region": "end_expanse", "sector": "end", "danger_tier": 5, "settlement_types": []}
    if any(piece in text for piece in ["nether", "crimson", "warped", "basalt", "soul_sand"]):
        return {"region": "nether_front", "sector": "nether", "danger_tier": 4, "settlement_types": ["fortified_outpost"]}
    if any(piece in text for piece in ["snow", "frozen", "ice", "cold", "taiga", "frost"]):
        return {
            "region": "frostmarch",
            "sector": "north",
            "danger_tier": 2,
            "settlement_types": ["village", "frontier_camp", "cold_port"],
        }
    if any(piece in text for piece in ["desert", "savanna", "badlands", "scorched", "volcanic", "ash"]):
        return {
            "region": "sunreach",
            "sector": "south",
            "danger_tier": 2,
            "settlement_types": ["oasis_village", "market_town", "road_camp"],
        }
    if any(piece in text for piece in ["jungle", "swamp", "mangrove", "ocean", "beach", "river", "coast"]):
        return {
            "region": "verdant_coast",
            "sector": "east",
            "danger_tier": 2,
            "settlement_types": ["fishing_village", "river_market", "frontier_camp"],
        }
    if any(piece in text for piece in ["mountain", "peak", "slope", "stony", "windswept", "cliff", "cave"]):
        return {
            "region": "stoneback_highlands",
            "sector": "west",
            "danger_tier": 2,
            "settlement_types": ["mining_village", "watch_post", "guild_town"],
        }
    if any(piece in text for piece in ["dark", "deep", "ancient", "spooky", "dead"]):
        return {
            "region": "deep_wilds",
            "sector": "outer_wilds",
            "danger_tier": 3,
            "settlement_types": ["frontier_camp", "ruined_settlement"],
        }
    return {
        "region": "crownlands",
        "sector": "center",
        "danger_tier": 0,
        "settlement_types": ["hamlet", "village", "large_village"],
    }


def structure_assignments() -> list[dict[str, Any]]:
    path = ROOT / "config/ascendant_index/structure_registry.json"
    if not path.exists():
        return []
    registry = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = []
    for structure in registry.get("structures", []):
        structure_id = structure.get("structure_id", "")
        structure_class = structure.get("structure_class", "uncategorized_structure")
        tier = {
            "settlement": 0,
            "landmark_or_ruin": 1,
            "dangerous_dungeon": 2,
            "boss_arena": 4,
            "dragon_tier_zone": 4,
            "uncategorized_structure": 2,
        }.get(structure_class, 2)
        rows.append(
            {
                "structure_id": structure_id,
                "source_mod": structure.get("source_mod", ""),
                "structure_class": structure_class,
                "atlas_tier": tier,
                "rank_band": PROGRESSION_TIERS[min(tier, len(PROGRESSION_TIERS) - 1)]["rank_band"],
                "loot_tier": structure.get("loot_tier", "review"),
                "allowed_near_spawn": tier <= 1,
                "atlas_notes": "Generated Atlas assignment; verify exact biome and spacing before hard overrides.",
            }
        )
    return sorted(rows, key=lambda item: item["structure_id"])


def make_state(name: str, properties: dict[str, str] | None = None) -> dict[str, Any]:
    state = {"Name": name}
    if properties:
        state["Properties"] = properties
    return state


def tag_int_list(values: list[int]) -> nbtlib.List[nbtlib.Int]:
    return nbtlib.List[nbtlib.Int]([nbtlib.Int(value) for value in values])


def make_compound(data: dict[str, Any]) -> nbtlib.Compound:
    result = nbtlib.Compound()
    for key, value in data.items():
        if isinstance(value, (nbtlib.Compound, nbtlib.List, nbtlib.String, nbtlib.Byte, nbtlib.Int, nbtlib.Long)):
            result[key] = value
        elif isinstance(value, str):
            result[key] = nbtlib.String(value)
        elif isinstance(value, dict):
            result[key] = make_compound(value)
        elif isinstance(value, list):
            if not value:
                result[key] = nbtlib.List([])
            elif all(isinstance(item, str) for item in value):
                result[key] = nbtlib.List[nbtlib.String]([nbtlib.String(item) for item in value])
            elif all(isinstance(item, dict) for item in value):
                result[key] = nbtlib.List[nbtlib.Compound]([make_compound(item) for item in value])
            else:
                raise TypeError(f"Unsupported NBT list for {key}: {value!r}")
        elif isinstance(value, bool):
            result[key] = nbtlib.Byte(1 if value else 0)
        elif isinstance(value, int):
            result[key] = nbtlib.Int(value)
        else:
            raise TypeError(f"Unsupported NBT value for {key}: {value!r}")
    return result


def set_block(
    blocks: dict[tuple[int, int, int], dict[str, Any]],
    x: int,
    y: int,
    z: int,
    name: str,
    properties: dict[str, str] | None = None,
    block_nbt: dict[str, Any] | None = None,
) -> None:
    blocks[(x, y, z)] = {"state": make_state(name, properties), "nbt": block_nbt}


def fill(
    blocks: dict[tuple[int, int, int], dict[str, Any]],
    start: tuple[int, int, int],
    end: tuple[int, int, int],
    name: str,
    properties: dict[str, str] | None = None,
) -> None:
    x1, y1, z1 = start
    x2, y2, z2 = end
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                set_block(blocks, x, y, z, name, properties)


def item_stack_nbt(item_id: str, slot: int | None = None, count: int = 1, tag: dict[str, Any] | None = None) -> nbtlib.Compound:
    data: dict[str, Any] = {"id": item_id, "Count": nbtlib.Byte(count)}
    if slot is not None:
        data["Slot"] = nbtlib.Byte(slot)
    if tag:
        data["tag"] = tag
    return make_compound(data)


def written_book_tag(title: str, lines: list[str]) -> dict[str, Any]:
    page_text = "\n".join(lines)
    return {
        "title": title[:32],
        "author": "Ascendant Atlas",
        "pages": [json.dumps({"text": page_text}, separators=(",", ":"))],
    }


def notice_board_nbt(title: str, lines: list[str]) -> dict[str, Any]:
    book = item_stack_nbt("minecraft:written_book", slot=0, tag=written_book_tag(title, lines))
    return {
        "id": "supplementaries:notice_board",
        "PageNumber": 0,
        "Items": nbtlib.List[nbtlib.Compound]([book]),
        "TextHolder": {
            "has_glowing_text": nbtlib.Byte(0),
            "color": "black",
            "message": [json.dumps({"text": line}, separators=(",", ":")) for line in lines],
            "has_antique_ink": nbtlib.Byte(0),
        },
    }


def container_loot_nbt(block_id: str, loot_table: str) -> dict[str, Any]:
    return {"id": block_id, "LootTable": loot_table}


def build_waymark(spec: dict[str, Any]) -> dict[tuple[int, int, int], dict[str, Any]]:
    blocks: dict[tuple[int, int, int], dict[str, Any]] = {}
    base = spec["base"]
    wood = spec["wood"]
    fill(blocks, (1, 0, 1), (5, 0, 3), base)
    fill(blocks, (2, 1, 3), (4, 3, 3), wood)
    set_block(blocks, 1, 1, 3, "minecraft:stripped_spruce_log", {"axis": "y"})
    set_block(blocks, 5, 1, 3, "minecraft:stripped_spruce_log", {"axis": "y"})
    set_block(blocks, 1, 2, 3, "minecraft:stripped_spruce_log", {"axis": "y"})
    set_block(blocks, 5, 2, 3, "minecraft:stripped_spruce_log", {"axis": "y"})
    set_block(blocks, 3, 2, 2, "supplementaries:notice_board", {"facing": "north", "has_book": "true"}, notice_board_nbt(spec["display_name"], spec["note_lines"]))
    set_block(blocks, 1, 3, 2, "mcwlights:tavern_wall_lantern", {"facing": "north"})
    set_block(blocks, 5, 3, 2, "mcwlights:tavern_wall_lantern", {"facing": "north"})
    set_block(blocks, 3, 4, 2, spec["banner"], {"rotation": "8"})
    set_block(blocks, 1, 1, 1, "minecraft:barrel", {"facing": "up", "open": "false"}, container_loot_nbt("minecraft:barrel", f"ascendant_atlas:chests/{spec['id']}"))
    set_block(blocks, 5, 1, 1, "minecraft:campfire", {"facing": "north", "lit": "true", "signal_fire": "false", "waterlogged": "false"})
    return blocks


def write_structure_nbt(relative_path: str, size: tuple[int, int, int], blocks: dict[tuple[int, int, int], dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    palette: list[dict[str, Any]] = []
    palette_keys: dict[str, int] = {}
    block_entries = []
    for pos, block in sorted(blocks.items(), key=lambda item: (item[0][1], item[0][2], item[0][0])):
        state = block["state"]
        key = json.dumps(state, sort_keys=True)
        if key not in palette_keys:
            palette_keys[key] = len(palette)
            palette.append(state)
        entry = nbtlib.Compound({"pos": tag_int_list([pos[0], pos[1], pos[2]]), "state": nbtlib.Int(palette_keys[key])})
        if block.get("nbt"):
            entry["nbt"] = make_compound(block["nbt"])
        block_entries.append(entry)
    root = nbtlib.Compound(
        {
            "DataVersion": nbtlib.Int(DATA_VERSION_1_20_1),
            "size": tag_int_list(list(size)),
            "palette": nbtlib.List[nbtlib.Compound]([make_compound(state) for state in palette]),
            "blocks": nbtlib.List[nbtlib.Compound](block_entries),
            "entities": nbtlib.List[nbtlib.Compound]([]),
        }
    )
    nbtlib.File(root).save(path, gzipped=True)


def loot_entry(item_id: str, weight: int = 1, count: tuple[int, int] | None = None) -> dict[str, Any]:
    entry: dict[str, Any] = {"type": "minecraft:item", "name": item_id, "weight": weight}
    if count:
        entry["functions"] = [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": count[0], "max": count[1]}}]
    return entry


def write_atlas_pack(base: str) -> None:
    clear_pack(base)
    write_json(base + "/pack.mcmeta", {"pack": {"pack_format": 15, "description": "Ascendant Atlas runtime status and debug waymark assets"}})
    write_text(
        base + "/README.md",
        """# Ascendant Realms Atlas Datapack

Generated by `scripts/generate-ascendant-atlas.py`.

This pack keeps the first Atlas-authored region waymarks as debug structure assets only. Natural placement is disabled while the live Atlas implementation focuses on the finite coordinate runtime, In Control areas, and density tuning.
""",
    )
    for spec in ATLAS_STRUCTURES:
        structure_id = "ascendant_atlas:" + spec["id"]
        pool_id = "ascendant_atlas:atlas/" + spec["id"]
        location = "ascendant_atlas:atlas/" + spec["id"]
        write_structure_nbt(base + f"/data/ascendant_atlas/structures/atlas/{spec['id']}.nbt", spec["size"], build_waymark(spec))
        write_json(
            base + f"/data/ascendant_atlas/worldgen/template_pool/atlas/{spec['id']}.json",
            {
                "name": pool_id,
                "fallback": "minecraft:empty",
                "elements": [
                    {
                        "weight": 1,
                        "element": {
                            "location": location,
                            "processors": "minecraft:empty",
                            "projection": "rigid",
                            "element_type": "minecraft:legacy_single_pool_element",
                        },
                    }
                ],
            },
        )
        write_json(
            base + f"/data/ascendant_atlas/worldgen/structure/{spec['id']}.json",
            {
                "type": "minecraft:jigsaw",
                "biomes": f"#ascendant_atlas:has_structure/{spec['id']}",
                "step": "surface_structures",
                "terrain_adaptation": "beard_thin",
                "spawn_overrides": {},
                "start_pool": pool_id,
                "size": 1,
                "start_height": {"absolute": 0},
                "project_start_to_heightmap": "WORLD_SURFACE_WG",
                "max_distance_from_center": 80,
                "use_expansion_hack": False,
            },
        )
        write_json(
            base + f"/data/ascendant_atlas/tags/worldgen/biome/has_structure/{spec['id']}.json",
            {"replace": False, "values": [{"id": biome, "required": False} for biome in spec["biomes"]]},
        )
        write_json(
            base + f"/data/ascendant_atlas/loot_tables/chests/{spec['id']}.json",
            {
                "type": "minecraft:chest",
                "pools": [
                    {
                        "rolls": {"type": "minecraft:uniform", "min": 2, "max": 4},
                        "entries": [
                            loot_entry("minecraft:bread", 4, (1, 3)),
                            loot_entry("minecraft:torch", 4, (2, 8)),
                            loot_entry("minecraft:paper", 2, (1, 4)),
                            loot_entry("minecraft:compass", 1, (1, 1)),
                            loot_entry("kubejs:guild_mark", 2, (1, 3)),
                        ],
                    }
                ],
            },
        )


def write_core_contracts() -> None:
    canonical_materials = {
        "copper": {"canonical": "minecraft:copper_ingot", "status": "live", "notes": "Vanilla copper remains canonical."},
        "iron": {"canonical": "minecraft:iron_ingot", "status": "live", "notes": "Base metal for early progression."},
        "gold": {"canonical": "minecraft:gold_ingot", "status": "live", "notes": "Trade and Sunreach material."},
        "silver": {"canonical": "iceandfire:silver_ingot", "status": "review", "notes": "Candidate canonical silver; verify JEI output and ore source before hard recipe rewrites."},
        "steel": {"canonical": "kubejs:tempered_steel", "status": "planned", "notes": "Progression glue item; recipe/live item pass is separate from this Atlas worldgen pass."},
        "dragon_material": {"canonical": "iceandfire:dragonbone", "status": "live_candidate", "notes": "Dragonbound material family, not a normal ore."},
    }
    write_json("config/ascendant_core/materials.json", {"version": 1, "canonical_materials": canonical_materials, "source": "Ascendant Core Integration brief"})
    write_json("config/ascendant_core/progression_tiers.json", {"version": 1, "tiers": PROGRESSION_TIERS})
    write_json(
        "config/ascendant_core/recipe_policy.json",
        {
            "version": 1,
            "policy": "KubeJS may add/remove/replace recipes only when the progression tier and canonical material owner are documented.",
            "rules": [
                "No legendary, mythic, or ascendant gear may have a vanilla-only basic recipe.",
                "Boss, dragon, and realm gear must require proof materials or ranked seals.",
                "Almost Unified owns broad duplicate recipe cleanup before hand-written KubeJS rewrites.",
            ],
        },
    )
    write_json(
        "config/ascendant_core/loot_policy.json",
        {
            "version": 1,
            "policy": "Loot rewards must follow structure tier, danger tier, and rarity registry.",
            "rarity_ceiling_by_tier": {
                "0": "uncommon",
                "1": "rare",
                "2": "epic",
                "3": "legendary",
                "4": "mythic",
                "5": "ascendant",
            },
        },
    )
    write_json(
        "config/ascendant_core/mob_policy.json",
        {
            "version": 1,
            "policy": "In Control caps and future finalize rules classify mobs by threat tier instead of removing content.",
            "live_files": ["config/incontrol/spawn.json", "config/ascendant_core/live_spawn_policy.json"],
        },
    )
    write_json(
        "config/ascendant_core/ore_generation.json",
        {
            "version": 1,
            "policy": "Do not let every installed mod define progression ore access independently.",
            "live_state": "audit_and_contract_only",
            "future_enforcement": [
                "disable duplicate ore gen in owning mod configs when clear",
                "use Open Loader datapack features for custom ore sources",
                "use Ascendant Atlas Forge module for coordinate/ring locks if datapacks are insufficient",
            ],
        },
    )
    write_json(
        "config/ascendant_core/structure_rewards.json",
        {
            "version": 1,
            "policy": "Structure rewards follow Atlas tier and rarity ceilings.",
            "source_registry": "config/ascendant_index/structure_registry.json",
            "atlas_source": "config/ascendant_atlas/structure_distribution.json",
        },
    )
    write_json(
        "config/ascendant_core/vendor_policy.json",
        {
            "version": 1,
            "policy": "Guild vendors and quartermasters should sell preparation, not skip progression.",
            "rank_unlocks": ["Guild Mark", "Hunter Seal", "Ascendant Sigil"],
        },
    )
    write_json(
        "config/ascendant_core/unification_policy.json",
        {
            "version": 1,
            "tools": ["Almost Unified", "Almost Unify Everything", "Polymorph", "KubeJS", "Open Loader"],
            "policy": "Almost Unified handles broad material convergence; KubeJS handles authored progression bridges.",
        },
    )
    write_json(
        "config/ascendant_core/dimension_policy.json",
        {
            "version": 1,
            "dimensions": {
                "minecraft:overworld": {"atlas_regions": ["crownlands", "frostmarch", "sunreach", "verdant_coast", "stoneback_highlands", "deep_wilds", "dragon_scars"]},
                "minecraft:the_nether": {"atlas_regions": ["nether_front"]},
                "minecraft:the_end": {"atlas_regions": ["end_expanse"]},
            },
        },
    )


def write_atlas_contracts() -> None:
    biomes = scan_biomes()
    assignments = [{"biome": biome, **assign_biome(biome)} for biome in biomes]
    structures = structure_assignments()
    write_json("config/ascendant_atlas/regions.json", {"version": 1, "regions": REGIONS})
    write_json("config/ascendant_atlas/difficulty_rings.json", {"version": 1, "rings": PROGRESSION_TIERS})
    write_json("config/ascendant_atlas/climate_sectors.json", {"version": 1, "sectors": CLIMATE_SECTORS})
    write_json("config/ascendant_atlas/biome_assignments.json", {"version": 1, "count": len(assignments), "assignments": assignments})
    write_json(
        "config/ascendant_atlas/settlement_rules.json",
        {
            "version": 1,
            "rules": [
                {"type": "hamlet", "required": ["houses", "food_source"], "forbidden": ["full_guild_hall"], "guild_presence": "none_or_notice"},
                {"type": "village", "required": ["houses", "farms", "guards", "local_notice"], "guild_presence": "hunter_board_allowed"},
                {"type": "large_village", "required": ["houses", "farms", "guards", "blacksmith_or_market"], "guild_presence": "hunter_board_expected"},
                {"type": "market_town", "required": ["market", "blacksmith", "tavern", "guards"], "guild_presence": "guild_clerk_expected"},
                {"type": "guild_town", "required": ["guild_hall", "rank_examiner", "bounty_master", "quartermaster", "training_yard"], "guild_presence": "full"},
            ],
        },
    )
    write_json(
        "config/ascendant_atlas/structure_distribution.json",
        {
            "version": 1,
            "source_registry": "config/ascendant_index/structure_registry.json",
            "count": len(structures),
            "assignments": structures,
            "live_atlas_structures": ATLAS_STRUCTURES,
        },
    )
    write_json(
        "config/ascendant_atlas/mob_distribution.json",
        {
            "version": 1,
            "source_registry": "config/ascendant_index/mob_registry.json",
            "policy": "Mobs are classified by threat tier, then filtered by region/biome/distance through In Control or a future helper module.",
            "live_guardrail": "config/incontrol/spawn.json",
        },
    )
    write_json(
        "config/ascendant_atlas/loot_distribution.json",
        {
            "version": 1,
            "policy": "Loot ceilings are enforced by Atlas tier. Atlas waymarks use only low-tier travel loot.",
            "prototype_tables": [f"ascendant_atlas:chests/{spec['id']}" for spec in ATLAS_STRUCTURES],
        },
    )
    write_json(
        "config/ascendant_atlas/ore_distribution.json",
        {
            "version": 1,
            "policy": "Ore control is contracted but not hard-overridden yet. The next safe step is one canonical ore/material vertical slice.",
            "tiers": [
                {"tier": 0, "materials": ["coal", "copper", "basic iron"]},
                {"tier": 1, "materials": ["iron", "gold", "redstone", "lapis"]},
                {"tier": 2, "materials": ["silver", "steel chain", "regional gems"]},
                {"tier": 3, "materials": ["diamond", "magic crystals", "rare boss fragments"]},
                {"tier": 4, "materials": ["dragon materials", "nether boss materials"]},
                {"tier": 5, "materials": ["ascendant materials"]},
            ],
        },
    )
    write_json(
        "config/ascendant_atlas/naming_pools.json",
        {
            "version": 1,
            "regions": {
                "crownlands": ["Halewick", "Brindleford", "Eastmere", "Oakrest"],
                "frostmarch": ["Frostmere", "Kaldvik", "Whitehall", "Rimeford"],
                "sunreach": ["Varnsun", "Ashmarket", "Redvale", "Sirocco Rest"],
                "verdant_coast": ["Mossbay", "Greenwater", "Reedcross", "Stormfen"],
                "stoneback_highlands": ["Varnhold", "Highmere", "Stonegate", "Ironwick"],
            },
        },
    )
    write_json(
        "config/ascendant_atlas/atlas_manifest.json",
        {
            "version": 1,
            "status": "active finite-world coordinate runtime; Atlas waymarks are debug-only assets",
            "datapack": "config/openloader/data/ascendant_realms_atlas",
            "runtime_config": "config/ascendant_atlas/runtime.json",
            "runtime_bridge": "kubejs/server_scripts/ascendant_atlas_runtime.js",
            "incontrol_areas": "config/incontrol/areas.json",
            "biomes_indexed": len(assignments),
            "structures_indexed": len(structures),
            "live_structure_ids": [],
            "debug_structure_ids": [f"ascendant_atlas:{spec['id']}" for spec in ATLAS_STRUCTURES],
            "live_runtime_features": [
                "60000 block world border centered at 0,0",
                "coordinate region/ring/sector scoreboards",
                "In Control coordinate areas for spawn guardrails",
                "structure density tuning for existing non-Atlas structures only; no Hunter Boards, Guild structures, decorative Atlas structures, or village injection are part of the terrain pass",
            ],
            "future_custom_module": "Approved helper module if needed for hard coordinate-locked biome-source control, road/bridge route generation, and structure-pool conflict resolution that datapacks/configs cannot safely express.",
        },
    )


def write_docs() -> None:
    live_rows = "\n".join(
        f"| `ascendant_atlas:{spec['id']}` | {spec['region']} | {spec['spacing']}/{spec['separation']} | Debug asset only; not registered for natural generation |"
        for spec in ATLAS_STRUCTURES
    )
    write_text(
        "docs/ASCENDANT_ATLAS_WORLDGEN.md",
        f"""# Ascendant Atlas Worldgen

Status: finite-world coordinate runtime active; Atlas waymarks are debug-only assets.

Ascendant Atlas is the pack-owned region and worldgen control layer for Ascendant Realms. The live testable layer now applies a 30000-block validation envelope, a 60000-block world border, region/ring/sector scoreboards, In Control coordinate areas, and the active coordinate-aware biome source.

## Debug Atlas Structures

| Structure | Region | Former Spacing/Separation | Current Use |
|---|---|---:|---|
{live_rows}

These structures are intentionally no longer registered in structure sets. They remain as source/debug assets only, because the current fresh-world test should focus on actual region rules, settlement density, and road/bridge behavior instead of placeholder waymarks.

## Authored Random Model

- Center: Crownlands, starter E/D danger, villages, small boards, common/uncommon loot.
- North: Frostmarch, cold pressure, Aquamirae/ice hooks, silver/cold survival identity.
- South: Sunreach, savanna/desert/badlands pressure, raiders, fire/sun reward themes.
- East: Verdant Coast, jungle/swamp/ocean routes, poison/water/storm identity.
- West: Stoneback Highlands, mountains, mines, bridges, steel/gem identity.
- Outer regions: Deep Wilds, Dragon Scars, Nether Front, and End Expanse.

## What Is Live Now

- `config/ascendant_atlas/runtime.json` defines the 30000-block validation envelope, world border, scoreboards, regions, and rings.
- `kubejs/server_scripts/ascendant_atlas_runtime.js` applies the world border and mirrors player position into Atlas scoreboards.
- `config/incontrol/areas.json` defines the coordinate boxes used by In Control spawn guardrails.
- `config/ascendant_atlas/road_bridge_policy.json` defines the road/bridge integration rulebook.
- `config/openloader/data/ascendant_realms_atlas/` keeps debug waymark structure assets and `/function ascendant_atlas:status`.

## What Still Needs A Custom Module

True biome-source replacement and terrain-aware road/bridge substitution need an Ascendant Atlas helper module or curated map workflow. Datapacks can add structures, tags, loot, and features; they cannot safely inspect roads crossing a river and replace them with bridge pieces after all terrain and structures generate.

## Test Plan

1. Launch a fresh creative test world.
2. Run `/function ascendant_atlas:status` at spawn and confirm region `0`, ring `0`.
3. Teleport to `0 100 -1600`, `0 100 1600`, `1600 100 0`, and `-1600 100 0`; rerun status each time.
4. Confirm region IDs change to Frostmarch, Sunreach, Verdant Coast, and Stoneback.
5. Fly villages/roads for 10-15 minutes and record any overlapping structures, floating roads, or river crossings without bridges.
6. Confirm the world border warning appears near the 30000-block edge.
7. Save/reload.
8. Repeat on a dedicated server after materializing server mods/configs.
""",
    )
    write_text(
        "docs/MATERIAL_UNIFICATION.md",
        """# Material Unification

Status: Ascendant Core contracts active; broad live unification is owned by Almost Unified, Almost Unify Everything, Polymorph, and KubeJS guardrails.

The pack-owned material lawbook is `config/ascendant_core/materials.json`. It chooses canonical material owners before recipe, loot, or ore rewrites happen.

Current rule: do not delete duplicate materials blindly. First choose a canonical item, then redirect recipes, loot, and JEI visibility through Almost Unified or a documented KubeJS pass.
""",
    )
    write_text(
        "docs/ORE_AND_WORLDGEN_CONTROL.md",
        """# Ore And Worldgen Control

Status: Atlas finite-world coordinate runtime and contracts active; ore generation remains contract/audit only.

`config/ascendant_core/ore_generation.json` and `config/ascendant_atlas/ore_distribution.json` define the intended progression curve. The next safe vertical slice is one material family, likely silver or steel, where we verify ore source, recipe path, loot source, JEI display, and progression tier before broad rewrites.

True coordinate-locked ore and hard climate-source control belongs in an Ascendant Atlas helper module if datapacks/configs are not enough.
""",
    )
    write_text(
        "docs/RECIPE_PROGRESSION.md",
        """# Recipe Progression

Status: policy active; no broad recipe deletion.

Recipes should answer where the item belongs in progression. Almost Unified handles duplicate material convergence first. KubeJS handles authored bridges, ranked seals, boss proofs, and custom glue recipes after the material owner and tier are recorded.
""",
    )
    write_text(
        "docs/LOOT_TABLE_CONTROL.md",
        """# Loot Table Control

Status: debug Atlas waymark loot tables retained as source material; broader loot rewrite pending.

Atlas debug waymarks use low-tier travel loot only if placed manually. Structure and dungeon loot should follow `config/ascendant_core/loot_policy.json`, `config/ascendant_core/structure_rewards.json`, and the generated rarity registry.
""",
    )
    write_text(
        "docs/MOB_SPAWN_AND_DROP_CONTROL.md",
        """# Mob Spawn And Drop Control

Status: In Control caps active; broader region-aware spawn/drop policy pending.

`config/incontrol/spawn.json` currently limits burst density by mod family. The Atlas mob policy defines the next step: classify mobs by threat tier, then apply biome/region/distance rules through In Control or a future helper module.
""",
    )


def main() -> int:
    write_core_contracts()
    write_atlas_contracts()
    for base in PACK_NAMES:
        write_atlas_pack(base)
    write_docs()
    print("Generated Ascendant Core contracts, Ascendant Atlas contracts, docs, and debug Atlas waymark assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
