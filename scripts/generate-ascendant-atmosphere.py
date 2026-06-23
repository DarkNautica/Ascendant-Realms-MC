#!/usr/bin/env python3
"""Generate Ascendant regional atmosphere policy docs and JSON."""

from __future__ import annotations

import json
import pathlib
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONFIG = ROOT / "config" / "ascendant_atmosphere"


REGIONS = [
    {
        "region_id": "hearthlands",
        "aliases": ["crownlands", "center"],
        "atlas_pool": "center",
        "display_name": "The Crownlands",
        "subtitle_flavor": "Safe roads, soft weather, and the first promise of the realm.",
        "music_mood": "warm medieval strings, light flute, calm travel themes",
        "ambient_sound_mood": "meadow wind, birds, soft village distance, light leaves",
        "weather_mood": "temperate rain and fair skies; storms should feel rare and readable",
        "particle_visual_notes": "subtle pollen, leaves, fireflies, gentle camp smoke near authored spaces",
        "season_behavior": "visible seasonal color shifts without heavy snow or ice conversion",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "starter region must remain temperate and beginner-friendly",
        },
        "danger_mood": "safe but not sterile; danger should be signposted and sparse",
        "title_color": "f0d68a",
    },
    {
        "region_id": "frostmarch",
        "aliases": ["north"],
        "atlas_pool": "north",
        "display_name": "The Frostmarch",
        "subtitle_flavor": "Cold wind, old ice, and the long white road north.",
        "music_mood": "low drones, lonely horns, glassy bells, restrained percussion",
        "ambient_sound_mood": "cold wind, crunching snow, distant ice cracks, aurora quiet",
        "weather_mood": "snow, blizzards, frozen fog, and hard winter visibility where safe",
        "particle_visual_notes": "windblown snow, frost motes, aurora-lit nights, icy breath",
        "season_behavior": "winter may be visually strong; snow and ice are region-appropriate",
        "snow_ice_permission": {
            "allow_snow_buildup": True,
            "allow_ice_buildup": True,
            "reason": "cold-intended region",
        },
        "danger_mood": "survival pressure, cold isolation, frozen-ocean threat",
        "title_color": "9bd8ff",
    },
    {
        "region_id": "sunreach",
        "aliases": ["south"],
        "atlas_pool": "south",
        "display_name": "Sunreach",
        "subtitle_flavor": "Red dust, bright heat, and caravan tracks under a hard sky.",
        "music_mood": "dry percussion, oud-like plucks, sparse desert travel lines",
        "ambient_sound_mood": "dry wind, sand hiss, insects, distant heat shimmer",
        "weather_mood": "dry, hot, dusty, storm-scarred; rain should be uncommon and snow forbidden",
        "particle_visual_notes": "dust, ash flecks in scarred areas, heat-haze color grading where possible",
        "season_behavior": "season color can shift plants, but winter must not whiten the region",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "warm/arid region; previous warm snow bug must not return",
        },
        "danger_mood": "exposed, thirsty, bright, predator-visible",
        "title_color": "d99a4e",
    },
    {
        "region_id": "verdant_coast",
        "aliases": ["east"],
        "atlas_pool": "east",
        "display_name": "The Verdant Coast",
        "subtitle_flavor": "Rain-wet leaves, river mouths, and the sound of distant surf.",
        "music_mood": "lush strings, hand drums, rainstick-like texture, coastal motifs",
        "ambient_sound_mood": "rainforest insects, frogs, surf, mangrove water, heavy leaves",
        "weather_mood": "wet, lush, stormy, coastal; lightning and heavy rain fit better than snow",
        "particle_visual_notes": "mist, rain streaks, water drips, pollen, fireflies in humid nights",
        "season_behavior": "wet seasons can feel strong; foliage shifts should stay lush",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "wet/coastal does not mean cold",
        },
        "danger_mood": "dense, alive, hard to see through, ambush-friendly",
        "title_color": "59bd70",
    },
    {
        "region_id": "stoneback_highlands",
        "aliases": ["west"],
        "atlas_pool": "west",
        "display_name": "The Stoneback Highlands",
        "subtitle_flavor": "Stone roads, echoing cliffs, and wind over old watchfires.",
        "music_mood": "low drums, hammered strings, mountain horns, sparse stone ambience",
        "ambient_sound_mood": "high wind, rock echoes, gravel steps, distant ravens or goats if present",
        "weather_mood": "windy, mountainous, exposed; rain and fog fit, broad snow does not",
        "particle_visual_notes": "mountain mist, dust off cliff faces, falling leaves in high forests",
        "season_behavior": "cool seasonal color is fine; Atlas removed snow-risk west biomes for a reason",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "west is highland/mountain-first, not Frostmarch snow identity",
        },
        "danger_mood": "vertical, exposed, echoing, hard to cross",
        "title_color": "c7b27a",
    },
    {
        "region_id": "north_east_marches",
        "aliases": ["north_east"],
        "atlas_pool": "north_east",
        "display_name": "The North-East Marches",
        "subtitle_flavor": "Cold rain, frozen river mouths, and dark coastal timber.",
        "music_mood": "frost strings blended with wet coastal ambience",
        "ambient_sound_mood": "cold surf, wet leaves, ice cracks, gulls if present",
        "weather_mood": "cold coastal storms, sleet-like mood, frozen crossings",
        "particle_visual_notes": "mist, sleet, frost motes, spray over ice",
        "season_behavior": "snow is allowed where the selected biome data is cold",
        "snow_ice_permission": {
            "allow_snow_buildup": True,
            "allow_ice_buildup": True,
            "reason": "cold diagonal blend with Frostmarch",
        },
        "danger_mood": "cold coastal frontier",
        "title_color": "7fcfb8",
    },
    {
        "region_id": "north_west_marches",
        "aliases": ["north_west"],
        "atlas_pool": "north_west",
        "display_name": "The North-West Marches",
        "subtitle_flavor": "Wind-cut ridges, black pines, and snow in the high passes.",
        "music_mood": "frost drones with mountain horns and stone percussion",
        "ambient_sound_mood": "cold high wind, snow through pines, rockfall echoes",
        "weather_mood": "cold mountain weather; snow allowed where biome data supports it",
        "particle_visual_notes": "windblown snow, cliff dust, frost on stone",
        "season_behavior": "winter identity can be visible but should still read mountainous",
        "snow_ice_permission": {
            "allow_snow_buildup": True,
            "allow_ice_buildup": True,
            "reason": "cold diagonal blend with Frostmarch",
        },
        "danger_mood": "cold, vertical, exposed",
        "title_color": "a7c7d9",
    },
    {
        "region_id": "south_east_wilds",
        "aliases": ["south_east"],
        "atlas_pool": "south_east",
        "display_name": "The South-East Wilds",
        "subtitle_flavor": "Hot rain, red mud, and green growth fighting the desert.",
        "music_mood": "humid percussion with desert plucks and low strings",
        "ambient_sound_mood": "rain on hot leaves, insects, distant surf, dry thunder",
        "weather_mood": "hot coastal storms and monsoon mood; no snow",
        "particle_visual_notes": "mist, dust after rain, fireflies, humid haze",
        "season_behavior": "wet/dry seasonal contrast, no winter whitening",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "warm diagonal blend",
        },
        "danger_mood": "lush but heat-stressed and unstable",
        "title_color": "9fc96c",
    },
    {
        "region_id": "south_west_wilds",
        "aliases": ["south_west"],
        "atlas_pool": "south_west",
        "display_name": "The South-West Wilds",
        "subtitle_flavor": "Broken mesas, dry canyons, and wind grinding stone to dust.",
        "music_mood": "desert percussion with stone drones and tense low brass",
        "ambient_sound_mood": "dry cliff wind, grit, distant rockslide, sparse insects",
        "weather_mood": "hot, arid, storm-carved; no snow or cold-season buildup",
        "particle_visual_notes": "red dust, canyon haze, ash flecks near scarred terrain",
        "season_behavior": "dry winter colors only; no snow accumulation",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "warm/arid diagonal blend",
        },
        "danger_mood": "dry, cracked, remote, predator territory",
        "title_color": "c98d57",
    },
    {
        "region_id": "outer_rim",
        "aliases": ["outer", "deep_wilds", "dragon_scars"],
        "atlas_pool": "outer",
        "display_name": "The Outer Rim",
        "subtitle_flavor": "The map thins, the sky bruises, and old powers press close.",
        "music_mood": "oppressive drones, broken choirs, sparse drums, corrupted ambience",
        "ambient_sound_mood": "distant thunder, unnatural wind, low rumbles, hostile silence",
        "weather_mood": "dangerous, oppressive, region-by-biome; do not blanket snow warm samples",
        "particle_visual_notes": "embers, ash, strange motes, dark fog near authored danger zones",
        "season_behavior": "season behavior must follow actual biome climate; corruption should not become random snow",
        "snow_ice_permission": {
            "allow_snow_buildup": "conditional_cold_biome_only",
            "allow_ice_buildup": "conditional_cold_biome_only",
            "reason": "outer pool includes both cold and hot biomes",
        },
        "danger_mood": "oppressive, ancient, high-rank, dangerous",
        "title_color": "8c78a8",
    },
    {
        "region_id": "nether_front",
        "aliases": ["nether"],
        "atlas_pool": None,
        "display_name": "The Nether Front",
        "subtitle_flavor": "Heat, basalt, and warlight beyond the Overworld line.",
        "music_mood": "low infernal drones, basalt percussion, distant ritual tones",
        "ambient_sound_mood": "fire, basalt echoes, soul wind, lava pressure",
        "weather_mood": "dimension atmosphere only; no Overworld storm control",
        "particle_visual_notes": "embers, ash, smoke, heat shimmer",
        "season_behavior": "no Serene Seasons behavior expected",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "Nether dimension",
        },
        "danger_mood": "hostile, infernal, advanced",
        "title_color": "c85a48",
    },
    {
        "region_id": "end_expanse",
        "aliases": ["end"],
        "atlas_pool": None,
        "display_name": "The End Expanse",
        "subtitle_flavor": "A silent horizon where the world stops answering.",
        "music_mood": "void pads, distant choir, sparse crystalline pulses",
        "ambient_sound_mood": "thin wind, chorus shimmer, void silence",
        "weather_mood": "dimension atmosphere only; no Overworld storm control",
        "particle_visual_notes": "void motes, chorus particles, pale glows",
        "season_behavior": "no Serene Seasons behavior expected",
        "snow_ice_permission": {
            "allow_snow_buildup": False,
            "allow_ice_buildup": False,
            "reason": "End dimension",
        },
        "danger_mood": "silent, alien, capstone",
        "title_color": "b78cff",
    },
]

