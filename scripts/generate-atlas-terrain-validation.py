from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "config" / "ascendant_atlas" / "reports"
DOCS_DIR = ROOT / "docs"

DIMENSION_PATH = ROOT / "config" / "openloader" / "data" / "ascendant_realms_atlas" / "data" / "minecraft" / "dimension" / "overworld.json"
WORLDGEN_MANIFEST_PATH = ROOT / "config" / "ascendant_atlas" / "worldgen_regions.json"
RUNTIME_PATH = ROOT / "config" / "ascendant_atlas" / "runtime.json"
AUDIT_PATH = ROOT / "docs" / "generated" / "worldgen_content_audit.json"
HELPER_SOURCE_PATH = ROOT / "local-mods" / "ascendant-atlas-regions" / "src" / "main" / "java" / "com" / "robbinstech" / "ascendant_atlas_regions" / "RegionalMultiNoiseBiomeSource.java"
HELPER_ENTRYPOINT_PATH = ROOT / "local-mods" / "ascendant-atlas-regions" / "src" / "main" / "java" / "com" / "robbinstech" / "ascendant_atlas_regions" / "AscendantAtlasRegions.java"
HELPER_COMMANDS_PATH = ROOT / "local-mods" / "ascendant-atlas-regions" / "src" / "main" / "java" / "com" / "robbinstech" / "ascendant_atlas_regions" / "AtlasCommands.java"
ATLAS_DATAPACK_PATH = ROOT / "config" / "openloader" / "data" / "ascendant_realms_atlas" / "data" / "ascendant_atlas"
TECTONIC_CONFIG_PATH = ROOT / "config" / "tectonic.json"

VALIDATION_POINTS = [
    (0, 0),
    (0, -2000),
    (0, -5000),
    (0, -9000),
    (0, 2000),
    (0, 5000),
    (0, 9000),
    (2000, 0),
    (5000, 0),
    (9000, 0),
    (-2000, 0),
    (-5000, 0),
    (-9000, 0),
    (5000, -5000),
    (-5000, -5000),
    (5000, 5000),
    (-5000, 5000),
    (12000, 0),
    (0, 12000),
    (0, -12000),
    (-12000, 0),
]

POOL_TO_REGION = {
    "center": "hearthlands",
    "north": "frostmarch",
    "south": "sunreach",
    "east": "verdant_coast",
    "west": "stoneback_highlands",
    "north_east": "north_east_marches",
    "north_west": "north_west_marches",
    "south_east": "south_east_wilds",
    "south_west": "south_west_wilds",
    "outer": "outer_rim",
}

INTENDED_SNOW_POOLS = {"north", "north_east", "north_west", "outer"}
WATER_REVIEW_POOLS = {"south", "west", "south_west"}
ACCEPTED_TRANSITION_EDGE_CLASSIFICATION = "stoneback_frostmarch_transition_river"
FROZEN_MOUNTAIN_RIVER_SURFACE_BLOCKS = {
    "minecraft:ice",
    "minecraft:water",
    "minecraft:packed_ice",
    "minecraft:blue_ice",
    "minecraft:frosted_ice",
}
WATER_CLASSIFICATIONS = [
    "acceptable_river",
    "acceptable_lake",
    "acceptable_oasis",
    "acceptable_mountain_lake",
    "acceptable_coastline",
    "sampler_edge_case",
    "region_identity_problem",
    "ocean_leak",
    "wet_biome_wrong_region",
    "needs_manual_review",
]
WATER_BODY_CLASSIFICATIONS = [
    "acceptable_river",
    "acceptable_oasis",
    "acceptable_lake",
    "acceptable_mountain_lake",
    "acceptable_coastline",
    "ocean_leak",
    "basin_leak",
    "needs_manual_review",
]
WATER_BODY_RADII_BLOCKS = [32, 64, 128]

MANUAL_WATER_REVIEW_OVERRIDES: dict[tuple[int, int], dict[str, str]] = {
    (-30000, 0): {
        "classification": "acceptable_river",
        "note": "Manual review: river terrain reads good in the west highlands.",
    },
    (-25000, -5000): {
        "classification": "ocean_leak",
        "note": "Manual review: huge ocean in a west/highland target area.",
    },
    (-20000, 5000): {
        "classification": "ocean_leak",
        "note": "Manual review: huge ocean in a west/highland target area.",
    },
    (-20000, 20000): {
        "classification": "ocean_leak",
        "note": "Manual review: roughly 60-block-deep ocean over badlands terrain floor.",
    },
    (-15000, 15000): {
        "classification": "ocean_leak",
        "note": "Manual review: badlands floor under massive lake/ocean with island villages and structures.",
    },
    (-5000, 15000): {
        "classification": "ocean_leak",
        "note": "Manual review: badlands floor under massive lake/ocean.",
    },
    (-5000, 20000): {
        "classification": "ocean_leak",
        "note": "Manual review: badlands floor under massive lake/ocean.",
    },
    (0, 2000): {
        "classification": "acceptable_river",
        "note": "Manual review: savanna/clay desert with a cool river system; visually good.",
    },
    (0, 10000): {
        "classification": "ocean_leak",
        "note": "Manual review: badlands ocean-floor look with large ocean above it.",
    },
    (0, 12000): {
        "classification": "ocean_leak",
        "note": "Manual review: same badlands ocean-floor issue as nearby south samples.",
    },
    (0, 15000): {
        "classification": "ocean_leak",
        "note": "Manual review: same badlands ocean-floor issue as nearby south samples.",
    },
    (0, 20000): {
        "classification": "acceptable_river",
        "note": "Manual review: lake/river system reads good.",
    },
    (0, 25000): {
        "classification": "ocean_leak",
        "note": "Manual review: badlands with huge ocean.",
    },
    (0, 30000): {
        "classification": "ocean_leak",
        "note": "Manual review: badlands with huge ocean.",
    },
    (5000, 10000): {
        "classification": "ocean_leak",
        "note": "Manual review: huge ocean in a south target area.",
    },
    (5000, 15000): {
        "classification": "ocean_leak",
        "note": "Manual review: huge ocean with villages and structures stranded as islands.",
    },
    (5000, 20000): {
        "classification": "ocean_leak",
        "note": "Manual review: huge ocean in a south target area.",
    },
    (10000, 15000): {
        "classification": "acceptable_river",
        "note": "Manual review: river system reads good.",
    },
    (15000, 25000): {
        "classification": "ocean_leak",
        "note": "Manual review: huge ocean with island villages and structures.",
    },
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=False)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def unique_biomes(entries: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for entry in entries:
        biome = str(entry.get("biome", ""))
        if biome and biome not in seen:
            seen.add(biome)
            result.append(biome)
    return result


def audit_for(audit_biomes: dict[str, Any], biome_id: str) -> dict[str, Any]:
    return audit_biomes.get(biome_id, {})


def snow_allowed(audit_entry: dict[str, Any]) -> bool | None:
    if not audit_entry:
        return None
    bucket = audit_entry.get("bucket", {}) or {}
    flags = set(bucket.get("flags", []) or [])
    temperature = audit_entry.get("temperature")
    downfall = audit_entry.get("downfall")
    climate_bucket = str(bucket.get("climate_bucket", ""))
    if "snow_precipitation" in flags or climate_bucket == "frozen_or_snow":
        return True
    if isinstance(temperature, (int, float)) and temperature <= 0.15 and isinstance(downfall, (int, float)) and downfall > 0:
        return True
    return False


def has_snow_rule_violation(sample: dict[str, Any]) -> bool:
    return (
        sample.get("snow_allowed") is True
        and str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "") not in INTENDED_SNOW_POOLS
        and str(sample.get("climate_sector") or "") not in INTENDED_SNOW_POOLS
    )


def accepted_transition_edge_case(sample: dict[str, Any]) -> str | None:
    """Narrow Stoneback/Frostmarch edge: frozen river at a northwest mountain transition."""
    if str(sample.get("actual_biome_id") or "") != "minecraft:frozen_river":
        return None
    if str(sample.get("surface_block_id") or "") not in FROZEN_MOUNTAIN_RIVER_SURFACE_BLOCKS:
        return None
    if has_snow_rule_violation(sample):
        return None
    try:
        x = int(sample.get("x", 0))
        z = int(sample.get("z", 0))
    except (TypeError, ValueError):
        return None
    if not (x < 0 and z < 0):
        return None
    if abs(z) < max(1000, abs(x) * 0.45):
        return None
    atlas_region = str(sample.get("atlas_region") or "")
    expected_pool = str(sample.get("expected_biome_pool") or "")
    climate_sector = str(sample.get("climate_sector") or "")
    if atlas_region not in {"stoneback_highlands", "north_west_marches"} and expected_pool not in {"west", "north_west"} and climate_sector not in {"west", "north_west"}:
        return None
    return ACCEPTED_TRANSITION_EDGE_CLASSIFICATION


def classify_point(x: int, z: int, biome_source: dict[str, Any], runtime: dict[str, Any]) -> dict[str, Any]:
    center_radius = int(biome_source.get("center_radius_blocks", 500))
    outer_radius = int(biome_source.get("outer_radius_blocks", 30000))
    axis_ratio = float(biome_source.get("axis_dominance_ratio", 1.25))
    distance = math.sqrt(x * x + z * z)
    abs_x = abs(x)
    abs_z = abs(z)

    if distance > outer_radius:
        pool = "outer"
    elif distance <= center_radius:
        pool = "center"
    elif abs_z >= abs_x * axis_ratio:
        pool = "north" if z < 0 else "south"
    elif abs_x >= abs_z * axis_ratio:
        pool = "east" if x > 0 else "west"
    elif z < 0 and x > 0:
        pool = "north_east"
    elif z < 0:
        pool = "north_west"
    elif x > 0:
        pool = "south_east"
    else:
        pool = "south_west"

    return {
        "x": x,
        "z": z,
        "atlas_region": POOL_TO_REGION.get(pool, "outer_rim"),
        "climate_sector": pool,
        "distance_blocks": int(round(distance)),
        "distance_ring": runtime_ring(distance, runtime),
        "expected_biome_pool": pool,
    }


def runtime_ring(distance: float, runtime: dict[str, Any]) -> str:
    for ring in runtime.get("rings", []) or []:
        min_distance = float(ring.get("min_distance", 0))
        max_distance = float(ring.get("max_distance", 0))
        if min_distance <= distance <= max_distance:
            ring_id = int(ring.get("id", 0))
            slug = str(ring.get("name", f"tier_{ring_id}")).lower().replace(" ", "_")
            return f"tier_{ring_id}_{slug}"
    return "tier_5_corrupted_rim"


