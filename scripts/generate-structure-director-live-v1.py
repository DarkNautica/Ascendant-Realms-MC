#!/usr/bin/env python3
"""Generate Ascendant Structure Director Live v1 resources.

This script intentionally writes only pack-owned policy, docs, rollback
snapshots, and OpenLoader datapack overrides. It does not touch live instances.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_INSTANCE = Path(r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)")
ACTIVE_MODS = ACTIVE_INSTANCE / "mods"
CONFIG_DIR = ROOT / "config" / "ascendant_structures"
DATAPACK = ROOT / "config" / "openloader" / "data" / "ascendant_structure_director_live"
ROLLBACK_DIR = CONFIG_DIR / "rollback" / "pre_structure_director_v1"
VERSION = "structure_director_live_v1"

# Evidence registries can contain biome IDs from optional mods or older pack states.
# Keep live OpenLoader tags free of IDs proven missing from the current pack.
MISSING_BIOME_IDS = {
    "projectvibrantjourneys:baobab_fields",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalize(data: bytes) -> bytes:
    return json.dumps(json.loads(data.decode("utf-8")), indent=2, ensure_ascii=False).encode("utf-8") + b"\n"


def read_original(resource_path: str, jar_name: str | None = None, source_path: Path | None = None) -> tuple[bytes, str]:
    if source_path is not None and source_path.exists():
        return source_path.read_bytes(), str(source_path.relative_to(ROOT))
    if jar_name is None:
        raise FileNotFoundError(resource_path)
    jar_path = ACTIVE_MODS / jar_name
    if not jar_path.exists():
        raise FileNotFoundError(f"Missing active jar for {resource_path}: {jar_path}")
    with zipfile.ZipFile(jar_path) as jar:
        with jar.open(resource_path) as handle:
            return handle.read(), f"{jar_name}!/{resource_path}"


def write_override(
    resource_path: str,
    data: dict[str, Any],
    source_bytes: bytes | None,
    source_label: str,
    live_changes: list[dict[str, Any]],
    rollback_files: list[dict[str, Any]],
    rule_id: str,
    evidence_ids: list[str],
    description: str,
) -> Path:
    output = DATAPACK / resource_path
    write_json(output, data)
    live_hash = sha256_file(output)
    if source_bytes is not None:
        rollback_path = ROLLBACK_DIR / "resources" / resource_path
        rollback_path.parent.mkdir(parents=True, exist_ok=True)
        rollback_path.write_bytes(source_bytes)
        rollback_files.append(
            {
                "resource_path": resource_path,
                "source": source_label,
                "rollback_path": str(rollback_path.relative_to(ROOT)).replace("\\", "/"),
                "source_sha256": sha256_bytes(source_bytes),
                "live_sha256": live_hash,
            }
        )
    live_changes.append(
        {
            "rule_id": rule_id,
            "resource_path": resource_path,
            "source": source_label,
            "live_sha256": live_hash,
            "evidence_ids": evidence_ids,
            "description": description,
        }
    )
    return output


def set_spacing(original: dict[str, Any], spacing: int, separation: int, exclusion_chunk_count: int | None = None) -> dict[str, Any]:
    data = json.loads(json.dumps(original))
    placement = data.setdefault("placement", {})
    placement["spacing"] = spacing
    placement["separation"] = separation
    if exclusion_chunk_count is not None:
        zone = placement.get("exclusion_zone") or placement.get("super_exclusion_zone")
        if isinstance(zone, dict):
            zone["chunk_count"] = exclusion_chunk_count
        else:
            placement["exclusion_zone"] = {"chunk_count": exclusion_chunk_count, "other_set": "minecraft:villages"}
    return data


def entry_set(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(row.get(key)): row for row in rows if isinstance(row, dict) and row.get(key)}


def clean_biomes(row: dict[str, Any], *, allow_wet_land: bool = False) -> list[Any]:
    bad_fragments = [
        "ocean",
        "river",
        "beach",
        "cave",
        "deep_dark",
        "swamp",
        "mangrove",
        "marsh",
        "isles",
        "lake",
    ]
    if allow_wet_land:
        bad_fragments = [part for part in bad_fragments if part not in {"swamp", "mangrove", "marsh"}]
    values: list[Any] = []
    for biome in row.get("allowed_biome_ids_if_resolved", []):
        if not isinstance(biome, str):
            continue
        if biome in MISSING_BIOME_IDS:
            continue
        if any(part in biome for part in bad_fragments):
            continue
        values.append(biome)
    return sorted(set(values))


def selected_structure_sets() -> list[dict[str, Any]]:
    return [
        {
            "set": "iceandfire:dragon_roost",
            "jar": "IceAndFireCE-1.2.5-1.20.1-forge.jar",
            "path": "data/iceandfire/worldgen/structure_set/dragon_roost.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": 16,
            "rule": "dragon_roost_land_first_rare",
            "evidence": [
                "iceandfire:fire_dragon_roost",
                "iceandfire:ice_dragon_roost",
                "iceandfire:lightning_dragon_roost",
            ],
        },
        {
            "set": "iceandfire:dragon_cave",
            "jar": "IceAndFireCE-1.2.5-1.20.1-forge.jar",
            "path": "data/iceandfire/worldgen/structure_set/dragon_cave.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": 16,
            "rule": "dragon_cave_underground_rare",
            "evidence": [
                "iceandfire:fire_dragon_cave",
                "iceandfire:ice_dragon_cave",
                "iceandfire:lightning_dragon_cave",
            ],
        },
        {
            "set": "iceandfire:siren_island",
            "jar": "IceAndFireCE-1.2.5-1.20.1-forge.jar",
            "path": "data/iceandfire/worldgen/structure_set/siren_island.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": None,
            "rule": "siren_island_ocean_only_rare",
            "evidence": ["iceandfire:siren_island"],
        },
        {
            "set": "idas:idas_rare",
            "jar": "idas_forge-1.13.0+1.20.1.jar",
            "path": "data/idas/worldgen/structure_set/idas_rare.json",
            "spacing": 72,
            "separation": 36,
            "exclusion": 5,
            "rule": "idas_rare_major_dungeon_spacing",
            "evidence": ["idas:labyrinth"],
        },
        {
            "set": "idas:idas_ocean",
            "jar": "idas_forge-1.13.0+1.20.1.jar",
            "path": "data/idas/worldgen/structure_set/idas_ocean.json",
            "spacing": 72,
            "separation": 36,
            "exclusion": 5,
            "rule": "idas_ocean_cluster_reduction",
            "evidence": ["idas:sunken_ship/sunken_ship", "idas:iceandfire/sirens_cove"],
        },
        {
            "set": "betterdungeons:small_dungeons",
            "jar": "YungsBetterDungeons-1.20-Forge-4.0.4.jar",
            "path": "data/betterdungeons/worldgen/structure_set/small_dungeons.json",
            "spacing": 32,
            "separation": 12,
            "exclusion": None,
            "rule": "yung_small_dungeons_density_reduction",
            "evidence": ["betterdungeons:small_dungeon"],
        },
        {
            "set": "bettermineshafts:mineshafts",
            "jar": "YungsBetterMineshafts-1.20-Forge-4.0.4.jar",
            "path": "data/bettermineshafts/worldgen/structure_set/mineshafts.json",
            "spacing": 32,
            "separation": 12,
            "exclusion": None,
            "rule": "yung_mineshaft_density_reduction",
            "evidence": ["bettermineshafts:mineshaft_acacia"],
        },
        {
            "set": "aquamirae:surface",
            "jar": None,
            "source_path": ROOT / "config/openloader/data/ascendant_realms_world_integration/data/aquamirae/worldgen/structure_set/surface.json",
            "path": "data/aquamirae/worldgen/structure_set/surface.json",
            "spacing": 28,
            "separation": 10,
            "exclusion": None,
            "rule": "aquamirae_surface_cluster_reduction",
            "evidence": ["aquamirae:surface/arch", "aquamirae:surface/spiral"],
        },
        {
            "set": "cataclysm:abandoned_structures",
            "jar": "L_Enders_Cataclysm-3.30.jar",
            "path": "data/cataclysm/worldgen/structure_set/abandoned_structures.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": 12,
            "rule": "cataclysm_abandoned_major_spacing",
            "evidence": ["cataclysm:abandoned_spire", "cataclysm:abandoned_temple", "cataclysm:abandoned_village"],
        },
        {
            "set": "cataclysm:amethyst_nest",
            "jar": "L_Enders_Cataclysm-3.30.jar",
            "path": "data/cataclysm/worldgen/structure_set/amethyst_nest.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": None,
            "rule": "cataclysm_amethyst_nest_major_spacing",
            "evidence": ["cataclysm:amethyst_nest"],
        },
        {
            "set": "cataclysm:desert_structures",
            "jar": "L_Enders_Cataclysm-3.30.jar",
            "path": "data/cataclysm/worldgen/structure_set/desert_structures.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": 12,
            "rule": "cataclysm_desert_major_spacing",
            "evidence": ["cataclysm:desert_site", "cataclysm:desert_occupied_village"],
        },
        {
            "set": "block_factorys_bosses:sandworm_nest",
            "jar": "block_factorys_bosses-2.1.2-forge-1.20.1.jar",
            "path": "data/block_factorys_bosses/worldgen/structure_set/sandworm_nest.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": None,
            "rule": "sandworm_nest_boss_spacing",
            "evidence": ["block_factorys_bosses:sandworm_nest"],
        },
        {
            "set": "block_factorys_bosses:yeti_hideout",
            "jar": "block_factorys_bosses-2.1.2-forge-1.20.1.jar",
            "path": "data/block_factorys_bosses/worldgen/structure_set/yeti_hideout.json",
            "spacing": 96,
            "separation": 48,
            "exclusion": None,
            "rule": "yeti_hideout_boss_spacing",
            "evidence": ["block_factorys_bosses:yeti_hideout"],
        },
        {
            "set": "towns_and_towers:towns",
            "jar": "Towns-and-Towers-1.12-Fabric+Forge.jar",
            "path": "data/towns_and_towers/worldgen/structure_set/towns.json",
            "spacing": 64,
            "separation": 32,
            "exclusion": 10,
            "rule": "towns_and_towers_settlement_overlap_reduction",
            "evidence": ["towns_and_towers:village_badlands"],
        },
        {
            "set": "towns_and_towers:towers",
            "jar": "Towns-and-Towers-1.12-Fabric+Forge.jar",
            "path": "data/towns_and_towers/worldgen/structure_set/towers.json",
            "spacing": 64,
            "separation": 32,
            "exclusion": 10,
            "rule": "towns_and_towers_outpost_overlap_reduction",
            "evidence": ["towns_and_towers:pillager_outpost_badlands"],
        },
    ]


def main() -> int:
    generated_at = now()
    evidence = load_json(CONFIG_DIR / "structure_evidence_registry.json")
    confidence = load_json(CONFIG_DIR / "structure_classification_confidence.json")
    evidence_by_id = entry_set(evidence["structures"], "structure_id")
    confidence_by_id = entry_set(confidence["structures"], "structure_id")

    if DATAPACK.exists():
        shutil.rmtree(DATAPACK)
    if ROLLBACK_DIR.exists():
        shutil.rmtree(ROLLBACK_DIR)
    DATAPACK.mkdir(parents=True, exist_ok=True)
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)

    live_changes: list[dict[str, Any]] = []
    rollback_files: list[dict[str, Any]] = []

    write_json(
        DATAPACK / "pack.mcmeta",
        {
            "pack": {
                "pack_format": 15,
                "description": "Ascendant Structure Director Live v1 - reversible evidence-backed structure density and context controls",
            }
        },
    )
    write_text(
        DATAPACK / "README.md",
        "# Ascendant Structure Director Live v1\n\n"
        "This OpenLoader datapack is generated from evidence-backed Structure Director policy. "
        "It changes newly generated chunks only and can be disabled with "
        "`scripts/disable-structure-director-live-v1.ps1`.\n",
    )

    for row in selected_structure_sets():
        original_bytes, source_label = read_original(
            row["path"],
            row.get("jar"),
            row.get("source_path"),
        )
        original = json.loads(original_bytes.decode("utf-8"))
        modified = set_spacing(original, row["spacing"], row["separation"], row.get("exclusion"))
        write_override(
            row["path"],
            modified,
            normalize(original_bytes),
            source_label,
            live_changes,
            rollback_files,
            row["rule"],
            row["evidence"],
            f"{row['set']} spacing {original['placement'].get('spacing')}->{row['spacing']} separation {original['placement'].get('separation')}->{row['separation']}",
        )

    # Split the manually observed vineyard out of broad IDAS common so it can be made rarer
    # without mutating all IDAS common structures into the same policy bucket.
    idas_common_bytes, idas_common_source = read_original(
        "data/idas/worldgen/structure_set/idas_common.json",
        "idas_forge-1.13.0+1.20.1.jar",
    )
    idas_common = json.loads(idas_common_bytes.decode("utf-8"))
    idas_common["structures"] = [
        entry for entry in idas_common["structures"] if entry.get("structure") != "idas:abandoned_vineyard"
    ]
    idas_common = set_spacing(idas_common, 32, 12, 4)
    write_override(
        "data/idas/worldgen/structure_set/idas_common.json",
        idas_common,
        normalize(idas_common_bytes),
        idas_common_source,
        live_changes,
        rollback_files,
        "idas_common_reduce_and_extract_vineyard",
        ["idas:abandoned_vineyard", "idas:haunted_manor"],
        "IDAS common set reduced from spacing 21 to 32 and abandoned_vineyard moved to its own rarer set.",
    )
    vineyard_set = {
        "structures": [{"structure": "idas:abandoned_vineyard", "weight": 1}],
        "placement": {
            "salt": 169480679,
            "spacing": 96,
            "separation": 48,
            "type": "integrated_api:advanced_random_spread",
            "super_exclusion_zone": {"chunk_count": 8, "other_set": "#idas:common_avoid"},
        },
    }
    write_override(
        "data/idas/worldgen/structure_set/abandoned_vineyard_director.json",
        vineyard_set,
        None,
        "new_structure_set_from_evidence",
        live_changes,
        rollback_files,
        "idas_abandoned_vineyard_dedicated_land_first_set",
        ["idas:abandoned_vineyard"],
        "Dedicated rarer vineyard set so the manually observed island-placement structure is no longer tied to dense IDAS common rolls.",
    )

    vineyard_structure_bytes, vineyard_structure_source = read_original(
        "data/idas/worldgen/structure/abandoned_vineyard.json",
        "idas_forge-1.13.0+1.20.1.jar",
    )
    vineyard_structure = json.loads(vineyard_structure_bytes.decode("utf-8"))
    vineyard_structure["terrain_height_radius_check"] = 4
    vineyard_structure["allowed_terrain_height_range"] = 6
    vineyard_structure["valid_biome_radius_check"] = 3
    write_override(
        "data/idas/worldgen/structure/abandoned_vineyard.json",
        vineyard_structure,
        normalize(vineyard_structure_bytes),
        vineyard_structure_source,
        live_changes,
        rollback_files,
        "idas_abandoned_vineyard_larger_land_context_check",
        ["idas:abandoned_vineyard"],
        "Vineyard now asks Integrated API to validate a larger, less jagged surrounding biome/terrain context.",
    )

    tag_rules = [
        ("data/iceandfire/tags/worldgen/biome/structure_gen/fire.json", "iceandfire:fire_dragon_roost", "dragon_fire_land_biomes"),
        ("data/iceandfire/tags/worldgen/biome/structure_gen/ice.json", "iceandfire:ice_dragon_roost", "dragon_ice_land_biomes"),
        ("data/iceandfire/tags/worldgen/biome/structure_gen/lightning.json", "iceandfire:lightning_dragon_roost", "dragon_lightning_land_biomes"),
        ("data/idas/tags/worldgen/biome/has_structure/savannas.json", "idas:abandoned_vineyard", "vineyard_land_savanna_biomes"),
    ]
    for path, sid, rule_id in tag_rules:
        row = evidence_by_id[sid]
        values = clean_biomes(row)
        if len(values) < 3:
            raise RuntimeError(f"Not enough evidence-backed land biomes for {sid}")
        write_override(
            path,
            {"replace": True, "values": values},
            None,
            "resolved_evidence_registry_allowed_biome_ids",
            live_changes,
            rollback_files,
            rule_id,
            [sid],
            f"Evidence-resolved land-biome tag for {sid}; water/ocean/river/cave IDs removed.",
        )

    # Siren island stays explicitly ocean-backed.
    write_override(
        "data/iceandfire/tags/worldgen/biome/structure_gen/siren_island.json",
        {"replace": True, "values": ["#minecraft:is_ocean", "#minecraft:is_deep_ocean"]},
        None,
        "evidence_registry_ocean_role",
        live_changes,
        rollback_files,
        "siren_island_preserve_ocean_context",
        ["iceandfire:siren_island"],
        "Siren island remains water/ocean content and does not receive land-only rules.",
    )

    land_water_rules = [
        {
            "rule_id": "dragon_roost_land_context",
            "structure_ids": [
                "iceandfire:fire_dragon_roost",
                "iceandfire:ice_dragon_roost",
                "iceandfire:lightning_dragon_roost",
            ],
            "structure_sets": ["iceandfire:dragon_roost"],
            "mode": "policy_and_datapack_density_active_helper_context_diagnostic",
            "center_must_be_land": True,
            "min_local_land_ratio": 0.75,
            "max_local_water_ratio": 0.25,
            "reject_ocean_scale_surrounding_water": True,
            "sample_radius_blocks": 96,
        },
        {
            "rule_id": "dragon_cave_land_or_mountain_cover",
            "structure_ids": [
                "iceandfire:fire_dragon_cave",
                "iceandfire:ice_dragon_cave",
                "iceandfire:lightning_dragon_cave",
            ],
            "structure_sets": ["iceandfire:dragon_cave"],
            "mode": "policy_and_datapack_density_active_helper_context_diagnostic",
            "requires_land_or_mountain_above": True,
            "preserve_underground_layer": True,
            "reject_ocean_floor_exposure": True,
        },
        {
            "rule_id": "vineyard_land_context",
            "structure_ids": ["idas:abandoned_vineyard"],
            "structure_sets": ["idas:abandoned_vineyard_director"],
            "mode": "datapack_dedicated_set_and_integrated_api_context_checks_active",
            "center_must_be_land": True,
            "min_local_land_ratio": 0.75,
            "max_local_water_ratio": 0.25,
            "reject_ocean_scale_surrounding_water": True,
            "sample_radius_blocks": 80,
        },
        {
            "rule_id": "siren_island_water_context",
            "structure_ids": ["iceandfire:siren_island"],
            "structure_sets": ["iceandfire:siren_island"],
            "mode": "datapack_ocean_tag_and_density_active",
            "center_must_be_water": True,
            "min_local_water_ratio": 0.70,
            "min_water_body": "ocean_or_deep_ocean_biome_tag",
        },
    ]

    settlement_exclusions = [
        {
            "family_id": "towns_and_towers_towns_vs_vanilla_villages",
            "member_structure_sets": ["towns_and_towers:towns", "minecraft:villages"],
            "minimum_separation_chunks": 10,
            "live_resource": "data/towns_and_towers/worldgen/structure_set/towns.json",
            "status": "active_spacing_and_exclusion_zone_override",
        },
        {
            "family_id": "integrated_villages_existing_exclusion_preserved",
            "member_structure_sets": ["integrated_villages:regular_villages"],
            "minimum_separation_chunks": 12,
            "live_resource": "config/openloader/data/ascendant_realms_world_integration/data/integrated_villages/worldgen/structure_set/regular_villages.json",
            "status": "existing_live_exclusion_preserved",
        },
    ]

    live_structure_ids = sorted({sid for change in live_changes for sid in change.get("evidence_ids", [])})
    live_structure_sets = sorted(
        {
            "iceandfire:dragon_roost",
            "iceandfire:dragon_cave",
            "iceandfire:siren_island",
            "idas:idas_common",
            "idas:abandoned_vineyard_director",
            "idas:idas_rare",
            "idas:idas_ocean",
            "betterdungeons:small_dungeons",
            "bettermineshafts:mineshafts",
            "aquamirae:surface",
            "cataclysm:abandoned_structures",
            "cataclysm:amethyst_nest",
            "cataclysm:desert_structures",
            "block_factorys_bosses:sandworm_nest",
            "block_factorys_bosses:yeti_hideout",
            "towns_and_towers:towns",
            "towns_and_towers:towers",
        }
    )

    live_policy = {
        "version": VERSION,
        "generated_at": generated_at,
        "enabled": True,
        "rollback_supported": True,
        "evidence_required": True,
        "minimum_live_confidence": "strong",
        "true_pre_generation_context_veto": {
            "status": "not_available_in_current_forge_event_surface",
            "reason": "Forge 47.4.20 exposes chunk-load events but no safe structure placement veto event in this helper without a mixin/generator wrapper.",
            "replacement_live_controls": [
                "structure_set spacing/separation overrides",
                "evidence-resolved biome tag replacement",
                "dedicated vineyard structure_set",
                "Integrated API terrain/biome radius checks for vineyard",
                "helper runtime context diagnostics",
            ],
        },
        "live_mode": {
            "density_overrides_active": True,
            "region_biome_tags_active": True,
            "land_water_context_policy_active": True,
            "helper_debug_commands_required": True,
            "candidate_only": False,
        },
        "land_water_rules": land_water_rules,
        "settlement_family_exclusions": settlement_exclusions,
    }
    write_json(CONFIG_DIR / "live_structure_policy.json", live_policy)

    datapack_file_paths = sorted(
        (path for path in DATAPACK.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(DATAPACK).as_posix(),
    )
    datapack_files = [
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in datapack_file_paths
    ]
    manifest = {
        "version": VERSION,
        "generated_at": generated_at,
        "enabled": True,
        "rollback_supported": True,
        "evidence_required": True,
        "minimum_live_confidence": "strong",
        "datapack_root": str(DATAPACK.relative_to(ROOT)).replace("\\", "/"),
        "datapack_hash": "",
        "live_structure_ids": live_structure_ids,
        "live_structure_sets": live_structure_sets,
        "live_change_count": len(live_changes),
        "density_override_count": len([c for c in live_changes if "structure_set" in c["resource_path"]]),
        "biome_tag_override_count": len([c for c in live_changes if "/tags/worldgen/biome/" in c["resource_path"]]),
        "land_water_context_rule_count": len(land_water_rules),
        "settlement_exclusion_count": len(settlement_exclusions),
        "live_changes": live_changes,
        "datapack_files": datapack_files,
    }
    datapack_hash = hashlib.sha256()
    for path in datapack_file_paths:
        datapack_relative = path.relative_to(DATAPACK).as_posix()
        datapack_hash.update(datapack_relative.encode("utf-8"))
        datapack_hash.update(path.read_bytes())
    manifest["datapack_hash"] = datapack_hash.hexdigest().upper()
    write_json(CONFIG_DIR / "live_structure_manifest.json", manifest)

    results = {
        "version": VERSION,
        "generated_at": generated_at,
        "status": "source_live_files_generated_not_in_game_validated",
        "minecraft_closed_at_generation": None,
        "active_instance_sync": "pending_sync_script",
        "source_datapack_hash": manifest["datapack_hash"],
        "active_datapack_hash": None,
        "source_helper_hash": sha256_file(ROOT / "mods/ascendant-atlas-regions-0.1.0.jar")
        if (ROOT / "mods/ascendant-atlas-regions-0.1.0.jar").exists()
        else None,
        "active_helper_hash": None,
        "packwiz_refresh": "pending",
        "check_pack": "pending",
        "client_export": "pending",
        "server_staging": "pending",
        "notes": [
            "Live datapack changes are source-side until sync/export commands complete.",
            "Fresh worlds or ungenerated chunks are required to see Structure Director Live v1 behavior.",
            "The current helper exposes diagnostics; a true pre-generation context veto still needs a later mixin/generator-wrapper implementation.",
        ],
    }
    write_json(CONFIG_DIR / "live_structure_results.json", results)

    rollback_manifest = {
        "version": VERSION,
        "generated_at": generated_at,
        "rollback_supported": True,
        "disable_script": "scripts/disable-structure-director-live-v1.ps1",
        "enable_script": "scripts/enable-structure-director-live-v1.ps1",
        "files": rollback_files,
    }
    write_json(ROLLBACK_DIR / "rollback_manifest.json", rollback_manifest)

    live_targets = {
        "version": VERSION,
        "generated_at": generated_at,
        "targets": [
            {
                "name": "Dragon roost land placement",
                "commands": ["/locate structure iceandfire:fire_dragon_roost", "/ascstructure test_context iceandfire:fire_dragon_roost"],
                "expected": "Roost should be rare and should not sit as a tiny island in ocean/lake terrain.",
            },
            {
                "name": "Abandoned vineyard land placement",
                "commands": ["/locate structure idas:abandoned_vineyard", "/ascstructure test_context idas:abandoned_vineyard"],
                "expected": "Vineyard should be rare, land-first, and not spawn as an island.",
            },
            {
                "name": "Siren island ocean placement",
                "commands": ["/locate structure iceandfire:siren_island", "/ascstructure test_context iceandfire:siren_island"],
                "expected": "Siren island should remain in ocean/deep-ocean context.",
            },
            {
                "name": "Settlement spacing",
                "commands": ["/locate structure towns_and_towers:village_badlands", "/locate structure minecraft:village_plains"],
                "expected": "Towns and Towers villages should be less likely to crowd vanilla villages.",
            },
        ],
    }
    write_json(CONFIG_DIR / "live_test_targets.json", live_targets)
    write_text(
        CONFIG_DIR / "live_test_commands.md",
        "# Structure Director Live v1 Test Commands\n\n"
        "Use a fresh creative world or ungenerated chunks.\n\n"
        "```mcfunction\n"
        "/ascstructure status\n"
        "/ascstructure dump_live_manifest\n"
        "/locate structure iceandfire:fire_dragon_roost\n"
        "/ascstructure test_context iceandfire:fire_dragon_roost\n"
        "/locate structure iceandfire:ice_dragon_roost\n"
        "/ascstructure test_context iceandfire:ice_dragon_roost\n"
        "/locate structure iceandfire:lightning_dragon_roost\n"
        "/ascstructure test_context iceandfire:lightning_dragon_roost\n"
        "/locate structure idas:abandoned_vineyard\n"
        "/ascstructure test_context idas:abandoned_vineyard\n"
        "/locate structure iceandfire:siren_island\n"
        "/ascstructure test_context iceandfire:siren_island\n"
        "/locate structure betterdungeons:small_dungeon\n"
        "/locate structure towns_and_towers:village_badlands\n"
        "```\n",
    )

    docs = {
        "STRUCTURE_DIRECTOR_LIVE_V1.md": f"""# Structure Director Live v1

