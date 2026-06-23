#!/usr/bin/env python3
"""Generate Ascendant Atlas worldgen audit data.

The coordinate-aware Overworld override is currently disabled by policy so the
pack can use normal random Tectonic/Terralith terrain again.
"""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ATLAS_CONFIG = ROOT / "config" / "ascendant_atlas"
OUTPUT_PACKS = [
    ROOT / "config" / "openloader" / "data" / "ascendant_realms_atlas",
    ROOT / "openloader" / "data" / "ascendant_realms_atlas",
]

WORLD_RADIUS_BLOCKS = 12000
# Keep regional biome identity beyond the 30000-block square playable border,
# including corners, so visible terrain does not snap to the shared outer pool.
OUTER_RADIUS_BLOCKS = 50000
CENTER_RADIUS_BLOCKS = 500
AXIS_DOMINANCE_RATIO = 1.25
TRANSITION_WIDTH_BLOCKS = 2800
DOMAIN_WARP_SCALE_BLOCKS = 5200
DOMAIN_WARP_STRENGTH_BLOCKS = 900
MINIMUM_SECONDARY_REGION_WEIGHT = 0.10
HYDROLOGY_FILTER_ENABLED = True
WORLDGEN_OVERRIDE_ENABLED = False
WORLDGEN_OVERRIDE_POLICY_PATH = ATLAS_CONFIG / "worldgen_override_policy.json"

OCEAN_BIOMES = {
    "minecraft:ocean",
    "minecraft:deep_ocean",
    "minecraft:warm_ocean",
    "minecraft:lukewarm_ocean",
    "minecraft:deep_lukewarm_ocean",
    "minecraft:cold_ocean",
    "minecraft:deep_cold_ocean",
    "minecraft:frozen_ocean",
    "minecraft:deep_frozen_ocean",
}
RIVER_BIOMES = {"minecraft:river", "minecraft:frozen_river", "terralith:warm_river"}
COAST_BIOMES = {"minecraft:beach", "minecraft:snowy_beach", "minecraft:stony_shore", "terralith:gravel_beach", "terralith:white_cliffs", "terralith:orchid_swamp"}
WETLAND_BIOMES = {"minecraft:swamp", "minecraft:mangrove_swamp", "terralith:orchid_swamp", "terralith:moonlight_grove"}

ATLAS_LAND_BIAS_DENSITY = {
    "type": "minecraft:add",
    "argument1": {
        "type": "minecraft:flat_cache",
        "argument": {
            "type": "minecraft:shifted_noise",
            "noise": "minecraft:continentalness",
            "shift_x": "minecraft:shift_x",
            "shift_y": 0.0,
            "shift_z": "minecraft:shift_z",
            "xz_scale": 0.25,
            "y_scale": 0.0,
        },
    },
    "argument2": {
        "type": "ascendant_atlas_regions:atlas_land_bias",
        "enabled": True,
        "center_radius_blocks": CENTER_RADIUS_BLOCKS,
        "inner_full_bias_radius_blocks": 6500,
        "outer_radius_blocks": OUTER_RADIUS_BLOCKS,
        "edge_fade_blocks": 6000,
        "axis_dominance_ratio": AXIS_DOMINANCE_RATIO,
        "domain_warp_scale_blocks": DOMAIN_WARP_SCALE_BLOCKS,
        "domain_warp_strength_blocks": DOMAIN_WARP_STRENGTH_BLOCKS,
        "south_inner_bias": 0.18,
        "south_outer_bias": 0.86,
        "south_east_inner_bias": 0.14,
        "south_east_outer_bias": 0.58,
        "west_inner_bias": 0.16,
        "west_outer_bias": 0.82,
        "south_west_inner_bias": 0.22,
        "south_west_outer_bias": 0.96,
    },
}

