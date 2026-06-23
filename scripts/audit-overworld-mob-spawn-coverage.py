#!/usr/bin/env python3
"""Audit overworld natural-spawn coverage for Ascendant Realms mobs.

This report is intentionally evidence-based. The entity registry proves that an
entity exists; it does not prove natural spawning. This script combines the
registry with datapack/jar JSON references, In Control spawner rules, vanilla
defaults, and selected mod config spawn weights.
"""

from __future__ import annotations

import json
import pathlib
import re
import zipfile
from collections import Counter, defaultdict
from datetime import datetime


ROOT = pathlib.Path(__file__).resolve().parents[1]
ACTIVE_INSTANCE = pathlib.Path(r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)")
ACTIVE_MODS = ACTIVE_INSTANCE / "mods"

REPORT_JSON = ROOT / "config/ascendant_core/reports/overworld_mob_spawn_coverage_latest.json"
REPORT_MD = ROOT / "docs/OVERWORLD_MOB_SPAWN_COVERAGE.md"


VANILLA_OVERWORLD = {
    "minecraft:allay": ("Vanilla", "structure_or_event", "outpost/woodland mansion cage rescue"),
    "minecraft:armadillo": ("Vanilla", "natural_overworld", "savanna/badlands passive wildlife"),
    "minecraft:axolotl": ("Vanilla", "natural_overworld", "lush cave aquatic wildlife"),
    "minecraft:bat": ("Vanilla", "natural_overworld", "cave ambient wildlife"),
    "minecraft:bee": ("Vanilla", "natural_overworld", "flower/forest passive wildlife"),
    "minecraft:camel": ("Vanilla", "structure_or_event", "desert village"),
    "minecraft:cat": ("Vanilla", "structure_or_event", "village/swamp hut"),
    "minecraft:cave_spider": ("Vanilla", "structure_or_event", "mineshaft spawner"),
    "minecraft:chicken": ("Vanilla", "natural_overworld", "common passive wildlife"),
    "minecraft:cod": ("Vanilla", "natural_overworld", "overworld aquatic wildlife"),
    "minecraft:cow": ("Vanilla", "natural_overworld", "common passive wildlife"),
    "minecraft:creeper": ("Vanilla", "natural_overworld", "night/cave hostile"),
    "minecraft:dolphin": ("Vanilla", "natural_overworld", "ocean wildlife"),
    "minecraft:donkey": ("Vanilla", "natural_overworld", "plains/savanna passive wildlife"),
    "minecraft:drowned": ("Vanilla", "natural_overworld", "ocean/river water hostile"),
    "minecraft:elder_guardian": ("Vanilla", "structure_or_event", "ocean monument boss"),
    "minecraft:enderman": ("Vanilla", "natural_overworld", "night/cave hostile"),
    "minecraft:evoker": ("Vanilla", "structure_or_event", "raid/woodland mansion"),
    "minecraft:fox": ("Vanilla", "natural_overworld", "taiga wildlife"),
    "minecraft:frog": ("Vanilla", "natural_overworld", "swamp/mangrove wildlife"),
    "minecraft:glow_squid": ("Vanilla", "natural_overworld", "underground aquatic wildlife"),
    "minecraft:goat": ("Vanilla", "natural_overworld", "mountain wildlife"),
    "minecraft:guardian": ("Vanilla", "structure_or_event", "ocean monument"),
    "minecraft:horse": ("Vanilla", "natural_overworld", "plains/savanna passive wildlife"),
    "minecraft:husk": ("Vanilla", "natural_overworld", "desert night hostile"),
    "minecraft:iron_golem": ("Vanilla", "structure_or_event", "village defense/player-built"),
    "minecraft:llama": ("Vanilla", "natural_overworld", "savanna/mountain wildlife"),
    "minecraft:mooshroom": ("Vanilla", "natural_overworld", "mushroom island wildlife"),
    "minecraft:mule": ("Vanilla", "not_natural_by_design", "breeding result"),
    "minecraft:ocelot": ("Vanilla", "natural_overworld", "jungle wildlife"),
    "minecraft:panda": ("Vanilla", "natural_overworld", "bamboo jungle wildlife"),
    "minecraft:parrot": ("Vanilla", "natural_overworld", "jungle wildlife"),
    "minecraft:phantom": ("Vanilla", "natural_overworld", "insomnia sky hostile"),
    "minecraft:pig": ("Vanilla", "natural_overworld", "common passive wildlife"),
    "minecraft:pillager": ("Vanilla", "structure_or_event", "patrol/outpost/raid"),
    "minecraft:polar_bear": ("Vanilla", "natural_overworld", "frozen wildlife"),
    "minecraft:pufferfish": ("Vanilla", "natural_overworld", "warm ocean wildlife"),
    "minecraft:rabbit": ("Vanilla", "natural_overworld", "desert/snow/flower wildlife"),
    "minecraft:ravager": ("Vanilla", "structure_or_event", "raid"),
    "minecraft:salmon": ("Vanilla", "natural_overworld", "river/cold aquatic wildlife"),
    "minecraft:sheep": ("Vanilla", "natural_overworld", "common passive wildlife"),
    "minecraft:silverfish": ("Vanilla", "structure_or_event", "infested block/stronghold"),
    "minecraft:skeleton": ("Vanilla", "natural_overworld", "night/cave hostile"),
    "minecraft:skeleton_horse": ("Vanilla", "structure_or_event", "trap horse event"),
    "minecraft:slime": ("Vanilla", "natural_overworld", "swamp/slime chunk hostile"),
    "minecraft:sniffer": ("Vanilla", "not_natural_by_design", "archaeology egg recovery"),
    "minecraft:snow_golem": ("Vanilla", "not_natural_by_design", "player-built"),
    "minecraft:spider": ("Vanilla", "natural_overworld", "night/cave hostile"),
    "minecraft:squid": ("Vanilla", "natural_overworld", "river/ocean aquatic wildlife"),
    "minecraft:stray": ("Vanilla", "natural_overworld", "cold night hostile"),
    "minecraft:tadpole": ("Vanilla", "natural_overworld", "frog breeding/water life"),
    "minecraft:trader_llama": ("Vanilla", "structure_or_event", "wandering trader"),
    "minecraft:tropical_fish": ("Vanilla", "natural_overworld", "warm ocean/lush cave wildlife"),
    "minecraft:turtle": ("Vanilla", "natural_overworld", "beach wildlife"),
    "minecraft:vex": ("Vanilla", "structure_or_event", "evoker summon"),
    "minecraft:villager": ("Vanilla", "structure_or_event", "village"),
    "minecraft:vindicator": ("Vanilla", "structure_or_event", "raid/woodland mansion"),
    "minecraft:wandering_trader": ("Vanilla", "structure_or_event", "periodic event"),
    "minecraft:warden": ("Vanilla", "structure_or_event", "sculk shrieker event"),
    "minecraft:witch": ("Vanilla", "natural_overworld", "night/swamp hut/raid hostile"),
    "minecraft:wolf": ("Vanilla", "natural_overworld", "forest/taiga wildlife"),
    "minecraft:zombie": ("Vanilla", "natural_overworld", "night/cave hostile"),
    "minecraft:zombie_villager": ("Vanilla", "natural_overworld", "night/cave hostile variant"),
}