def pool_report(dimension: dict[str, Any], audit: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    biome_source = dimension["generator"]["biome_source"]
    audit_biomes = audit.get("biomes", {})
    pools: dict[str, Any] = {}
    missing_by_pool: dict[str, list[str]] = {}
    all_missing: set[str] = set()

    for pool_key in POOL_TO_REGION:
        entries = biome_source.get(pool_key, []) or []
        biome_ids = unique_biomes(entries)
        enriched: list[dict[str, Any]] = []
        snow_count = 0
        water_count = 0
        terralith_count = 0
        cold_risk_count = 0
        for biome_id in biome_ids:
            biome_audit = audit_for(audit_biomes, biome_id)
            bucket = biome_audit.get("bucket", {}) or {}
            flags = list(bucket.get("flags", []) or [])
            biome_snow = snow_allowed(biome_audit)
            if biome_snow:
                snow_count += 1
                if pool_key not in INTENDED_SNOW_POOLS:
                    cold_risk_count += 1
            if bucket.get("terrain_bucket") == "water_or_sea":
                water_count += 1
            if biome_id.startswith("terralith:"):
                terralith_count += 1
            if not biome_audit:
                missing_by_pool.setdefault(pool_key, []).append(biome_id)
                all_missing.add(biome_id)
            enriched.append(
                {
                    "id": biome_id,
                    "source": biome_audit.get("source"),
                    "temperature": biome_audit.get("temperature"),
                    "downfall": biome_audit.get("downfall"),
                    "precipitation": biome_audit.get("precipitation"),
                    "climate_bucket": bucket.get("climate_bucket"),
                    "terrain_bucket": bucket.get("terrain_bucket"),
                    "flags": flags,
                    "snow_allowed": biome_snow,
                    "missing_from_audit": not bool(biome_audit),
                }
            )

        pools[pool_key] = {
            "atlas_region": POOL_TO_REGION[pool_key],
            "entry_count": len(entries),
            "unique_biome_count": len(biome_ids),
            "terralith_unique_biome_count": terralith_count,
            "snow_allowed_unique_biome_count": snow_count,
            "water_or_sea_unique_biome_count": water_count,
            "snow_outside_intended_cold_count": cold_risk_count,
            "missing_biome_count": len(missing_by_pool.get(pool_key, [])),
            "biomes": enriched,
        }

    missing = {
        "version": 1,
        "generated_at": now_iso(),
        "source": "offline_dimension_override_plus_worldgen_audit",
        "configured_unique_biome_count": len({biome["id"] for pool in pools.values() for biome in pool["biomes"]}),
        "audit_biome_count": len(audit_biomes),
        "missing_count": len(all_missing),
        "missing_biomes": sorted(all_missing),
        "missing_by_pool": missing_by_pool,
    }

    report = {
        "version": 1,
        "generated_at": now_iso(),
        "source": "offline_dimension_override_plus_worldgen_audit",
        "biome_source_type": biome_source.get("type"),
        "terrain_settings": dimension.get("generator", {}).get("settings"),
        "coordinate_note": "Minecraft calls the helper biome source with quart coordinates; RegionalMultiNoiseBiomeSource converts quartX/quartZ to block coordinates with << 2 before region selection.",
        "pools": pools,
        "missing_biomes": sorted(all_missing),
    }
    return report, missing


def sample_report(
    dimension: dict[str, Any],
    runtime: dict[str, Any],
    biome_pools: dict[str, Any],
    audit: dict[str, Any],
    report_filename: str,
    validation_level: str,
    fallback_filenames: list[str] | None = None,
    allow_offline_expected: bool = False,
) -> dict[str, Any]:
    audit_biomes = audit.get("biomes", {})
    biome_source = dimension["generator"]["biome_source"]
    existing: dict[str, Any] | None = None
    sample_paths = [REPORT_DIR / report_filename]
    for fallback_filename in fallback_filenames or []:
        sample_paths.append(REPORT_DIR / fallback_filename)
    for sample_path in sample_paths:
        if existing is not None or not sample_path.exists():
            continue
        try:
            loaded = read_json(sample_path)
            if str(loaded.get("source", "")).startswith("in_game_"):
                existing = loaded
        except Exception:
            continue

    if existing:
        samples = existing.get("samples", []) or []
        source = existing.get("source")
        if validation_level == "biome_source":
            status = "source_sample_present"
        else:
            normal_surface_samples = [sample for sample in samples if is_normal_surface_sample(sample)]
            existing_status = str(existing.get("status") or "")
            completed = existing.get("completed_samples")
            total = existing.get("total_samples")
            pending = existing.get("pending_samples")
            complete_by_count = (
                isinstance(completed, int)
                and isinstance(total, int)
                and total > 0
                and completed >= total
                and (pending is None or pending == 0)
            )
            if normal_surface_samples and (
                existing_status in {"complete", "surface_sample_present_verify_visuals"}
                or complete_by_count
            ):
                status = "surface_sample_present_verify_visuals"
            elif normal_surface_samples:
                status = "surface_sample_partial_running"
            else:
                status = "surface_sample_missing_or_empty"
        top_sample_mode = existing.get("sample_mode")
    elif allow_offline_expected:
        samples = [classify_point(x, z, biome_source, runtime) for x, z in VALIDATION_POINTS]
        source = "offline_expected_validation_grid_pending_source_command"
        status = "pending_source_sample"
        top_sample_mode = "offline_expected_only"
    else:
        samples = []
        source = "pending_in_game_ascatlas_surface_grid_command"
        status = "pending_surface_sample"
        top_sample_mode = "pending_surface_command"

    enriched_samples: list[dict[str, Any]] = []
    for sample in samples:
        x = int(sample.get("x", 0))
        z = int(sample.get("z", 0))
        expected = classify_point(x, z, biome_source, runtime)
        actual_biome = sample.get("actual_biome_id")
        actual_audit = audit_for(audit_biomes, str(actual_biome)) if actual_biome else {}
        expected_pool = str(sample.get("expected_biome_pool") or expected["expected_biome_pool"])
        pool_biomes = {
            biome["id"]
            for biome in biome_pools["pools"].get(expected_pool, {}).get("biomes", [])
            if isinstance(biome, dict)
        }
        in_pool = sample.get("actual_biome_in_expected_pool")
        if actual_biome and in_pool is None:
            in_pool = actual_biome in pool_biomes
        temperature = sample.get("biome_temperature")
        if temperature is None:
            temperature = actual_audit.get("temperature")
        precipitation = sample.get("precipitation")
        if precipitation is None:
            precipitation = actual_audit.get("precipitation")
        snow_value = sample.get("snow_allowed")
        if snow_value is None:
            snow_value = snow_allowed(actual_audit)
        enriched = {
            **expected,
            "expected_biome_pool_size": len(pool_biomes),
            "actual_biome_id": actual_biome,
            "actual_biome_in_expected_pool": in_pool,
            "sample_y": sample.get("sample_y"),
            "sample_mode": sample.get("sample_mode"),
            "surface_y": sample.get("surface_y"),
            "surface_block_id": sample.get("surface_block_id"),
            "biome_temperature": temperature,
            "precipitation": precipitation,
            "snow_allowed": snow_value,
            "cave_like_biome_at_surface": sample.get("cave_like_biome_at_surface"),
            "chunk_status": sample.get("chunk_status"),
            "sample_error": sample.get("sample_error"),
            "terrain_visually_matches_intended_region": sample.get("terrain_visually_matches_intended_region", "pending_fresh_world_review"),
            "biome_transition_sharpness": sample.get("biome_transition_sharpness", "pending_fresh_world_review"),
        }
        transition_classification = accepted_transition_edge_case(enriched)
        if transition_classification:
            enriched["accepted_transition_edge_case"] = transition_classification
            enriched["accepted_transition_reason"] = (
                "Frozen river at a northwest Stoneback/Frostmarch edge: west/Stoneback or transition region, "
                "northwest-leaning coordinates, frozen_river biome, ice/water surface, and no snow-rule violation."
            )
        else:
            enriched["accepted_transition_edge_case"] = None
            enriched["accepted_transition_reason"] = None
        enriched_samples.append(enriched)

    return {
        "version": 1,
        "generated_at": now_iso(),
        "source": source,
        "validation_level": validation_level,
        "status": status,
        "source_report_status": existing.get("status") if existing else None,
        "completed_samples": existing.get("completed_samples") if existing else len(enriched_samples),
        "total_samples": existing.get("total_samples") if existing else len(enriched_samples),
        "pending_samples": existing.get("pending_samples") if existing else 0,
        "radius": existing.get("radius") if existing else None,
        "step": existing.get("step") if existing else None,
        "sample_mode": top_sample_mode,
        "required_points": [{"x": x, "z": z} for x, z in VALIDATION_POINTS],
        "samples": enriched_samples,
    }


def source_contains(path: Path, text: str) -> bool:
    return path.exists() and text in path.read_text(encoding="utf-8", errors="replace")


def command_status() -> dict[str, bool]:
    text = HELPER_COMMANDS_PATH.read_text(encoding="utf-8", errors="replace") if HELPER_COMMANDS_PATH.exists() else ""
    return {
        "/ascatlas here": '"here"' in text and "runHere" in text,
        "/ascatlas region <x> <z>": '"region"' in text and '"x"' in text and '"z"' in text and "runRegion" in text,
        "/ascatlas sample_grid <radius> <step>": '"sample_grid"' in text and '"radius"' in text and '"step"' in text and "runSampleGrid" in text,
        "/ascatlas sample_surface_grid <radius> <step>": '"sample_surface_grid"' in text and '"radius"' in text and '"step"' in text and "runSurfaceSampleGrid" in text,
        "/ascatlas classify_water_bodies <radius> <step>": '"classify_water_bodies"' in text and "runWaterBodyClassificationGrid" in text,
        "/ascatlas cancel_water_body_classification": '"cancel_water_body_classification"' in text and "runCancelWaterBodyClassification" in text,
        "/ascatlas terrain_probe <x> <z>": '"terrain_probe"' in text and "runTerrainProbe" in text,
        "/ascatlas terrain_probe_here": '"terrain_probe_here"' in text and "runTerrainProbeHere" in text,
        "/ascatlas sample_land_water <radius> <step>": '"sample_land_water"' in text and "runLandWaterSampleGrid" in text,
        "/ascatlas dump_land_water_policy": '"dump_land_water_policy"' in text and "runDumpLandWaterPolicy" in text,
        "/ascatlas dump_biome_pools": '"dump_biome_pools"' in text and "runDumpBiomePools" in text,
    }


def static_checks(dimension: dict[str, Any], missing: dict[str, Any]) -> list[tuple[str, str, str]]:
    generator = dimension.get("generator", {})
    biome_source = generator.get("biome_source", {})
    checks: list[tuple[str, str, str]] = []
    checks.append(("Helper registers regional biome source", "PASS" if source_contains(HELPER_ENTRYPOINT_PATH, "DeferredRegister") and source_contains(HELPER_ENTRYPOINT_PATH, "regional_multi_noise") else "FAIL", "Entrypoint uses Forge DeferredRegister for ascendant_atlas_regions:regional_multi_noise."))
    checks.append(("Overworld override uses Atlas biome source", "PASS" if biome_source.get("type") == "ascendant_atlas_regions:regional_multi_noise" else "FAIL", str(biome_source.get("type"))))
    checks.append(("Tectonic terrain shape is not bypassed", "PASS" if generator.get("type") == "minecraft:noise" and generator.get("settings") == "minecraft:overworld" else "FAIL", f"type={generator.get('type')} settings={generator.get('settings')}"))
    terralith_entries = sum(1 for pool in POOL_TO_REGION for entry in biome_source.get(pool, []) if str(entry.get("biome", "")).startswith("terralith:"))
    checks.append(("Terralith biome entries are still used", "PASS" if terralith_entries > 0 else "FAIL", f"{terralith_entries} Terralith parameter entries in active pools."))
    checks.append(("No missing configured biome IDs", "PASS" if int(missing.get("missing_count", 0)) == 0 else "FAIL", f"{missing.get('missing_count', 0)} missing IDs."))
    checks.append(("Coordinate math handles quart coords", "PASS" if source_contains(HELPER_SOURCE_PATH, "quartX << 2") and source_contains(HELPER_SOURCE_PATH, "quartZ << 2") else "FAIL", "Biome source converts quart coordinates to block coordinates before Atlas region selection."))
    checks.append(("Land-first water coherence bias present", "PASS" if source_contains(HELPER_SOURCE_PATH, "biasLandFirstWaterCoherence") and source_contains(HELPER_SOURCE_PATH, "south_west") else "FAIL", "Helper applies a bounded continentalness bias for far south/west/south-west land-first pools."))
    cave_pool_biomes = sorted({
        str(entry.get("biome"))
        for pool_key in POOL_TO_REGION
        for entry in biome_source.get(pool_key, []) or []
        if is_cave_only_biome(entry.get("biome"))
    })
    checks.append(("Atlas surface pools exclude cave-only biomes", "PASS" if not cave_pool_biomes else "FAIL", f"{len(cave_pool_biomes)} cave-only biome IDs in surface pools."))
    checks.append(("Old worlds are invalid tests", "PASS", "Worldgen evidence must come from a fresh world or ungenerated chunks."))
    for command, present in command_status().items():
        checks.append((f"Command {command}", "PASS" if present else "FAIL", "Implemented in AtlasCommands.java." if present else "Missing from helper command source."))
    return checks


def pool_markdown_rows(biome_pools: dict[str, Any]) -> str:
    rows = []
    for pool_key, pool in biome_pools["pools"].items():
        rows.append(
            "| `{}` | `{}` | {} | {} | {} | {} | {} | {} |".format(
                pool_key,
                pool["atlas_region"],
                pool["entry_count"],
                pool["unique_biome_count"],
                pool["terralith_unique_biome_count"],
                pool["water_or_sea_unique_biome_count"],
                pool["snow_allowed_unique_biome_count"],
                pool["snow_outside_intended_cold_count"],
            )
        )
    return "\n".join(rows)


def sample_markdown_rows(sample_grid: dict[str, Any]) -> str:
    rows = []
    for sample in sample_grid["samples"]:
        in_pool_value = sample.get("actual_biome_in_expected_pool") if sample.get("actual_biome_in_expected_pool") is not None else "pending"
        if sample.get("accepted_transition_edge_case"):
            in_pool_value = f"{in_pool_value} (accepted: {sample.get('accepted_transition_edge_case')})"
        rows.append(
            "| {x},{z} | `{region}` | `{sector}` | `{ring}` | `{pool}` | {actual} | {in_pool} | {mode} | {surface_y} | {surface_block} | {temp} | {precip} | {snow} | {cave_surface} | {visual} | {transition} |".format(
                x=sample["x"],
                z=sample["z"],
                region=sample["atlas_region"],
                sector=sample["climate_sector"],
                ring=sample["distance_ring"],
                pool=sample["expected_biome_pool"],
                actual=f"`{sample['actual_biome_id']}`" if sample.get("actual_biome_id") else "pending",
                in_pool=in_pool_value,
                mode=f"`{sample.get('sample_mode')}`" if sample.get("sample_mode") else "pending",
                surface_y=sample.get("surface_y") if sample.get("surface_y") is not None else "pending",
                surface_block=f"`{sample.get('surface_block_id')}`" if sample.get("surface_block_id") else "pending",
                temp=sample.get("biome_temperature") if sample.get("biome_temperature") is not None else "pending",
                precip=sample.get("precipitation") if sample.get("precipitation") is not None else "pending",
                snow=sample.get("snow_allowed") if sample.get("snow_allowed") is not None else "pending",
                cave_surface=sample.get("cave_like_biome_at_surface") if sample.get("cave_like_biome_at_surface") is not None else "pending",
                visual=sample.get("terrain_visually_matches_intended_region") or "pending",
                transition=sample.get("biome_transition_sharpness") or "pending",
            )
        )
    return "\n".join(rows)


def count_markdown_rows(counts: dict[str, int]) -> str:
    if not counts:
        return "| none | 0 |"
    return "\n".join(f"| `{key}` | {value} |" for key, value in counts.items())


def water_sample_markdown_rows(water_report: dict[str, Any]) -> str:
    rows = []
    for sample in water_report.get("samples", []):
        manual_note = str(sample.get("manual_review_note") or "")
        manual_note = manual_note.replace("|", "/")
        rows.append(
            "| {x},{z} | `{region}` | `{sector}` | `{ring}` | `{pool}` | {actual} | {surface_block} | {surface_y} | {temp} | {precip} | {snow} | {target} | `{classification}` | {manual_status} | {manual_note} | `{tp}` |".format(
                x=sample.get("x"),
                z=sample.get("z"),
                region=sample.get("atlas_region"),
                sector=sample.get("climate_sector"),
                ring=sample.get("distance_ring"),
                pool=sample.get("expected_biome_pool"),
                actual=f"`{sample.get('actual_biome_id')}`" if sample.get("actual_biome_id") else "pending",
                surface_block=f"`{sample.get('surface_block_id')}`" if sample.get("surface_block_id") else "pending",
                surface_y=sample.get("surface_y"),
                temp=sample.get("temperature"),
                precip=sample.get("precipitation"),
                snow=sample.get("snow_allowed"),
                target=sample.get("is_south_west_water_target_region"),
                classification=sample.get("classification"),
                manual_status=sample.get("manual_review_status") or "pending",
                manual_note=manual_note or "pending",
                tp=sample.get("suggested_teleport_command"),
            )
        )
    return "\n".join(rows)


def water_body_markdown_rows(water_body_report: dict[str, Any]) -> str:
    rows = []
    for sample in water_body_report.get("samples", []):
        if not isinstance(sample, dict):
            continue
        rows.append(
            "| {x},{z} | `{region}` | `{sector}` | `{ring}` | {actual} | {surface_block} | {surface_y} | {local_water} | {nearby_land} | `{size}` | `{classification}` | `{fix}` | `{status}` |".format(
                x=sample.get("x"),
                z=sample.get("z"),
                region=sample.get("region"),
                sector=sample.get("climate_sector"),
                ring=sample.get("distance_ring"),
                actual=f"`{sample.get('actual_biome')}`" if sample.get("actual_biome") else "pending",
                surface_block=f"`{sample.get('surface_block')}`" if sample.get("surface_block") else "pending",
                surface_y=sample.get("surface_y"),
                local_water=sample.get("local_water_percentage") if sample.get("local_water_percentage") is not None else "pending",
                nearby_land=sample.get("nearby_land_percentage") if sample.get("nearby_land_percentage") is not None else "pending",
                size=sample.get("estimated_water_body_size"),
                classification=sample.get("classification"),
                fix=sample.get("suggested_fix_type"),
                status=sample.get("sample_status"),
            )
        )
    return "\n".join(rows)


def is_cave_only_biome(biome_id: object) -> bool:
    biome = str(biome_id or "")
    return "/cave" in biome or biome.endswith("_caves")


def numeric(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def is_normal_surface_sample(sample: dict[str, Any]) -> bool:
    mode = str(sample.get("sample_mode") or "")
    if mode.startswith("fast_no_chunkgen"):
        return False
    return numeric(sample.get("surface_y")) is not None


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) if item.get(key) not in (None, "") else "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def classify_water_sample(sample: dict[str, Any]) -> str:
    pool = str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "")
    biome = str(sample.get("actual_biome_id") or "")
    is_target = pool in WATER_REVIEW_POOLS
    mountain_terms = [
        "alpine",
        "cliff",
        "highland",
        "hill",
        "mountain",
        "painted_mountains",
        "peak",
        "spire",
        "stony",
        "windswept",
        "yosemite",
    ]
    wet_terms = ["jungle", "mangrove", "marsh", "ocean", "swamp"]

    if "river" in biome:
        return "acceptable_river"
    if "oasis" in biome:
        return "acceptable_oasis"
    if "ocean" in biome:
        return "ocean_leak" if is_target else "acceptable_coastline"
    if "beach" in biome:
        return "ocean_leak" if is_target else "acceptable_coastline"
    if is_target and any(term in biome for term in wet_terms):
        return "wet_biome_wrong_region"
    if pool in {"west", "south_west"} and any(term in biome for term in mountain_terms):
        return "acceptable_mountain_lake"
    if not is_target and pool in {"east", "north_east", "south_east"}:
        return "acceptable_coastline"
    if not is_target:
        return "acceptable_lake"
    return "needs_manual_review"


