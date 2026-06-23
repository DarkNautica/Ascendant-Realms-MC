#!/usr/bin/env python3
"""Generate Ascendant travel-network audit docs and policy JSON."""

from __future__ import annotations

import json
import pathlib
import re
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
ACTIVE_INSTANCE = pathlib.Path(
    r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)"
)
DOCS = ROOT / "docs"
CONFIG = ROOT / "config" / "ascendant_travel"
AUDIT_PATH = DOCS / "generated" / "worldgen_content_audit.json"
WATER_REVIEW_PATH = ROOT / "config" / "ascendant_atlas" / "reports" / "water_surface_samples_latest.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def read_json(path: pathlib.Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def preview(values: list[str], limit: int = 8) -> str:
    values = [value for value in values if value]
    if len(values) <= limit:
        return ", ".join(f"`{value}`" for value in values)
    shown = ", ".join(f"`{value}`" for value in values[:limit])
    return f"{shown}, ... ({len(values)} total)"


def parse_packwiz_filename(toml_path: pathlib.Path) -> str | None:
    text = read_text(toml_path)
    match = re.search(r'(?m)^filename\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else None


def active_jar_from_mod_toml(toml_name: str) -> pathlib.Path | None:
    filename = parse_packwiz_filename(ROOT / "mods" / toml_name)
    if not filename:
        return None
    candidates = [
        ACTIVE_INSTANCE / "mods" / filename,
        ROOT / "mods" / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def jar_scan(jar_path: pathlib.Path | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": str(jar_path) if jar_path else None,
        "exists": bool(jar_path and jar_path.exists()),
        "is_zip": False,
        "worldgen_files": 0,
        "structure_json_files": 0,
        "structure_set_json_files": 0,
        "template_pool_json_files": 0,
        "structure_nbt_files": 0,
        "road_or_path_files": 0,
        "bridge_files": 0,
        "river_or_crossing_files": 0,
        "dock_or_port_files": 0,
        "biome_tag_files": [],
        "examples": {},
    }
    if not jar_path or not jar_path.exists() or not zipfile.is_zipfile(jar_path):
        return result

    result["is_zip"] = True
    with zipfile.ZipFile(jar_path) as jar:
        names = jar.namelist()

    lower_names = [(name, name.lower()) for name in names]
    data_names = [(name, lower) for name, lower in lower_names if lower.startswith("data/") and not lower.endswith("/")]
    worldgen = [name for name, lower in data_names if "/worldgen/" in lower]
    structures = [name for name, lower in data_names if "/worldgen/structure/" in lower and lower.endswith(".json")]
    structure_sets = [
        name for name, lower in data_names if "/worldgen/structure_set/" in lower and lower.endswith(".json")
    ]
    template_pools = [
        name for name, lower in data_names if "/worldgen/template_pool/" in lower and lower.endswith(".json")
    ]
    nbt = [name for name, lower in data_names if "/structures/" in lower and lower.endswith(".nbt")]
    road_path = [
        name
        for name, lower in data_names
        if any(token in lower for token in ("road", "path", "street", "crossroad"))
    ]
    bridge = [name for name, lower in data_names if "bridge" in lower]
    river_crossing = [
        name for name, lower in data_names if any(token in lower for token in ("river", "crossing", "ford"))
    ]
    dock_port = [
        name for name, lower in data_names if any(token in lower for token in ("dock", "port", "harbor", "pier"))
    ]
    biome_tags = [
        name
        for name, lower in data_names
        if "/tags/worldgen/biome/" in lower and lower.endswith(".json")
    ]

    result.update(
        {
            "worldgen_files": len(worldgen),
            "structure_json_files": len(structures),
            "structure_set_json_files": len(structure_sets),
            "template_pool_json_files": len(template_pools),
            "structure_nbt_files": len(nbt),
            "road_or_path_files": len(road_path),
            "bridge_files": len(bridge),
            "river_or_crossing_files": len(river_crossing),
            "dock_or_port_files": len(dock_port),
            "biome_tag_files": biome_tags[:30],
            "examples": {
                "road_or_path": road_path[:12],
                "bridge": bridge[:12],
                "river_or_crossing": river_crossing[:12],
                "dock_or_port": dock_port[:12],
                "worldgen": worldgen[:12],
            },
        }
    )
    return result


def top_blocks(entry: dict[str, Any]) -> dict[str, int]:
    profile = entry.get("block_profile") or {}
    blocks = profile.get("top_blocks") or {}
    return {str(key): int(value) for key, value in blocks.items() if isinstance(value, int)}


def block_count(blocks: dict[str, int], tokens: tuple[str, ...]) -> int:
    total = 0
    for block_id, count in blocks.items():
        low = block_id.lower()
        if any(token in low for token in tokens):
            total += count
    return total


def first_structure_set(entry: dict[str, Any]) -> dict[str, Any]:
    sets = entry.get("structure_sets") or []
    if sets and isinstance(sets[0], dict):
        return sets[0]
    return {}


def source_family(structure_id: str, entry: dict[str, Any]) -> str:
    source = str(entry.get("source") or "")
    if structure_id.startswith("minecraft:village_"):
        return "minecraft_vanilla_villages"
    if structure_id.startswith("integrated_villages:"):
        return "integrated_villages"
    if structure_id.startswith("towns_and_towers:"):
        return "towns_and_towers"
    if structure_id.startswith("mvs:"):
        return "moogs_voyager_structures"
    if structure_id.startswith("idas:"):
        return "integrated_dungeons_and_structures"
    if structure_id.startswith("structory:"):
        return "structory"
    if structure_id.startswith("humancompanions:"):
        return "human_companions"
    if structure_id.startswith("supplementaries:"):
        return "supplementaries"
    return source.replace(".jar", "") or "unknown"


def analyze_audit(audit: dict[str, Any]) -> dict[str, Any]:
    structures = audit.get("structures", {})
    path_rows: list[dict[str, Any]] = []
    water_rows: list[dict[str, Any]] = []
    family_counts: Counter[str] = Counter()
    set_spacing: dict[str, dict[str, Any]] = {}

    for structure_id, entry in structures.items():
        if not isinstance(entry, dict):
            continue
        if str(structure_id).startswith(("ascendant_atlas:", "ascendant_guild:")):
            continue
        if str(entry.get("source") or "").startswith(
            (
                "active-instance-openloader:ascendant_realms_atlas",
                "active-instance-openloader:ascendant_realms_guild",
            )
        ):
            continue
        blocks = top_blocks(entry)
        path_count = block_count(blocks, ("path", "road", "street"))
        water_count = block_count(blocks, ("water",))
        start_pool = str(entry.get("start_pool") or "")
        searchable = f"{structure_id} {start_pool}".lower()
        travel_name_hit = any(
            token in searchable for token in ("path", "road", "street", "bridge", "dock", "river", "crossing", "port")
        )
        if path_count or travel_name_hit:
            family = source_family(str(structure_id), entry)
            family_counts[family] += 1
            set_entry = first_structure_set(entry)
            if set_entry.get("structure_set"):
                set_spacing[str(set_entry["structure_set"])] = {
                    "structure_set": set_entry.get("structure_set"),
                    "spacing": set_entry.get("spacing"),
                    "separation": set_entry.get("separation"),
                    "salt": set_entry.get("salt"),
                    "source": set_entry.get("source"),
                }
            path_rows.append(
                {
                    "structure_id": str(structure_id),
                    "source_mod": str(entry.get("source") or "unknown"),
                    "family": family,
                    "start_pool": start_pool or None,
                    "path_like_block_count": path_count,
                    "water_block_count": water_count,
                    "structure_sets": entry.get("structure_sets") or [],
                    "recommendation": structure_path_recommendation(str(structure_id), family, path_count, water_count),
                    "known_failure_types": structure_path_failures(str(structure_id), family, path_count, water_count),
                }
            )
        elif water_count:
            water_rows.append(
                {
                    "structure_id": str(structure_id),
                    "source_mod": str(entry.get("source") or "unknown"),
                    "start_pool": start_pool or None,
                    "water_block_count": water_count,
                    "structure_sets": entry.get("structure_sets") or [],
                }
            )

    path_rows.sort(key=lambda row: (row["path_like_block_count"], row["water_block_count"]), reverse=True)
    water_rows.sort(key=lambda row: row["water_block_count"], reverse=True)
    return {
        "path_rows": path_rows,
        "water_rows": water_rows,
        "family_counts": dict(family_counts),
        "set_spacing": sorted(set_spacing.values(), key=lambda row: str(row.get("structure_set"))),
    }


def structure_path_recommendation(structure_id: str, family: str, path_count: int, water_count: int) -> str:
    if structure_id.startswith("minecraft:village_"):
        return "keep_manual_review"
    if family == "towns_and_towers":
        return "keep_but_manual_review_before_settlement_work"
    if family == "integrated_villages":
        return "keep_but_review_paths_docks_and_local_bridges"
    if structure_id == "mvs:paths":
        return "manual_review_for_roads_to_nowhere"
    if path_count >= 100:
        return "manual_review_high_path_volume"
    if water_count:
        return "manual_review_water_edge_behavior"
    return "keep_observe_only"


def structure_path_failures(structure_id: str, family: str, path_count: int, water_count: int) -> list[str]:
    failures: list[str] = []
    if family in {"minecraft_vanilla_villages", "integrated_villages", "towns_and_towers"}:
        failures.extend(["slope_behavior_unknown", "bridge_absence_risk"])
    if path_count >= 100:
        failures.append("high_template_path_volume")
    if water_count:
        failures.append("water_edge_or_crossing_risk")
    if structure_id == "mvs:paths":
        failures.extend(["roads_to_nowhere_risk", "purpose_not_connected_to_settlements"])
    return sorted(set(failures))


def water_summary() -> dict[str, Any]:
    data = read_json(WATER_REVIEW_PATH, {})
    summary = data.get("summary", {}) if isinstance(data, dict) else {}
    samples = data.get("samples", []) if isinstance(data, dict) else []
    by_classification: Counter[str] = Counter()
    by_region: Counter[str] = Counter()
    ocean_leak_samples: list[dict[str, Any]] = []
    acceptable_crossing_samples: list[dict[str, Any]] = []
    if isinstance(samples, list):
        for sample in samples:
            if not isinstance(sample, dict):
                continue
            classification = str(sample.get("classification") or "unclassified")
            region = str(sample.get("region") or sample.get("atlas_region") or "unknown")
            by_classification[classification] += 1
            by_region[region] += 1
            compact = {
                "x": sample.get("x"),
                "z": sample.get("z"),
                "region": region,
                "classification": classification,
                "biome": sample.get("actual_biome_id") or sample.get("actual_biome"),
                "surface_y": sample.get("surface_y"),
                "suggested_teleport": sample.get("suggested_teleport"),
            }
            if classification == "ocean_leak":
                ocean_leak_samples.append(compact)
            elif classification in {"acceptable_river", "acceptable_oasis", "acceptable_mountain_lake", "acceptable_coastline"}:
                acceptable_crossing_samples.append(compact)

    return {
        "source": str(WATER_REVIEW_PATH.relative_to(ROOT)),
        "summary": summary,
        "by_classification": dict(sorted(by_classification.items())),
        "by_region": dict(sorted(by_region.items())),
        "ocean_leak_samples": ocean_leak_samples,
        "acceptable_crossing_samples": acceptable_crossing_samples[:20],
    }


def make_policies(
    generated_at: str,
    audit_info: dict[str, Any],
    jar_info: dict[str, dict[str, Any]],
    water: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    path_rows = audit_info["path_rows"]

    road_sources = [
        {
            "source_id": "minecraft:village_paths",
            "mod_source": "Minecraft vanilla villages",
            "config_path": None,
            "structure_ids_or_templates": [
                row["structure_id"] for row in path_rows if row["structure_id"].startswith("minecraft:village_")
            ],
            "biome_tags": "vanilla village biome tags",
            "spacing_density": "minecraft:villages spacing 34 / separation 8 from generated audit",
            "slope_behavior": "template and jigsaw terrain adaptation; not Atlas-aware",
            "bridge_behavior": "not a reliable road bridge layer",
            "known_failure_types": ["bridge_absence_risk", "slope_behavior_unknown", "water_edge_or_crossing_risk"],
            "recommendation": "keep_manual_review",
        },
        {
            "source_id": "integrated_villages:path_networks",
            "mod_source": "Integrated Villages",
            "config_path": "config/integrated_villages-forge-1_20.toml",
            "structure_ids_or_templates": [
                row["structure_id"] for row in path_rows if row["family"] == "integrated_villages"
            ],
            "biome_tags": "integrated_villages biome tags plus OpenLoader repairs",
            "spacing_density": "regular_villages spacing 64 / separation 32 from OpenLoader override",
            "slope_behavior": "template-local paths; final slope handling needs in-game field review",
            "bridge_behavior": "mossy_mounds has bridge templates; pirate_village has docks; not a general road network",
            "known_failure_types": ["bridge_absence_risk", "dock_water_edge_risk", "slope_behavior_unknown"],
            "recommendation": "keep_but_review_paths_docks_and_local_bridges",
        },
        {
            "source_id": "towns_and_towers:streets",
            "mod_source": "Towns and Towers",
            "config_path": "config/towns_and_towers/structure_rarity_new.json5",
            "structure_ids_or_templates": [
                row["structure_id"] for row in path_rows if row["family"] == "towns_and_towers"
            ],
            "biome_tags": "Towns and Towers structure biome tags",
            "spacing_density": "towns 52/24, towers 48/22, other 36/14 from active config",
            "slope_behavior": "village street templates; no terrain-aware Atlas road correction",
            "bridge_behavior": "no direct bridge/dock template evidence found in jar scan",
            "known_failure_types": ["bridge_absence_risk", "slope_behavior_unknown", "village_town_overlap_risk"],
            "recommendation": "keep_but_manual_review_before_settlement_work",
        },
        {
            "source_id": "mvs:paths",
            "mod_source": "Moog's Voyager Structures",
            "config_path": None,
            "structure_ids_or_templates": ["mvs:paths"],
            "biome_tags": "MVS structure biome tags",
            "spacing_density": "spacing 35 / separation 12 from generated audit",
            "slope_behavior": "small path landmark; terrain purpose unknown",
            "bridge_behavior": "not a river crossing system",
            "known_failure_types": ["roads_to_nowhere_risk", "purpose_not_connected_to_settlements"],
            "recommendation": "manual_review_for_roads_to_nowhere",
        },
        {
            "source_id": "supplementaries:way_sign",
            "mod_source": "Supplementaries",
            "config_path": None,
            "structure_ids_or_templates": ["supplementaries:way_sign"],
            "biome_tags": "Supplementaries worldgen tags",
            "spacing_density": "spacing 19 / separation 10 from structure density audit",
            "slope_behavior": "not a road, but a travel marker that should not imply missing routes",
            "bridge_behavior": "none",
            "known_failure_types": ["travel_marker_without_route_context"],
            "recommendation": "keep_observe_only",
        },
        {
            "source_id": "template_local_paths:idas_structory_humancompanions_moog",
            "mod_source": "IDAS, Structory, Human Companions, Moog structures",
            "config_path": None,
            "structure_ids_or_templates": [
                row["structure_id"]
                for row in path_rows
                if row["family"]
                in {
                    "integrated_dungeons_and_structures",
                    "structory",
                    "human_companions",
                    "moogs_voyager_structures",
                }
            ][:60],
            "biome_tags": "per-mod structure biome tags",
            "spacing_density": "varies by structure set; see template_local_path_risks",
            "slope_behavior": "template-local paths/grounds only",
            "bridge_behavior": "not a connected bridge system",
            "known_failure_types": ["local_path_edge_risk", "slope_behavior_unknown"],
            "recommendation": "keep_observe_only",
        },
    ]

    bridge_sources = [
        {
            "source_id": "yungsbridges:bridges",
            "mod_source": "YUNG's Bridges",
            "config_path": "mods/yungs-bridges.pw.toml",
            "structure_ids_or_templates": jar_info["yungs_bridges"].get("examples", {}).get("worldgen", []),
            "biome_tags": jar_info["yungs_bridges"].get("biome_tag_files", []),
            "spacing_density": "code-driven or non-json; no structure_set JSON visible in jar scan",
            "slope_behavior": "unknown from datapack JSON; requires live bridge field review",
            "bridge_behavior": "standalone world bridge landmarks, not linked to Atlas road routing",
            "known_failure_types": ["not_linked_to_road_network", "slope_behavior_unknown", "water_crossing_strategy_unlinked"],
            "recommendation": "keep_manual_review",
        },
        {
            "source_id": "macaws_bridges:palette",
            "mod_source": "Macaw's Bridges",
            "config_path": "mods/macaws-bridges.pw.toml",
            "structure_ids_or_templates": [],
            "biome_tags": [],
            "spacing_density": "no worldgen files detected; palette only",
            "slope_behavior": "not applicable",
            "bridge_behavior": "build palette for future authored/helper bridge pieces",
            "known_failure_types": [],
            "recommendation": "keep_palette_only",
        },
        {
            "source_id": "integrated_villages:mossy_mounds_bridge",
            "mod_source": "Integrated Villages",
            "config_path": "config/integrated_villages-forge-1_20.toml",
            "structure_ids_or_templates": [
                item for item in jar_info["integrated_villages"].get("examples", {}).get("bridge", [])
            ],
            "biome_tags": "Integrated Villages mossy_mounds tags",
            "spacing_density": "inherits integrated_villages:regular_villages 64/32",
            "slope_behavior": "template-local; field review needed",
            "bridge_behavior": "local village bridge, not global road crossing",
            "known_failure_types": ["local_only_bridge_strategy", "slope_behavior_unknown"],
            "recommendation": "keep_manual_review",
        },
        {
            "source_id": "integrated_villages:pirate_village_docks",
            "mod_source": "Integrated Villages",
            "config_path": "config/integrated_villages-forge-1_20.toml",
            "structure_ids_or_templates": [
                item for item in jar_info["integrated_villages"].get("examples", {}).get("dock_or_port", [])
            ],
            "biome_tags": "Integrated Villages pirate/coastal tags",
            "spacing_density": "inherits integrated village spacing",
            "slope_behavior": "coastal template behavior; field review needed",
            "bridge_behavior": "dock behavior only",
            "known_failure_types": ["dock_water_edge_risk"],
            "recommendation": "keep_manual_review",
        },
    ]

    road_validation = {
        "active_road_bridge_generators_without_policy": [],
        "road_sources_with_known_cliff_or_floating_failures": [
            source["source_id"]
            for source in road_sources
            if any("slope" in failure or "bridge_absence" in failure for failure in source["known_failure_types"])
        ],
        "road_sources_with_roads_to_nowhere_risk": [
            source["source_id"]
            for source in road_sources
            if any("nowhere" in failure or "purpose" in failure for failure in source["known_failure_types"])
        ],
        "bridge_sources_without_crossing_strategy": [
            "yungsbridges:bridges",
            "integrated_villages:mossy_mounds_bridge",
        ],
        "travel_network_docs_missing": [],
        "live_generation_changes_enabled": [],
    }

    road_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "reconnaissance_only_no_worldgen_changes",
        "scope": {
            "adds_roads": False,
            "adds_bridges": False,
            "injects_villages": False,
            "changes_live_generation": False,
        },
        "summary": {
            "road_sources": len(road_sources),
            "path_or_travel_structures_detected": len(path_rows),
            "path_structure_families": audit_info["family_counts"],
            "note": "Road evidence is mostly template-local village/path content, not a connected Atlas travel network.",
        },
        "road_sources": road_sources,
        "template_local_path_risks": path_rows[:80],
        "structure_set_spacing_evidence": audit_info["set_spacing"],
        "validation": road_validation,
    }

    bridge_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "reconnaissance_only_no_worldgen_changes",
        "scope": {
            "adds_bridges": False,
            "changes_live_generation": False,
            "uses_macaws_as_palette_only": True,
        },
        "summary": {
            "bridge_sources": len(bridge_sources),
            "yungs_bridge_worldgen_files": jar_info["yungs_bridges"].get("worldgen_files"),
            "macaws_worldgen_files": jar_info["macaws_bridges"].get("worldgen_files"),
            "integrated_villages_bridge_files": jar_info["integrated_villages"].get("bridge_files"),
            "integrated_villages_dock_files": jar_info["integrated_villages"].get("dock_or_port_files"),
            "towns_and_towers_bridge_files": jar_info["towns_and_towers"].get("bridge_files"),
        },
        "bridge_sources": bridge_sources,
        "jar_evidence": jar_info,
        "validation": {
            "active_road_bridge_generators_without_policy": [],
            "bridge_sources_without_crossing_strategy": road_validation["bridge_sources_without_crossing_strategy"],
            "live_generation_changes_enabled": [],
        },
    }

    crossing_rules = [
        {
            "region": "hearthlands",
            "strategy": "safe low-grade roads; short timber or stone bridges over small rivers; avoid dangerous cliffs near spawn",
        },
        {
            "region": "sunreach",
            "strategy": "caravan roads, dry washes, rare oases, and small river bridges; avoid ocean-like basins as road anchors",
        },
        {
            "region": "frostmarch",
            "strategy": "snow roads, frozen crossings, mountain passes, and sturdy cold-weather bridges",
        },
        {
            "region": "stoneback_highlands",
            "strategy": "passes, switchbacks, tunnels, mountain bridges, and supported roads instead of straight cliff paths",
        },
        {
            "region": "verdant_coast",
            "strategy": "river bridges, docks, swamp boardwalks, port roads, and coastal crossings",
        },
        {
            "region": "outer_rim",
            "strategy": "dangerous, sparse routes; ruins, broken bridges, and difficult crossings are acceptable when intentional",
        },
    ]

    river_crossing_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "reconnaissance_only_no_worldgen_changes",
        "water_review_source": water["source"],
        "water_review_summary": water["summary"],
        "water_samples_by_classification": water["by_classification"],
        "water_samples_by_region": water["by_region"],
        "confirmed_ocean_leaks": water["ocean_leak_samples"],
        "acceptable_crossing_examples": water["acceptable_crossing_samples"],
        "rules": crossing_rules,
        "bridge_source_linkage": [
            {
                "source_id": "yungsbridges:bridges",
                "linkage_status": "standalone_landmark_not_route_linked",
                "action": "manual_review_before_using_as_travel_network_solution",
            },
            {
                "source_id": "macaws_bridges:palette",
                "linkage_status": "palette_for_future_authored_or_helper_bridge_pieces",
                "action": "keep_palette_only",
            },
            {
                "source_id": "integrated_villages:mossy_mounds_bridge",
                "linkage_status": "local_template_bridge_only",
                "action": "field_review_bridge_fit",
            },
        ],
        "validation": {
            "bridge_sources_without_crossing_strategy": road_validation["bridge_sources_without_crossing_strategy"],
            "ocean_leak_samples_blocking_route_design": len(water["ocean_leak_samples"]),
            "live_generation_changes_enabled": [],
        },
    }

    candidates = {
        "version": 1,
        "generated_at": generated_at,
        "status": "disabled_review_only_no_live_generation_changes",
        "candidates": [
            {
                "candidate_id": "field_sample_road_water_crossings",
                "type": "manual_validation",
                "enabled": False,
                "description": "Record coordinates where village or structure paths cross rivers, ravines, cliffs, or ocean-leak basins.",
                "depends_on": ["Atlas land/water coherence signoff"],
            },
            {
                "candidate_id": "ascendant_route_bridge_helper",
                "type": "future_helper_module",
                "enabled": False,
                "description": "Terrain-aware route helper that detects road/water/cliff crossings after generation and substitutes bridge/support pieces.",
                "depends_on": ["terrain validation", "settlement policy", "bridge palette decisions"],
            },
            {
                "candidate_id": "region_road_material_palettes",
                "type": "future_structure_palette",
                "enabled": False,
                "description": "Define Crownlands, Frostmarch, Sunreach, Verdant, and Stoneback road material palettes before authoring roads.",
                "depends_on": ["manual visual pass"],
            },
            {
                "candidate_id": "towns_and_towers_bridge_gap_review",
                "type": "manual_review",
                "enabled": False,
                "description": "Inspect Towns and Towers village streets for bridge gaps, cliff cuts, and island settlements in fresh terrain.",
                "depends_on": ["village injection remains untouched"],
            },
            {
                "candidate_id": "yungs_bridges_route_linkage_review",
                "type": "manual_review",
                "enabled": False,
                "description": "Field-check YUNG's Bridges as scenic landmarks and decide whether any should become route anchors later.",
                "depends_on": ["fresh-world bridge coordinates"],
            },
        ],
        "explicitly_not_enabled": [
            "new road generation",
            "new bridge generation",
            "village pool injection",
            "road density changes",
            "structure set rewrites",
        ],
        "validation": {
            "candidate_rewrites_enabled": [],
            "live_generation_changes_enabled": [],
        },
    }

    return road_policy, bridge_policy, river_crossing_policy, candidates