REGION_BIOMES: dict[str, set[str]] = {
    "center": {
        "minecraft:plains",
        "minecraft:sunflower_plains",
        "minecraft:forest",
        "minecraft:birch_forest",
        "minecraft:old_growth_birch_forest",
        "minecraft:flower_forest",
        "minecraft:meadow",
        "minecraft:cherry_grove",
        "terralith:blooming_valley",
        "terralith:blooming_plateau",
        "terralith:lavender_forest",
        "terralith:lavender_valley",
        "terralith:moonlight_grove",
        "terralith:moonlight_valley",
        "terralith:sakura_grove",
        "terralith:sakura_valley",
        "terralith:shield",
        "terralith:shield_clearing",
        "terralith:valley_clearing",
    },
    "north": {
        "minecraft:frozen_ocean",
        "minecraft:frozen_river",
        "minecraft:ice_spikes",
        "minecraft:old_growth_pine_taiga",
        "minecraft:old_growth_spruce_taiga",
        "minecraft:snowy_plains",
        "minecraft:snowy_taiga",
        "minecraft:taiga",
        "terralith:birch_taiga",
        "terralith:cave/frostfire_caves",
        "terralith:cold_shrubland",
        "terralith:glacial_chasm",
        "terralith:rocky_shrubland",
        "terralith:siberian_grove",
        "terralith:siberian_taiga",
        "terralith:snowy_badlands",
        "terralith:snowy_cherry_grove",
        "terralith:snowy_maple_forest",
        "terralith:snowy_shield",
        "terralith:wintry_forest",
        "terralith:wintry_lowlands",
    },
    "south": {
        "minecraft:badlands",
        "minecraft:desert",
        "minecraft:eroded_badlands",
        "minecraft:savanna",
        "minecraft:savanna_plateau",
        "minecraft:warm_ocean",
        "minecraft:windswept_savanna",
        "minecraft:wooded_badlands",
        "terralith:arid_highlands",
        "terralith:ashen_savanna",
        "terralith:bryce_canyon",
        "terralith:cave/desert_caves",
        "terralith:desert_canyon",
        "terralith:desert_oasis",
        "terralith:desert_spires",
        "terralith:fractured_savanna",
        "terralith:hot_shrubland",
        "terralith:lush_desert",
        "terralith:red_oasis",
        "terralith:savanna_badlands",
        "terralith:savanna_slopes",
        "terralith:steppe",
        "terralith:volcanic_crater",
        "terralith:volcanic_peaks",
        "terralith:white_mesa",
    },
    "east": {
        "minecraft:bamboo_jungle",
        "minecraft:beach",
        "minecraft:deep_lukewarm_ocean",
        "minecraft:deep_ocean",
        "minecraft:jungle",
        "minecraft:lukewarm_ocean",
        "minecraft:mangrove_swamp",
        "minecraft:ocean",
        "minecraft:river",
        "minecraft:sparse_jungle",
        "minecraft:swamp",
        "minecraft:warm_ocean",
        "terralith:amethyst_rainforest",
        "terralith:cave/underground_jungle",
        "terralith:cloud_forest",
        "terralith:jungle_mountains",
        "terralith:orchid_swamp",
        "terralith:rocky_jungle",
        "terralith:tropical_jungle",
        "terralith:warm_river",
    },
    "west": {
        "minecraft:dripstone_caves",
        "minecraft:lush_caves",
        "minecraft:stony_peaks",
        "minecraft:stony_shore",
        "minecraft:windswept_forest",
        "minecraft:windswept_gravelly_hills",
        "minecraft:windswept_hills",
        "terralith:alpine_highlands",
        "terralith:amethyst_canyon",
        "terralith:cave/andesite_caves",
        "terralith:cave/deep_caves",
        "terralith:cave/diorite_caves",
        "terralith:cave/fungal_caves",
        "terralith:cave/granite_caves",
        "terralith:cave/infested_caves",
        "terralith:cave/mantle_caves",
        "terralith:cave/thermal_caves",
        "terralith:cave/tuff_caves",
        "terralith:forested_highlands",
        "terralith:granite_cliffs",
        "terralith:haze_mountain",
        "terralith:highlands",
        "terralith:mountain_steppe",
        "terralith:painted_mountains",
        "terralith:rocky_mountains",
        "terralith:stony_spires",
        "terralith:temperate_highlands",
        "terralith:white_cliffs",
        "terralith:windswept_spires",
        "terralith:yosemite_cliffs",
        "terralith:yosemite_lowlands",
    },
}