Generated: {generated_at}

Structure Director Live v1 is the first reversible live structure-control pass. It changes newly generated worlds through OpenLoader datapack overrides and helper diagnostics. It does not add mods, place NPCs, inject Hunter Boards, add Guild Halls, rewrite loot, rewrite recipes, or change roads/bridges.

## Active Live Controls

- Live datapack: `config/openloader/data/ascendant_structure_director_live/`.
- Enabled policy: `config/ascendant_structures/live_structure_policy.json`.
- Rollback manifest: `config/ascendant_structures/rollback/pre_structure_director_v1/rollback_manifest.json`.
- Structure-set overrides active: {manifest['density_override_count']}.
- Biome-tag overrides active: {manifest['biome_tag_override_count']}.
- Land/water policy rules recorded: {len(land_water_rules)}.
- Settlement overlap reductions active: {len(settlement_exclusions)}.

## Important Honesty Boundary

Forge 47.4.20 does not expose a safe pack-owned structure placement veto event to this helper. Live v1 therefore uses real datapack controls now: spacing/separation, evidence-resolved biome tags, a dedicated vineyard structure set, and larger Integrated API terrain/biome context checks. The helper commands expose policy/context diagnostics. A true before-placement land/water veto remains a future mixin or generator-wrapper job.

## Known Manual Fixes