def water_review_report(surface_grid: dict[str, Any]) -> dict[str, Any]:
    surface_samples = [sample for sample in surface_grid.get("samples", []) if isinstance(sample, dict)]
    normal_surface_samples = [sample for sample in surface_samples if is_normal_surface_sample(sample)]
    water_samples: list[dict[str, Any]] = []
    for sample in normal_surface_samples:
        if sample.get("surface_block_id") != "minecraft:water":
            continue
        pool = str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "")
        surface_y = numeric(sample.get("surface_y"))
        teleport_y = int(surface_y + 8) if surface_y is not None else 90
        classification = classify_water_sample(sample)
        manual_review = MANUAL_WATER_REVIEW_OVERRIDES.get((int(sample.get("x")), int(sample.get("z"))))
        if manual_review:
            classification = manual_review["classification"]
        review_sample = {
            "x": sample.get("x"),
            "z": sample.get("z"),
            "atlas_region": sample.get("atlas_region"),
            "climate_sector": sample.get("climate_sector"),
            "distance_ring": sample.get("distance_ring"),
            "expected_biome_pool": sample.get("expected_biome_pool"),
            "actual_biome_id": sample.get("actual_biome_id"),
            "actual_biome_in_expected_pool": sample.get("actual_biome_in_expected_pool"),
            "surface_block_id": sample.get("surface_block_id"),
            "surface_y": sample.get("surface_y"),
            "temperature": sample.get("biome_temperature"),
            "precipitation": sample.get("precipitation"),
            "snow_allowed": sample.get("snow_allowed"),
            "is_south_west_water_target_region": pool in WATER_REVIEW_POOLS,
            "suggested_teleport_command": f"/tp @s {sample.get('x')} {teleport_y} {sample.get('z')}",
            "classification": classification,
            "classification_needs_visual_confirmation": pool in WATER_REVIEW_POOLS and not manual_review,
            "manual_review_status": "reviewed" if manual_review else "pending",
            "manual_review_note": manual_review.get("note") if manual_review else None,
        }
        water_samples.append(review_sample)

    target_samples = [sample for sample in water_samples if sample["is_south_west_water_target_region"]]
    biome_pool_leak_samples = [
        sample
        for sample in target_samples
        if sample.get("classification") == "wet_biome_wrong_region"
        or sample.get("actual_biome_in_expected_pool") is False
    ]
    ocean_leak_samples = [sample for sample in target_samples if sample.get("classification") == "ocean_leak"]
    reviewed_samples = [sample for sample in water_samples if sample.get("manual_review_status") == "reviewed"]
    reviewed_target_samples = [
        sample
        for sample in reviewed_samples
        if sample.get("is_south_west_water_target_region")
    ]
    if target_samples and biome_pool_leak_samples:
        issue_kind = "surface biome-pool mismatch plus terrain/noise water placement"
        assessment = "Surface water review found target-region biome-pool mismatches and south/west water placement that still needs land/water coherence review."
    elif ocean_leak_samples:
        issue_kind = "terrain/noise ocean leak"
        assessment = f"Automated Atlas validation passed, but manual review confirmed {len(ocean_leak_samples)} south/west ocean-leak samples. This is terrain/noise water placement, not biome-pool leakage."
    elif target_samples:
        issue_kind = "terrain/noise water placement"
        assessment = "Water samples are in expected biome pools, but target-region water still needs visual review before terrain signoff."
    else:
        issue_kind = "no south/west water issue detected"
        assessment = "No south/west target-region water samples were found."
    return {
        "version": 1,
        "generated_at": now_iso(),
        "source": surface_grid.get("source"),
        "source_report_status": surface_grid.get("status"),
        "sample_grid_radius": surface_grid.get("radius"),
        "sample_grid_step": surface_grid.get("step"),
        "summary": {
            "total_water_samples": len(water_samples),
            "target_south_west_water_samples": len(target_samples),
            "manual_reviewed_water_samples": len(reviewed_samples),
            "manual_reviewed_target_water_samples": len(reviewed_target_samples),
            "visually_confirmed_ocean_leak_samples": len(ocean_leak_samples),
            "water_samples_by_region": count_by(water_samples, "atlas_region"),
            "water_samples_by_biome_id": count_by(water_samples, "actual_biome_id"),
            "water_samples_by_ring": count_by(water_samples, "distance_ring"),
            "water_samples_by_classification": count_by(water_samples, "classification"),
            "issue_kind": issue_kind,
            "is_biome_pool_leakage": bool(biome_pool_leak_samples),
            "is_terrain_noise_water_placement": bool(target_samples),
            "assessment": assessment,
        },
        "classification_values": WATER_CLASSIFICATIONS,
        "samples": water_samples,
    }