REGION_BIOMES["north_east"] = REGION_BIOMES["north"] | REGION_BIOMES["east"]
REGION_BIOMES["north_west"] = REGION_BIOMES["north"] | REGION_BIOMES["west"]
REGION_BIOMES["south_east"] = {
    "minecraft:badlands",
    "minecraft:bamboo_jungle",
    "minecraft:desert",
    "minecraft:jungle",
    "minecraft:mangrove_swamp",
    "minecraft:river",
    "minecraft:savanna",
    "minecraft:savanna_plateau",
    "minecraft:sparse_jungle",
    "minecraft:swamp",
    "minecraft:windswept_savanna",
    "minecraft:wooded_badlands",
    "terralith:amethyst_rainforest",
    "terralith:arid_highlands",
    "terralith:ashen_savanna",
    "terralith:desert_canyon",
    "terralith:desert_oasis",
    "terralith:fractured_savanna",
    "terralith:hot_shrubland",
    "terralith:lush_desert",
    "terralith:orchid_swamp",
    "terralith:red_oasis",
    "terralith:savanna_badlands",
    "terralith:savanna_slopes",
    "terralith:steppe",
    "terralith:tropical_jungle",
    "terralith:warm_river",
}
REGION_BIOMES["south_west"] = REGION_BIOMES["south"] | REGION_BIOMES["west"]
REGION_BIOMES["outer"] = (
    REGION_BIOMES["north"]
    | REGION_BIOMES["south"]
    | REGION_BIOMES["west"]
    | {
        "minecraft:dark_forest",
        "minecraft:deep_dark",
        "minecraft:eroded_badlands",
        "terralith:ancient_sands",
        "terralith:caldera",
        "terralith:desert_canyon",
        "terralith:scarlet_mountains",
        "terralith:volcanic_crater",
        "terralith:volcanic_peaks",
        "terralith:warped_mesa",
        "terralith:yellowstone",
    }
)

MIN_REGION_ENTRIES = {
    "center": 80,
    "north": 80,
    "south": 80,
    "east": 60,
    "west": 60,
    "north_east": 120,
    "north_west": 120,
    "south_east": 120,
    "south_west": 120,
    "outer": 160,
}


def is_cave_only_biome(biome_id: str) -> bool:
    return "/cave" in biome_id or biome_id.endswith("_caves") or biome_id == "minecraft:deep_dark"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def find_terralith_jar() -> Path:
    override = os.environ.get("ASCENDANT_TERRALITH_JAR", "").strip()
    if override:
        path = Path(override)
        if path.exists():
            return path
        raise FileNotFoundError(f"ASCENDANT_TERRALITH_JAR does not exist: {path}")

    instances_root = Path(r"C:\Users\Jayden\curseforge\minecraft\Instances")
    candidates: list[Path] = []
    if instances_root.exists():
        for instance in instances_root.glob("Ascendant Realms*"):
            candidates.extend(instance.glob("mods/Terralith_1.20.x_v2.5.4.jar"))
            candidates.extend(instance.glob("mods/Terralith*.jar"))

    if candidates:
        return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]

    raise FileNotFoundError(
        "Could not find a Terralith jar. Set ASCENDANT_TERRALITH_JAR to the active Terralith jar path."
    )


def read_terralith_overworld() -> dict:
    terralith_jar = find_terralith_jar()
    with zipfile.ZipFile(terralith_jar) as archive:
        return json.loads(archive.read("data/minecraft/dimension/overworld.json"))