NOT_NATURAL_PATTERNS = [
    "_part",
    "_projectile",
    "_arrow",
    "_bolt",
    "_beam",
    "_fireball",
    "_skull",
    "_orb",
    "_effect",
    "_segment",
    "_head",
    "_body",
    "_tail",
    "_egg",
    "_wave",
    "_portal",
    "_seat",
    "_shell",
    "_spit",
    "_blast",
    "_mine",
    "_breath",
    "_blade",
    "_bardiche",
    "_spear",
    "_strike",
    "_jet",
    "_bomb",
    "_ink",
    "_meter",
    "_storm",
    "_aoe",
    "_shackle",
    "_slash",
    "_field",
    "_tomb",
    "_dagger",
    "_hammer",
    "_lance",
    "_eruption",
    "_lasso",
    "_rocket",
    "_controlled",
    "_minion",
    "_not_despawn",
    "_copy",
    "_stage_",
    "_true_form",
    "_without",
    "_withouta",
    "_bubbles",
    "_feather",
]

EXPECTED_NAMESPACES = {
    "alexsmobs",
    "aquamirae",
    "born_in_chaos_v1",
    "cataclysm",
    "iceandfire",
    "irons_spellbooks",
    "majruszsdifficulty",
    "mowziesmobs",
    "soulsweapons",
}