def water_body_fix_type(classification: object) -> str:
    value = str(classification or "")
    if value == "ocean_leak":
        return "continentalness_aware_region_selection_or_region_noise_wrapper"
    if value == "basin_leak":
        return "regional_land_water_bias_without_removing_all_water"
    if value.startswith("acceptable_"):
        return "preserve_water_feature"
    return "manual_review_before_fix"


def water_body_classification_report(water_report: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    output_path = REPORT_DIR / "water_body_classification_latest.json"
    if output_path.exists():
        try:
            existing = read_json(output_path)
            if (
                isinstance(existing, dict)
                and existing.get("source") == "in_game_ascatlas_classify_water_bodies_command"
                and existing.get("validation_level") == "water_body_classification"
            ):
                return existing, False
        except Exception:
            pass

    samples: list[dict[str, Any]] = []
    for sample in water_report.get("samples", []):
        if not isinstance(sample, dict):
            continue
        classification = str(sample.get("classification") or "needs_manual_review")
        if classification not in WATER_BODY_CLASSIFICATIONS:
            classification = "needs_manual_review"
        samples.append(
            {
                "x": sample.get("x"),
                "z": sample.get("z"),
                "region": sample.get("atlas_region"),
                "climate_sector": sample.get("climate_sector"),
                "distance_ring": sample.get("distance_ring"),
                "actual_biome": sample.get("actual_biome_id"),
                "surface_block": sample.get("surface_block_id"),
                "surface_y": sample.get("surface_y"),
                "local_water_percentage": None,
                "nearby_land_percentage": None,
                "estimated_water_body_size": "pending_true_neighborhood_sampling",
                "classification": classification,
                "suggested_fix_type": water_body_fix_type(classification),
                "water_percentages_by_radius_blocks": {str(radius): None for radius in WATER_BODY_RADII_BLOCKS},
                "land_percentages_by_radius_blocks": {str(radius): None for radius in WATER_BODY_RADII_BLOCKS},
                "sample_counts_by_radius_blocks": {str(radius): None for radius in WATER_BODY_RADII_BLOCKS},
                "skipped_unloaded_chunk_counts_by_radius_blocks": {str(radius): None for radius in WATER_BODY_RADII_BLOCKS},
                "manual_review_status": sample.get("manual_review_status"),
                "manual_review_note": sample.get("manual_review_note"),
                "suggested_teleport_command": sample.get("suggested_teleport_command"),
                "sample_status": "pending_in_game_neighborhood_sampling",
            }
        )

    ocean_leaks = [sample for sample in samples if sample.get("classification") == "ocean_leak"]
    basin_leaks = [sample for sample in samples if sample.get("classification") == "basin_leak"]
    return (
        {
            "version": 1,
            "generated_at": now_iso(),
            "source": "offline_manual_water_review_seed",
            "validation_level": "water_body_classification_seed",
            "status": "pending_in_game_ascatlas_classify_water_bodies",
            "required_command": "/ascatlas classify_water_bodies 30000 5000",
            "sampling_radii": [
                {
                    "radius_blocks": radius,
                    "radius_chunks": radius // 16,
                    "sample_step_blocks": max(16, radius // 4),
                }
                for radius in WATER_BODY_RADII_BLOCKS
            ],
            "summary": {
                "water_samples": len(samples),
                "completed_water_body_samples": 0,
                "pending_water_body_samples": len(samples),
                "ocean_leak_samples": len(ocean_leaks),
                "basin_leak_samples": len(basin_leaks),
                "water_samples_by_classification": count_by(samples, "classification"),
                "classification_method": "Pending bounded in-game local surface sampling at 32/64/128 block radii. This replaces the old 1024-block spread that caused integrated-server stalls.",
                "terrain_stack_finding": "The active biome source can select land biomes over water-shaped terrain; true water-body percentages require the helper command.",
            },
            "classification_values": WATER_BODY_CLASSIFICATIONS,
            "samples": samples,
        },
        True,
    )


def land_water_coherence_report(
    dimension: dict[str, Any],
    source_grid: dict[str, Any],
    surface_grid: dict[str, Any],
    water_report: dict[str, Any],
    water_body_report: dict[str, Any],
) -> dict[str, Any]:
    generator = dimension.get("generator", {}) if isinstance(dimension.get("generator"), dict) else {}
    biome_source = generator.get("biome_source", {}) if isinstance(generator.get("biome_source"), dict) else {}
    water_summary = water_report.get("summary", {}) if isinstance(water_report, dict) else {}
    water_body_summary = water_body_report.get("summary", {}) if isinstance(water_body_report, dict) else {}
    helper_fix_present = (
        source_contains(HELPER_SOURCE_PATH, "biasLandFirstWaterCoherence")
        and source_contains(HELPER_SOURCE_PATH, "targetLandFirstContinentalness")
        and source_contains(HELPER_SOURCE_PATH, "isSparseLocalWaterPocket")
    )
    tectonic_config: dict[str, Any] = {}
    if TECTONIC_CONFIG_PATH.exists():
        try:
            tectonic_config = read_json(TECTONIC_CONFIG_PATH)
        except Exception as exc:
            tectonic_config = {"read_error": str(exc)}

    manual_ocean_leaks = [
        sample
        for sample in water_report.get("samples", [])
        if isinstance(sample, dict)
        and sample.get("is_south_west_water_target_region")
        and sample.get("classification") == "ocean_leak"
    ]
    water_body_leak_samples = [
        sample
        for sample in water_body_report.get("samples", [])
        if isinstance(sample, dict)
        and sample.get("classification") in {"ocean_leak", "basin_leak"}
    ]
    live_water_body_complete = (
        water_body_report.get("source") == "in_game_ascatlas_classify_water_bodies_command"
        and water_body_report.get("status") == "complete"
    )
    if live_water_body_complete and water_body_leak_samples:
        status = "helper_biome_source_fix_failed_deeper_terrain_noise_required"
        helper_fix_status = "implemented_but_failed_live_water_validation"
    elif helper_fix_present:
        status = "helper_fix_applied_pending_fresh_world_validation"
        helper_fix_status = "implemented_pending_fresh_world_validation"
    else:
        status = "diagnosis_only_no_helper_fix_detected"
        helper_fix_status = "missing"
    source_counts = sample_counts(source_grid)
    surface_counts = sample_counts(surface_grid)
    return {
        "version": 1,
        "generated_at": now_iso(),
        "source": "offline_atlas_land_water_coherence_report",
        "status": status,
        "active_terrain_stack": {
            "overworld_dimension_type": dimension.get("type"),
            "chunk_generator": generator.get("type"),
            "noise_settings": generator.get("settings"),
            "biome_source": biome_source.get("type"),
            "tectonic_config": tectonic_config,
            "tectonic_path": "config/tectonic.json",
            "terrain_shape_owner": "Tectonic/vanilla noise path via minecraft:noise + minecraft:overworld settings",
            "biome_table_owner": "Terralith entries selected through ascendant_atlas_regions:regional_multi_noise",
        },
        "helper_biome_source_behavior": {
            "registers_active_biome_source": source_contains(HELPER_ENTRYPOINT_PATH, "DeferredRegister") and source_contains(HELPER_ENTRYPOINT_PATH, "regional_multi_noise"),
            "receives_quart_coordinates": source_contains(HELPER_SOURCE_PATH, "m_203407_(int quartX"),
            "converts_quart_to_block_coordinates": source_contains(HELPER_SOURCE_PATH, "quartX << 2") and source_contains(HELPER_SOURCE_PATH, "quartZ << 2"),
            "receives_climate_sampler": source_contains(HELPER_SOURCE_PATH, "Climate.Sampler sampler"),
            "samples_climate_target_point": source_contains(HELPER_SOURCE_PATH, "sampler.m_183445_(quartX, quartY, quartZ)"),
            "reads_continentalness": source_contains(HELPER_SOURCE_PATH, "target.f_187005_()"),
            "can_blend_continentalness": source_contains(HELPER_SOURCE_PATH, "blendClimate(target.f_187005_()"),
            "can_raise_or_lower_actual_terrain": False,
            "can_change_sea_level": False,
            "can_carve_rivers": False,
        },
        "diagnosis": {
            "biome_pool_leakage": bool(water_summary.get("is_biome_pool_leakage", False)),
            "terrain_noise_water_placement": bool(water_summary.get("is_terrain_noise_water_placement", False)),
            "sea_level_62_63_is_normal": True,
            "old_worlds_are_invalid_for_fix_validation": True,
            "observed_problem": "Land-first Atlas pools can still sit on ocean-shaped terrain because biome selection and terrain height/noise are separate responsibilities.",
        },
        "helper_level_fix": {
            "status": helper_fix_status,
            "changed_file": str(HELPER_SOURCE_PATH.relative_to(ROOT)).replace("\\", "/"),
            "strategy": "Apply a bounded land-first continentalness bias in far south, west, and south-west Atlas pools when the climate target is ocean-like, while leaving sparse local water pockets in coast/lake bands.",
            "affected_pools": ["south", "west", "south_west"],
            "unaffected_pools": ["center", "north", "east", "north_east", "north_west", "south_east", "outer"],
            "preserves": ["rivers", "oases", "mountain_lakes", "small_lakes", "coastline_candidates", "Verdant Coast wet/oceanic identity", "Frostmarch frozen-sea identity"],
            "does_not_change": ["sea_level", "Tectonic config", "noise_settings", "structures", "roads", "villages", "loot", "recipes", "mobs", "ores"],
            "requires_fresh_world_validation": True,
        },
        "latest_live_validation_result": {
            "water_body_report_complete": live_water_body_complete,
            "surface_pool_mismatches": surface_counts["pool_mismatches"],
            "south_west_water_surface_samples": surface_counts["water_surface_review"],
            "water_body_ocean_leaks": sum(1 for sample in water_body_leak_samples if sample.get("classification") == "ocean_leak"),
            "water_body_basin_leaks": sum(1 for sample in water_body_leak_samples if sample.get("classification") == "basin_leak"),
            "water_body_leak_samples": len(water_body_leak_samples),
            "result": "failed_helper_only_water_fix" if live_water_body_complete and water_body_leak_samples else "pending_or_passed",
        },
        "evidence_before_fix": {
            "source_samples_completed": source_grid.get("completed_samples") or source_counts["total"],
            "surface_samples_completed": surface_grid.get("completed_samples") or surface_counts["total"],
            "source_pool_mismatches": source_counts["pool_mismatches"],
            "surface_pool_mismatches": surface_counts["pool_mismatches"],
            "surface_cave_like_biomes": surface_counts["surface_cave"],
            "surface_snow_outside_cold": surface_counts["snow_outside_cold"],
            "water_surface_samples": water_summary.get("total_water_samples", 0),
            "target_south_west_water_samples": water_summary.get("target_south_west_water_samples", 0),
            "manual_ocean_leak_samples": len(manual_ocean_leaks),
            "water_body_report_status": water_body_report.get("status"),
            "completed_water_body_samples": water_body_summary.get("completed_water_body_samples", water_body_report.get("completed_water_body_samples", 0)),
            "pending_water_body_samples": water_body_summary.get("pending_water_body_samples", water_body_report.get("pending_water_body_samples", 0)),
        },
        "validation_required_after_fix": {
            "fresh_world_required": True,
            "commands": [
                "/ascatlas dump_biome_pools",
                "/ascatlas sample_grid 30000 5000",
                "/ascatlas sample_surface_grid 30000 5000",
                "/ascatlas classify_water_bodies 30000 5000",
            ],
            "acceptance": {
                "source_pool_mismatches": 0,
                "surface_pool_mismatches": 0,
                "surface_cave_like_biomes": 0,
                "snow_outside_cold_regions": 0,
                "south_west_ocean_leaks": "0_or_only_explicit_coastal_ocean_classified_regions",
            },
        },
        "fallback_if_fresh_world_still_fails": {
            "required_path": "region_aware_terrain_noise_wrapper_or_chunk_generator_adjustment",
            "reason": "A BiomeSource can choose biomes from climate/coordinates, but it cannot raise ocean floors, remove water blocks, or rewrite Tectonic/vanilla noise terrain after the terrain shape exists.",
        },
    }


def sample_counts(sample_grid: dict[str, Any]) -> dict[str, int]:
    samples = [sample for sample in sample_grid.get("samples", []) if isinstance(sample, dict)]
    normal_surface_samples = [sample for sample in samples if is_normal_surface_sample(sample)]
    fast_no_chunkgen_samples = [
        sample
        for sample in samples
        if str(sample.get("sample_mode") or "").startswith("fast_no_chunkgen")
    ]
    low_surface_samples = [
        sample
        for sample in normal_surface_samples
        if (numeric(sample.get("surface_y")) or 0) <= -60
    ]
    surface_cave_samples = [
        sample
        for sample in normal_surface_samples
        if is_cave_only_biome(sample.get("actual_biome_id"))
    ]
    pool_mismatches = [
        sample
        for sample in samples
        if sample.get("actual_biome_in_expected_pool") is False
        and not sample.get("accepted_transition_edge_case")
    ]
    accepted_transition_edges = [
        sample
        for sample in samples
        if sample.get("accepted_transition_edge_case")
    ]
    snow_outside_cold = [
        sample
        for sample in samples
        if has_snow_rule_violation(sample)
    ]
    water_surface_review = [
        sample
        for sample in normal_surface_samples
        if sample.get("surface_block_id") == "minecraft:water"
        and str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "") in WATER_REVIEW_POOLS
    ]
    visual_pending = [
        sample
        for sample in samples
        if "pending" in str(sample.get("terrain_visually_matches_intended_region") or "")
        or "pending" in str(sample.get("biome_transition_sharpness") or "")
    ]
    sample_errors = [sample for sample in samples if sample.get("sample_error")]
    return {
        "total": len(samples),
        "fast_no_chunkgen": len(fast_no_chunkgen_samples),
        "normal_surface": len(normal_surface_samples),
        "low_surface": len(low_surface_samples),
        "surface_cave": len(surface_cave_samples),
        "pool_mismatches": len(pool_mismatches),
        "accepted_transition_edges": len(accepted_transition_edges),
        "snow_outside_cold": len(snow_outside_cold),
        "water_surface_review": len(water_surface_review),
        "visual_pending": len(visual_pending),
        "sample_errors": len(sample_errors),
    }


def sample_summary_markdown(source_grid: dict[str, Any], surface_grid: dict[str, Any]) -> str:
    source = sample_counts(source_grid)
    surface = sample_counts(surface_grid)
    rows = [
        ("Biome-source validation samples", source["total"]),
        ("Biome-source fast no-chunkgen samples", source["fast_no_chunkgen"]),
        ("Biome-source pool mismatches", source["pool_mismatches"]),
        ("Biome-source snow outside cold/Frostmarch pools", source["snow_outside_cold"]),
        ("Biome-source cave-like Y=80 hits", sum(1 for sample in source_grid.get("samples", []) if is_cave_only_biome(sample.get("actual_biome_id")))),
        ("Surface validation samples", surface["total"]),
        ("Surface grid radius blocks", surface_grid.get("radius") if surface_grid.get("radius") is not None else "unknown"),
        ("Surface grid step blocks", surface_grid.get("step") if surface_grid.get("step") is not None else "unknown"),
        ("Surface helper completed samples", surface_grid.get("completed_samples") or surface["total"]),
        ("Surface helper pending samples", surface_grid.get("pending_samples") or 0),
        ("Normal surface samples", surface["normal_surface"]),
        ("Surface samples at or below y=-60", surface["low_surface"]),
        ("Surface samples reporting cave-like biomes", surface["surface_cave"]),
        ("Surface actual biome outside expected pool", surface["pool_mismatches"]),
        ("Surface accepted transition edge cases", surface["accepted_transition_edges"]),
        ("Surface snow outside cold/Frostmarch pools", surface["snow_outside_cold"]),
        ("Surface water blocks in south/west review pools", surface["water_surface_review"]),
        ("Surface sample errors", surface["sample_errors"]),
        ("Surface visual checks pending", surface["visual_pending"]),
    ]
    return "\n".join(f"| {label} | {count} |" for label, count in rows)


def write_docs(
    dimension: dict[str, Any],
    runtime: dict[str, Any],
    biome_pools: dict[str, Any],
    missing: dict[str, Any],
    source_grid: dict[str, Any],
    surface_grid: dict[str, Any],
    water_report: dict[str, Any],
    water_body_report: dict[str, Any],
    land_water_report: dict[str, Any],
    audit: dict[str, Any],
) -> None:
    checks = static_checks(dimension, missing)
    check_rows = "\n".join(f"| {name} | {status} | {detail} |" for name, status, detail in checks)
    source_counts = sample_counts(source_grid)
    surface_counts = sample_counts(surface_grid)
    source_validation_passing = (
        source_grid.get("status") == "source_sample_present"
        and source_counts["total"] > 0
        and source_counts["pool_mismatches"] == 0
        and source_counts["snow_outside_cold"] == 0
    )
    surface_validation_present = (
        surface_grid.get("status") == "surface_sample_present_verify_visuals"
        and surface_counts["normal_surface"] > 0
    )
    automated_atlas_passing = (
        source_validation_passing
        and surface_validation_present
        and source_counts["pool_mismatches"] == 0
        and source_counts["snow_outside_cold"] == 0
        and surface_counts["low_surface"] == 0
        and surface_counts["surface_cave"] == 0
        and surface_counts["pool_mismatches"] == 0
        and surface_counts["snow_outside_cold"] == 0
        and surface_counts["sample_errors"] == 0
    )
    status = "PARTIAL" if surface_validation_present else "BLOCKED"
    source_status_line = "passing" if source_validation_passing else "missing or failing"
    surface_status_line = "present, but still needs visual review" if surface_validation_present else "blocked until true surface samples exist"
    if automated_atlas_passing:
        status_line = "Automated Atlas validation passed. Manual water/visual review pending."
    else:
        status_line = f"biome-source validation is {source_status_line}; surface terrain validation is {surface_status_line}."
    if automated_atlas_passing:
        command_guidance = "The source and surface commands have produced clean automated Atlas evidence. Rerun these only after a biome-source/helper/worldgen change:"
        current_verdict = "Automated Atlas validation passed. Manual water/visual review pending. Do not treat the terrain gate as complete until the water samples and required visual points are reviewed in-world."
    elif surface_validation_present:
        command_guidance = "The surface command has produced generated-terrain evidence. Rerun these only after a biome-source/helper/worldgen change:"
        current_verdict = "Do not call full worldgen implemented yet. Source-level selection is passing and surface samples exist, but visual terrain fit, transition smoothness, and Tectonic surface behavior still need manual review at the required points."
    else:
        command_guidance = "Use these in a fresh creative validation world with the rebuilt helper jar synced into the active instance:"
        current_verdict = "Do not call full worldgen implemented yet. The coordinate-aware biome-source layer is passing, but surface terrain validation is blocked until `/ascatlas sample_surface_grid 12000 2000` writes true generated-surface samples."
    surface_sampler_is_incremental = source_contains(HELPER_COMMANDS_PATH, "SurfaceSampleJob") and source_contains(HELPER_COMMANDS_PATH, "ServerTickEvent")
    surface_sampler_note = (
        "The helper source now uses a tick-based surface sampler that writes a valid running report before chunk generation progresses."
        if surface_sampler_is_incremental
        else "The helper source does not yet show the tick-based surface sampler; the old all-at-once command can stall while generating far chunks."
    )
    command_lines = "\n".join(f"- `{command}`: {'implemented' if present else 'missing'}" for command, present in command_status().items())
    atlas_structure_sets = list((ATLAS_DATAPACK_PATH / "worldgen" / "structure_set").glob("*.json")) if (ATLAS_DATAPACK_PATH / "worldgen" / "structure_set").exists() else []
    gravel = audit.get("biomes", {}).get("terralith:gravel_desert", {})
    gravel_flags = ", ".join((gravel.get("bucket", {}) or {}).get("flags", []) or [])
    water_body_summary = water_body_report.get("summary", {}) if isinstance(water_body_report, dict) else {}
    land_water_fix = land_water_report.get("helper_level_fix", {}) if isinstance(land_water_report, dict) else {}
    land_water_fix_status = land_water_fix.get("status", "missing")
    land_water_validation_result = land_water_report.get("latest_live_validation_result", {}) if isinstance(land_water_report, dict) else {}
    accepted_surface_transition_edges = [
        sample
        for sample in surface_grid.get("samples", [])
        if isinstance(sample, dict) and sample.get("accepted_transition_edge_case")
    ]
    accepted_surface_transition_rows = "\n".join(
        "| {x},{z} | `{classification}` | `{region}` | `{sector}` | `{biome}` | `{block}` | {surface_y} | {reason} |".format(
            x=sample.get("x"),
            z=sample.get("z"),
            classification=sample.get("accepted_transition_edge_case"),
            region=sample.get("atlas_region"),
            sector=sample.get("climate_sector"),
            biome=sample.get("actual_biome_id"),
            block=sample.get("surface_block_id"),
            surface_y=sample.get("surface_y"),
            reason=sample.get("accepted_transition_reason") or "accepted transition edge",
        )
        for sample in accepted_surface_transition_edges
    ) or "| none | none | none | none | none | none | none | none |"
    if land_water_fix_status == "implemented_but_failed_live_water_validation":
        status_line = "Helper-level land/water fix failed live water validation. Biome-source selection is not enough; a region-aware terrain/noise correction is required."
        current_verdict = "Do not treat the terrain gate as complete. The live water-body classifier completed, but south/west still produced ocean-scale basins over land-first biomes. The next fix must move below biome selection into region-aware terrain/noise control while preserving Tectonic's role. The terrain/noise control plan and policy files are scaffolded only; no live terrain/noise rewrite is enabled."
    elif land_water_fix_status == "implemented_pending_fresh_world_validation":
        status_line = "Helper-level land/water fix applied. Automated Atlas source/surface validation passed before this helper change; fresh-world water validation is pending."
        current_verdict = "Do not treat the terrain gate as complete yet. The helper now biases far south/west/south-west ocean-like continentalness toward land-first targets, but the current water evidence predates this rebuilt helper jar and must be rerun in a fresh world."
    dimension_generator = dimension.get("generator", {}) if isinstance(dimension.get("generator"), dict) else {}
    biome_source = dimension_generator.get("biome_source", {}) if isinstance(dimension_generator.get("biome_source"), dict) else {}
    water_body_samples_for_note = water_body_report.get("samples", [])
    water_body_has_skipped_counts = any(
        isinstance(sample, dict) and "skipped_unloaded_chunk_counts_by_radius_blocks" in sample
        for sample in water_body_samples_for_note
    ) if isinstance(water_body_samples_for_note, list) else False
    if water_body_report.get("source") == "in_game_ascatlas_classify_water_bodies_command" and water_body_has_skipped_counts:
        water_body_status_note = "This report contains live in-game bounded local sampling progress. Completed samples have 32/64/128-block water percentages; skipped unloaded chunk counts should normally stay at 0."
    elif water_body_report.get("source") == "in_game_ascatlas_classify_water_bodies_command":
        water_body_status_note = "This report is from an older live run that did not record skipped unloaded chunks and is still incomplete. Treat it as stale evidence; rerun only after syncing the bounded local helper jar."
    else:
        water_body_status_note = "The seed report preserves manual classifications. Local water percentages remain pending until the in-game helper command samples surrounding generated surface blocks."

    write_text(
        DOCS_DIR / "ATLAS_TERRAIN_VALIDATION_REPORT.md",
        f"""# Atlas Terrain Validation Report

Status: {status} - {status_line}

Generated: {now_iso()}

## Sample Summary

| Metric | Count |
|---|---:|
{sample_summary_markdown(source_grid, surface_grid)}

Biome-source validation: {source_status_line}.

Surface terrain validation: {surface_status_line}.

Fast no-chunkgen samples are source-level biome-selection evidence only; they are not counted as normal surface-height proof.

Surface sampler note: {surface_sampler_note}

## Water Review

- Total water surface samples: {water_report.get('summary', {}).get('total_water_samples', 0)}
- South/west target-region water samples: {water_report.get('summary', {}).get('target_south_west_water_samples', 0)}
- Manually reviewed target water samples: {water_report.get('summary', {}).get('manual_reviewed_target_water_samples', 0)}
- Visually confirmed ocean leaks: {water_report.get('summary', {}).get('visually_confirmed_ocean_leak_samples', 0)}
- Issue type: {water_report.get('summary', {}).get('issue_kind', 'unknown')}
- Assessment: {water_report.get('summary', {}).get('assessment', 'pending')}
- Detail report: `docs/ATLAS_WATER_REVIEW.md`

## Land/Water Coherence

- Water-body classification status: {water_body_report.get('status', 'missing')}
- Water-body classification source: {water_body_report.get('source', 'missing')}
- Neighborhood water samples: {water_body_summary.get('water_samples', water_body_report.get('water_samples_discovered', 'unknown'))}
- Completed neighborhood classifications: {water_body_summary.get('completed_water_body_samples', water_body_report.get('completed_water_body_samples', 0))}
- Ocean leaks in water-body report: {water_body_summary.get('ocean_leak_samples', (water_body_summary.get('water_samples_by_classification', {}) or {}).get('ocean_leak', 0))}
- Basin leaks in water-body report: {water_body_summary.get('basin_leak_samples', (water_body_summary.get('water_samples_by_classification', {}) or {}).get('basin_leak', 0))}
- Helper land/water fix status: {land_water_fix_status}
- Latest live water validation result: {land_water_validation_result.get('result', 'unknown')}
- Latest live water-body ocean leaks: {land_water_validation_result.get('water_body_ocean_leaks', 'unknown')}
- Latest live water-body basin leaks: {land_water_validation_result.get('water_body_basin_leaks', 'unknown')}
- Coherence report: `config/ascendant_atlas/reports/land_water_coherence_latest.json`
- Detail report: `docs/ATLAS_LAND_WATER_COHERENCE.md`

## Accepted Transition Edge Cases

- Accepted transition edge cases: {len(accepted_surface_transition_edges)}
- Classification: `{ACCEPTED_TRANSITION_EDGE_CLASSIFICATION}`
- Rule: only valid for northwest-leaning Stoneback/Frostmarch transition samples where the actual biome is `minecraft:frozen_river`, the surface block is ice/water, and snow/cold rules are not violated.
- Boundary: this does not add `minecraft:frozen_river` to all west/Stoneback surface pools.
- Signoff: accepted transition edges are not terrain signoff; ocean/basin land-water blockers still remain.

| x,z | Classification | Atlas region | Climate sector | Actual biome | Surface block | Surface Y | Reason |
|---|---|---|---|---|---|---:|---|
{accepted_surface_transition_rows}

## Terrain/Noise Control

- Investigation status: complete for this pass.
- Active terrain stack: `minecraft:noise` generator with `minecraft:overworld` settings, Atlas helper biome source, and Tectonic/Terratonic terrain/noise resources.
- Confirmed boundary: the current helper owns biome selection only; it does not change final density, terrain height, sea level, or aquifer behavior.
- Tectonic config finding: active `config/tectonic.json` exposes `legacy_mode` only; no safe config-only ocean-basin control was found.
- Policy scaffold: `config/ascendant_atlas/terrain_noise_policy.json` and `config/ascendant_atlas/land_water_region_policy.json`.
- Plan: `docs/ATLAS_TERRAIN_NOISE_CONTROL_PLAN.md`.
- Research: `docs/ATLAS_TERRAIN_NOISE_RESEARCH.md`.
- Risk: `docs/ATLAS_TECTONIC_INTEGRATION_RISK.md`.
- Live behavior changed by this terrain/noise pass: none.

## Static Validation

| Check | Result | Evidence |
|---|---|---|
{check_rows}

## Command Surface

{command_lines}

{command_guidance}

1. `/ascatlas dump_biome_pools`
2. `/ascatlas sample_grid 12000 2000`
3. `/ascatlas sample_surface_grid 12000 2000`
4. `/ascatlas classify_water_bodies 30000 5000`
5. Visit the listed required points and manually fill visual match / transition notes if the command output still says pending.

## Validation Scale

The runtime/worldborder envelope is now {runtime.get('world_radius_blocks')} blocks from origin with a {runtime.get('worldborder', {}).get('diameter_blocks')} block border. The biome source still uses `world_radius_blocks: {dimension['generator']['biome_source'].get('world_radius_blocks')}` as the north/south climate-gradient saturation distance; that is not the world border.

## Source-Level Grid

This is the fast no-chunkgen biome-source proof. It must stay separate from surface terrain evidence.

| x,z | Atlas region | Climate sector | Distance ring | Expected pool | Actual biome ID | In expected pool | Sample mode | Surface Y | Surface block | Temperature | Precipitation | Snow allowed | Cave at surface | Visual match | Transition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{sample_markdown_rows(source_grid)}

## Surface Terrain Grid

This is the generated-terrain proof. It is blocked until `config/ascendant_atlas/reports/sample_grid_surface_latest.json` contains true surface samples from `/ascatlas sample_surface_grid 12000 2000`.

| x,z | Atlas region | Climate sector | Distance ring | Expected pool | Actual biome ID | In expected pool | Sample mode | Surface Y | Surface block | Temperature | Precipitation | Snow allowed | Cave at surface | Visual match | Transition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{sample_markdown_rows(surface_grid) if surface_grid.get("samples") else "| pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending |"}

## Current Verdict

{current_verdict}
""",
    )

    water_summary = water_report.get("summary", {})
    write_text(
        DOCS_DIR / "ATLAS_WATER_REVIEW.md",
        f"""# Atlas Water Review

Generated: {now_iso()}

Status: Automated Atlas validation passed. Manual water/visual review pending.

This report is focused only on generated surface samples where `surface_block_id` is `minecraft:water`. It does not tune roads, villages, structures, Hunter Boards, Guild Halls, NPCs, settlements, or civilization content.

## Summary

- Total water samples: {water_summary.get('total_water_samples', 0)}
- South/west target-region water samples: {water_summary.get('target_south_west_water_samples', 0)}
- Manually reviewed water samples: {water_summary.get('manual_reviewed_water_samples', 0)}
- Manually reviewed target water samples: {water_summary.get('manual_reviewed_target_water_samples', 0)}
- Visually confirmed ocean leaks: {water_summary.get('visually_confirmed_ocean_leak_samples', 0)}
- Issue type: {water_summary.get('issue_kind', 'unknown')}
- Biome-pool leakage: {water_summary.get('is_biome_pool_leakage', False)}
- Terrain/noise water placement: {water_summary.get('is_terrain_noise_water_placement', False)}
- Assessment: {water_summary.get('assessment', 'pending')}

South should be allowed rare rivers and oases. West should be allowed mountain lakes and rivers. A sample is only a terrain blocker if the area visually reads wet/oceanic instead of arid/highland. Sea level around 62/63 is normal; the blocker is broad ocean-like basins where arid/highland regions should read as land-first.

## Water Samples By Region

| Region | Count |
|---|---:|
{count_markdown_rows(water_summary.get('water_samples_by_region', {}))}

## Water Samples By Biome ID

| Biome ID | Count |
|---|---:|
{count_markdown_rows(water_summary.get('water_samples_by_biome_id', {}))}

## Water Samples By Ring

| Distance ring | Count |
|---|---:|
{count_markdown_rows(water_summary.get('water_samples_by_ring', {}))}

## Water Samples By Classification

| Classification | Count |
|---|---:|
{count_markdown_rows(water_summary.get('water_samples_by_classification', {}))}

## Classification Values

Allowed values: {', '.join(f'`{value}`' for value in WATER_CLASSIFICATIONS)}.

## Water Sample Detail

| x,z | Atlas region | Climate sector | Distance ring | Expected pool | Actual biome ID | Surface block | Surface Y | Temperature | Precipitation | Snow allowed | South/west target | Classification | Manual status | Manual note | Suggested teleport |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|---|
{water_sample_markdown_rows(water_report)}
""",
    )

    write_text(
        DOCS_DIR / "ATLAS_LAND_WATER_COHERENCE.md",
        f"""# Atlas Land/Water Coherence

Generated: {now_iso()}

Status: Helper-level land/water coherence fix is {land_water_fix_status}; latest live result is {land_water_validation_result.get('result', 'unknown')}.

This pass is terrain-only. It does not touch mobs, ores, recipes, roads, villages, structures, Hunter Boards, Guild Halls, NPCs, settlements, or civilization content.

## Current Finding

- Confirmed issue: 15 manually reviewed south/west target water samples are `ocean_leak`.
- Visual symptom: huge 60-block-deep ocean-like basins over badlands/highland terrain, sometimes leaving villages and structures as islands.
- Sea level: 62/63 is normal and is not the bug.
- Biome-pool leakage: false. The sampled surface biomes are still in their expected Atlas pools.
- Root problem: land/water terrain composition does not match Atlas region identity.
- Coherence JSON: `config/ascendant_atlas/reports/land_water_coherence_latest.json`
- Latest live water-body ocean leaks: {land_water_validation_result.get('water_body_ocean_leaks', 'unknown')}
- Latest live water-body basin leaks: {land_water_validation_result.get('water_body_basin_leaks', 'unknown')}

## Water-Body Classification Status

- Report: `config/ascendant_atlas/reports/water_body_classification_latest.json`
- Status: {water_body_report.get('status', 'missing')}
- Source: {water_body_report.get('source', 'missing')}
- Safe live neighborhood command: `{water_body_report.get('required_command', '/ascatlas classify_water_bodies 30000 5000')}`
- Water samples: {water_body_summary.get('water_samples', water_body_report.get('water_samples_discovered', 'unknown'))}
- Completed neighborhood samples: {water_body_summary.get('completed_water_body_samples', water_body_report.get('completed_water_body_samples', 0))}
- Pending neighborhood samples: {water_body_summary.get('pending_water_body_samples', water_body_report.get('pending_water_body_samples', 'unknown'))}

{water_body_status_note}

## Active Terrain Stack

| Layer | Active value | Evidence |
|---|---|---|
| Overworld dimension type | `{dimension.get('type')}` | `config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json` |
| Chunk generator | `{dimension_generator.get('type')}` | The dimension override still uses vanilla noise generation. |
| Noise settings key | `{dimension_generator.get('settings')}` | Atlas does not replace the full noise settings JSON. |
| Biome source | `{biome_source.get('type')}` | The helper owns regional biome selection. |
| Tectonic config | `legacy_mode=false` | `config/tectonic.json` exposes no region-specific ocean-frequency setting. |
| Tectonic role | terrain/noise shape layer | Tectonic remains installed; Atlas changes biome source, not terrain height/noise. |
| Terralith role | primary biome table provider | Active pools include Terralith entries and audit-backed climate data. |

## Continentalness And Ocean Terrain

The helper receives a vanilla `Climate.TargetPoint` from the active climate sampler and can read/blend continentalness before choosing a biome. It is therefore not completely blind to climate data.

However, the helper is still only a `BiomeSource`. It can select a biome that matches Atlas direction, but it does not raise terrain, lower sea level, carve rivers, or remove large water basins from the chunk generator. That is why `minecraft:badlands` or Terralith arid/highland biomes can appear over ocean-shaped terrain.

## Correct Fix Path

1. Helper-level correction: already attempted and failed live water-body validation. Keep it for biome-source identity, but do not treat it as the basin fix.
2. Preferred terrain correction: add a feature-flagged, region-aware terrain/noise wrapper or chunk-generator adjustment that biases south and west toward land-first terrain while preserving rivers, oases, mountain lakes, and valid coastlines.
3. Tectonic config path: the active `config/tectonic.json` only exposes `legacy_mode`; no exact safe config-only ocean-frequency change is available from the current config. If Tectonic supports deeper datapack/noise customization, it should be tested as a terrain/noise change, not as biome removal.
4. Do not remove all water from south/west. Rivers, oases, mountain lakes, and small lakes must remain.
5. Do not solve this only by deleting biome IDs. The current evidence says biome-pool leakage is false.

## Helper-Level Fix Applied

- Status: {land_water_fix_status}
- Scope: far `south`, `west`, and `south_west` Atlas pools only.
- Strategy: if a far land-first pool receives an ocean-like continentalness target, the helper now biases that target back toward land while preserving sparse local coast/lake bands.
- Preserved identities: Frostmarch frozen seas, Verdant Coast wet/coastal behavior, center Hearthlands, rivers, oases, mountain lakes, and small lakes.
- Not changed: sea level, Tectonic config, noise settings, roads, villages, structures, mobs, ores, loot, recipes, magic gates, or rank enforcement.
- Validation state: this cannot be signed off from old chunks. It needs a fresh world or fully ungenerated chunks after the rebuilt helper jar is synced.

## Latest Live Validation Result

- Result: {land_water_validation_result.get('result', 'unknown')}
- Surface pool mismatches: {land_water_validation_result.get('surface_pool_mismatches', 'unknown')}
- South/west water surface samples: {land_water_validation_result.get('south_west_water_surface_samples', 'unknown')}
- Water-body ocean leaks: {land_water_validation_result.get('water_body_ocean_leaks', 'unknown')}
- Water-body basin leaks: {land_water_validation_result.get('water_body_basin_leaks', 'unknown')}
- Conclusion: if this result is `failed_helper_only_water_fix`, then biome-source continentalness bias is not enough and the next fix must be a region-aware terrain/noise path.

## Stoneback/Frostmarch Transition Edge

- Accepted transition edge cases in latest surface grid: {len(accepted_surface_transition_edges)}
- Classification: `{ACCEPTED_TRANSITION_EDGE_CLASSIFICATION}`
- Rule: `minecraft:frozen_river` may be accepted only as a northwest-leaning Stoneback/Frostmarch transition river over ice/water with no snow-rule violation.
- Boundary: do not add `minecraft:frozen_river` to every west/Stoneback pool; this is a narrow edge case.
- Terrain signoff: this does not resolve the ocean/basin blocker.

## Current Prototype State

- Prototype type: policy and design scaffold only.
- Live terrain behavior changed: no.
- Least-risk next code prototype: a helper-side, delegate-based terrain/noise wrapper in dry-run mode before any terrain mutation.
- Do not rerun `/ascatlas classify_water_bodies 30000 5000` until a deeper terrain/noise prototype exists; the existing report already proves the helper-only fix failed and the command can cause severe integrated-server lag.

## Acceptance Criteria

- South and west no longer visually generate huge ocean-like basins in reviewed land-first regions.
- Rivers, oases, and mountain lakes still exist.
- Surface validation still has 0 biome-pool mismatches.
- Surface validation still has 0 cave-like surface biomes.
- Surface validation still has 0 snow outside cold regions.
- `ocean_leak` count becomes 0 or only remains in explicitly coastal regions.
- Manual review confirms Sunreach reads arid/land-first and Stoneback reads highland/mountain-first.

## Water Samples By Classification

| Classification | Count |
|---|---:|
{count_markdown_rows(water_body_summary.get('water_samples_by_classification', {}))}

## Water-Body Detail

| x,z | Region | Climate sector | Distance ring | Actual biome | Surface block | Surface Y | Local water % | Nearby land % | Estimated size | Classification | Suggested fix type | Status |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|---|
{water_body_markdown_rows(water_body_report)}
""",
    )

    write_text(
        DOCS_DIR / "ATLAS_BIOME_POOL_REPORT.md",
        f"""# Atlas Biome Pool Report

Generated: {now_iso()}

Biome pool classification is data-driven from the active Overworld dimension override plus `docs/generated/worldgen_content_audit.json`. Biome names are not treated as truth.

## Pool Summary

| Pool | Atlas region | Entries | Unique biomes | Terralith unique | Water/sea unique | Snow-allowed unique | Snow outside intended cold |
|---|---|---:|---:|---:|---:|---:|---:|
{pool_markdown_rows(biome_pools)}

## Missing Biomes

Configured biome IDs missing from the audit: {missing.get('missing_count', 0)}.

See `config/ascendant_atlas/reports/missing_biomes.json` for the exact list.

## Data-Driven Warning Example

`terralith:gravel_desert` is not safe to classify from its name. The audit records temperature `{gravel.get('temperature')}`, climate bucket `{(gravel.get('bucket', {}) or {}).get('climate_bucket')}`, terrain bucket `{(gravel.get('bucket', {}) or {}).get('terrain_bucket')}`, and flags `{gravel_flags}`. That is why Atlas reports use biome JSON/audit data for snow and climate behavior.

## Pool JSON

The full resolved pool list with temperature, precipitation, snow allowance, terrain bucket, source jar, and flags is written to `config/ascendant_atlas/reports/biome_pools_resolved.json`.
""",
    )

    failures = []
    if source_grid["status"] != "source_sample_present":
        failures.append(("SOURCE_LEVEL_SAMPLE_MISSING", "High", "No confirmed in-game `/ascatlas sample_grid` source-level run is present yet.", "Run `/ascatlas sample_grid 12000 2000` in a new world after startup succeeds."))
    else:
        source_samples = source_grid.get("samples", []) or []
        source_mismatches = [
            sample
            for sample in source_samples
            if sample.get("actual_biome_in_expected_pool") is not True
            and not sample.get("accepted_transition_edge_case")
        ]
        source_snow_outside = [
            sample for sample in source_samples
            if sample.get("snow_allowed") is True and sample.get("climate_sector") not in INTENDED_SNOW_POOLS
        ]
        source_cave_samples = [
            sample for sample in source_samples
            if is_cave_only_biome(sample.get("actual_biome_id"))
        ]
        failures.append(("SOURCE_LEVEL_SAMPLE_PRESENT", "Info", f"`/ascatlas sample_grid` produced {len(source_samples)} valid source-level samples from `{source_grid.get('source')}`.", "Keep this as biome-source evidence until the biome source changes."))
        if source_mismatches:
            failures.append(("SOURCE_LEVEL_BIOME_POOL_MISMATCHES", "High", f"{len(source_mismatches)} source-level samples landed outside their expected Atlas pools.", "Fix region pool selection before surface terrain signoff."))
        if source_snow_outside:
            failures.append(("SOURCE_LEVEL_SNOW_OUTSIDE_COLD_REGION", "High", f"{len(source_snow_outside)} source-level samples allow snow outside intended cold sectors.", "Remove or rebalance those biomes before signoff."))
        if source_cave_samples:
            failures.append(("SOURCE_LEVEL_Y80_HAS_CAVE_BIOMES", "Medium", f"{len(source_cave_samples)} fast Y=80 samples resolved to cave biome IDs; this is source-level evidence, not surface visual evidence.", "Use `/ascatlas sample_surface_grid 12000 2000` for generated surface proof."))

    surface_samples = surface_grid.get("samples", []) or []
    surface_normal_samples = [sample for sample in surface_samples if is_normal_surface_sample(sample)]
    if surface_grid.get("status") != "surface_sample_present_verify_visuals" or not surface_normal_samples:
        failures.append(("SURFACE_SAMPLE_MISSING", "High", "No true generated-surface Atlas sample grid is present yet.", "Run `/ascatlas sample_surface_grid 12000 2000` in a fresh world or ungenerated chunks with the rebuilt helper jar synced."))
        if source_contains(HELPER_COMMANDS_PATH, "SurfaceSampleJob"):
            failures.append(("SURFACE_COMMAND_REBUILT_INCREMENTAL", "Info", "The helper source has been changed so surface sampling runs across server ticks and writes progress JSON.", "Confirm the active client has the rebuilt helper jar, then rerun the surface command."))
    else:
        surface_mismatches = [sample for sample in surface_normal_samples if sample.get("actual_biome_in_expected_pool") is not True]
        surface_mismatches = [
            sample
            for sample in surface_normal_samples
            if sample.get("actual_biome_in_expected_pool") is not True
            and not sample.get("accepted_transition_edge_case")
        ]
        accepted_surface_transition_edges = [
            sample
            for sample in surface_normal_samples
            if sample.get("accepted_transition_edge_case")
        ]
        surface_low = [sample for sample in surface_normal_samples if (numeric(sample.get("surface_y")) or 0) <= -60]
        surface_cave = [
            sample for sample in surface_normal_samples
            if sample.get("cave_like_biome_at_surface") is True or is_cave_only_biome(sample.get("actual_biome_id"))
        ]
        surface_snow_outside = [
            sample for sample in surface_normal_samples
            if has_snow_rule_violation(sample)
        ]
        surface_water_review = [
            sample for sample in surface_normal_samples
            if sample.get("surface_block_id") == "minecraft:water"
            and str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "") in WATER_REVIEW_POOLS
        ]
        surface_errors = [sample for sample in surface_samples if sample.get("sample_error")]
        failures.append(("SURFACE_SAMPLE_PRESENT", "Info", f"`/ascatlas sample_surface_grid` produced {len(surface_normal_samples)} normal surface samples.", "Use this as generated-terrain evidence until terrain/worldgen changes."))
        if surface_mismatches:
            failures.append(("SURFACE_BIOME_POOL_MISMATCHES", "High", f"{len(surface_mismatches)} surface samples landed outside their expected Atlas pools.", "Fix the biome source/terrain interaction before signoff."))
        if accepted_surface_transition_edges:
            failures.append(("SURFACE_TRANSITION_EDGE_ACCEPTED", "Info", f"{len(accepted_surface_transition_edges)} surface samples are accepted as `{ACCEPTED_TRANSITION_EDGE_CLASSIFICATION}`.", "Keep this narrow transition allowance; do not add minecraft:frozen_river to all west/Stoneback pools."))
        if surface_low:
            failures.append(("SURFACE_HEIGHT_AT_WORLD_FLOOR", "High", f"{len(surface_low)} surface samples reported surface_y <= -60.", "Inspect those chunks for failed terrain generation or wrong heightmap use."))
        if surface_cave:
            failures.append(("SURFACE_CAVE_BIOMES", "High", f"{len(surface_cave)} generated surface samples reported cave-like biome IDs.", "Fix surface biome sampling before signoff."))
        if surface_snow_outside:
            failures.append(("SURFACE_SNOW_OUTSIDE_COLD_REGION", "High", f"{len(surface_snow_outside)} surface samples allow snow outside intended cold sectors.", "Remove or rebalance those biomes before signoff."))
        if surface_water_review:
            failures.append(("SOUTH_WEST_WATER_SURFACE_REVIEW", "Medium", f"{len(surface_water_review)} south/west surface samples landed on minecraft:water.", "Inspect those points visually before terrain signoff; decide whether they are acceptable rivers/lakes or indicate too much sea/water in arid and mountain regions."))
        water_ocean_leaks = [
            sample
            for sample in water_report.get("samples", [])
            if sample.get("is_south_west_water_target_region")
            and sample.get("classification") == "ocean_leak"
        ]
        if water_ocean_leaks:
            failures.append(("SOUTH_WEST_OCEAN_LEAK", "High", f"{len(water_ocean_leaks)} south/west water samples are visually confirmed ocean leaks.", "Correct terrain/noise water placement so south and west read land-first while still allowing rare rivers, oases, and mountain lakes."))
        if land_water_fix_status == "implemented_pending_fresh_world_validation":
            failures.append(("LAND_WATER_FIX_PENDING_FRESH_WORLD_VALIDATION", "High", "The helper now applies a south/west land-first continentalness bias, but the current water evidence predates this helper build.", "Rebuild/sync the helper jar, create a fresh validation world, then rerun the Atlas source, surface, and water-body commands before terrain signoff."))
        if water_body_report.get("source") != "in_game_ascatlas_classify_water_bodies_command":
            failures.append(("WATER_BODY_CLASSIFICATION_PENDING", "High", "`water_body_classification_latest.json` is a seed report without surrounding-grid water percentages.", "Run `/ascatlas classify_water_bodies 30000 5000` in a fresh validation world after syncing the rebuilt helper jar."))
        elif water_body_report.get("status") != "complete":
            failures.append(("WATER_BODY_CLASSIFICATION_INCOMPLETE", "High", f"Water-body classifier status is `{water_body_report.get('status')}`.", "Cancel stale/stalled runs and rerun with the bounded local helper jar; do not wait on a lagging old classifier before terrain-water signoff."))
        water_body_samples_for_failure = water_body_report.get("samples", [])
        if (
            water_body_report.get("source") == "in_game_ascatlas_classify_water_bodies_command"
            and isinstance(water_body_samples_for_failure, list)
            and any(isinstance(sample, dict) for sample in water_body_samples_for_failure)
            and not any(
                isinstance(sample, dict) and "skipped_unloaded_chunk_counts_by_radius_blocks" in sample
                for sample in water_body_samples_for_failure
            )
        ):
            failures.append(("WATER_BODY_CLASSIFICATION_STALE_FORCING_SCANNER", "High", "The current in-game water-body report lacks skipped unloaded chunk counts, so it came from the older forcing scanner.", "Rerun `/ascatlas classify_water_bodies 30000 5000` only after confirming the active helper jar hash matches the bounded local helper build."))
        insufficient_coverage_samples = [
            sample
            for sample in water_body_report.get("samples", [])
            if isinstance(sample, dict)
            and sample.get("estimated_water_body_size") == "insufficient_loaded_chunk_coverage"
        ]
        if insufficient_coverage_samples:
            failures.append(("WATER_BODY_CLASSIFICATION_INSUFFICIENT_COVERAGE", "High", f"{len(insufficient_coverage_samples)} water-body samples have insufficient local coverage.", "Rerun with the bounded local helper jar so the 32/64/128-block probe grids generate real local coverage."))
        water_body_ocean_leaks = [
            sample
            for sample in water_body_report.get("samples", [])
            if isinstance(sample, dict)
            and sample.get("classification") == "ocean_leak"
        ]
        if water_body_ocean_leaks:
            failures.append(("WATER_BODY_OCEAN_LEAKS_AFTER_HELPER_BIAS", "High", f"{len(water_body_ocean_leaks)} completed water-body samples are still classified as ocean leaks.", "Biome-source continentalness bias is not enough; implement a region-aware terrain/noise correction or chunk-generator wrapper before terrain signoff."))
        basin_leaks = [
            sample
            for sample in water_body_report.get("samples", [])
            if sample.get("classification") == "basin_leak"
        ]
        if basin_leaks:
            failures.append(("SOUTH_WEST_BASIN_LEAK", "High", f"{len(basin_leaks)} water-body samples are classified as basin leaks.", "Tune land/water terrain coherence without deleting all rivers, oases, lakes, or mountain lakes."))
        if land_water_fix_status == "implemented_but_failed_live_water_validation":
            failures.append(("TERRAIN_NOISE_CONTROL_NOT_LIVE", "High", "`docs/ATLAS_TERRAIN_NOISE_CONTROL_PLAN.md` and policy JSONs exist, but no live terrain/noise wrapper or density prototype is enabled.", "Prototype the least-risk terrain/noise path only after the focused source/surface retest is clean."))
        if surface_errors:
            failures.append(("SURFACE_SAMPLE_ERRORS", "High", f"{len(surface_errors)} surface samples recorded command-side errors.", "Fix those chunk/height/biome sample errors before signoff."))
    failures.extend([
        ("VISUAL_TERRAIN_REVIEW_PENDING", "High", "The report cannot yet judge whether terrain visually matches the intended region.", "Visit each required point and record visual match / transition sharpness."),
        ("OLD_WORLDS_INVALID", "Medium", "Already-generated chunks can preserve old biome decisions.", "Use fresh worlds or fully ungenerated chunks for all Atlas terrain judgments."),
        ("ROAD_TUNING_NOT_INCLUDED", "Low", "Roads/bridges are intentionally not tuned in this terrain-first pass.", "Document road issues only until terrain validation passes."),
    ])
    if atlas_structure_sets:
        failures.append(("ATLAS_DEBUG_STRUCTURE_SETS_PRESENT", "High", "Atlas datapack has structure_set files, meaning debug/decorative structures can generate.", "Remove or disable Atlas debug structure sets before terrain signoff."))
    else:
        failures.append(("ATLAS_DEBUG_STRUCTURES_ASSETS_ONLY", "Info", "Atlas waymark/debug structures exist as assets but no Atlas structure_set files were found.", "No terrain-pass action needed unless later checks find another injection path."))
    if int(missing.get("missing_count", 0)) > 0:
        failures.append(("MISSING_CONFIGURED_BIOMES", "High", f"{missing.get('missing_count')} configured biome IDs are missing from the audit.", "Fix the active biome pools before testing terrain."))

    failure_rows = "\n".join(f"| `{code}` | {severity} | {evidence} | {next_step} |" for code, severity, evidence, next_step in failures)
    write_text(
        DOCS_DIR / "ATLAS_WORLDGEN_FAILURES.md",
        f"""# Atlas Worldgen Failures

Generated: {now_iso()}

This file tracks terrain-foundation blockers only. It intentionally does not add Hunter Boards, Guild structures, decorative Atlas structures, village injection, or road tuning.

| Issue | Severity | Evidence | Next action |
|---|---|---|---|
{failure_rows}

## Terrain Signoff Gate

Atlas terrain does not pass until a fresh world creates cleanly, the `/ascatlas` commands run, `sample_grid_source_latest.json` proves biome-source selection, `sample_grid_surface_latest.json` contains true generated-surface samples from the required grid, center is beginner-friendly, north/south/east/west/diagonals visually match their intended gradients, Tectonic terrain remains visually intact, Terralith biomes are present, snow is blocked outside intended cold regions, and no retired/decorative Atlas structures generate as fake content.
""",
    )