def selected_entries(all_entries: list[dict], biome_ids: set[str], label: str) -> list[dict]:
    surface_biome_ids = {biome_id for biome_id in biome_ids if not is_cave_only_biome(biome_id)}
    entries = [copy.deepcopy(entry) for entry in all_entries if entry.get("biome") in surface_biome_ids]
    minimum = MIN_REGION_ENTRIES[label]
    if len(entries) < minimum:
        raise RuntimeError(f"Atlas region {label} only has {len(entries)} biome entries; expected at least {minimum}.")
    return entries


def unique_biomes(entries: list[dict]) -> list[str]:
    return sorted({str(entry.get("biome")) for entry in entries})


def parameter_range(entry: dict, key: str) -> tuple[float | None, float | None]:
    params = entry.get("parameters", {})
    value = params.get(key)
    if isinstance(value, list) and len(value) == 2:
        return float(value[0]), float(value[1])
    if isinstance(value, (int, float)):
        return float(value), float(value)
    return None, None


def classify_hydrology_from_evidence(biome_id: str, entries: list[dict]) -> tuple[list[str], list[str], str]:
    if biome_id in OCEAN_BIOMES:
        return ["ocean", "deep_ocean", "coast"], ["exact_water_biome_id"], "strong"
    if biome_id in RIVER_BIOMES:
        return ["river", "inland_water", "coast"], ["exact_river_biome_id"], "strong"
    if biome_id in COAST_BIOMES:
        return ["coast", "inland_water", "inland_lowland"], ["exact_coast_biome_id"], "strong"
    if biome_id in WETLAND_BIOMES:
        return ["coast", "inland_water", "river", "inland_lowland"], ["exact_wetland_biome_id"], "strong"

    continental_values: list[float] = []
    depth_values: list[float] = []
    erosion_values: list[float] = []
    for entry in entries:
        c0, c1 = parameter_range(entry, "continentalness")
        d0, d1 = parameter_range(entry, "depth")
        e0, e1 = parameter_range(entry, "erosion")
        if c0 is not None and c1 is not None:
            continental_values.extend([c0, c1])
        if d0 is not None and d1 is not None:
            depth_values.extend([d0, d1])
        if e0 is not None and e1 is not None:
            erosion_values.extend([e0, e1])

    classes = {"inland_lowland", "inland_highland"}
    evidence = ["terralith_parameter_point"]
    if continental_values and min(continental_values) < -0.45:
        classes.add("coast")
        classes.add("inland_water")
    if erosion_values and min(erosion_values) < -0.70:
        classes.add("mountain")
    if depth_values and max(depth_values) > 0.45:
        classes.add("mountain")
    confidence = "medium" if evidence else "weak"
    return sorted(classes), evidence, confidence


def build_hydrology_registry(region_entries: dict[str, list[dict]]) -> dict:
    entries_by_biome: dict[str, list[dict]] = {}
    regions_by_biome: dict[str, set[str]] = {}
    for region, entries in region_entries.items():
        for entry in entries:
            biome_id = str(entry.get("biome"))
            entries_by_biome.setdefault(biome_id, []).append(entry)
            regions_by_biome.setdefault(biome_id, set()).add(region)

    biome_rows = []
    for biome_id in sorted(entries_by_biome):
        allowed, evidence, confidence = classify_hydrology_from_evidence(biome_id, entries_by_biome[biome_id])
        biome_rows.append({
            "biome_id": biome_id,
            "allowed_hydrology_classes": allowed,
            "atlas_regions": sorted(regions_by_biome[biome_id]),
            "entry_count": len(entries_by_biome[biome_id]),
            "evidence": evidence,
            "confidence": confidence,
            "classification_method": "exact_id_or_parameter_data_not_name_tokens",
        })
    return {
        "version": 1,
        "generated_by": "scripts/generate-ascendant-atlas-worldgen.py",
        "status": "source_generated",
        "classification_rule": "Exact water IDs and Terralith climate parameter ranges are used; path/name token guessing is not accepted as evidence.",
        "hydrology_classes": [
            "deep_ocean",
            "ocean",
            "coast",
            "river",
            "inland_water",
            "inland_lowland",
            "inland_highland",
            "mountain",
        ],
        "biomes": biome_rows,
    }