WARM_REGIONS = {
    "hearthlands",
    "sunreach",
    "verdant_coast",
    "stoneback_highlands",
    "south_east_wilds",
    "south_west_wilds",
    "nether_front",
    "end_expanse",
}


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


def mod_present(toml_name: str) -> bool:
    return (ROOT / "mods" / toml_name).exists()


def gather_evidence() -> dict[str, Any]:
    weather2 = read_text(ROOT / "config" / "Weather2" / "Snow.toml")
    snow_real_magic = read_text(ROOT / "config" / "snowrealmagic-common.yaml")
    serene = read_text(ROOT / "config" / "sereneseasons" / "seasons.toml")
    traveler_titles = read_text(ROOT / "config" / "travelerstitles-forge-1_20.toml")
    sound_physics = read_text(ROOT / "config" / "sound_physics_remastered" / "soundphysics.properties")
    resource_overrides = read_json(ROOT / "config" / "resourcepackoverrides.json", {})
    default_packs = resource_overrides.get("default_packs", []) if isinstance(resource_overrides, dict) else []
    title_lang_path = (
        ROOT
        / "resourcepacks"
        / "ascendant-realms-travelers-titles"
        / "assets"
        / "travelerstitles"
        / "lang"
        / "en_us.json"
    )
    title_lang = read_json(title_lang_path, {})
    title_keys = list(title_lang) if isinstance(title_lang, dict) else []

    return {
        "mods": {
            "Weather2": mod_present("weather-storms-tornadoes.pw.toml"),
            "Serene Seasons": mod_present("serene-seasons.pw.toml"),
            "Snow Real Magic": mod_present("snow-real-magic.pw.toml"),
            "AmbientSounds": mod_present("ambientsounds.pw.toml"),
            "Biome Music": mod_present("biome-music.pw.toml"),
            "Presence Footsteps": mod_present("presence-footsteps-forge.pw.toml"),
            "Sound Physics Remastered": mod_present("sound-physics-remastered.pw.toml"),
            "Traveler's Titles": mod_present("travelers-titles.pw.toml"),
            "Titles": mod_present("titles.pw.toml"),
            "Auroras": mod_present("auroras.pw.toml"),
            "Enhanced Celestials": mod_present("enhanced-celestials.pw.toml"),
        },
        "config_paths": {
            "weather2_snow": "config/Weather2/Snow.toml",
            "snow_real_magic": "config/snowrealmagic-common.yaml",
            "serene_seasons": "config/sereneseasons/seasons.toml",
            "traveler_titles": "config/travelerstitles-forge-1_20.toml",
            "sound_physics": "config/sound_physics_remastered/soundphysics.properties",
            "resource_pack_overrides": "config/resourcepackoverrides.json",
            "ascendant_titles_pack": str(title_lang_path.relative_to(ROOT)),
        },
        "snow_guards": {
            "weather2_allow_outside_cold_biomes": "Snowstorm_Snow_Buildup_AllowOutsideColdBiomes = false" in weather2,
            "serene_blanket_snow_ice_disabled": "generate_snow_ice = false" in serene,
            "snow_real_magic_melts_warm_biomes": "snowAndIceMeltInWarmBiomes: true" in snow_real_magic,
            "snow_real_magic_winter_only": "accumulationWinterOnly: true" in snow_real_magic,
            "snow_real_magic_snowfall_accumulation_disabled": "accumulatesDuringSnowfall: false" in snow_real_magic,
        },
        "title_evidence": {
            "traveler_biome_titles_enabled": '"Enable Biome Titles" = true' in traveler_titles,
            "traveler_dimension_titles_enabled": '"Enable Dimension Titles" = true' in traveler_titles,
            "only_show_biome_titles_under_sky": '"Only Show Biome Titles When Exposed To Skylight" = true' in traveler_titles,
            "ascendant_titles_pack_present": title_lang_path.exists(),
            "ascendant_titles_lang_keys": len(title_keys),
            "region_specific_title_keys": [
                key
                for key in title_keys
                if any(token in key for token in ("frostmarch", "sunreach", "verdant", "stoneback", "hearthlands", "outer_rim"))
            ],
            "required_resource_packs_present": {
                "Visual Titles 1.3.zip": "file/Visual Titles 1.3.zip" in default_packs,
                "Visual Travelers Titles Biomes Addon.zip": "file/Visual Travelers Titles Biomes Addon.zip" in default_packs,
                "ascendant-realms-travelers-titles": "file/ascendant-realms-travelers-titles" in default_packs,
                "MedievalMusic.zip": "file/MedievalMusic.zip" in default_packs,
            },
        },
        "sound_physics": {
            "enabled": "enabled=true" in sound_physics,
            "evaluate_ambient_sounds": "evaluate_ambient_sounds=true" in sound_physics,
            "debug_logging": "debug_logging=true" in sound_physics,
        },
    }