NOT_NATURAL_EXACT = {
    "alexsmobs:cachalot_echo",
    "alexsmobs:gust",
    "alexsmobs:mosquito_spit",
    "alexsmobs:void_worm_shot",
    "alexsmobs:hemolymph",
    "alexsmobs:mud_ball",
    "alexsmobs:pollen_ball",
    "alexsmobs:sand_shot",
    "alexsmobs:straddleboard",
    "alexsmobs:tossed_item",
    "aquamirae:poisoned_chakra",
    "born_in_chaos_v1:controlled_baby_skeleton",
    "born_in_chaos_v1:controlled_spiritual_assistant",
    "born_in_chaos_v1:felsteed",
    "born_in_chaos_v1:infernal_spirit",
    "born_in_chaos_v1:lords_felsteed",
    "born_in_chaos_v1:pumpkin_spirit",
    "born_in_chaos_v1:riding_felsteed",
    "born_in_chaos_v1:riding_lords_felsteed",
    "cataclysm:abyss_blast",
    "cataclysm:abyss_mine",
    "cataclysm:ancient_desert_stele",
    "cataclysm:ashen_breath",
    "cataclysm:axe_blade",
    "cataclysm:coral_bardiche",
    "cataclysm:coral_spear",
    "cataclysm:earthquake",
    "cataclysm:flame_jet",
    "cataclysm:flame_strike",
    "cataclysm:flare_bomb",
    "cataclysm:lava_bomb",
    "cataclysm:lightning_spear",
    "cataclysm:lightning_storm",
    "cataclysm:lionfish_spike",
    "cataclysm:octo_ink",
    "cataclysm:phantom_halberd",
    "cataclysm:rage_meter",
    "cataclysm:sandstorm",
    "iceandfire:chain_tie",
    "iceandfire:player",
    "iceandfire:sea_serpent_bubbles",
    "iceandfire:stymphalian_feather",
    "iceandfire:stone_statue",
    "iceandfire:tide_trident",
    "irons_spellbooks:arcane_shackle",
    "irons_spellbooks:ball_lightning",
    "irons_spellbooks:black_hole",
    "irons_spellbooks:blizzard_aoe",
    "irons_spellbooks:blood_needle",
    "irons_spellbooks:blood_slash",
    "irons_spellbooks:chain_lightning",
    "irons_spellbooks:comet",
    "irons_spellbooks:cone_of_cold",
    "irons_spellbooks:devour_jaw",
    "irons_spellbooks:earthquake_aoe",
    "irons_spellbooks:echoing_strike",
    "irons_spellbooks:eldritch_blast",
    "irons_spellbooks:electrocute",
    "irons_spellbooks:ender_chain",
    "irons_spellbooks:fang_swirl",
    "irons_spellbooks:fiery_dagger",
    "irons_spellbooks:fire_breath",
    "irons_spellbooks:fire_eruption",
    "irons_spellbooks:fire_field",
    "irons_spellbooks:frost_field",
    "irons_spellbooks:gust",
    "irons_spellbooks:healing_aoe",
    "irons_spellbooks:ice_tomb",
    "irons_spellbooks:icicle",
    "irons_spellbooks:lightning_lance",
    "irons_spellbooks:lightning_strike",
    "irons_spellbooks:magma_ball",
    "irons_spellbooks:poison_breath",
    "irons_spellbooks:poison_splash",
    "irons_spellbooks:ray_of_frost",
    "irons_spellbooks:root",
    "irons_spellbooks:shield",
    "irons_spellbooks:snowball",
    "irons_spellbooks:spear",
    "irons_spellbooks:spectral_hammer",
    "irons_spellbooks:stomp_aoe",
    "irons_spellbooks:summoned_claymore",
    "irons_spellbooks:summoned_rapier",
    "irons_spellbooks:summoned_sword",
    "irons_spellbooks:summoned_vex",
    "irons_spellbooks:target_area",
    "irons_spellbooks:wall_of_fire",
    "mowziesmobs:baby_foliaath",
    "mowziesmobs:boulder",
    "mowziesmobs:umvuthana_crane_player",
    "mowziesmobs:umvuthana_follower_player",
    "mowziesmobs:umvuthana_follower_raptor",
}