def build_policy_files(region_entries: dict[str, list[dict]]) -> dict[str, dict]:
    return {
        "hydrology_policy": {
            "version": 1,
            "enabled": HYDROLOGY_FILTER_ENABLED,
            "model": "hydrology_first_biome_selection",
            "selection_order": [
                "sample_minecraft_climate_target",
                "classify_hydrology_from_continentalness_erosion_weirdness_and_query_y",
                "compute_continuous_domain_warped_region_weights",
                "filter_biome_candidates_by_hydrology_compatibility",
                "choose_nearest_compatible_terralith_parameter_point",
            ],
            "invalid_rules": [
                "ocean_biome_on_inland_highland_or_mountain",
                "land_biome_in_deep_ocean_without_island_or_coast_allowance",
                "water_wetland_biome_in_dry_land_first_context",
            ],
            "preserve": ["rivers", "oases", "mountain_lakes", "coastlines", "verdant_water_identity", "frozen_ocean_identity"],
        },
        "coastal_policy": {
            "version": 1,
            "coast_allowed_hydrology_classes": ["coast", "ocean", "deep_ocean"],
            "coast_allowed_pools": ["east", "north_east", "south_east", "north", "south", "outer"],
            "land_first_regions_require_physical_water_evidence": True,
            "ocean_biome_requires_low_query_y_or_ocean_hydrology": True,
        },
        "region_gradient_policy": {
            "version": 1,
            "mode": "continuous_region_weights",
            "hard_axis_boundaries": False,
            "world_radius_blocks": WORLD_RADIUS_BLOCKS,
            "outer_radius_blocks": OUTER_RADIUS_BLOCKS,
            "center_radius_blocks": CENTER_RADIUS_BLOCKS,
            "transition_width_blocks": TRANSITION_WIDTH_BLOCKS,
            "minimum_secondary_region_weight": MINIMUM_SECONDARY_REGION_WEIGHT,
            "regions": sorted(region_entries),
        },
        "transition_adjacency": {
            "version": 1,
            "mode": "adjacent_weight_blend",
            "allowed_neighbors": {
                "center": ["north", "south", "east", "west", "north_east", "north_west", "south_east", "south_west"],
                "north": ["center", "north_east", "north_west", "east", "west"],
                "south": ["center", "south_east", "south_west", "east", "west"],
                "east": ["center", "north_east", "south_east", "north", "south"],
                "west": ["center", "north_west", "south_west", "north", "south"],
                "south_east": ["south", "east", "center"],
                "south_west": ["south", "west", "center"],
                "north_east": ["north", "east", "center"],
                "north_west": ["north", "west", "center"],
            },
        },
        "domain_warp_policy": {
            "version": 1,
            "enabled": True,
            "scale_blocks": DOMAIN_WARP_SCALE_BLOCKS,
            "strength_blocks": DOMAIN_WARP_STRENGTH_BLOCKS,
            "purpose": "break visible straight Atlas sector lines while keeping deterministic region identity",
        },
    }


def placeholder_report(name: str) -> dict:
    return {
        "version": 1,
        "generated_by": "scripts/generate-ascendant-atlas-worldgen.py",
        "status": "pending_in_game_command",
        "report": name,
        "note": "Run the matching /ascatlas command in a fresh generated world to replace this source placeholder.",
    }


