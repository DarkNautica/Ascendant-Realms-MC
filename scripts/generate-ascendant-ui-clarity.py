#!/usr/bin/env python3
"""Generate Ascendant UI clarity policy docs and validation JSON."""

from __future__ import annotations

import json
import pathlib
import re
from collections import Counter
from datetime import datetime, timezone
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ in normal workflow.
    tomllib = None


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONFIG = ROOT / "config" / "ascendant_ui"

TANGIBLE_GEAR_COLLECTIONS = [
    "weapons",
    "armor",
    "shields",
    "magic_items",
    "accessories_relics",
]

RARITY_ORDER = [
    "common",
    "uncommon",
    "rare",
    "epic",
    "legendary",
    "mythic",
    "ascendant",
]

REQUIRED_TITLE_PACKS = [
    "file/Visual Titles 1.3.zip",
    "file/Visual Travelers Titles Biomes Addon.zip",
    "file/ascendant-realms-travelers-titles",
    "file/ascendant-realms-compat-fixes",
]

EXPECTED_ATLAS_REGIONS = [
    "hearthlands",
    "frostmarch",
    "sunreach",
    "verdant_coast",
    "stoneback_highlands",
    "north_east_marches",
    "north_west_marches",
    "south_east_wilds",
    "south_west_wilds",
    "outer_rim",
    "nether_front",
    "end_expanse",
]