- Dragon roosts are rarer, keep land-biome tags, and exclude ocean/river/cave/wet biome IDs from their evidence-resolved tags.
- Dragon caves are rarer and remain underground content.
- `idas:abandoned_vineyard` is split out of broad `idas:idas_common` into `idas:abandoned_vineyard_director`, made rarer, and gets larger Integrated API context checks.
- `iceandfire:siren_island` remains ocean/deep-ocean content.
- IDAS replacement cases stay documented: gorgon temple can resolve to `idas:labyrinth`; graveyard can resolve to `idas:haunted_manor`.
""",
        "STRUCTURE_DIRECTOR_LIVE_CHANGELOG.md": f"""# Structure Director Live Changelog

Generated: {generated_at}

## Live v1

- Created `ascendant_structure_director_live` OpenLoader datapack.
- Activated {manifest['density_override_count']} structure-set or structure JSON overrides.
- Activated {manifest['biome_tag_override_count']} evidence-backed biome tag overrides.
- Split `idas:abandoned_vineyard` out of `idas:idas_common`.
- Reduced major dragon/boss/dungeon density where evidence was strong.
- Added Towns and Towers settlement/outpost spacing and vanilla-village exclusion strengthening.
- Added rollback snapshot and enable/disable/verify scripts.
""",
        "STRUCTURE_DIRECTOR_ROLLBACK.md": """# Structure Director Rollback