def build_dimension() -> tuple[dict, dict]:
    terralith_dimension = read_terralith_overworld()
    base_source = terralith_dimension.get("generator", {}).get("biome_source", {})
    all_entries = base_source.get("biomes", [])
    if not isinstance(all_entries, list) or len(all_entries) < 500:
        raise RuntimeError("Terralith Overworld biome source did not expose the expected explicit biome table.")

    region_entries = {
        label: selected_entries(all_entries, ids, label)
        for label, ids in REGION_BIOMES.items()
    }

    biome_source = {
        "type": "ascendant_atlas_regions:regional_multi_noise",
        "world_radius_blocks": WORLD_RADIUS_BLOCKS,
        "outer_radius_blocks": OUTER_RADIUS_BLOCKS,
        "center_radius_blocks": CENTER_RADIUS_BLOCKS,
        "axis_dominance_ratio": AXIS_DOMINANCE_RATIO,
        "transition_width_blocks": TRANSITION_WIDTH_BLOCKS,
        "domain_warp_scale_blocks": DOMAIN_WARP_SCALE_BLOCKS,
        "domain_warp_strength_blocks": DOMAIN_WARP_STRENGTH_BLOCKS,
        "minimum_secondary_region_weight": MINIMUM_SECONDARY_REGION_WEIGHT,
        "hydrology_filter_enabled": HYDROLOGY_FILTER_ENABLED,
    }
    for label in [
        "center",
        "north",
        "south",
        "east",
        "west",
        "north_east",
        "north_west",
        "south_east",
        "south_west",
        "outer",
    ]:
        biome_source[label] = region_entries[label]

    dimension = {
        "type": "minecraft:overworld",
        "generator": {
            "type": "minecraft:noise",
            "settings": "minecraft:overworld",
            "biome_source": biome_source,
        },
    }

    manifest = {
        "version": 1,
        "status": "disabled_random_terralith_tectonic_baseline",
        "helper_mod_id": "ascendant_atlas_regions",
        "biome_source_type": "ascendant_atlas_regions:regional_multi_noise",
        "dimension_override": "data/minecraft/dimension/overworld.json",
        "worldgen_override_enabled": WORLDGEN_OVERRIDE_ENABLED,
        "active_worldgen_mode": "random_terralith_tectonic_baseline",
        "terrain_settings": "minecraft:overworld",
        "world_radius_blocks": WORLD_RADIUS_BLOCKS,
        "outer_radius_blocks": OUTER_RADIUS_BLOCKS,
        "center_radius_blocks": CENTER_RADIUS_BLOCKS,
        "axis_dominance_ratio": AXIS_DOMINANCE_RATIO,
        "transition_width_blocks": TRANSITION_WIDTH_BLOCKS,
        "domain_warp_scale_blocks": DOMAIN_WARP_SCALE_BLOCKS,
        "domain_warp_strength_blocks": DOMAIN_WARP_STRENGTH_BLOCKS,
        "minimum_secondary_region_weight": MINIMUM_SECONDARY_REGION_WEIGHT,
        "hydrology_filter_enabled": HYDROLOGY_FILTER_ENABLED,
        "source_biome_entries": len(all_entries),
        "regions": {
            label: {
                "entry_count": len(entries),
                "unique_biome_count": len(unique_biomes(entries)),
                "surface_excluded_cave_biome_count": len(
                    sorted(biome_id for biome_id in REGION_BIOMES[label] if is_cave_only_biome(biome_id))
                ),
                "biomes": unique_biomes(entries),
            }
            for label, entries in region_entries.items()
        },
        "notes": [
            "The coordinate-aware Overworld override is currently disabled by config/ascendant_atlas/worldgen_override_policy.json.",
            "Normal random Terralith/Tectonic terrain is the active baseline while structure and road tuning proceed.",
            "Biome tables are selected from Terralith's explicit Overworld multi-noise source.",
            "The helper mod chooses a table by Atlas X/Z region, then delegates to normal multi-noise selection inside that table.",
            "Cave-only biome IDs are excluded from Atlas surface pools because surface validation proved they can appear at generated terrain height.",
            "The shared outer table is intentionally delayed until 50000 blocks so terrain visible beyond the 30000-block square world border keeps directional identity, including corners.",
            "The helper applies a north/south climate gradient: north trends cold to frozen, while south trends warm coast to arid land.",
            "The helper stretches the primary climate gradient across 12000 blocks so climate shifts read as travel-scale transitions instead of abrupt bands near spawn.",
            "The south-east pool is land-first transition terrain. It intentionally excludes ocean biome IDs so jungle/badlands land is not labelled as ocean and does not invite ocean-only structures.",
            "The datapack overrides minecraft:overworld/continents with a small ascendant_atlas_regions:atlas_land_bias density function so Tectonic naturally favors land in Sunreach/Stoneback without post-generation block filling.",
            "The dimension keeps minecraft:overworld terrain settings so Tectonic's noise-settings override remains in control of terrain shape.",
        ],
    }
    policies = build_policy_files(region_entries)
    hydrology_registry = build_hydrology_registry(region_entries)
    manifest["generated_policy_files"] = sorted(policies)
    manifest["generated_registry_files"] = ["biome_hydrology_registry"]
    return dimension, manifest, policies, hydrology_registry