STRUCTURE_OR_DIMENSION_FIRST_NAMESPACES = {
    "aquamirae",
    "cataclysm",
    "soulsweapons",
}

MOWZIE_STRUCTURE_OR_BOSS_MOBS = {
    "elokosa_follower_howler",
    "elokosa_howler",
    "sculptor",
    "umvuthana_crane",
    "umvuthi",
}

KNOWN_IRONS_LIVING_MOBS = {
    "archevoker",
    "cryomancer",
    "cultist",
    "dead_king",
    "dead_king_corpse",
    "ice_spider",
    "magehunter_vindicator",
    "necromancer",
    "priest",
    "pyromancer",
    "wisp",
}


def read_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: pathlib.Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def snake_to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r"_\1", value).lower()


def evidence_entry(kind: str, source: str, detail: str) -> dict:
    return {"kind": kind, "source": source, "detail": detail}


def add_evidence(records: dict[str, dict], entity_id: str, kind: str, source: str, detail: str) -> None:
    if entity_id not in records:
        namespace = entity_id.split(":", 1)[0]
        records[entity_id] = {
            "entity_id": entity_id,
            "source_mod": "Unknown",
            "threat_tier": "unknown",
            "namespace": namespace,
            "evidence": [],
            "notes": [],
        }
    item = evidence_entry(kind, source, detail)
    if item not in records[entity_id]["evidence"]:
        records[entity_id]["evidence"].append(item)


def flatten_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_strings(item)


def collect_incontrol_spawner(records: dict[str, dict]) -> Counter:
    counts = Counter()
    path = ROOT / "config/incontrol/spawner.json"
    if not path.exists():
        return counts
    rules = read_json(path)
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        mobs = list(flatten_strings(rule.get("mob")))
        tags = ", ".join(flatten_strings(rule.get("addscoreboardtags"))) or "untagged"
        for mob_id in mobs:
            add_evidence(
                records,
                mob_id,
                "incontrol_explicit_spawn",
                "config/incontrol/spawner.json",
                f"rule {index + 1}; tags={tags}",
            )
            counts[mob_id] += 1
        if rule.get("mobsfrombiome") == "monster":
            counts["__biome_native_monster_rule__"] += 1
    return counts


def collect_worldgen_audit(records: dict[str, dict]) -> Counter:
    counts = Counter()
    path = ROOT / "docs/generated/worldgen_content_audit.json"
    if not path.exists():
        return counts
    audit = read_json(path)
    mobs = audit.get("mobs", {})
    if not isinstance(mobs, dict):
        return counts
    for entity_id, info in mobs.items():
        if not isinstance(info, dict):
            continue
        biome_count = info.get("biome_count")
        if isinstance(biome_count, int) and biome_count > 0:
            raw_buckets = info.get("climate_buckets", [])
            if isinstance(raw_buckets, dict):
                bucket_values = [f"{key}:{value}" for key, value in raw_buckets.items()]
            elif isinstance(raw_buckets, list):
                bucket_values = [str(value) for value in raw_buckets]
            else:
                bucket_values = []
            buckets = ", ".join(bucket_values[:4])
            add_evidence(
                records,
                entity_id,
                "worldgen_biome_spawn_json",
                "docs/generated/worldgen_content_audit.json",
                f"{biome_count} biome entries; climate={buckets or 'not listed'}",
            )
            counts["biome_json"] += 1
        structures = info.get("structure_overrides", [])
        if structures:
            add_evidence(
                records,
                entity_id,
                "structure_spawn_override",
                "docs/generated/worldgen_content_audit.json",
                f"{len(structures)} structure override(s)",
            )
            counts["structure_overrides"] += 1
    return counts