Use rollback only if new worlds show serious structure-regression behavior.

## Disable

Run:

```powershell
.\\scripts\\disable-structure-director-live-v1.ps1
```

This renames the live OpenLoader datapack folder to `.disabled`, sets `live_structure_policy.enabled=false`, and preserves evidence/candidate files.

## Enable

Run:

```powershell
.\\scripts\\enable-structure-director-live-v1.ps1
```

Then sync/export again before testing active CurseForge or packaged copies.
""",
        "STRUCTURE_DIRECTOR_LIVE_V1_TESTING.md": """# Structure Director Live v1 Testing

Use a fresh creative world, or fly into ungenerated chunks. Existing generated structures will not move.

## First Commands

```mcfunction
/ascstructure status
/ascstructure dump_live_manifest
/ascstructure here
```

## Priority Visual Checks

1. Dragon roosts: locate each roost variant and confirm it is not a tiny island in ocean/lake terrain.
2. Abandoned vineyard: confirm it is land-first and not isolated in water.
3. Siren island: confirm it still belongs in actual ocean/deep-ocean water.
4. Major boss/dungeon sets: confirm they feel rarer and are not starter-region spam.
5. Town/village spacing: confirm Towns and Towers and vanilla villages are not cramped on top of each other.

## Exact Locate/Test Context Commands

See `config/ascendant_structures/live_test_commands.md`.
""",
    }
    for name, text in docs.items():
        write_text(ROOT / "docs" / name, text)

    print(f"Generated Structure Director Live v1 with {len(live_changes)} live changes.")
    print(f"Datapack hash: {manifest['datapack_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
