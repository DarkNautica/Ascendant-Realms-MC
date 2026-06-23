#!/usr/bin/env python3
"""Generate the first Ascendant Structure Director visual review route."""

from __future__ import annotations

import json
import pathlib
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONFIG = ROOT / "config" / "ascendant_structures"

COMMON_VISUAL_QUESTIONS = [
    "Does it belong in this biome/region?",
    "Is it too close to spawn?",
    "Is it too common?",
    "Is it buried, floating, or clipping?",
    "Does terrain support it naturally?",
    "Does loot/danger appear appropriate?",
]

SECTION_QUESTIONS = {
    "beginner_region_structures": [
        "Does this feel safe enough for Crownlands/Hearthlands play?",
        "Should this be kept near spawn, pushed outward, or reviewed for region lock?",
    ],
    "dungeon_structures": [
        "Does the entrance read clearly as a dungeon?",
        "Does this feel common, large, underground, boss-tier, or late-game?",
    ],
    "water_structures": [
        "Does water structure actually sit in appropriate water?",
        "Does sea-floor structure actually sit on sea floor?",
        "Does the shoreline/coastline placement look natural?",
    ],
    "sky_structures": [
        "Does sky structure feel rare/special or spammy?",
        "Does the vertical placement look intentional from the ground?",
    ],
    "village_town_settlement_structures": [
        "Does village/town structure overlap or compress?",
        "Which settlement pieces may later accept Hunter Boards/Guild Halls?",
    ],
    "boss_dragon_structures": [
        "Does boss structure feel too early?",
        "Should this be pushed away from center or locked to a stronger region/ring?",
    ],
    "region_fit_checks": [
        "Does the structure reinforce the target Atlas region identity?",
        "Does it break the intended north/south/east/west gradient?",
    ],
}

REGION_SEARCH_ORIGINS = {
    "hearthlands": "/tp @s 0 120 0",
    "crownlands": "/tp @s 0 120 0",
    "frostmarch": "/tp @s 0 130 -9000",
    "north_east_marches": "/tp @s 8000 130 -8000",
    "north_west_marches": "/tp @s -8000 140 -8000",
    "sunreach": "/tp @s 0 120 9000",
    "south_east_wilds": "/tp @s 8000 120 8000",
    "south_west_wilds": "/tp @s -8000 140 8000",
    "verdant_coast": "/tp @s 9000 120 0",
    "stoneback_highlands": "/tp @s -9000 150 0",
    "outer": "/tp @s 22000 160 22000",
    "boss_theme_region": "/tp @s 18000 160 18000",
    "coastal_only": "/tp @s 9000 120 2000",
    "frozen_ocean_only": "/tp @s 0 130 -14000",
    "frostmarch_if_frozen": "/tp @s 0 130 -12000",
    "nether_only": "Use the Nether before locating this structure.",
    "end_only": "Use the End before locating this structure.",
    "atlas_region_matching_biome_tag": "Start in the Atlas region you want to test, then run locate.",
    "region_compatible_settlement": "/tp @s 0 120 0",
}