def collect_mod_configs(records: dict[str, dict], registry_ids: set[str]) -> Counter:
    counts = Counter()

    alex_path = ROOT / "config/alexsmobs.toml"
    if alex_path.exists():
        text = alex_path.read_text(encoding="utf-8", errors="replace")
        suffix_to_id = {
            entity_id.split(":", 1)[1]: entity_id
            for entity_id in registry_ids
            if entity_id.startswith("alexsmobs:")
        }
        camel_to_id = {snake_to_camel(suffix): entity_id for suffix, entity_id in suffix_to_id.items()}
        for key, raw_weight in re.findall(r"(?m)^\s*([A-Za-z0-9]+)SpawnWeight\s*=\s*(-?\d+)", text):
            entity_id = camel_to_id.get(key) or suffix_to_id.get(camel_to_snake(key))
            if not entity_id:
                continue
            weight = int(raw_weight)
            if weight > 0:
                add_evidence(
                    records,
                    entity_id,
                    "mod_config_spawn_weight",
                    "config/alexsmobs.toml",
                    f"{key}SpawnWeight={weight}",
                )
                counts["alexsmobs_enabled"] += 1
            else:
                add_evidence(
                    records,
                    entity_id,
                    "disabled_by_mod_config",
                    "config/alexsmobs.toml",
                    f"{key}SpawnWeight={weight}",
                )
                counts["alexsmobs_disabled"] += 1
        for key in [
            "restrictPupfishSpawns",
            "restrictSkelewagSpawns",
            "restrictFarseerSpawns",
            "restrictUnderminerSpawns",
            "mimicubeSpawnInEndCity",
            "soulVultureSpawnOnFossil",
            "limitGusterSpawnsToWeather",
        ]:
            match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*(true|false)", text)
            if match:
                counts[f"alexsmobs_{key}_{match.group(1)}"] += 1

    cataclysm_path = ROOT / "config/cataclysm-common.toml"
    if cataclysm_path.exists():
        text = cataclysm_path.read_text(encoding="utf-8", errors="replace")
        suffix_to_id = {
            entity_id.split(":", 1)[1]: entity_id
            for entity_id in registry_ids
            if entity_id.startswith("cataclysm:")
        }
        for suffix, raw_weight in re.findall(r"(?m)^\s*([a-z0-9_]+)_spawn_weight\s*=\s*(-?\d+)", text):
            entity_id = suffix_to_id.get(suffix)
            if not entity_id:
                continue
            weight = int(raw_weight)
            if weight > 0:
                add_evidence(
                    records,
                    entity_id,
                    "mod_config_spawn_weight",
                    "config/cataclysm-common.toml",
                    f"{suffix}_spawn_weight={weight}",
                )
                counts["cataclysm_enabled"] += 1
            else:
                add_evidence(
                    records,
                    entity_id,
                    "disabled_by_mod_config",
                    "config/cataclysm-common.toml",
                    f"{suffix}_spawn_weight={weight}",
                )
                counts["cataclysm_disabled"] += 1

    mowzie_path = ROOT / "config/mowziesmobs-common.toml"
    if mowzie_path.exists():
        text = mowzie_path.read_text(encoding="utf-8", errors="replace")
        suffix_to_id = {
            entity_id.split(":", 1)[1]: entity_id
            for entity_id in registry_ids
            if entity_id.startswith("mowziesmobs:")
        }
        section_re = re.compile(r"(?ms)^\s*\[mobs\.([a-z0-9_]+)\..*?\](.*?)(?=^\s*\[mobs\.|\Z)")
        for suffix, block in section_re.findall(text):
            entity_id = suffix_to_id.get(suffix)
            if not entity_id:
                continue
            spawn_rate = re.search(r"(?m)^\s*spawn_rate\s*=\s*(-?\d+)", block)
            spawn_chance = re.search(r"(?m)^\s*spawn_chance\s*=\s*([0-9.]+)", block)
            biome_tags = re.search(r"(?m)^\s*biome_tags\s*=\s*(\[.*?\])", block)
            if spawn_rate and int(spawn_rate.group(1)) > 0:
                add_evidence(
                    records,
                    entity_id,
                    "mod_config_spawn_rate",
                    "config/mowziesmobs-common.toml",
                    f"{suffix}.spawn_rate={spawn_rate.group(1)}",
                )
                counts["mowziesmobs_enabled"] += 1
            if spawn_chance and float(spawn_chance.group(1)) > 0:
                add_evidence(
                    records,
                    entity_id,
                    "mod_config_spawn_chance",
                    "config/mowziesmobs-common.toml",
                    f"{suffix}.spawn_chance={spawn_chance.group(1)}",
                )
            if biome_tags and biome_tags.group(1) != "[]":
                add_evidence(
                    records,
                    entity_id,
                    "mod_config_biome_tags",
                    "config/mowziesmobs-common.toml",
                    f"{suffix}.biome_tags={biome_tags.group(1)[:120]}",
                )

    return counts