def build_policies(generated_at: str, evidence: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    region_ids = [region["region_id"] for region in REGIONS]
    warm_regions_allowing_snow = [
        region["region_id"]
        for region in REGIONS
        if region["region_id"] in WARM_REGIONS and region["snow_ice_permission"]["allow_snow_buildup"] is True
    ]
    region_atmosphere = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_live_atmosphere_changes",
        "scope": {
            "changes_terrain": False,
            "changes_mobs": False,
            "changes_ores": False,
            "changes_structures": False,
            "changes_weather_configs": False,
            "changes_audio_configs": False,
            "changes_title_resource_pack": False,
        },
        "known_region_ids": region_ids,
        "warm_regions": sorted(WARM_REGIONS),
        "regions": REGIONS,
        "validation": {
            "missing_region_atmosphere": [],
            "warm_regions_allowing_snow_buildup": warm_regions_allowing_snow,
            "policy_references_missing_region_ids": [],
        },
    }

    weather_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_weather_config_changes",
        "weather_layers": [
            {
                "mod": "Weather2",
                "role": "major storm/weather layer",
                "config_path": evidence["config_paths"]["weather2_snow"],
                "policy": "Keep conservative. Snowstorm buildup must stay blocked outside cold biomes.",
            },
            {
                "mod": "Serene Seasons",
                "role": "season color and weather-frequency layer",
                "config_path": evidence["config_paths"]["serene_seasons"],
                "policy": "Season color is welcome, blanket snow/ice generation stays off.",
            },
            {
                "mod": "Snow Real Magic",
                "role": "snow visual/accumulation layer",
                "config_path": evidence["config_paths"]["snow_real_magic"],
                "policy": "Warm biome melt and winter-only accumulation must remain on.",
            },
            {
                "mod": "Auroras",
                "role": "night sky atmosphere, strongest in Frostmarch and cold outer regions",
                "config_path": None,
                "policy": "Visual layer only; do not use it as proof of cold climate correctness.",
            },
            {
                "mod": "Enhanced Celestials",
                "role": "moon/event atmosphere",
                "config_path": None,
                "policy": "Use for danger mood but do not let event pressure replace Atlas progression.",
            },
        ],
        "region_weather_policy": [
            {
                "region_id": region["region_id"],
                "weather_mood": region["weather_mood"],
                "season_behavior": region["season_behavior"],
                "snow_ice_permission": region["snow_ice_permission"],
            }
            for region in REGIONS
        ],
        "config_evidence": evidence["snow_guards"],
        "validation": {
            "warm_regions_allowing_snow_buildup": warm_regions_allowing_snow,
            "weather2_allows_outside_cold_snow": not evidence["snow_guards"]["weather2_allow_outside_cold_biomes"],
            "serene_seasons_blanket_snow_enabled": not evidence["snow_guards"]["serene_blanket_snow_ice_disabled"],
            "snow_real_magic_warm_melt_disabled": not evidence["snow_guards"]["snow_real_magic_melts_warm_biomes"],
        },
    }

    audio_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_audio_config_changes",
        "audio_layers": [
            {
                "mod": "AmbientSounds",
                "role": "biome/weather ambient texture",
                "present": evidence["mods"]["AmbientSounds"],
                "policy": "Use volume tuning before removal if regions sound too busy.",
            },
            {
                "mod": "Biome Music",
                "role": "biome music variation",
                "present": evidence["mods"]["Biome Music"],
                "policy": "Future region playlists should map Atlas mood to biome pools, not names alone.",
            },
            {
                "mod": "Presence Footsteps",
                "role": "ground material/body presence",
                "present": evidence["mods"]["Presence Footsteps"],
                "policy": "Keep material feedback; verify snow/sand/stone footstep contrast in field tests.",
            },
            {
                "mod": "Sound Physics Remastered",
                "role": "occlusion/reverb/spatial mix",
                "present": evidence["mods"]["Sound Physics Remastered"],
                "policy": "Keep debug logging off; check caves/mountains for overpowering echo.",
            },
            {
                "mod": "Medieval Music",
                "role": "resource-pack music identity",
                "present": evidence["title_evidence"]["required_resource_packs_present"].get("MedievalMusic.zip", False),
                "policy": "Supports broad fantasy tone; region-specific playlists remain future work.",
            },
        ],
        "region_audio_policy": [
            {
                "region_id": region["region_id"],
                "music_mood": region["music_mood"],
                "ambient_sound_mood": region["ambient_sound_mood"],
                "danger_mood": region["danger_mood"],
            }
            for region in REGIONS
        ],
        "config_evidence": {
            "sound_physics": evidence["sound_physics"],
            "resource_packs": evidence["title_evidence"]["required_resource_packs_present"],
        },
        "validation": {
            "policy_references_missing_region_ids": [],
            "audio_policy_documented": True,
        },
    }

    title_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_title_resource_pack_changes",
        "current_title_stack": {
            "travelers_titles_config": evidence["config_paths"]["traveler_titles"],
            "biome_titles_enabled": evidence["title_evidence"]["traveler_biome_titles_enabled"],
            "dimension_titles_enabled": evidence["title_evidence"]["traveler_dimension_titles_enabled"],
            "visual_title_resource_packs": evidence["title_evidence"]["required_resource_packs_present"],
            "ascendant_titles_pack_keys": evidence["title_evidence"]["ascendant_titles_lang_keys"],
            "region_specific_title_keys": evidence["title_evidence"]["region_specific_title_keys"],
            "assessment": "Biome titles are live, but Atlas region titles are policy-only until a runtime/resource-pack hook is added.",
        },
        "region_titles": [
            {
                "region_id": region["region_id"],
                "display_name": region["display_name"],
                "subtitle_flavor": region["subtitle_flavor"],
                "title_color": region["title_color"],
                "implementation_status": "policy_only_not_live_region_trigger",
            }
            for region in REGIONS
        ],
        "validation": {
            "missing_region_title_policy": [],
            "policy_references_missing_region_ids": [],
            "title_policy_documented": True,
            "region_titles_live_enforced": False,
        },
    }
    return region_atmosphere, weather_policy, audio_policy, title_policy