def make_docs(
    generated_at: str,
    road_policy: dict[str, Any],
    bridge_policy: dict[str, Any],
    crossing_policy: dict[str, Any],
    candidates: dict[str, Any],
) -> tuple[str, str, str]:
    road_sources = road_policy["road_sources"]
    bridge_sources = bridge_policy["bridge_sources"]
    path_rows = road_policy["template_local_path_risks"]
    validation = road_policy["validation"]
    water_summary_data = crossing_policy["water_review_summary"]
    water_by_class = crossing_policy["water_samples_by_classification"]

    audit_rows = [
        [
            f"`{source['source_id']}`",
            source["mod_source"],
            source["config_path"] or "none",
            source["spacing_density"],
            source["slope_behavior"],
            source["bridge_behavior"],
            source["recommendation"],
        ]
        for source in road_sources
    ]
    bridge_rows = [
        [
            f"`{source['source_id']}`",
            source["mod_source"],
            source["config_path"] or "none",
            source["spacing_density"],
            source["bridge_behavior"],
            source["recommendation"],
        ]
        for source in bridge_sources
    ]
    top_path_rows = [
        [
            f"`{row['structure_id']}`",
            row["source_mod"],
            row["path_like_block_count"],
            row["water_block_count"],
            row["recommendation"],
        ]
        for row in path_rows[:25]
    ]
    crossing_rows = [
        [f"`{rule['region']}`", rule["strategy"]]
        for rule in crossing_policy["rules"]
    ]

    audit_doc = f"""
# Ascendant Travel Network Audit

Generated: {generated_at}

Status: reconnaissance only. No roads, bridges, village pools, structure sets, or active generation configs were changed.

## Summary

- Road/path sources covered: {len(road_sources)}
- Bridge sources covered: {len(bridge_sources)}
- Path or travel-like structures detected in the generated worldgen audit: {road_policy['summary']['path_or_travel_structures_detected']}
- Confirmed south/west ocean-leak water samples still blocking travel signoff: {len(crossing_policy['confirmed_ocean_leaks'])}
- Live generation changes enabled by this pass: 0

The current pack does not have one intentional connected travel network yet. It has village-local paths, template-local grounds, standalone bridge landmarks, way signs, and a bridge block palette. That is enough raw material, but not enough authorship. Future roads should wait until Atlas terrain-water coherence is signed off.

## Road And Path Sources

{md_table(['Source', 'Mod/source', 'Config path', 'Spacing/density', 'Slope behavior', 'Bridge behavior', 'Recommendation'], audit_rows)}

## Bridge Sources

{md_table(['Source', 'Mod/source', 'Config path', 'Spacing/density', 'Bridge behavior', 'Recommendation'], bridge_rows)}

## Template-Local Path Risks

These are the highest path-like structures from `docs/generated/worldgen_content_audit.json`. A path count does not prove a broken road; it marks field-review priority.

{md_table(['Structure', 'Source', 'Path-like blocks', 'Water blocks', 'Recommendation'], top_path_rows)}

## River And Crossing Context

Water review remains relevant to travel design because bad roads can look even worse when placed on the confirmed south/west ocean-leak basins.

{md_table(['Classification', 'Count'], [[f'`{key}`', value] for key, value in sorted(water_by_class.items())])}

Manual water review status from `config/ascendant_atlas/reports/water_surface_samples_latest.json`:

- Total water samples: {water_summary_data.get('total_water_samples', 'unknown')}
- South/west target-region water samples: {water_summary_data.get('target_south_west_water_samples', 'unknown')}
- Manually reviewed target samples: {water_summary_data.get('manual_reviewed_target_water_samples', 'unknown')}
- Visually confirmed ocean leaks: {water_summary_data.get('visually_confirmed_ocean_leak_samples', len(crossing_policy['confirmed_ocean_leaks']))}

## Design Rule Preview

{md_table(['Region', 'Travel strategy'], crossing_rows)}

## Validation Warnings To Keep

- Road sources with unknown cliff/slope or bridge-absence risk: {preview(validation['road_sources_with_known_cliff_or_floating_failures'])}
- Road sources with route-purpose risk: {preview(validation['road_sources_with_roads_to_nowhere_risk'])}
- Bridge sources not yet linked to a crossing strategy: {preview(validation['bridge_sources_without_crossing_strategy'])}

## No-Change Confirmation

This pass created documentation and `config/ascendant_travel/*.json` policy files only. It did not add roads, add bridges, inject villages, enable candidates, or rewrite live structure density.
"""

    failures = [
        {
            "id": "atlas_south_west_ocean_leak_blocks_travel_signoff",
            "severity": "terrain_blocker",
            "evidence": f"{len(crossing_policy['confirmed_ocean_leaks'])} confirmed ocean-leak water samples remain in south/west target regions.",
            "recommendation": "Resolve Atlas land/water coherence before designing permanent roads through Sunreach or Stoneback.",
        },
        {
            "id": "template_paths_not_terrain_aware",
            "severity": "manual_review",
            "evidence": "Vanilla villages, Integrated Villages, and Towns and Towers provide local paths/streets, but no Atlas-aware slope or cliff correction.",
            "recommendation": "Field-test path crossings after terrain signoff; future helper should substitute bridges/supports.",
        },
        {
            "id": "yungs_bridges_are_standalone",
            "severity": "manual_review",
            "evidence": "YUNG's Bridges is active, but jar inspection found no JSON route linkage to road networks.",
            "recommendation": "Keep as scenic landmarks until route anchor behavior is manually reviewed.",
        },
        {
            "id": "macaws_bridges_are_palette_only",
            "severity": "not_a_failure",
            "evidence": "Macaw's Bridges has no worldgen files in jar inspection.",
            "recommendation": "Use as future authored/helper bridge blocks, not as an automatic fix.",
        },
        {
            "id": "towns_and_towers_bridge_gap_risk",
            "severity": "manual_review",
            "evidence": "Towns and Towers has road/crossroad template evidence but no direct bridge template evidence from jar scan.",
            "recommendation": "Inspect villages near rivers and cliffs before enabling any settlement expansion.",
        },
        {
            "id": "mvs_paths_route_purpose_unknown",
            "severity": "manual_review",
            "evidence": "`mvs:paths` is a generated path structure with spacing 35 / separation 12.",
            "recommendation": "Check whether it reads like useful trail detail or roads to nowhere.",
        },
    ]
    failure_rows = [
        [f"`{failure['id']}`", failure["severity"], failure["evidence"], failure["recommendation"]]
        for failure in failures
    ]
    failure_doc = f"""
# Road, Bridge, And River Failures

Generated: {generated_at}

Status: reconnaissance only. No road or bridge behavior was changed.

## Summary

- Confirmed terrain-water issue affecting road design: south/west ocean-like basins.
- Confirmed connected-road issue: no pack-owned connected road network exists yet.
- Confirmed bridge issue: bridge content exists, but route linkage is not established.
- Confirmed no-change rule: all candidates remain disabled.

## Failure Register

{md_table(['Failure', 'Severity', 'Evidence', 'Recommendation'], failure_rows)}

## Field Evidence Needed Later

- Coordinates where village paths cross rivers without bridges.
- Coordinates where paths float, cut cliffs, or shear through steep terrain.
- Coordinates where YUNG's Bridges generate naturally and whether they align with nearby roads or settlements.
- Coordinates where Towns and Towers streets meet rivers, ravines, ocean-leak basins, or cliff edges.
- Coordinates where Integrated Villages docks or local bridges create useful crossings versus awkward water edges.

## Current Do-Not-Fix-Yet Boundary

Do not disable road, village, bridge, or structure sources only because they are listed here. The current pass is evidence-gathering. The only terrain blocker still confirmed is Atlas land/water coherence in south/west regions.
"""

    rule_sections = []
    for rule in crossing_policy["rules"]:
        rule_sections.append(f"### {rule['region'].replace('_', ' ').title()}\n\n- {rule['strategy']}")
    design_doc = f"""
# Travel Network Design Rules

Generated: {generated_at}

Status: design scaffold only. These rules are not active generation logic.

## Core Rules

- Roads should connect settlements, waystations, bridges, passes, ports, and future Guild outposts.
- Roads should not generate randomly without a visible purpose.
- Roads should not cross large cliffs without switchbacks, stairs, tunnels, supports, or bridges.
- River roads should prefer bridges, fords, docks, or intentional crossings rather than flat path pieces through water.
- Crownlands/Hearthlands should have the safest and clearest starter road network.
- Dangerous or broken roads are allowed only when the region identity supports it and the player can read the intent.

## Regional Rules

{chr(10).join(rule_sections)}

## Source Ownership

- YUNG's Bridges: keep as natural bridge landmarks until field review proves route value.
- Macaw's Bridges: keep as a build palette for future authored or helper-placed bridge pieces.
- Integrated Villages: treat roads, docks, and mossy_mounds bridge pieces as local settlement content.
- Towns and Towers: treat streets as local settlement content until bridge gaps, slopes, and overlap are reviewed.
- Moog/IDAS/Structory/Human Companions: treat path blocks as local template dressing, not as the Atlas road network.

## Future Helper Boundary

A real route layer needs terrain awareness after chunks, roads, water, ravines, and cliffs exist. Datapack rules can define palettes and structures, but a helper module is the right tool for detecting bad crossings and replacing a road segment with a bridge, stair, tunnel, or support piece.

## Candidate Status

All travel candidates in `config/ascendant_travel/travel_network_candidates.json` are disabled review items. Do not enable them until terrain signoff and explicit approval.
"""
    return audit_doc, failure_doc, design_doc