def main() -> None:
    dimension, manifest, policies, hydrology_registry = build_dimension()

    if WORLDGEN_OVERRIDE_ENABLED:
        for pack_root in OUTPUT_PACKS:
            write_json(pack_root / "data" / "minecraft" / "dimension" / "overworld.json", dimension)
            write_json(
                pack_root / "data" / "minecraft" / "worldgen" / "density_function" / "overworld" / "continents.json",
                ATLAS_LAND_BIAS_DENSITY,
            )
    else:
        manifest["disabled_influence_files"] = [
            str((pack_root / "data" / "minecraft" / "dimension" / "overworld.json").relative_to(ROOT)).replace("\\", "/")
            for pack_root in OUTPUT_PACKS
        ] + [
            str((pack_root / "data" / "minecraft" / "worldgen" / "density_function" / "overworld" / "continents.json").relative_to(ROOT)).replace("\\", "/")
            for pack_root in OUTPUT_PACKS
        ]

    write_json(ATLAS_CONFIG / "worldgen_regions.json", manifest)
    write_json(ATLAS_CONFIG / "biome_hydrology_registry.json", hydrology_registry)
    write_json(ATLAS_CONFIG / "hydrology_policy.json", policies["hydrology_policy"])
    write_json(ATLAS_CONFIG / "coastal_policy.json", policies["coastal_policy"])
    write_json(ATLAS_CONFIG / "region_gradient_policy.json", policies["region_gradient_policy"])
    write_json(ATLAS_CONFIG / "transition_adjacency.json", policies["transition_adjacency"])
    write_json(ATLAS_CONFIG / "domain_warp_policy.json", policies["domain_warp_policy"])
    report_dir = ATLAS_CONFIG / "reports"
    write_json(report_dir / "hydrology_grid_latest.json", placeholder_report("hydrology_grid_latest.json"))
    write_json(report_dir / "region_gradient_grid_latest.json", placeholder_report("region_gradient_grid_latest.json"))
    write_json(report_dir / "transition_transects_latest.json", placeholder_report("transition_transects_latest.json"))
    write_json(report_dir / "invalid_ocean_selections_latest.json", placeholder_report("invalid_ocean_selections_latest.json"))
    print("Generated Ascendant Atlas worldgen audit data.")
    if not WORLDGEN_OVERRIDE_ENABLED:
        print("- Atlas Overworld biome-source and land-bias overrides are disabled; random Tectonic/Terralith generation remains active.")
    for label, info in manifest["regions"].items():
        print(f"- {label}: {info['entry_count']} entries / {info['unique_biome_count']} biomes")


if __name__ == "__main__":
    main()