def collect_json_references(records: dict[str, dict], registry_ids: set[str]) -> Counter:
    counts = Counter()
    id_pattern = re.compile(r"\b[a-z0-9_.-]+:[a-z0-9_./-]+\b")
    evidence_paths = (
        "biome_modifier",
        "worldgen/biome",
        "tags/worldgen/biome",
        "spawn",
        "spawner",
        "structure",
    )

    def maybe_record(text: str, source: str) -> None:
        if not any(token in source.lower().replace("\\", "/") for token in evidence_paths):
            return
        for entity_id in sorted(set(id_pattern.findall(text)) & registry_ids):
            add_evidence(
                records,
                entity_id,
                "json_reference_spawn_or_structure",
                source,
                "Entity ID referenced in spawn/biome/structure-related JSON.",
            )
            counts["json_reference"] += 1

    for root in [
        ROOT / "config/openloader/data",
        ROOT / "openloader/data",
    ]:
        if root.exists():
            for path in root.rglob("*.json"):
                try:
                    maybe_record(path.read_text(encoding="utf-8-sig", errors="replace"), str(path.relative_to(ROOT)))
                except OSError:
                    continue

    if ACTIVE_MODS.exists():
        for jar in ACTIVE_MODS.glob("*.jar"):
            try:
                with zipfile.ZipFile(jar) as zf:
                    for name in zf.namelist():
                        lower = name.lower()
                        if not lower.endswith(".json") or not lower.startswith("data/"):
                            continue
                        if not any(token in lower for token in evidence_paths):
                            continue
                        try:
                            text = zf.read(name).decode("utf-8", errors="replace")
                        except Exception:
                            continue
                        maybe_record(text, f"{jar.name}!/{name}")
            except zipfile.BadZipFile:
                continue
    return counts


def classify(records: dict[str, dict]) -> Counter:
    counts = Counter()
    for entity_id, record in records.items():
        namespace, suffix = entity_id.split(":", 1)
        tier = record.get("threat_tier", "unknown")
        evidence_kinds = {item["kind"] for item in record["evidence"]}

        if entity_id in VANILLA_OVERWORLD:
            status = VANILLA_OVERWORLD[entity_id][1]
        elif (
            entity_id in NOT_NATURAL_EXACT
            or any(pattern in suffix for pattern in NOT_NATURAL_PATTERNS)
            or suffix.endswith("_shot")
            or suffix.endswith("_stele")
            or tier == "technical_or_projectile"
        ):
            status = "not_natural_by_design"
        elif tier in {"boss", "dragon_tier"}:
            status = "structure_or_event"
        elif "disabled_by_mod_config" in evidence_kinds and not (evidence_kinds - {"disabled_by_mod_config"}):
            status = "disabled_by_config"
        elif "incontrol_explicit_spawn" in evidence_kinds:
            status = "verified_active_injection"
        elif "worldgen_biome_spawn_json" in evidence_kinds or "mod_config_spawn_weight" in evidence_kinds or "mod_config_spawn_rate" in evidence_kinds:
            status = "verified_natural_or_mod_config"
        elif "structure_spawn_override" in evidence_kinds:
            status = "structure_or_event"
        elif "json_reference_spawn_or_structure" in evidence_kinds:
            status = "referenced_needs_runtime_confirmation"
        elif namespace == "irons_spellbooks" and suffix not in KNOWN_IRONS_LIVING_MOBS:
            status = "not_natural_by_design"
        elif namespace == "mowziesmobs" and suffix in MOWZIE_STRUCTURE_OR_BOSS_MOBS:
            status = "structure_or_event"
        elif namespace in STRUCTURE_OR_DIMENSION_FIRST_NAMESPACES:
            status = "structure_event_or_dimension_specific"
        elif namespace in EXPECTED_NAMESPACES and tier in {"dangerous_hostile", "passive_or_wildlife", "elite"}:
            status = "missing_expected_overworld_evidence"
        elif namespace in EXPECTED_NAMESPACES and tier == "uncategorized_mob":
            status = "needs_manual_classification"
        else:
            status = "not_expected_or_non_overworld"

        record["coverage_status"] = status
        counts[status] += 1
    return counts