def make_docs(
    generated_at: str,
    region_atmosphere: dict[str, Any],
    weather_policy: dict[str, Any],
    audio_policy: dict[str, Any],
    title_policy: dict[str, Any],
) -> tuple[str, str, str]:
    region_rows = [
        [
            f"`{region['region_id']}`",
            region["display_name"],
            region["music_mood"],
            region["weather_mood"],
            region["snow_ice_permission"]["allow_snow_buildup"],
            region["danger_mood"],
        ]
        for region in region_atmosphere["regions"]
    ]
    weather_rows = [
        [
            layer["mod"],
            layer["role"],
            layer["config_path"] or "none",
            layer["policy"],
        ]
        for layer in weather_policy["weather_layers"]
    ]
    audio_rows = [
        [layer["mod"], layer["role"], layer["present"], layer["policy"]]
        for layer in audio_policy["audio_layers"]
    ]
    title_rows = [
        [
            f"`{entry['region_id']}`",
            entry["display_name"],
            entry["subtitle_flavor"],
            entry["title_color"],
            entry["implementation_status"],
        ]
        for entry in title_policy["region_titles"]
    ]

    regional_doc = f"""
# Ascendant Regional Atmosphere

Generated: {generated_at}

Status: audit/control scaffold only. This pass did not change terrain, mobs, ores, structures, weather configs, audio configs, or title resource packs.

## Summary

- Region atmosphere rows: {len(region_atmosphere['regions'])}
- Warm regions allowing snow buildup: {len(region_atmosphere['validation']['warm_regions_allowing_snow_buildup'])}
- Weather snow guardrails currently documented: Weather2 outside-cold buildup blocked, Serene Seasons blanket snow/ice disabled, Snow Real Magic warm-biome melt enabled.
- Atlas region titles are policy-only; current Traveler's Titles support is biome/dimension title presentation, not coordinate-region title enforcement.

## Region Atmosphere Matrix

{md_table(['Region', 'Title', 'Music mood', 'Weather mood', 'Snow buildup', 'Danger mood'], region_rows)}

## Current Presentation Stack

- Weather: Weather2, Serene Seasons, Snow Real Magic, Auroras, Enhanced Celestials.
- Audio: AmbientSounds, Biome Music, Presence Footsteps, Sound Physics Remastered, Medieval Music resource pack.
- Titles/UI feedback: Traveler's Titles, Titles, Visual Titles, Visual Traveler's Title Biomes Addon, pack-owned `ascendant-realms-travelers-titles`.

## Important Boundary

This is a regional presentation policy. It does not prove terrain signoff and does not replace the Atlas water review. Terrain remains partial until the south/west ocean-leak samples are resolved or accepted through manual review.
"""

    weather_doc = f"""
# Weather And Season Region Policy

Generated: {generated_at}

Status: audit/control scaffold only. No weather or season config was changed by this pass.

## Weather Layer Audit

{md_table(['Layer', 'Role', 'Config path', 'Policy'], weather_rows)}

## Snow Guard Evidence

| Guard | Current result |
| --- | --- |
| Weather2 blocks snow buildup outside cold biomes | {weather_policy['config_evidence']['weather2_allow_outside_cold_biomes']} |
| Serene Seasons blanket snow/ice conversion disabled | {weather_policy['config_evidence']['serene_blanket_snow_ice_disabled']} |
| Snow Real Magic melts snow/ice in warm biomes | {weather_policy['config_evidence']['snow_real_magic_melts_warm_biomes']} |
| Snow Real Magic accumulation is winter-only | {weather_policy['config_evidence']['snow_real_magic_winter_only']} |
| Snow Real Magic snowfall accumulation disabled | {weather_policy['config_evidence']['snow_real_magic_snowfall_accumulation_disabled']} |

## Regional Rules

- Frostmarch can use snow, cold wind, auroras, frozen ambience, snow roads, and harsh winter presentation.
- Sunreach should remain dry, hot, dusty, and storm-scarred, with no snow or ice buildup.
- Verdant Coast should be wet, lush, stormy, coastal, and humid rather than cold.
- Stoneback Highlands should feel windy, mountainous, echoing, and rocky; do not reintroduce broad snow.
- Hearthlands/Crownlands should stay safe, temperate, readable, and beginner-friendly.
- Outer regions can be oppressive and dangerous, but snow must still follow actual cold biome intent instead of blanket conversion.
"""

    audio_title_doc = f"""
# Biome Title And Audio Policy

Generated: {generated_at}

Status: audit/control scaffold only. No title resource pack, audio config, or UI config was changed by this pass.

## Audio Layer Audit

{md_table(['Layer', 'Role', 'Present', 'Policy'], audio_rows)}

## Region Title Policy

{md_table(['Region', 'Display title', 'Subtitle flavor', 'Color', 'Implementation'], title_rows)}

## Current Title Stack Evidence

- Traveler's Titles biome titles enabled: {title_policy['current_title_stack']['biome_titles_enabled']}
- Traveler's Titles dimension titles enabled: {title_policy['current_title_stack']['dimension_titles_enabled']}
- Pack-owned Traveler's Titles fallback keys: {title_policy['current_title_stack']['ascendant_titles_pack_keys']}
- Region-specific title keys currently present: {len(title_policy['current_title_stack']['region_specific_title_keys'])}

## Implementation Boundary

Biome titles are currently live through Traveler's Titles. Atlas coordinate-region titles are not live-enforced yet. A future KubeJS/resource-pack or helper hook should display region names from `config/ascendant_atmosphere/title_policy.json` using Atlas region scoreboards, but that should wait until terrain and water review are accepted.
"""
    return regional_doc, weather_doc, audio_title_doc