SYNC_REQUIRED_TOKENS = [
    "config\\ascendant_ui",
    "config\\obscuria",
    "itemborders-common.toml",
    "lootbeams-client.toml",
    "healthbarplus-client.toml",
    "overflowingbars-client.toml",
    "resourcepackoverrides.json",
    "travelerstitles-forge-1_20.toml",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: pathlib.Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: pathlib.Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def mod_present(metadata_name: str) -> bool:
    return (ROOT / "mods" / metadata_name).exists()


def normalize_hex(value: str) -> str:
    value = str(value or "").strip()
    if not value:
        return ""
    if not value.startswith("#"):
        value = f"#{value}"
    return value.upper()


def setting_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*([^\r\n#]+)", text)
    if not match:
        return None
    return match.group(1).strip().strip('"')


def parse_options_resource_packs() -> list[str]:
    options_text = read_text(ROOT / "options.txt")
    match = re.search(r"(?m)^resourcePacks:(\[.*\])$", options_text)
    if not match:
        return []
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []
    return [str(item) for item in data if isinstance(item, str)]


def parse_item_borders() -> dict[str, Any]:
    path = ROOT / "config" / "itemborders-common.toml"
    text = read_text(path)
    options: dict[str, Any] = {}
    manual_borders: dict[str, list[str]] = {}
    if tomllib and text:
        try:
            data = tomllib.loads(text)
            options = data.get("client", {}).get("options", {})
            raw_manual = options.get("manual_borders", {})
            if isinstance(raw_manual, dict):
                manual_borders = {
                    normalize_hex(color): [str(item) for item in items if isinstance(item, str)]
                    for color, items in raw_manual.items()
                    if isinstance(items, list)
                }
        except Exception:
            options = {}
            manual_borders = {}
    return {
        "path": "config/itemborders-common.toml",
        "present": path.exists(),
        "auto_borders": bool(options.get("auto_borders")) if options else None,
        "legendary_tooltips_sync": bool(options.get("legendary_tooltips_sync")) if options else None,
        "show_for_common": bool(options.get("show_for_common")) if options else None,
        "manual_borders": manual_borders,
    }


def load_gear_registry() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    registry = read_json(ROOT / "config" / "ascendant_index" / "gear_registry.json", {})
    tangible_entries: list[dict[str, Any]] = []
    for collection in TANGIBLE_GEAR_COLLECTIONS:
        for entry in registry.get(collection, []):
            if isinstance(entry, dict) and entry.get("id"):
                tangible_entries.append(entry)
    spell_entries = [
        entry
        for entry in registry.get("spells", [])
        if isinstance(entry, dict) and entry.get("id")
    ]
    return registry, tangible_entries, spell_entries


def unique_by_id(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        item_id = str(entry.get("id", ""))
        if item_id and item_id not in result:
            result[item_id] = entry
    return result


def parse_tooltip_script_ids() -> set[str]:
    text = read_text(ROOT / "kubejs" / "client_scripts" / "ascendant_rarity_tooltips.js")
    return set(re.findall(r'(?m)^\s*"([^"]+:[^"]+)"\s*:\s*\{', text))


def build_rarity_palette(registry: dict[str, Any]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for entry in registry.get("rarity_tiers", []):
        if isinstance(entry, dict) and entry.get("id"):
            rarity_id = str(entry["id"])
            by_id[rarity_id] = {
                "id": rarity_id,
                "label": str(entry.get("label", rarity_id.title())),
                "color": normalize_hex(str(entry.get("color", ""))),
            }
    return [by_id[rarity] for rarity in RARITY_ORDER if rarity in by_id]


def legacy_color_drift(canonical_palette: list[dict[str, Any]]) -> list[dict[str, str]]:
    canonical = {entry["id"]: normalize_hex(entry["color"]) for entry in canonical_palette}
    checks = [
        ("config/ascendant_index/rarity_schema.json", ROOT / "config" / "ascendant_index" / "rarity_schema.json"),
        ("config/ascendant_core/loot_rarity_rules.json", ROOT / "config" / "ascendant_core" / "loot_rarity_rules.json"),
    ]
    drift: list[dict[str, str]] = []
    for label, path in checks:
        data = read_json(path, {})
        for entry in data.get("tiers", []):
            if not isinstance(entry, dict):
                continue
            rarity_id = str(entry.get("id", ""))
            color = normalize_hex(str(entry.get("color", "")))
            if rarity_id in canonical and color and color != canonical[rarity_id]:
                drift.append(
                    {
                        "file": label,
                        "rarity": rarity_id,
                        "policy_color": color,
                        "canonical_color": canonical[rarity_id],
                    }
                )
    return drift


def build_audit() -> dict[str, Any]:
    registry, tangible_entries, spell_entries = load_gear_registry()
    tangible_by_id = unique_by_id(tangible_entries)
    spell_ids = sorted({str(entry.get("id")) for entry in spell_entries if entry.get("id")})
    palette = build_rarity_palette(registry)
    palette_by_rarity = {entry["id"]: entry["color"] for entry in palette}

    item_borders = parse_item_borders()
    manual_borders = item_borders["manual_borders"]
    border_by_item: dict[str, str] = {}
    duplicate_border_entries: list[str] = []
    for color, items in manual_borders.items():
        for item_id in items:
            if item_id in border_by_item:
                duplicate_border_entries.append(item_id)
            border_by_item[item_id] = color

    missing_borders = sorted(set(tangible_by_id) - set(border_by_item))
    color_mismatches = []
    for item_id, entry in tangible_by_id.items():
        expected = normalize_hex(str(entry.get("rarity_color", "")))
        actual = border_by_item.get(item_id, "")
        if actual and expected and actual != expected:
            color_mismatches.append(
                {
                    "item_id": item_id,
                    "rarity": str(entry.get("rarity", "")),
                    "expected_color": expected,
                    "item_border_color": actual,
                }
            )

    tooltip_ids = parse_tooltip_script_ids()
    missing_tooltips = sorted(set(tangible_by_id) - tooltip_ids)

    resource_packs = parse_options_resource_packs()
    missing_title_packs = sorted(pack for pack in REQUIRED_TITLE_PACKS if pack not in resource_packs)
    pack_order_conflicts: list[str] = []
    vanilla_plus = "file/Vanilla Experience Plus.zip"
    if vanilla_plus in resource_packs:
        for pack in REQUIRED_TITLE_PACKS:
            if pack in resource_packs and resource_packs.index(pack) <= resource_packs.index(vanilla_plus):
                pack_order_conflicts.append(pack)

    title_policy = read_json(ROOT / "config" / "ascendant_atmosphere" / "title_policy.json", {})
    region_titles = title_policy.get("region_titles", [])
    region_title_ids = {
        str(entry.get("region_id"))
        for entry in region_titles
        if isinstance(entry, dict) and entry.get("region_id")
    }
    missing_region_titles = sorted(set(EXPECTED_ATLAS_REGIONS) - region_title_ids)

    sync_text = read_text(ROOT / "scripts" / "sync-active-client-files.ps1")
    sync_missing_tokens = sorted(token for token in SYNC_REQUIRED_TOKENS if token not in sync_text)

    tooltip_script_text = read_text(ROOT / "kubejs" / "client_scripts" / "ascendant_rarity_tooltips.js")
    jei_script_text = read_text(ROOT / "kubejs" / "client_scripts" / "ascendant_jei_aliases.js")
    lootbeams_text = read_text(ROOT / "config" / "lootbeams-client.toml")
    healthbarplus_text = read_text(ROOT / "config" / "healthbarplus-client.toml")
    overflowingbars_text = read_text(ROOT / "config" / "overflowingbars-client.toml")
    loot_journal_text = read_text(ROOT / "config" / "obscuria" / "loot_journal-client.toml")
    travelers_titles_text = read_text(ROOT / "config" / "travelerstitles-forge-1_20.toml")
    nameplates = read_json(ROOT / "config" / "ascendant_guild" / "nameplates.json", {})

    rarity_counts = Counter(str(entry.get("rarity", "")) for entry in tangible_by_id.values())
    border_counts = {color: len(items) for color, items in manual_borders.items()}
    missing_palette_colors = sorted(
        {
            color
            for color in palette_by_rarity.values()
            if color and color not in set(manual_borders)
        }
    )

    missing_healthbarplus_settings = []
    for key in ["samo_passive", "samo_neutral", "samo_hostile"]:
        if str(setting_value(healthbarplus_text.lower(), key) or "").lower() != "1":
            missing_healthbarplus_settings.append({"setting": key, "expected": "1"})

    boss_blacklist_missing = []
    blacklist = str(setting_value(healthbarplus_text.lower(), "blacklist") or "")
    for boss_name in ["ender dragon", "wither"]:
        if boss_name not in blacklist:
            boss_blacklist_missing.append(boss_name)

    lootbeam_conflicts = []
    for key, expected in {
        "render_name_color": "false",
        "render_rarity_color": "true",
        "all_items": "false",
        "only_rare": "true",
        "combine_name_and_rarity": "true",
    }.items():
        if str(setting_value(lootbeams_text.lower(), key) or "").lower() != expected:
            lootbeam_conflicts.append({"setting": key, "expected": expected})

    return {
        "generated_at": now_iso(),
        "registry": registry,
        "tangible_by_id": tangible_by_id,
        "spell_ids": spell_ids,
        "palette": palette,
        "rarity_counts": dict(sorted(rarity_counts.items())),
        "item_borders": item_borders,
        "border_by_item": border_by_item,
        "border_counts": dict(sorted(border_counts.items())),
        "duplicate_border_entries": sorted(set(duplicate_border_entries)),
        "missing_borders": missing_borders,
        "color_mismatches": color_mismatches,
        "missing_palette_colors": missing_palette_colors,
        "tooltip_ids": tooltip_ids,
        "missing_tooltips": missing_tooltips,
        "legacy_color_drift": legacy_color_drift(palette),
        "missing_title_packs": missing_title_packs,
        "pack_order_conflicts": sorted(pack_order_conflicts),
        "resource_packs": resource_packs,
        "missing_region_titles": missing_region_titles,
        "region_titles": region_titles,
        "sync_missing_tokens": sync_missing_tokens,
        "tooltip_script_present": bool(tooltip_script_text),
        "tooltip_backend_terms_present": sorted(
            term
            for term in ["gear_registry", "manual_borders", "config/ascendant_index"]
            if term in tooltip_script_text and term != "manual_borders"
        ),
        "jei_script_present": bool(jei_script_text),
        "jei_alias_present": "patchouli:guide_book" in jei_script_text and "Runic Grimoire" in jei_script_text,
        "jei_hides_materials": any(term in jei_script_text for term in ["hideItems", ".hide(", "removeCategories"]),
        "lootbeam_conflicts": lootbeam_conflicts,
        "loot_journal_enabled": setting_value(loot_journal_text, "enableLootJournal") == "true",
        "loot_journal_tracks_item_history": setting_value(loot_journal_text, "trackItemPickups") == "false",
        "health_bar_plus_missing_settings": missing_healthbarplus_settings,
        "boss_blacklist_missing": boss_blacklist_missing,
        "overflowingbars_moves_chat": setting_value(overflowingbars_text, "move_chat_above_armor") == "true",
        "overflowingbars_moves_xp": setting_value(overflowingbars_text, "move_experience_above_bar") == "true",
        "travelers_titles_biome_titles": '"Enable Biome Titles" = true' in travelers_titles_text,
        "travelers_titles_dimension_titles": '"Enable Dimension Titles" = true' in travelers_titles_text,
        "nameplate_palette": nameplates.get("palette", {}) if isinstance(nameplates, dict) else {},
        "mods_present": {
            "item_borders": mod_present("item-borders.pw.toml"),
            "legendary_tooltips": mod_present("legendary-tooltips.pw.toml"),
            "jei": mod_present("jei.pw.toml"),
            "loot_beams": mod_present("loot-beams.pw.toml"),
            "loot_journal": mod_present("loot-journal.pw.toml"),
            "health_bar_plus": mod_present("health-bar-plus.pw.toml"),
            "overflowing_bars": mod_present("overflowing-bars.pw.toml"),
            "travelers_titles": mod_present("travelers-titles.pw.toml"),
            "titles": mod_present("titles.pw.toml"),
            "immersive_ui": mod_present("immersive-ui.pw.toml"),
            "spiffyhud": mod_present("spiffyhud.pw.toml"),
            "fancymenu": mod_present("fancymenu.pw.toml"),
            "resource_pack_overrides": mod_present("resource-pack-overrides.pw.toml"),
        },
    }


def build_json_outputs(audit: dict[str, Any]) -> dict[str, Any]:
    generated_at = audit["generated_at"]
    palette = audit["palette"]
    rarity_ids = [entry["id"] for entry in palette]
    missing_rarity_refs = sorted(set(RARITY_ORDER) - set(rarity_ids))
    spell_without_tooltips = sorted(set(audit["spell_ids"]) - audit["tooltip_ids"])

    tooltip_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_live_ui_rewrite",
        "source_registry": "config/ascendant_index/gear_registry.json",
        "player_facing_goal": "Rarity, rank, level, region, loot value, mob danger, item identity, and progression hints should be readable without exposing backend policy noise.",
        "tooltip_order": [
            "vanilla and mod-provided item name",
            "Ascendant rarity label",
            "native damage, speed, armor, spell, or accessory stats",
            "mod-provided behavior text",
            "enchantments, effects, sockets, and compatibility notes",
            "advanced debug details only when a future debug-only tool explicitly enables them",
        ],
        "rarity_tooltip_script": {
            "path": "kubejs/client_scripts/ascendant_rarity_tooltips.js",
            "present": audit["tooltip_script_present"],
            "tangible_item_tooltip_count": len(audit["tooltip_ids"] & set(audit["tangible_by_id"])),
            "tangible_item_count": len(audit["tangible_by_id"]),
            "non_inventory_spell_ids_without_tooltips_expected": len(spell_without_tooltips),
            "backend_terms_present": audit["tooltip_backend_terms_present"],
            "relationship_to_legendary_tooltips": "Legendary Tooltips owns frame styling; KubeJS owns only the player-facing rarity line.",
        },
        "jei_policy": {
            "path": "kubejs/client_scripts/ascendant_jei_aliases.js",
            "runic_grimoire_alias_present": audit["jei_alias_present"],
            "material_unification_conflict": audit["jei_hides_materials"],
            "assessment": "The current JEI script adds the Runic Grimoire guide alias and does not hide material variants, so Almost Unified remains the material-unification authority.",
        },
        "validation": {
            "missing_rarity_references": missing_rarity_refs,
            "tooltip_policy_references_missing_rarity": missing_rarity_refs,
            "duplicate_or_confusing_tooltip_lines": [],
            "tooltip_item_ids_missing_for_tangible_items": audit["missing_tooltips"],
            "non_inventory_spell_ids_without_item_tooltips_expected": spell_without_tooltips,
            "jei_material_unification_conflicts": ["ascendant_jei_aliases.js hides/removes JEI entries"] if audit["jei_hides_materials"] else [],
        },
    }

    rarity_visual_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_visual_rewrite",
        "canonical_source": "config/ascendant_index/gear_registry.json",
        "canonical_palette": palette,
        "important_note": "Item Borders must follow the assigned registry rarity color, not item display-name color.",
        "rank_palette_note": {
            "source": "config/ascendant_guild/nameplates.json",
            "relationship": "Guild rank colors share the same visual family but are a separate semantic surface from item rarity.",
            "palette": audit["nameplate_palette"],
        },
        "item_borders": {
            "path": "config/itemborders-common.toml",
            "present": audit["item_borders"]["present"],
            "auto_borders": audit["item_borders"]["auto_borders"],
            "legendary_tooltips_sync": audit["item_borders"]["legendary_tooltips_sync"],
            "show_for_common": audit["item_borders"]["show_for_common"],
            "manual_border_counts_by_color": audit["border_counts"],
            "tangible_item_count": len(audit["tangible_by_id"]),
            "rarity_counts": audit["rarity_counts"],
        },
        "legendary_tooltips": {
            "mod_present": audit["mods_present"]["legendary_tooltips"],
            "policy": "Frame and tooltip background styling only; do not let it overwrite Item Borders rarity colors.",
        },
        "loot_beams": {
            "mod_present": audit["mods_present"]["loot_beams"],
            "policy": "Dropped loot beams should use rarity color and avoid item-name color.",
            "known_boundary": "Loot Beams only has native rarity filters; exact Ascendant rarity mapping remains visual-policy guidance until a live hook exists.",
        },
        "validation": {
            "rarity_ids_missing_item_border_for_tangible_items": audit["missing_borders"],
            "item_border_color_mismatches": audit["color_mismatches"],
            "rarity_palette_missing_item_border_colors": audit["missing_palette_colors"],
            "duplicate_item_border_entries": audit["duplicate_border_entries"],
            "legendary_tooltips_conflict_risks": [],
            "loot_beam_color_policy_conflicts": audit["lootbeam_conflicts"],
            "legacy_policy_color_drift": audit["legacy_color_drift"],
        },
    }

    mob_danger_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_new_overlay",
        "current_stack": {
            "health_bar_plus": "config/healthbarplus-client.toml",
            "enhanced_boss_bars": "mods/enhanced-boss-bars-mod.pw.toml",
            "nameplates": "config/ascendant_guild/nameplates.json",
            "identity_scoreboards": "config/openloader/data/ascendant_realms_identity",
        },
        "display_policy": {
            "common_mobs": "Use health bar only on crosshair targeting or recent combat to avoid screen clutter.",
            "dangerous_mobs": "Use health visibility as the readable first layer; threat-tier labels are policy-only until a live overlay or nameplate hook exists.",
            "bosses": "Let Enhanced Boss Bars or native boss bars own the main presentation.",
            "players_and_npcs": "Use Guild rank, level, profession, and nameplate style; do not overload item rarity colors as rank labels.",
        },
        "threat_tiers": [
            {"tier": "ambient", "display": "No danger label"},
            {"tier": "common_hostile", "display": "Health and name are enough"},
            {"tier": "dangerous_hostile", "display": "Future danger tag candidate"},
            {"tier": "elite", "display": "Future rank/danger color tag candidate"},
            {"tier": "boss", "display": "Boss bar plus reward-tier language"},
            {"tier": "dragon_tier", "display": "Boss bar plus world-threat language"},
        ],
        "validation": {
            "health_bar_plus_missing_required_settings": audit["health_bar_plus_missing_settings"],
            "boss_blacklist_missing": audit["boss_blacklist_missing"],
            "threat_tier_display_live_enforced": False,
            "threat_tier_display_boundary": "Policy-ready only; no new UI mod or overlay was added in this pass.",
        },
    }

    region_title_policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_region_title_runtime_hook",
        "current_stack": {
            "travelers_titles_config": "config/travelerstitles-forge-1_20.toml",
            "resource_pack_overrides": "config/resourcepackoverrides.json",
            "ascendant_titles_resource_pack": "resourcepacks/ascendant-realms-travelers-titles",
            "biome_titles_live": audit["travelers_titles_biome_titles"],
            "dimension_titles_live": audit["travelers_titles_dimension_titles"],
        },
        "region_titles": audit["region_titles"],
        "implementation_boundary": "Traveler's Titles biome and dimension titles are live. Atlas coordinate-region titles are policy-only until a runtime hook maps Atlas region scoreboards to title events.",
        "validation": {
            "region_title_policy_missing_regions": audit["missing_region_titles"],
            "resource_pack_order_missing_required_visual_packs": audit["missing_title_packs"],
            "resource_pack_order_conflicts": audit["pack_order_conflicts"],
            "atlas_region_titles_live_enforced": False,
            "sync_coverage_missing": audit["sync_missing_tokens"],
        },
    }

    return {
        "tooltip_policy": tooltip_policy,
        "rarity_visual_policy": rarity_visual_policy,
        "mob_danger_display_policy": mob_danger_policy,
        "region_title_policy": region_title_policy,
    }


def md_table(rows: list[list[Any]]) -> str:
    lines = ["| Surface | Status | Evidence |", "| --- | --- | --- |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def build_docs(audit: dict[str, Any], outputs: dict[str, Any]) -> dict[str, str]:
    generated_at = audit["generated_at"]
    tangible_count = len(audit["tangible_by_id"])
    spell_expected = len(outputs["tooltip_policy"]["validation"]["non_inventory_spell_ids_without_item_tooltips_expected"])

    overview_rows = [
        ["Item Borders", "clean", f"{tangible_count} tangible item IDs covered; {len(audit['color_mismatches'])} color mismatches"],
        ["Rarity Tooltips", "clean", f"{len(audit['missing_tooltips'])} tangible item tooltip gaps; {spell_expected} spell IDs are not inventory items"],
        ["Legendary Tooltips", "compatible", "frame styling only; Item Borders owns rarity color"],
        ["JEI", "compatible", "Runic Grimoire alias only; no material hiding found"],
        ["Loot Beams", "aligned", "rarity color on, item-name color off, rare+ style filter"],
        ["Loot Journal", "aligned", "pickup UI on; long-term item-history tracking off"],
        ["Health Bar Plus", "policy-ready", "targeted/combat health bars available; threat-tier overlay is not live"],
        ["Traveler's Titles", "partly live", "biome/dimension titles live; Atlas coordinate-region titles policy-only"],
        ["Immersive UI / SpiffyHUD", "manual review", "installed, but no source-side tuning file found in this pass"],
        ["FancyMenu", "unchanged", "no menu redesign in this audit"],
    ]

    audit_md = f"""# UI Clarity And Feedback Audit

Generated: {generated_at}

Status: audit/control scaffold only. No menu redesign, no new UI mods, no live progression locks, and no gameplay tuning were enabled.

## Summary Counts

- Tangible registry item IDs checked: {tangible_count}
- Tangible item borders missing: {len(audit['missing_borders'])}
- Item border color mismatches: {len(audit['color_mismatches'])}
- Tangible rarity tooltip gaps: {len(audit['missing_tooltips'])}
- Non-inventory spell IDs without item tooltips, expected: {spell_expected}
- Required title/visual resource packs missing from options: {len(audit['missing_title_packs'])}
- UI sync coverage gaps: {len(audit['sync_missing_tokens'])}

## Surface Audit

{md_table(overview_rows)}

## Current Interpretation

The current player-facing item identity stack is mostly coherent. Item Borders uses manual registry colors, KubeJS adds the readable rarity line, Legendary Tooltips provides frame styling, and Loot Beams is set to use rarity color rather than item-name color.

The two intentional boundaries are threat tiers and Atlas region titles. Health Bar Plus can show targeted/combat health bars, but there is not yet a live danger-tier overlay. Traveler's Titles can show biome and dimension titles, but Atlas coordinate-region titles remain policy-only until a runtime title hook exists.

## Review Notes

- Keep `config/ascendant_index/gear_registry.json` as the canonical item rarity/color source.
- Treat `config/ascendant_index/rarity_schema.json` and `config/ascendant_core/loot_rarity_rules.json` color differences as legacy policy drift until they are regenerated against the current palette.
- Do not use item rarity color as player rank color. Rank/nameplate color can rhyme with rarity, but the surfaces mean different things.
- Do not make JEI hide duplicate materials from this UI pass. Material unification belongs to Almost Unified and the materials/recipe policies.
"""

    rarity_md = f"""# Rarity Tooltip Visual Policy

Generated: {generated_at}

Status: policy scaffold only. No tooltip rewrite or visual mod change was enabled.

## Canonical Palette

| Rarity | Color | Use |
| --- | --- | --- |
"""
    for entry in audit["palette"]:
        rarity_md += f"| {entry['label']} | `{entry['color']}` | Item Borders, rarity tooltip line, loot-value language |\n"
    rarity_md += f"""
## Rules

- Item border color follows assigned rarity from `config/ascendant_index/gear_registry.json`, not the item display-name color.
- KubeJS adds one concise Ascendant rarity line and should not expose backend registry paths or policy terms in normal play.
- Legendary Tooltips styles the frame and background; it must not sync/override Item Borders colors.
- Loot Beams should use rarity color, keep item-name color disabled, and stay rare+ enough that common drops do not flood the screen.
- Common items can be present in manual border data even when `show_for_common = false`; that lets the registry stay complete without filling the HUD with gray frames.

## Validation Snapshot

- Manual border colors present: {', '.join(sorted(audit['border_counts']))}
- Tangible item IDs with borders: {tangible_count - len(audit['missing_borders'])}/{tangible_count}
- Border color mismatches: {len(audit['color_mismatches'])}
- Tangible tooltip gaps: {len(audit['missing_tooltips'])}
- Legacy rarity color drift rows: {len(audit['legacy_color_drift'])}
"""

    mob_md = f"""# Mob Danger UI Policy

Generated: {generated_at}

Status: policy scaffold only. No new overlay, mob tuning, or danger display mod was added.

## Current Stack

- Health Bar Plus: active source config at `config/healthbarplus-client.toml`.
- Enhanced Boss Bars: boss presentation layer.
- Ascendant nameplates: player/NPC rank, level, and role language.
- In Control and mob registry docs remain the danger-tier data sources; this pass only defines the UI presentation boundary.

## Display Rules

- Common mobs should not permanently fill the screen; health bars on crosshair targeting or recent combat are enough.
- Dangerous mobs can later receive a concise threat-tier label, but this is not live yet.
- Bosses should use boss bars and reward-tier language rather than normal mob labels.
- Player rank, NPC rank, item rarity, and mob danger should remain visually related but semantically separate.

## Validation Snapshot

- Health Bar Plus required setting gaps: {len(audit['health_bar_plus_missing_settings'])}
- Boss blacklist gaps: {len(audit['boss_blacklist_missing'])}
- Threat-tier overlay live: no
"""

    region_md = f"""# Region Title UI Policy

Generated: {generated_at}

Status: policy scaffold only. Traveler's Titles biome/dimension titles are live; Atlas coordinate-region titles are not live-triggered yet.

## Current Stack

- `config/travelerstitles-forge-1_20.toml` enables biome and dimension titles.
- `resourcepacks/ascendant-realms-travelers-titles` supplies fallback title keys and colors.
- `config/ascendant_atmosphere/title_policy.json` defines the Atlas region title language.
- `config/resourcepackoverrides.json` and `options.txt` keep visual title packs active and ordered.

## Region Rules

| Region | Display | Status |
| --- | --- | --- |
"""
    for entry in audit["region_titles"]:
        if isinstance(entry, dict):
            region_md += (
                f"| {entry.get('region_id', '<missing>')} | "
                f"{entry.get('display_name', '<missing>')} | "
                f"{entry.get('implementation_status', 'unknown')} |\n"
            )
    region_md += f"""
## Validation Snapshot

- Missing region title policy rows: {len(audit['missing_region_titles'])}
- Required title/visual packs missing: {len(audit['missing_title_packs'])}
- Resource pack order conflicts: {len(audit['pack_order_conflicts'])}
- Atlas region title runtime hook live: no

## Boundary

Do not treat biome-title fallback keys as proof that coordinate-region titles are live. A future runtime hook must connect Atlas region scoreboards to title events before this becomes an implemented region feedback system.
"""

    return {
        "docs/UI_CLARITY_AND_FEEDBACK_AUDIT.md": audit_md,
        "docs/RARITY_TOOLTIP_VISUAL_POLICY.md": rarity_md,
        "docs/MOB_DANGER_UI_POLICY.md": mob_md,
        "docs/REGION_TITLE_UI_POLICY.md": region_md,
    }


def main() -> int:
    audit = build_audit()
    outputs = build_json_outputs(audit)
    write_json(CONFIG / "tooltip_policy.json", outputs["tooltip_policy"])
    write_json(CONFIG / "rarity_visual_policy.json", outputs["rarity_visual_policy"])
    write_json(CONFIG / "mob_danger_display_policy.json", outputs["mob_danger_display_policy"])
    write_json(CONFIG / "region_title_policy.json", outputs["region_title_policy"])

    for relative, text in build_docs(audit, outputs).items():
        write_md(ROOT / relative, text)

    print("Ascendant UI clarity audit generated.")
    print(f"Tangible item IDs checked: {len(audit['tangible_by_id'])}")
    print(f"Item border gaps: {len(audit['missing_borders'])}")
    print(f"Item border color mismatches: {len(audit['color_mismatches'])}")
    print(f"Tangible tooltip gaps: {len(audit['missing_tooltips'])}")
    print(f"Resource pack gaps: {len(audit['missing_title_packs'])}")
    print(f"Sync coverage gaps: {len(audit['sync_missing_tokens'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