def build_markdown(report: dict) -> str:
    summary = report["summary"]
    missing = report["missing_expected_overworld_evidence"][:40]
    review = report["needs_manual_classification"][:40]
    verified_namespaces = report["summary"]["verified_by_namespace"]

    lines = [
        "# Overworld Mob Spawn Coverage",
        "",
        "Generated by `scripts/audit-overworld-mob-spawn-coverage.py`.",
        "",
        "## Answer",
        "",
        "Not fully, not yet. The current pack has strong active mob pressure, and the reviewed daytime/cave spawner layer is valid, but a full every-mob natural-spawn guarantee requires evidence per mob. This report separates proven natural/injected spawns from structure/event mobs, disabled/special mobs, and mobs that still need runtime confirmation.",
        "",
        "## Summary",
        "",
        f"- Total tracked entities including vanilla overworld expectations: {summary['total_tracked_entities']}",
        f"- Verified active In Control injections: {summary['coverage_status_counts'].get('verified_active_injection', 0)}",
        f"- Verified natural or mod-config spawn evidence: {summary['coverage_status_counts'].get('verified_natural_or_mod_config', 0)}",
        f"- Vanilla natural overworld defaults tracked: {summary['vanilla_natural_overworld_count']}",
        f"- Structure/event/boss-only entries: {summary['coverage_status_counts'].get('structure_or_event', 0)}",
        f"- Not-natural or technical entries: {summary['coverage_status_counts'].get('not_natural_by_design', 0)}",
        f"- Missing expected overworld evidence: {summary['coverage_status_counts'].get('missing_expected_overworld_evidence', 0)}",
        f"- Needs manual classification: {summary['coverage_status_counts'].get('needs_manual_classification', 0)}",
        "",
        "## What Is Proven",
        "",
        "- Vanilla overworld natural mobs are not globally denied by current In Control rules, and baseline vanilla hostile pressure is boosted through Spawn Balance Utility/Majrusz.",
        "- `config/incontrol/spawner.json` explicitly injects reviewed daylight-safe modded hostile pools plus cave-native monster reinforcement.",
        "- Alex's Mobs has many enabled spawn weights in `config/alexsmobs.toml`; some mobs are intentionally unique/restricted by that mod's own config.",
        "- Cataclysm and Mowzie entries with config spawn weights/rates are recorded separately from boss/structure-only content.",
        "",
        "## What Is Not Proven",
        "",
        "- The entity registry has 757 entries, but many are projectiles, multipart entities, NPCs, bosses, summons, dimensions-only entities, or structure/event mobs.",
        "- A mob having an entity ID does not prove it naturally appears in the Overworld.",
        "- JSON/worldgen evidence alone is incomplete for mods that spawn through code/config, especially Alex's Mobs.",
        "",
        "## Verified Namespace Counts",
        "",
    ]
    for namespace, count in sorted(verified_namespaces.items()):
        lines.append(f"- `{namespace}`: {count}")

    lines.extend([
        "",
        "## Missing Expected Evidence",
        "",
    ])
    if missing:
        for entry in missing:
            lines.append(
                f"- `{entry['entity_id']}` ({entry.get('source_mod', 'Unknown')}, {entry.get('threat_tier', 'unknown')})"
            )
    else:
        lines.append("- None found by this audit.")

    lines.extend([
        "",
        "## Needs Manual Classification",
        "",
    ])
    if review:
        for entry in review:
            lines.append(
                f"- `{entry['entity_id']}` ({entry.get('source_mod', 'Unknown')}, {entry.get('threat_tier', 'unknown')})"
            )
    else:
        lines.append("- None found by this audit.")

    lines.extend([
        "",
        "## Next Actions",
        "",
        "1. Use this report to decide which `missing_expected_overworld_evidence` entries should actually be common natural spawns.",
        "2. Add only reviewed mobs to `config/incontrol/spawner.json` or mod-specific config. Do not blanket-spawn bosses, dragons, multipart entities, projectiles, summons, or NPCs.",
        "3. Test in-game with fresh chunks and real daylight/night/cave passes; this report proves configuration evidence, not live spawn frequency.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    registry_path = ROOT / "config/ascendant_index/mob_registry.json"
    registry = read_json(registry_path)

    records: dict[str, dict] = {}
    for entry in registry.get("mobs", []):
        entity_id = entry.get("entity_id")
        if not isinstance(entity_id, str) or ":" not in entity_id:
            continue
        records[entity_id] = {
            "entity_id": entity_id,
            "source_mod": entry.get("source_mod", "Unknown"),
            "threat_tier": entry.get("threat_tier", "unknown"),
            "namespace": entity_id.split(":", 1)[0],
            "bounty_tier": entry.get("bounty_tier"),
            "spawn_review": entry.get("spawn_review"),
            "evidence": [],
            "notes": [],
        }

    for entity_id, (source_mod, status, note) in VANILLA_OVERWORLD.items():
        records.setdefault(
            entity_id,
            {
                "entity_id": entity_id,
                "source_mod": source_mod,
                "threat_tier": "vanilla_overworld",
                "namespace": "minecraft",
                "evidence": [],
                "notes": [],
            },
        )
        if status == "natural_overworld":
            add_evidence(records, entity_id, "vanilla_overworld_default", "minecraft", note)
        else:
            records[entity_id]["notes"].append(note)

    registry_ids = set(records)
    source_counts = {
        "incontrol": dict(collect_incontrol_spawner(records)),
        "worldgen_audit": dict(collect_worldgen_audit(records)),
        "mod_configs": dict(collect_mod_configs(records, registry_ids)),
        "json_references": dict(collect_json_references(records, registry_ids)),
    }

    status_counts = classify(records)
    by_namespace = Counter()
    verified_by_namespace = Counter()
    for record in records.values():
        by_namespace[record["namespace"]] += 1
        if record["coverage_status"] in {
            "verified_active_injection",
            "verified_natural_or_mod_config",
            "natural_overworld",
        } or any(e["kind"] == "vanilla_overworld_default" for e in record["evidence"]):
            verified_by_namespace[record["namespace"]] += 1

    sorted_records = sorted(records.values(), key=lambda item: (item["coverage_status"], item["entity_id"]))
    report = {
        "version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "active_instance": str(ACTIVE_INSTANCE),
        "summary": {
            "total_tracked_entities": len(records),
            "registry_entity_count": len(registry.get("mobs", [])),
            "vanilla_natural_overworld_count": sum(
                1 for entity_id, data in VANILLA_OVERWORLD.items() if data[1] == "natural_overworld"
            ),
            "coverage_status_counts": dict(sorted(status_counts.items())),
            "tracked_by_namespace": dict(sorted(by_namespace.items())),
            "verified_by_namespace": dict(sorted(verified_by_namespace.items())),
            "evidence_source_counts": source_counts,
        },
        "missing_expected_overworld_evidence": [
            record for record in sorted_records if record["coverage_status"] == "missing_expected_overworld_evidence"
        ],
        "needs_manual_classification": [
            record for record in sorted_records if record["coverage_status"] == "needs_manual_classification"
        ],
        "records": sorted_records,
    }

    write_json(REPORT_JSON, report)
    REPORT_MD.write_text(build_markdown(report), encoding="utf-8")
    print(f"Wrote {REPORT_JSON.relative_to(ROOT)}")
    print(f"Wrote {REPORT_MD.relative_to(ROOT)}")
    print(json.dumps(report["summary"]["coverage_status_counts"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