def main() -> int:
    generated_at = now_iso()
    audit = read_json(AUDIT_PATH, {})
    audit_info = analyze_audit(audit)

    jar_info = {
        "yungs_bridges": jar_scan(active_jar_from_mod_toml("yungs-bridges.pw.toml")),
        "macaws_bridges": jar_scan(active_jar_from_mod_toml("macaws-bridges.pw.toml")),
        "integrated_villages": jar_scan(active_jar_from_mod_toml("integrated-villages.pw.toml")),
        "towns_and_towers": jar_scan(active_jar_from_mod_toml("towns-and-towers.pw.toml")),
    }
    water = water_summary()

    road_policy, bridge_policy, crossing_policy, candidates = make_policies(
        generated_at, audit_info, jar_info, water
    )
    audit_doc, failure_doc, design_doc = make_docs(
        generated_at, road_policy, bridge_policy, crossing_policy, candidates
    )

    write_json(CONFIG / "road_policy.json", road_policy)
    write_json(CONFIG / "bridge_policy.json", bridge_policy)
    write_json(CONFIG / "river_crossing_policy.json", crossing_policy)
    write_json(CONFIG / "travel_network_candidates.json", candidates)
    write_md(DOCS / "ASCENDANT_TRAVEL_NETWORK_AUDIT.md", audit_doc)
    write_md(DOCS / "ROAD_BRIDGE_RIVER_FAILURES.md", failure_doc)
    write_md(DOCS / "TRAVEL_NETWORK_DESIGN_RULES.md", design_doc)

    print("Generated Ascendant travel network audit and policy scaffold.")
    print(f"Road sources: {len(road_policy['road_sources'])}")
    print(f"Bridge sources: {len(bridge_policy['bridge_sources'])}")
    print(f"Path/travel structures detected: {road_policy['summary']['path_or_travel_structures_detected']}")
    print(f"Confirmed ocean leaks carried into travel review: {len(crossing_policy['confirmed_ocean_leaks'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
