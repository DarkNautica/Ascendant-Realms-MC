#!/usr/bin/env python3
"""Audit active biome, structure, and spawn content for Atlas placement decisions."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
import gzip
import io
import json
import math
from pathlib import Path
import zipfile

from nbt import nbt


ROOT = Path(__file__).resolve().parents[1]
INSTANCE = Path(r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)")
MINECRAFT_JAR = Path(r"C:\Users\Jayden\curseforge\minecraft\Install\versions\1.20.1\1.20.1.jar")
OUTPUT_JSON = ROOT / "docs/generated/worldgen_content_audit.json"
OUTPUT_MD = ROOT / "docs/WORLDGEN_CONTENT_AUDIT.md"
TERRALITH_OVERWORLD = "data/minecraft/dimension/overworld.json"

BIOME_PATH = "/worldgen/biome/"
STRUCTURE_PATH = "/worldgen/structure/"
STRUCTURE_SET_PATH = "/worldgen/structure_set/"
TEMPLATE_POOL_PATH = "/worldgen/template_pool/"
STRUCTURE_NBT_PATH = "/structures/"

LANDMARK_BLOCK_TOKENS = {
    "wood": ["_log", "_wood", "planks", "stairs", "slab", "fence", "door", "trapdoor"],
    "chest": ["chest", "barrel"],
    "ice": ["ice", "snow", "frosted"],
    "sand": ["sand", "terracotta", "red_sand"],
    "stone": ["stone", "deepslate", "cobble", "andesite", "diorite", "granite", "tuff"],
    "prismarine": ["prismarine", "sea_lantern", "coral"],
    "nether": ["netherrack", "basalt", "blackstone", "soul_", "nether"],
    "end": ["end_stone", "purpur", "chorus"],
    "metal": ["iron", "chain", "copper", "gold", "anvil"],
    "vegetation": ["leaves", "sapling", "flower", "grass", "moss", "vine", "mushroom"],
}


@dataclass(frozen=True)
class ResourceSource:
    label: str
    path: Path
    priority: int
    kind: str


def read_json_text(text: str) -> dict | list | None:
    try:
        return json.loads(text)
    except Exception:
        return None


def resource_id_from_path(path: str, marker: str, suffix: str = ".json") -> str | None:
    path = path.replace("\\", "/")
    if not path.startswith("data/") or marker not in path or not path.endswith(suffix):
        return None
    namespace = path.split("/", 2)[1]
    rest = path.split(marker, 1)[1][:-len(suffix)]
    return f"{namespace}:{rest}"


def iter_sources() -> list[ResourceSource]:
    sources: list[ResourceSource] = []
    if MINECRAFT_JAR.exists():
        sources.append(ResourceSource("minecraft-1.20.1", MINECRAFT_JAR, 0, "jar"))

    mods = INSTANCE / "mods"
    if mods.exists():
        for jar in sorted(mods.glob("*.jar")):
            sources.append(ResourceSource(jar.name, jar, 10, "jar"))

    # Pack-owned data overrides should win over jar defaults for duplicated ids.
    for label, folder, priority in [
        ("source-openloader", ROOT / "openloader/data", 80),
        ("active-openloader-source", ROOT / "config/openloader/data", 90),
        ("active-instance-openloader", INSTANCE / "config/openloader/data", 100),
    ]:
        if folder.exists():
            for pack in sorted(path for path in folder.iterdir() if path.is_dir()):
                sources.append(ResourceSource(f"{label}:{pack.name}", pack, priority, "dir"))
    return sources


def collect_json_resources(sources: list[ResourceSource], marker: str) -> dict[str, dict]:
    found: dict[str, dict] = {}
    source_lists: dict[str, list[str]] = defaultdict(list)
    for source in sources:
        if source.kind == "jar":
            try:
                with zipfile.ZipFile(source.path) as jar:
                    for name in jar.namelist():
                        rid = resource_id_from_path(name, marker)
                        if not rid:
                            continue
                        data = read_json_text(jar.read(name).decode("utf-8"))
                        if isinstance(data, dict):
                            current = found.get(rid)
                            if current is None or source.priority >= current["_priority"]:
                                data = dict(data)
                                data["_source"] = source.label
                                data["_path"] = name
                                data["_priority"] = source.priority
                                found[rid] = data
                            source_lists[rid].append(source.label)
            except zipfile.BadZipFile:
                continue
        else:
            for file in source.path.rglob("*.json"):
                rel = file.relative_to(source.path).as_posix()
                rid = resource_id_from_path(rel, marker)
                if not rid:
                    continue
                data = read_json_text(file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    current = found.get(rid)
                    if current is None or source.priority >= current["_priority"]:
                        data = dict(data)
                        data["_source"] = source.label
                        data["_path"] = rel
                        data["_priority"] = source.priority
                        found[rid] = data
                    source_lists[rid].append(source.label)
    for rid, data in found.items():
        data["_sources_seen"] = sorted(set(source_lists[rid]))
    return found


def collect_nbt_templates(sources: list[ResourceSource]) -> dict[str, tuple[ResourceSource, str, bytes]]:
    found: dict[str, tuple[ResourceSource, str, bytes]] = {}
    for source in sources:
        if source.kind == "jar":
            try:
                with zipfile.ZipFile(source.path) as jar:
                    for name in jar.namelist():
                        rid = resource_id_from_path(name, STRUCTURE_NBT_PATH, ".nbt")
                        if not rid:
                            continue
                        current = found.get(rid)
                        if current is None or source.priority >= current[0].priority:
                            found[rid] = (source, name, jar.read(name))
            except zipfile.BadZipFile:
                continue
        else:
            for file in source.path.rglob("*.nbt"):
                rel = file.relative_to(source.path).as_posix()
                rid = resource_id_from_path(rel, STRUCTURE_NBT_PATH, ".nbt")
                if not rid:
                    continue
                current = found.get(rid)
                if current is None or source.priority >= current[0].priority:
                    found[rid] = (source, rel, file.read_bytes())
    return found


def collect_terralith_climate_entries(sources: list[ResourceSource]) -> dict[str, list[dict]]:
    entries: dict[str, list[dict]] = defaultdict(list)
    overworld_data = None
    for source in sources:
        if source.kind != "jar" or not source.label.lower().startswith("terralith"):
            continue
        try:
            with zipfile.ZipFile(source.path) as jar:
                if TERRALITH_OVERWORLD in jar.namelist():
                    overworld_data = read_json_text(jar.read(TERRALITH_OVERWORLD).decode("utf-8"))
                    break
        except zipfile.BadZipFile:
            continue

    if not isinstance(overworld_data, dict):
        return entries

    biome_source = overworld_data.get("generator", {}).get("biome_source", {})
    if biome_source.get("type") == "minecraft:multi_noise":
        biome_entries = biome_source.get("biomes", [])
    elif biome_source.get("type") == "terrablender:overworld":
        biome_entries = biome_source.get("biomes", [])
    else:
        biome_entries = biome_source.get("biomes", [])

    for entry in biome_entries:
        if not isinstance(entry, dict):
            continue
        biome = entry.get("biome")
        params = entry.get("parameters", {})
        if isinstance(biome, str) and isinstance(params, dict):
            entries[biome].append(params)
    return entries


def flatten_feature_ids(value) -> list[str]:
    ids: list[str] = []
    if isinstance(value, str):
        ids.append(value)
    elif isinstance(value, list):
        for item in value:
            ids.extend(flatten_feature_ids(item))
    elif isinstance(value, dict):
        for item in value.values():
            ids.extend(flatten_feature_ids(item))
    return ids


def param_midpoint(value) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, list) and len(value) == 2:
        try:
            return (float(value[0]) + float(value[1])) / 2.0
        except Exception:
            return None
    return None


def climate_summary(params: list[dict]) -> dict:
    result: dict[str, dict] = {}
    for key in ["temperature", "humidity", "continentalness", "erosion", "weirdness", "depth"]:
        values = [param_midpoint(entry.get(key)) for entry in params]
        values = [value for value in values if value is not None]
        if values:
            result[key] = {
                "min": round(min(values), 4),
                "max": round(max(values), 4),
                "avg": round(sum(values) / len(values), 4),
            }
    result["entry_count"] = len(params)
    return result


def bucket_biome(biome_id: str, biome: dict, climate: dict) -> dict:
    temperature = biome.get("temperature")
    downfall = biome.get("downfall")
    precipitation = biome.get("precipitation")
    has_precipitation = biome.get("has_precipitation")
    feature_ids = flatten_feature_ids(biome.get("features", []))
    spawners = biome.get("spawners", {})
    continental_avg = climate.get("continentalness", {}).get("avg")

    flags: set[str] = set()
    if isinstance(temperature, (int, float)):
        if temperature <= 0.05:
            flags.add("freezing")
        elif temperature <= 0.35:
            flags.add("cold")
        elif temperature >= 1.0:
            flags.add("hot")
        elif temperature >= 0.75:
            flags.add("warm")
        else:
            flags.add("temperate")
    if has_precipitation is True and isinstance(downfall, (int, float)) and downfall > 0.55:
        flags.add("wet")
    if precipitation == "snow" or (has_precipitation is True and isinstance(temperature, (int, float)) and temperature <= 0.15):
        flags.add("snow_precipitation")
    if isinstance(continental_avg, (int, float)):
        if continental_avg < -0.45:
            flags.add("oceanic_noise")
        elif continental_avg < -0.12:
            flags.add("coastal_noise")
        else:
            flags.add("land_noise")
    feature_text = " ".join(feature_ids).lower()
    for flag, tokens in [
        ("ice_features", ["freeze_top_layer", "/snowy/", "iceberg", "packed_ice", "blue_ice"]),
        ("tree_features", ["tree", "forest", "vegetation", "patch_grass", "flower"]),
        ("aquatic_features", ["kelp", "seagrass", "coral", "sea_pickle", "warm_ocean_vegetation"]),
        ("desert_features", ["cactus", "desert", "dead_bush"]),
        ("mountain_features", ["ore_emerald", "rock", "boulder", "spring_lava"]),
    ]:
        if any(token in feature_text for token in tokens):
            flags.add(flag)
    if spawners:
        flags.add("has_spawns")

    if "oceanic_noise" in flags or "coastal_noise" in flags or "aquatic_features" in flags:
        terrain = "water_or_sea"
    elif "mountain_features" in flags:
        terrain = "mountain_or_highland"
    else:
        terrain = "land"

    if "hot" in flags or (
        isinstance(temperature, (int, float))
        and temperature >= 0.65
        and isinstance(downfall, (int, float))
        and downfall <= 0.35
        and "desert_features" in flags
    ):
        climate_bucket = "hot_arid"
    elif "freezing" in flags or "snow_precipitation" in flags:
        climate_bucket = "frozen_or_snow"
    elif "cold" in flags:
        climate_bucket = "cold"
    elif "warm" in flags:
        climate_bucket = "warm"
    elif "wet" in flags:
        climate_bucket = "temperate_wet"
    else:
        climate_bucket = "temperate"

    return {
        "climate_bucket": climate_bucket,
        "terrain_bucket": terrain,
        "flags": sorted(flags),
    }


def continental_bucket(params: dict) -> str:
    midpoint = param_midpoint(params.get("continentalness"))
    if midpoint is None:
        return "unknown"
    if midpoint < -0.455:
        return "deep_ocean_noise"
    if midpoint < -0.20:
        return "sea_noise"
    if midpoint < 0.05:
        return "coast_or_lowland_noise"
    return "inland_noise"


def collect_atlas_region_review(biome_audit: dict[str, dict]) -> dict:
    dimension_path = ROOT / "config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json"
    if not dimension_path.exists():
        return {}
    dimension = json.loads(dimension_path.read_text(encoding="utf-8"))
    source = dimension.get("generator", {}).get("biome_source", {})
    review = {}
    for region in [
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
        entries = source.get(region, [])
        climate_counts = Counter()
        terrain_counts = Counter()
        biome_counts = Counter()
        flagged: dict[str, list[str]] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            biome_id = entry.get("biome")
            params = entry.get("parameters", {})
            if isinstance(biome_id, str):
                biome_counts[biome_id] += 1
            noise_bucket = continental_bucket(params)
            terrain_counts[noise_bucket] += 1
            biome_info = biome_audit.get(str(biome_id), {})
            climate_bucket = biome_info.get("bucket", {}).get("climate_bucket", "unknown")
            climate_counts[climate_bucket] += 1
        for biome_id in biome_counts:
            warnings = []
            biome_info = biome_audit.get(biome_id, {})
            bucket = biome_info.get("bucket", {})
            if region == "center":
                if bucket.get("terrain_bucket") == "water_or_sea":
                    warnings.append("water_biome_in_center")
                if bucket.get("climate_bucket") in ["frozen_or_snow", "cold"]:
                    warnings.append("cold_or_snow_biome_in_center")
            if region == "north" and bucket.get("terrain_bucket") == "water_or_sea":
                warnings.append("water_biome_in_north")
            if region in ["south", "south_west"] and bucket.get("climate_bucket") in ["frozen_or_snow", "cold"]:
                warnings.append("cold_or_snow_biome_in_south")
            if warnings:
                flagged[biome_id] = warnings
        total = sum(terrain_counts.values()) or 1
        review[region] = {
            "entry_count": len(entries),
            "climate_buckets": dict(climate_counts.most_common()),
            "terrain_noise_buckets": dict(terrain_counts.most_common()),
            "water_noise_entry_share": round(
                (terrain_counts["deep_ocean_noise"] + terrain_counts["sea_noise"]) / total,
                4,
            ),
            "top_biomes_by_entry_count": dict(biome_counts.most_common(20)),
            "flagged_biomes": flagged,
        }
    return review


def decode_nbt(data: bytes):
    try:
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        return nbt.NBTFile(buffer=io.BytesIO(data))
    except Exception:
        return None


def count_template_blocks(template_bytes: bytes) -> Counter:
    parsed = decode_nbt(template_bytes)
    counts: Counter = Counter()
    if parsed is None:
        return counts
    palette = parsed.get("palette")
    blocks = parsed.get("blocks")
    if palette is None or blocks is None:
        return counts
    palette_names: list[str] = []
    for entry in palette:
        name = entry.get("Name")
        palette_names.append(str(name.value if hasattr(name, "value") else name))
    for block in blocks:
        state = block.get("state")
        if state is None:
            continue
        idx = int(state.value)
        if 0 <= idx < len(palette_names):
            counts[palette_names[idx]] += 1
    return counts


def template_locations_from_pool(pool: dict) -> list[str]:
    locations: list[str] = []

    def visit(value):
        if isinstance(value, dict):
            location = value.get("location")
            if isinstance(location, str):
                locations.append(location)
            for nested in value.values():
                visit(nested)
        elif isinstance(value, list):
            for nested in value:
                visit(nested)

    visit(pool.get("elements", []))
    return locations


def block_tags(counts: Counter) -> dict:
    total = sum(counts.values()) or 1
    tag_counts: dict[str, int] = {}
    for tag, tokens in LANDMARK_BLOCK_TOKENS.items():
        tag_counts[tag] = sum(count for block, count in counts.items() if any(token in block for token in tokens))
    dominant = [tag for tag, count in tag_counts.items() if count / total >= 0.05]
    return {
        "total_blocks_sampled": total,
        "dominant_materials": sorted(dominant),
        "material_counts": {key: value for key, value in sorted(tag_counts.items()) if value},
        "top_blocks": dict(counts.most_common(20)),
    }


def main() -> None:
    sources = iter_sources()
    biomes = collect_json_resources(sources, BIOME_PATH)
    structures = collect_json_resources(sources, STRUCTURE_PATH)
    structure_sets = collect_json_resources(sources, STRUCTURE_SET_PATH)
    template_pools = collect_json_resources(sources, TEMPLATE_POOL_PATH)
    templates = collect_nbt_templates(sources)
    climate_entries = collect_terralith_climate_entries(sources)

    biome_audit: dict[str, dict] = {}
    mob_evidence: dict[str, dict] = defaultdict(lambda: {"biomes": Counter(), "spawn_groups": Counter(), "climate_buckets": Counter()})
    for biome_id, biome in sorted(biomes.items()):
        climate = climate_summary(climate_entries.get(biome_id, []))
        bucket = bucket_biome(biome_id, biome, climate)
        spawner_count = 0
        for group, entries in biome.get("spawners", {}).items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, dict) or not isinstance(entry.get("type"), str):
                    continue
                mob = entry["type"]
                spawner_count += 1
                mob_evidence[mob]["biomes"][biome_id] += int(entry.get("weight", 1) or 1)
                mob_evidence[mob]["spawn_groups"][group] += int(entry.get("weight", 1) or 1)
                mob_evidence[mob]["climate_buckets"][bucket["climate_bucket"]] += int(entry.get("weight", 1) or 1)
        biome_audit[biome_id] = {
            "source": biome.get("_source"),
            "temperature": biome.get("temperature"),
            "downfall": biome.get("downfall"),
            "precipitation": biome.get("precipitation"),
            "climate": climate,
            "bucket": bucket,
            "feature_count": len(flatten_feature_ids(biome.get("features", []))),
            "spawner_entry_count": spawner_count,
        }

    structure_sets_by_structure: dict[str, list[dict]] = defaultdict(list)
    for set_id, set_data in structure_sets.items():
        placement = set_data.get("placement", {})
        for entry in set_data.get("structures", []):
            if isinstance(entry, dict) and isinstance(entry.get("structure"), str):
                structure_sets_by_structure[entry["structure"]].append({
                    "structure_set": set_id,
                    "spacing": placement.get("spacing"),
                    "separation": placement.get("separation"),
                    "salt": placement.get("salt"),
                    "source": set_data.get("_source"),
                })

    structure_audit: dict[str, dict] = {}
    structure_spawn_evidence: dict[str, list[str]] = defaultdict(list)
    for structure_id, structure in sorted(structures.items()):
        pools_to_check = []
        start_pool = structure.get("start_pool")
        if isinstance(start_pool, str):
            pools_to_check.append(start_pool)
        template_ids: list[str] = []
        for pool_id in pools_to_check:
            pool = template_pools.get(pool_id)
            if pool:
                template_ids.extend(template_locations_from_pool(pool))
        counts: Counter = Counter()
        for template_id in sorted(set(template_ids)):
            source_tuple = templates.get(template_id)
            if source_tuple:
                counts.update(count_template_blocks(source_tuple[2]))
        overrides = structure.get("spawn_overrides", {})
        for group, override in overrides.items():
            if not isinstance(override, dict):
                continue
            for spawn in override.get("spawns", []):
                if isinstance(spawn, dict) and isinstance(spawn.get("type"), str):
                    structure_spawn_evidence[spawn["type"]].append(structure_id)
        structure_audit[structure_id] = {
            "source": structure.get("_source"),
            "type": structure.get("type"),
            "biomes": structure.get("biomes"),
            "step": structure.get("step"),
            "start_pool": start_pool,
            "structure_sets": structure_sets_by_structure.get(structure_id, []),
            "templates_sampled": len(set(template_ids)),
            "block_profile": block_tags(counts),
            "spawn_override_groups": sorted(overrides.keys()) if isinstance(overrides, dict) else [],
        }

    mob_audit = {}
    for mob, data in sorted(mob_evidence.items()):
        mob_audit[mob] = {
            "biome_count": len(data["biomes"]),
            "top_biomes": dict(data["biomes"].most_common(12)),
            "spawn_groups": dict(data["spawn_groups"].most_common()),
            "climate_buckets": dict(data["climate_buckets"].most_common()),
            "structure_overrides": sorted(structure_spawn_evidence.get(mob, [])),
        }
    for mob, structures_for_mob in sorted(structure_spawn_evidence.items()):
        if mob not in mob_audit:
            mob_audit[mob] = {
                "biome_count": 0,
                "top_biomes": {},
                "spawn_groups": {},
                "climate_buckets": {},
                "structure_overrides": sorted(structures_for_mob),
            }

    region_review = collect_atlas_region_review(biome_audit)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": [{"label": source.label, "path": str(source.path), "kind": source.kind} for source in sources],
        "counts": {
            "biomes": len(biome_audit),
            "structures": len(structure_audit),
            "structure_sets": len(structure_sets),
            "template_pools": len(template_pools),
            "templates": len(templates),
            "mobs_with_json_spawn_evidence": len(mob_audit),
        },
        "region_review": region_review,
        "biomes": biome_audit,
        "structures": structure_audit,
        "mobs": mob_audit,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    flagged_lines = []
    for region, review in region_review.items():
        if review["flagged_biomes"]:
            flagged_lines.append(f"- `{region}`: " + ", ".join(f"`{biome}` ({', '.join(flags)})" for biome, flags in review["flagged_biomes"].items()))
    if not flagged_lines:
        flagged_lines.append("- No current Atlas region flags from the JSON audit.")

    north_biomes = region_review.get("north", {})
    top_structure_density = []
    for structure_id, audit in structure_audit.items():
        for set_info in audit["structure_sets"]:
            spacing = set_info.get("spacing")
            try:
                spacing_value = int(spacing)
            except Exception:
                continue
            if spacing_value and spacing_value <= 12:
                top_structure_density.append((spacing_value, structure_id, set_info))
    top_structure_density = sorted(top_structure_density)[:20]

    md = [
        "# Worldgen Content Audit",
        "",
        f"Generated: {output['generated_at']}",
        "",
        "This audit reads active Minecraft, mod jar, and OpenLoader data instead of classifying only by names.",
        "",
        "## Counts",
        "",
        f"- Biomes with JSON: {output['counts']['biomes']}",
        f"- Structures with JSON: {output['counts']['structures']}",
        f"- Structure templates indexed: {output['counts']['templates']}",
        f"- Mobs with JSON spawn evidence: {output['counts']['mobs_with_json_spawn_evidence']}",
        "",
        "## Current Atlas Region Flags",
        "",
        *flagged_lines,
        "",
        "## North Region Snapshot",
        "",
        f"- Climate buckets: `{north_biomes.get('climate_buckets', {})}`",
        f"- Terrain noise buckets: `{north_biomes.get('terrain_noise_buckets', {})}`",
        f"- Water/sea noise entry share: `{north_biomes.get('water_noise_entry_share')}`",
        "",
        "## Dense Structure Sets To Review",
        "",
    ]
    if top_structure_density:
        for spacing, structure_id, set_info in top_structure_density:
            md.append(f"- `{structure_id}` via `{set_info['structure_set']}` spacing `{spacing}`, separation `{set_info.get('separation')}`")
    else:
        md.append("- No structure sets at spacing 12 or below after current overrides.")
    md.extend([
        "",
        "## Data Limits",
        "",
        "- Mobs registered only through mod code are not fully visible in JSON. This audit records biome JSON spawns and structure spawn overrides, then marks code-only behavior for in-game/runtime testing.",
        "- Structure block profiles sample the direct start-pool templates first. Deep jigsaw children still need spot checks for major settlement packs.",
        "",
        f"Full machine-readable output: `{OUTPUT_JSON.relative_to(ROOT).as_posix()}`",
        "",
    ])
    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_MD.relative_to(ROOT)}")
    print(json.dumps(output["counts"], indent=2))


if __name__ == "__main__":
    main()