BEGINNER_REGIONS = {"hearthlands", "crownlands", "center", "region_compatible_settlement"}
WATER_REGIONS = {
    "verdant_coast",
    "coastal_only",
    "frostmarch_if_frozen",
    "frozen_ocean_only",
    "frostmarch",
    "north_east_marches",
    "south_east_wilds",
}
RISKY_SOURCE_TOKENS = [
    "Integrated Dungeons",
    "Integrated Villages",
    "Towns and Towers",
    "Ice And Fire",
    "cataclysm",
    "Bosses",
    "moogs",
    "YUNG",
    "Aquamirae",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: pathlib.Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_md(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    if value in (None, ""):
        return []
    return [str(value)]


def structure_set_ids(value: Any) -> list[str]:
    if isinstance(value, list):
        output = []
        for item in value:
            if isinstance(item, dict):
                set_id = item.get("structure_set")
                if set_id:
                    output.append(str(set_id))
            elif item:
                output.append(str(item))
        return output
    if isinstance(value, dict):
        set_id = value.get("structure_set")
        return [str(set_id)] if set_id else []
    if value in (None, ""):
        return []
    return [str(value)]


def first_or_unknown(values: list[str]) -> str:
    return values[0] if values else "unknown"


def md_cell(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    output = ["| " + " | ".join(headers) + " |"]
    output.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        output.append("| " + " | ".join(md_cell(cell) for cell in row) + " |")
    return "\n".join(output)


def preview_ids(entries: list[dict[str, Any]], limit: int = 20) -> list[str]:
    return [str(entry.get("structure_id")) for entry in entries[:limit]]


def load_maps() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    registry = read_json(CONFIG / "structure_registry.json", {})
    density = read_json(CONFIG / "structure_density_policy.json", {})
    region_rules = read_json(CONFIG / "structure_region_rules.json", {})
    vertical_rules = read_json(CONFIG / "structure_vertical_layer_rules.json", {})
    loot_linkage = read_json(CONFIG / "structure_loot_linkage.json", {})

    structures = {
        str(entry.get("structure_id")): dict(entry)
        for entry in registry.get("structures", [])
        if isinstance(entry, dict) and entry.get("structure_id")
    }

    density_by_id = {
        str(entry.get("structure_id")): dict(entry)
        for entry in density.get("structures", [])
        if isinstance(entry, dict) and entry.get("structure_id")
    }
    region_by_id = {
        str(entry.get("structure_id")): dict(entry)
        for entry in region_rules.get("region_rules", [])
        if isinstance(entry, dict) and entry.get("structure_id")
    }
    vertical_by_id = {
        str(entry.get("structure_id")): dict(entry)
        for entry in vertical_rules.get("vertical_layer_rules", [])
        if isinstance(entry, dict) and entry.get("structure_id")
    }
    loot_by_id = {
        str(entry.get("structure_id")): dict(entry)
        for entry in loot_linkage.get("structure_loot_linkage", [])
        if isinstance(entry, dict) and entry.get("structure_id")
    }

    structure_set_lookup: dict[str, list[str]] = {}
    for structure_set in density.get("structure_sets", []):
        if not isinstance(structure_set, dict):
            continue
        set_id = str(structure_set.get("structure_set", ""))
        for item in structure_set.get("structures", []):
            if not isinstance(item, dict):
                continue
            sid = item.get("structure")
            if sid:
                structure_set_lookup.setdefault(str(sid), []).append(set_id)

    for sid, entry in structures.items():
        entry.update({k: v for k, v in density_by_id.get(sid, {}).items() if v not in (None, [], "")})
        entry.update({k: v for k, v in region_by_id.get(sid, {}).items() if v not in (None, [], "")})
        entry.update({k: v for k, v in vertical_by_id.get(sid, {}).items() if v not in (None, [], "")})
        entry.update({k: v for k, v in loot_by_id.get(sid, {}).items() if v not in (None, [], "")})
        entry["structure_sets"] = sorted(set(structure_set_ids(entry.get("structure_sets")) + structure_set_lookup.get(sid, [])))

    return structures, density_by_id, region_by_id, vertical_by_id


def risk_score(entry: dict[str, Any]) -> int:
    score = 0
    priority = str(entry.get("manual_review_priority", "")).lower()
    score += {"critical": 50, "high": 35, "medium": 18, "low": 5}.get(priority, 0)

    action = str(entry.get("recommended_action", "")).lower()
    score += {
        "should_disable": 35,
        "should_reduce": 26,
        "should_region_lock": 24,
        "needs_test": 22,
        "defer_until_guild_phase": 8,
        "should_keep_debug_only": 8,
    }.get(action, 0)

    density_risk = str(entry.get("density_risk", "")).lower()
    score += {"dangerously_dense": 28, "dense": 20, "missing_spacing_data": 12}.get(density_risk, 0)

    structure_class = str(entry.get("structure_class", "")).lower()
    score += {"boss_arena": 32, "dragon_tier_zone": 34, "dangerous_dungeon": 18, "settlement": 14}.get(
        structure_class, 0
    )

    try:
        danger_tier = int(entry.get("danger_tier", 0))
    except (TypeError, ValueError):
        danger_tier = 0
    score += danger_tier * 3

    regions = set(as_list(entry.get("atlas_allowed_regions")))
    if regions & BEGINNER_REGIONS and (danger_tier >= 3 or structure_class in {"boss_arena", "dragon_tier_zone"}):
        score += 35

    water_role = str(entry.get("water_role", "none"))
    sky_role = str(entry.get("sky_role", "none"))
    layers = set(as_list(entry.get("vertical_layers")))
    if water_role != "none" or layers & {"sea_floor", "sea_surface", "river_or_wetland", "coastal_surface"}:
        score += 14
        if not regions & WATER_REGIONS and "atlas_region_matching_biome_tag" not in regions:
            score += 18
    if sky_role != "none" or layers & {"sky_low", "sky_high"}:
        score += 18
        if entry.get("density_class") in {"common", "uncommon"}:
            score += 12

    source_mod = str(entry.get("source_mod", ""))
    if any(token.lower() in source_mod.lower() for token in RISKY_SOURCE_TOKENS):
        score += 7

    risk_flags = as_list(entry.get("risk_flags"))
    score += min(len(risk_flags) * 3, 18)
    if entry.get("manual_review_required") is True:
        score += 30
    confidence = str(entry.get("classification_confidence", "")).lower()
    score += {"weak": 35, "medium": 16}.get(confidence, 0)
    if "manual_water_island_placement_issue" in risk_flags:
        score += 45
    if entry.get("name_only_classification") is True:
        score += 50
    return score


def infer_search_origin(regions: list[str]) -> str:
    for region in regions:
        if region in REGION_SEARCH_ORIGINS:
            return REGION_SEARCH_ORIGINS[region]
    return "Start in the region you want to validate, then run locate."


def focus_tags(entry: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    sid = str(entry.get("structure_id", ""))
    structure_class = str(entry.get("structure_class", ""))
    water_role = str(entry.get("water_role", "none"))
    sky_role = str(entry.get("sky_role", "none"))
    layers = set(as_list(entry.get("vertical_layers")))
    regions = set(as_list(entry.get("atlas_allowed_regions")))

    if structure_class == "dangerous_dungeon" or "dungeon" in sid or "mineshaft" in sid:
        tags.append("dungeon")
    if structure_class in {"boss_arena", "dragon_tier_zone"} or int(entry.get("danger_tier") or 0) >= 5:
        tags.append("boss_or_dragon")
    if structure_class == "settlement" or any(word in sid for word in ["village", "town", "camp", "house", "inn"]):
        tags.append("village_town_settlement")
    if water_role != "none" or layers & {"sea_floor", "sea_surface", "river_or_wetland", "coastal_surface"}:
        tags.append("water")
    if layers & {"sea_floor"} or water_role == "sea_floor":
        tags.append("sea_floor")
    if layers & {"sea_surface"} or water_role == "ship_or_ocean_surface":
        tags.append("ship_or_ocean_surface")
    if sky_role != "none" or layers & {"sky_low", "sky_high"} or "airship" in sid or "floating" in sid:
        tags.append("sky")
    if regions & BEGINNER_REGIONS:
        tags.append("beginner_region")
    if str(entry.get("recommended_action")) in {"should_reduce", "should_region_lock", "needs_test"}:
        tags.append(str(entry.get("recommended_action")))
    return sorted(set(tags))


def entry_for_route(entry: dict[str, Any], section_id: str, region_focus: str | None = None) -> dict[str, Any]:
    regions = as_list(entry.get("atlas_allowed_regions"))
    layers = as_list(entry.get("vertical_layers"))
    visual_questions = list(dict.fromkeys(COMMON_VISUAL_QUESTIONS + SECTION_QUESTIONS.get(section_id, [])))
    return {
        "structure_id": str(entry.get("structure_id")),
        "structure_set_id": first_or_unknown(structure_set_ids(entry.get("structure_sets"))),
        "structure_set_ids": structure_set_ids(entry.get("structure_sets")),
        "source_mod": str(entry.get("source_mod", "unknown")),
        "category": str(entry.get("category", "unknown")),
        "structure_class": str(entry.get("structure_class", "unknown")),
        "expected_atlas_region": first_or_unknown(regions),
        "expected_atlas_regions": regions,
        "expected_region_focus": region_focus or first_or_unknown(regions),
        "expected_distance_ring": first_or_unknown(as_list(entry.get("distance_ring"))),
        "expected_vertical_layer": first_or_unknown(layers),
        "expected_vertical_layers": layers,
        "expected_rarity_density": str(entry.get("density_class", "unknown")),
        "expected_danger_tier": entry.get("danger_tier", "unknown"),
        "expected_loot_tier": str(entry.get("loot_tier", "review")),
        "guild_rank_tier": str(entry.get("guild_rank_tier", "manual_review")),
        "recommended_action": str(entry.get("recommended_action", "manual_review")),
        "manual_review_priority": str(entry.get("manual_review_priority", "manual_review")),
        "classification_confidence": str(entry.get("classification_confidence", "unknown")),
        "confidence": entry.get("confidence", "unknown"),
        "evidence_source": as_list(entry.get("evidence_source")),
        "classification_reason": str(entry.get("classification_reason", "")),
        "manual_review_required": entry.get("manual_review_required", True),
        "name_only_classification": entry.get("name_only_classification", False),
        "risk_flags": as_list(entry.get("risk_flags")),
        "focus_tags": focus_tags(entry),
        "locate_command": f"/locate structure {entry.get('structure_id')}",
        "suggested_search_origin_tp": infer_search_origin(regions),
        "suggested_tp_command_after_locate": "/tp @s <x> ~ <z>  (replace <x>/<z> with the coordinates returned by /locate)",
        "visual_questions": visual_questions,
        "review_result": {
            "pass": None,
            "fail": None,
            "manual_review": True,
            "observed_coordinates": "",
            "observed_atlas_region": "",
            "observed_biome": "",
            "notes": "",
            "screenshot_paths": [],
        },
    }


def unique_sorted(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output = []
    for entry in sorted(entries, key=lambda e: (-risk_score(e), str(e.get("structure_id")))):
        sid = str(entry.get("structure_id"))
        if sid in seen:
            continue
        seen.add(sid)
        output.append(entry)
    return output


def unique_sorted_by(entries: list[dict[str, Any]], score_func: Any) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output = []
    for entry in sorted(entries, key=lambda e: (-score_func(e), -risk_score(e), str(e.get("structure_id")))):
        sid = str(entry.get("structure_id"))
        if sid in seen:
            continue
        seen.add(sid)
        output.append(entry)
    return output


def pick(entries: list[dict[str, Any]], predicate: Any, limit: int) -> list[dict[str, Any]]:
    return unique_sorted([entry for entry in entries if predicate(entry)])[:limit]


def pick_by(entries: list[dict[str, Any]], predicate: Any, limit: int, score_func: Any) -> list[dict[str, Any]]:
    return unique_sorted_by([entry for entry in entries if predicate(entry)], score_func)[:limit]


def has_any(entry: dict[str, Any], values: set[str]) -> bool:
    return bool(set(as_list(entry.get("atlas_allowed_regions"))) & values)


def water_priority_score(entry: dict[str, Any]) -> int:
    water_role = str(entry.get("water_role", "none"))
    layers = set(as_list(entry.get("vertical_layers")))
    score = {
        "sea_floor": 120,
        "ship_or_ocean_surface": 110,
        "ocean": 95,
        "coastline": 85,
        "river_or_wetland": 65,
        "frozen_ocean": 45,
    }.get(water_role, 0)
    if "sea_floor" in layers:
        score += 80
    if "sea_surface" in layers:
        score += 70
    if "coastal_surface" in layers:
        score += 45
    if "river_or_wetland" in layers:
        score += 35
    return score


def generate_sections(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    beginner = pick(
        entries,
        lambda e: has_any(e, BEGINNER_REGIONS)
        or (
            int(e.get("danger_tier") or 0) <= 2
            and first_or_unknown(as_list(e.get("vertical_layers"))) in {"surface_land", "underground"}
        ),
        36,
    )
    dungeons = pick(
        entries,
        lambda e: str(e.get("structure_class")) == "dangerous_dungeon"
        or "dungeon" in str(e.get("structure_id"))
        or "mineshaft" in str(e.get("structure_id"))
        or "underground" in as_list(e.get("vertical_layers")),
        42,
    )
    water = pick_by(
        entries,
        lambda e: str(e.get("water_role", "none")) != "none"
        or bool(set(as_list(e.get("vertical_layers"))) & {"sea_floor", "sea_surface", "river_or_wetland", "coastal_surface"}),
        36,
        water_priority_score,
    )
    sky = pick(
        entries,
        lambda e: str(e.get("sky_role", "none")) != "none"
        or bool(set(as_list(e.get("vertical_layers"))) & {"sky_low", "sky_high"})
        or "airship" in str(e.get("structure_id"))
        or "floating" in str(e.get("structure_id")),
        16,
    )
    settlements = pick(
        entries,
        lambda e: str(e.get("structure_class")) == "settlement"
        or any(word in str(e.get("structure_id")) for word in ["village", "town", "camp", "house", "inn", "lumber"]),
        40,
    )
    bosses = pick(
        entries,
        lambda e: str(e.get("structure_class")) in {"boss_arena", "dragon_tier_zone"}
        or int(e.get("danger_tier") or 0) >= 5,
        36,
    )

    region_specs = [
        ("frostmarch", {"frostmarch", "north_east_marches", "frozen_ocean_only", "frostmarch_if_frozen"}),
        ("sunreach", {"sunreach", "south_west_wilds"}),
        ("verdant_coast", {"verdant_coast", "south_east_wilds", "coastal_only"}),
        ("stoneback_highlands", {"stoneback_highlands", "north_west_marches", "stoneback_if_taiga"}),
        ("crownlands_hearthlands", {"crownlands", "hearthlands", "region_compatible_settlement"}),
        ("outer_rim_high_danger", {"outer", "boss_theme_region"}),
    ]
    region_fit_entries: list[dict[str, Any]] = []
    for focus, regions in region_specs:
        for entry in pick(entries, lambda e, regions=regions: has_any(e, regions), 12):
            route_entry = entry_for_route(entry, "region_fit_checks", region_focus=focus)
            region_fit_entries.append(route_entry)

    sections = [
        ("beginner_region_structures", "Beginner-region structures", beginner),
        ("dungeon_structures", "Dungeon structures", dungeons),
        ("water_structures", "Water structures", water),
        ("sky_structures", "Sky structures", sky),
        ("village_town_settlement_structures", "Village/town/settlement structures", settlements),
        ("boss_dragon_structures", "Boss/dragon structures", bosses),
    ]

    output = []
    for section_id, title, section_entries in sections:
        output.append(
            {
                "section_id": section_id,
                "title": title,
                "entry_count": len(section_entries),
                "entries": [entry_for_route(entry, section_id) for entry in section_entries],
            }
        )

    output.append(
        {
            "section_id": "region_fit_checks",
            "title": "Region-fit checks",
            "entry_count": len(region_fit_entries),
            "entries": region_fit_entries,
        }
    )
    return output


def generate_priority_queues(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    highest = unique_sorted(entries)[:20]
    water = pick_by(
        entries,
        lambda e: str(e.get("water_role", "none")) != "none"
        or bool(set(as_list(e.get("vertical_layers"))) & {"sea_floor", "sea_surface", "coastal_surface"}),
        10,
        water_priority_score,
    )
    sky = pick(
        entries,
        lambda e: str(e.get("sky_role", "none")) != "none"
        or bool(set(as_list(e.get("vertical_layers"))) & {"sky_low", "sky_high"})
        or "airship" in str(e.get("structure_id"))
        or "floating" in str(e.get("structure_id")),
        10,
    )
    boss_dungeon = pick(
        entries,
        lambda e: str(e.get("structure_class")) in {"boss_arena", "dragon_tier_zone", "dangerous_dungeon"}
        or int(e.get("danger_tier") or 0) >= 3,
        10,
    )
    settlement = pick(
        entries,
        lambda e: str(e.get("structure_class")) == "settlement"
        or any(word in str(e.get("structure_id")) for word in ["village", "town", "camp", "house", "inn"]),
        10,
    )
    beginner = pick(
        entries,
        lambda e: has_any(e, BEGINNER_REGIONS)
        or (int(e.get("danger_tier") or 0) >= 3 and has_any(e, BEGINNER_REGIONS)),
        10,
    )
    return {
        "highest_risk_first_20": [entry_for_route(entry, "region_fit_checks") for entry in highest],
        "water_ship_seafloor_top_10": [entry_for_route(entry, "water_structures") for entry in water],
        "sky_floating_top_10": [entry_for_route(entry, "sky_structures") for entry in sky],
        "boss_dungeon_top_10": [entry_for_route(entry, "boss_dragon_structures") for entry in boss_dungeon],
        "village_town_overlap_top_10": [entry_for_route(entry, "village_town_settlement_structures") for entry in settlement],
        "beginner_region_risks_top_10": [entry_for_route(entry, "beginner_region_structures") for entry in beginner],
    }


def route_summary(route: dict[str, Any], priority_queues: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    section_counts = {section["section_id"]: section["entry_count"] for section in route["sections"]}
    locate_commands = {
        entry["locate_command"]
        for section in route["sections"]
        for entry in section["entries"]
    }
    priority_ids = {
        entry["structure_id"]
        for queue in priority_queues.values()
        for entry in queue
    }
    return {
        "section_counts": section_counts,
        "unique_locate_command_count": len(locate_commands),
        "priority_queue_total_entries": sum(len(queue) for queue in priority_queues.values()),
        "priority_queue_unique_structures": len(priority_ids),
    }


def write_locate_commands(route: dict[str, Any], priority_queues: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# Ascendant Structure Locate Commands",
        "",
        f"Generated: {route['generated_at']}",
        "",
        "These commands are review-only. They do not enable structure overrides, inject villages, add Hunter Boards, add Guild Halls, place NPCs, or change loot.",
        "",
        "Workflow:",
        "1. Create a fresh creative validation world.",
        "2. Use the suggested search-origin teleport when one is listed.",
        "3. Run the locate command.",
        "4. Use `/tp @s <x> ~ <z>` with the coordinates returned by `/locate`.",
        "5. Run `/ascatlas here` at the result and record the visible biome, Atlas region, clipping, density, danger, and screenshots.",
        "",
    ]

    for queue_name, entries in priority_queues.items():
        lines.extend([f"## {queue_name}", ""])
        for entry in entries:
            lines.append(f"- `{entry['structure_id']}`")
            lines.append(f"  - Search origin: `{entry['suggested_search_origin_tp']}`")
            lines.append(f"  - Locate: `{entry['locate_command']}`")
            lines.append(f"  - After locate: `{entry['suggested_tp_command_after_locate']}`")
        lines.append("")

    for section in route["sections"]:
        lines.extend([f"## {section['title']}", ""])
        for entry in section["entries"]:
            lines.append(f"- `{entry['locate_command']}` - {entry['structure_id']}")
        lines.append("")

    write_md(CONFIG / "structure_locate_commands.md", "\n".join(lines))


def write_route_doc(route: dict[str, Any], priority_queues: dict[str, list[dict[str, Any]]], summary: dict[str, Any]) -> None:
    rows = [
        [section["title"], section["section_id"], section["entry_count"]]
        for section in route["sections"]
    ]
    priority_rows = [
        [queue_name, len(entries), ", ".join(preview_ids(entries, 5))]
        for queue_name, entries in priority_queues.items()
    ]
    first_rows = [
        [
            entry["structure_id"],
            entry["source_mod"],
            entry["expected_atlas_region"],
            entry["expected_vertical_layer"],
            entry["expected_rarity_density"],
            entry["expected_danger_tier"],
            entry["expected_loot_tier"],
            entry["recommended_action"],
            entry["locate_command"],
        ]
        for entry in priority_queues["highest_risk_first_20"]
    ]
    text = f"""# Structure Visual Review Route

Generated: {route['generated_at']}

This is the first in-game Structure Director validation route. It is review-only. It does not add mods, enable live structure overrides, inject Hunter Boards or Guild Halls, place NPCs, alter villages, alter roads or bridges, rewrite loot, rewrite recipes, enable magic gates, or enable rank gates.

## Summary

- Route sections: {len(route['sections'])}.
- Unique locate commands in route: {summary['unique_locate_command_count']}.
- Priority queue entries: {summary['priority_queue_total_entries']}.
- Unique priority structures: {summary['priority_queue_unique_structures']}.
- Source structure registry rows: {route['source_counts']['structure_registry_rows']}.
- Structure set policy rows: {route['source_counts']['structure_set_policy_rows']}.
- Candidate overrides remain disabled under `config/ascendant_structures/candidates/`.
- Latest field findings, when present: `docs/STRUCTURE_VISUAL_REVIEW_FINDINGS.md`.

## How To Use

1. Create a fresh creative validation world or fly into ungenerated chunks.
2. Open `config/ascendant_structures/structure_locate_commands.md`.
3. Start with `highest_risk_first_20`, then water, sky, boss/dungeon, village/town, and beginner-region queues.
4. For each entry, use the search-origin teleport if listed, run `/locate structure <id>`, then teleport to the returned coordinates.
5. Run `/ascatlas here` at the located structure and record the Atlas region, visible biome, coordinates, screenshots, and pass/fail notes.

## Route Sections

{md_table(["Section", "ID", "Entries"], rows)}

## Priority Queues

{md_table(["Queue", "Entries", "First IDs"], priority_rows)}

## First 20 Highest-Risk Checks

{md_table(["Structure", "Mod", "Region", "Layer", "Density", "Danger", "Loot", "Action", "Locate"], first_rows)}

## Review Questions

- Does it belong in this biome/region?
- Is it too close to spawn?
- Is it too common?
- Is it buried, floating, or clipping?
- Does terrain support it naturally?
- Does water structure actually sit in appropriate water?
- Does sea-floor structure actually sit on sea floor?
- Does sky structure feel rare/special or spammy?
- Does boss structure feel too early?
- Does village/town structure overlap or compress?
- Does loot/danger appear appropriate?

## Boundaries

- Do not enable candidate overrides from this route.
- Do not move files into OpenLoader from this route.
- Do not inject villages, roads, bridges, Hunter Boards, Guild Halls, NPCs, loot rewrites, recipe gates, magic gates, or rank gates.
- Use this route to gather evidence, not to make automatic decisions.
"""
    write_md(DOCS / "STRUCTURE_VISUAL_REVIEW_ROUTE.md", text)


def write_review_template(route: dict[str, Any]) -> None:
    text = f"""# Structure Director Review Results Template

Generated: {route['generated_at']}

Copy one block per located structure into the review notes. This is manual evidence only; it does not approve live overrides by itself.

## Review Entry

- Structure ID:
- Structure set ID:
- Source mod:
- Locate command:
- Locate result coordinates:
- Teleport used:
- Atlas region from `/ascatlas here`:
- Visible biome:
- Expected Atlas region:
- Expected distance ring:
- Expected vertical layer:
- Expected density:
- Expected danger tier:
- Expected loot tier:
- Screenshots:

## Visual Answers

- Does it belong in this biome/region?
- Is it too close to spawn?
- Is it too common?
- Is it buried, floating, or clipping?
- Does terrain support it naturally?
- Does water structure actually sit in appropriate water?
- Does sea-floor structure actually sit on sea floor?
- Does sky structure feel rare/special or spammy?
- Does boss structure feel too early?
- Does village/town structure overlap or compress?
- Does loot/danger appear appropriate?

## Decision

- Pass:
- Fail:
- Manual review:
- Classification:
- Suggested action:
- Notes:
"""
    write_md(DOCS / "STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md", text)


def write_testing_checklist(route: dict[str, Any], summary: dict[str, Any]) -> None:
    text = f"""# Structure Testing Checklist

Generated: {route['generated_at']}

Use this after Jayden accepts the current Atlas terrain enough to test structures. Always use a fresh world or ungenerated chunks.

## Setup

1. Create a fresh creative validation world.
2. Keep the current Atlas terrain validation reports for reference.
3. Open `docs/STRUCTURE_VISUAL_REVIEW_ROUTE.md` for the route overview.
4. Open `config/ascendant_structures/structure_locate_commands.md` for copy-ready commands.
5. For each find, record coordinates, Atlas region, visible biome, structure ID, nearby structures, and a screenshot if it fails.

## Current Review Route

- Route file: `config/ascendant_structures/structure_visual_review_route.json`.
- Locate commands: `config/ascendant_structures/structure_locate_commands.md`.
- Priority queue: `config/ascendant_structures/structure_review_priority_queue.json`.
- Results template: `docs/STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md`.
- Unique locate commands: {summary['unique_locate_command_count']}.
- Priority queue entries: {summary['priority_queue_total_entries']}.

## Recommended Order

1. `highest_risk_first_20`
2. `water_ship_seafloor_top_10`
3. `sky_floating_top_10`
4. `boss_dungeon_top_10`
5. `village_town_overlap_top_10`
6. `beginner_region_risks_top_10`
7. Section sweeps for beginner, dungeon, water, sky, settlement, boss/dragon, and region-fit checks.

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
- Do not move review candidates into OpenLoader.
- Do not rewrite loot or recipes.
"""
    write_md(DOCS / "STRUCTURE_TESTING_CHECKLIST.md", text)


def main() -> int:
    structures, _density_by_id, _region_by_id, _vertical_by_id = load_maps()
    entries = list(structures.values())
    generated_at = now_iso()
    sections = generate_sections(entries)
    priority_queues = generate_priority_queues(entries)

    density = read_json(CONFIG / "structure_density_policy.json", {})
    route = {
        "version": 1,
        "generated_at": generated_at,
        "status": "manual_visual_review_route_no_live_generation_changes",
        "fresh_world_required": True,
        "live_gameplay_files_changed": False,
        "active_instance_sync_required": False,
        "constraints": [
            "Do not add new mods.",
            "Do not enable live structure overrides.",
            "Do not inject Hunter Boards or Guild Halls.",
            "Do not place NPCs.",
            "Do not alter villages, roads, bridges, loot, recipes, magic gates, or rank gates.",
        ],
        "source_counts": {
            "structure_registry_rows": len(entries),
            "structure_set_policy_rows": len(density.get("structure_sets", [])),
        },
        "global_visual_questions": COMMON_VISUAL_QUESTIONS,
        "sections": sections,
    }
    summary = route_summary(route, priority_queues)
    route["summary"] = summary

    queue = {
        "version": 1,
        "generated_at": generated_at,
        "status": "manual_priority_queue_no_live_generation_changes",
        "priority_queues": priority_queues,
        "summary": summary,
    }

    write_json(CONFIG / "structure_visual_review_route.json", route)
    write_json(CONFIG / "structure_review_priority_queue.json", queue)
    write_locate_commands(route, priority_queues)
    write_route_doc(route, priority_queues, summary)
    write_review_template(route)
    write_testing_checklist(route, summary)

    print(f"Generated structure visual review route with {summary['unique_locate_command_count']} locate commands.")
    print(f"Generated {summary['priority_queue_total_entries']} priority queue entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