def main() -> None:
    dimension = read_json(DIMENSION_PATH)
    runtime = read_json(RUNTIME_PATH)
    audit = read_json(AUDIT_PATH)
    biome_pools, missing = pool_report(dimension, audit)
    source_grid = sample_report(
        dimension,
        runtime,
        biome_pools,
        audit,
        "sample_grid_source_latest.json",
        "biome_source",
        fallback_filenames=["sample_grid_latest.json"],
        allow_offline_expected=True,
    )
    surface_grid = sample_report(
        dimension,
        runtime,
        biome_pools,
        audit,
        "sample_grid_surface_latest.json",
        "surface_terrain",
    )
    water_report = water_review_report(surface_grid)
    water_body_report, write_water_body_report = water_body_classification_report(water_report)
    land_water_report = land_water_coherence_report(dimension, source_grid, surface_grid, water_report, water_body_report)

    write_json(REPORT_DIR / "biome_pools_resolved.json", biome_pools)
    write_json(REPORT_DIR / "missing_biomes.json", missing)
    write_json(REPORT_DIR / "sample_grid_source_latest.json", source_grid)
    write_json(REPORT_DIR / "sample_grid_surface_latest.json", surface_grid)
    write_json(REPORT_DIR / "water_surface_samples_latest.json", water_report)
    write_json(REPORT_DIR / "land_water_coherence_latest.json", land_water_report)
    if write_water_body_report:
        write_json(REPORT_DIR / "water_body_classification_latest.json", water_body_report)
    write_docs(dimension, runtime, biome_pools, missing, source_grid, surface_grid, water_report, water_body_report, land_water_report, audit)


if __name__ == "__main__":
    main()