def main() -> int:
    generated_at = now_iso()
    evidence = gather_evidence()
    region_atmosphere, weather_policy, audio_policy, title_policy = build_policies(generated_at, evidence)
    regional_doc, weather_doc, audio_title_doc = make_docs(
        generated_at, region_atmosphere, weather_policy, audio_policy, title_policy
    )

    write_json(CONFIG / "region_atmosphere.json", region_atmosphere)
    write_json(CONFIG / "weather_policy.json", weather_policy)
    write_json(CONFIG / "audio_policy.json", audio_policy)
    write_json(CONFIG / "title_policy.json", title_policy)
    write_md(DOCS / "ASCENDANT_REGIONAL_ATMOSPHERE.md", regional_doc)
    write_md(DOCS / "WEATHER_AND_SEASON_REGION_POLICY.md", weather_doc)
    write_md(DOCS / "BIOME_TITLE_AND_AUDIO_POLICY.md", audio_title_doc)

    print("Generated Ascendant regional atmosphere audit and policies.")
    print(f"Regions: {len(region_atmosphere['regions'])}")
    print(f"Warm regions allowing snow: {len(region_atmosphere['validation']['warm_regions_allowing_snow_buildup'])}")
    print(f"Title fallback keys: {title_policy['current_title_stack']['ascendant_titles_pack_keys']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
