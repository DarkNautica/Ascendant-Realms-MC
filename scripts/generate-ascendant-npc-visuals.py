#!/usr/bin/env python3
"""Generate Ascendant NPC visual identity policy and validation reports."""

from __future__ import annotations

import json
import os
import pathlib
import re
import zipfile
from collections import Counter
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
OUT_DIR = ROOT / "config" / "ascendant_guild"
ACTIVE_INSTANCE = pathlib.Path(
    os.environ.get(
        "ASCENDANT_ACTIVE_INSTANCE",
        r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)",
    )
)

MCA_MEDIEVAL_PACK_FILE = "MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip"
MCA_MEDIEVAL_PACK_KEY = f"file/{MCA_MEDIEVAL_PACK_FILE}"
MODERN_TONE_TERMS = [
    "hoodie",
    "jeans",
    "tshirt",
    "t_shirt",
    "sneaker",
    "suit",
    "tie",
    "business",
    "school",
    "uniform",
    "modern",
]

RIVAL_IDS = ["mira_ash", "darius_crowe", "seren_valehart", "kael_vorn", "black_hound"]
IMPORTANT_PROFESSION_IDS = [
    "guild_clerk",
    "rank_examiner",
    "bounty_master",
    "guild_arcanist",
    "hunter_quartermaster",
    "guard_captain",
    "tavern_keeper",
    "village_elder",
    "rival_hunter",
]

SILHOUETTE_OVERRIDES: dict[str, dict[str, Any]] = {
    "guild_clerk": {
        "display_name": "Guild Clerk",
        "role": "contracts, local registry, beginner guidance",
        "preferred_tool": "Easy NPC",
        "silhouette_read": "ledger cane, villager hat, simple robe, approachable Guild colors",
        "required_visual_cues": ["staff or cane", "civilian hat", "robe or clerk coat", "no combat-heavy armor"],
        "avoid_terms": ["hoodie", "jeans", "modern civilian"],
    },
    "rank_examiner": {
        "display_name": "Rank Examiner",
        "role": "formal public rank evaluation",
        "preferred_tool": "Easy NPC",
        "silhouette_read": "judgment blade, crown or formal headpiece, heroic armor",
        "required_visual_cues": ["authority headpiece", "formal weapon", "high-rank armor"],
        "avoid_terms": ["casual streetwear", "plain villager clothing"],
    },
    "bounty_master": {
        "display_name": "Bounty Master",
        "role": "contract board anchor and threat dispatcher",
        "preferred_tool": "Easy NPC",
        "silhouette_read": "crossbow, heavy field armor, practical hunter stance",
        "required_visual_cues": ["crossbow or sidearm", "field armor", "contract-board presence"],
        "avoid_terms": ["office modern", "unarmed merchant only"],
    },
    "guild_arcanist": {
        "display_name": "Guild Arcanist",
        "role": "spell research, corruption warnings, magic contracts",
        "preferred_tool": "Easy NPC",
        "silhouette_read": "staff, visible spellbook, academy mage coat",
        "required_visual_cues": ["staff", "spellbook", "mage robe or coat"],
        "avoid_terms": ["mundane villager only", "modern lab coat"],
    },
    "hunter_quartermaster": {
        "display_name": "Quartermaster",
        "role": "supplies, exchange, rank vendor prototype",
        "preferred_tool": "Easy NPC",
        "silhouette_read": "utility armor, practical weapon, workshop gear",
        "required_visual_cues": ["supply-side weapon", "workshop or utility armor", "no luxury noble look"],
        "avoid_terms": ["modern shopkeeper", "plain robe only"],
    },
    "guard_captain": {
        "display_name": "Guard Captain",
        "role": "settlement defense and road danger warnings",
        "preferred_tool": "CustomNPCs or Guard Villagers where combat is required",
        "silhouette_read": "longsword, shield, warrior armor, clear captain profile",
        "required_visual_cues": ["sword", "shield", "warrior armor", "settlement-defense colors"],
        "avoid_terms": ["civilian clothing", "unarmed guard captain"],
    },
    "tavern_keeper": {
        "display_name": "Tavern Keeper",
        "role": "rumors, local hospitality, soft quest hints",
        "preferred_tool": "Easy NPC",
        "silhouette_read": "warm tavern clothing, rumor prop, visible noncombat role",
        "required_visual_cues": ["tavern prop", "simple robe or apron-like clothing", "noncombat posture"],
        "avoid_terms": ["modern bartender", "full boss armor"],
    },
    "village_elder": {
        "display_name": "Village Elder",
        "role": "village memory, local stakes, settlement identity",
        "preferred_tool": "Easy NPC",
        "silhouette_read": "cane, villager hat, elder robe, low-threat posture",
        "required_visual_cues": ["cane or staff", "simple headwear", "elder robe"],
        "avoid_terms": ["modern civilian", "heavy elite armor"],
    },
    "wounded_hunter": {
        "display_name": "Wounded Hunter",
        "role": "field warning and danger foreshadowing",
        "preferred_tool": "CustomNPCs for encounter prototypes",
        "silhouette_read": "bow, damaged-looking hunter armor, field survival read",
        "required_visual_cues": ["bow", "hunter armor", "injured or exhausted posture"],
        "avoid_terms": ["clean noble robe", "modern explorer"],
    },
    "rival_hunter": {
        "display_name": "Rival Hunter",
        "role": "named hunters who communicate rank, class, and threat at a glance",
        "preferred_tool": "CustomNPCs-Unofficial for combat-capable prototypes; Easy NPC for social versions",
        "silhouette_read": "class-specific gear, visible rank palette, distinct weapon profile",
        "required_visual_cues": ["rank-coded nameplate", "class-readable weapon", "curated armor tier"],
        "avoid_terms": ["random gear soup", "modern civilian skin", "anonymous villager profile"],
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: pathlib.Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def rank_label(rank_id: str) -> str:
    if rank_id == "unranked":
        return "Unranked"
    if rank_id.endswith("_rank"):
        return f"{rank_id[0].upper()}-Rank"
    return rank_id


def rank_id(value: str) -> str:
    clean = value.strip().lower().replace("-", "_").replace(" ", "_")
    if clean in {"unranked", "guild_staff"}:
        return clean
    if clean.endswith("_rank"):
        return clean
    if len(clean) == 1:
        return f"{clean}_rank"
    return clean


def load_gear_items(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    for value in registry.values():
        if not isinstance(value, list):
            continue
        for entry in value:
            if isinstance(entry, dict) and entry.get("id"):
                items[str(entry["id"])] = entry
    return items


def equipment_list(profile: dict[str, Any]) -> list[dict[str, Any]]:
    equipment = profile.get("equipment", {})
    if not isinstance(equipment, dict):
        return []
    rows: list[dict[str, Any]] = []
    for slot, data in equipment.items():
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            if isinstance(entry, dict):
                item_id = str(entry.get("item", ""))
                rows.append(
                    {
                        "slot": slot,
                        "item_id": item_id,
                        "name": entry.get("name", item_id),
                        "rarity": entry.get("rarity"),
                        "player_obtainable": bool(entry.get("player_obtainable", True)),
                        "slot_note": entry.get("slot_note", ""),
                    }
                )
    return rows


def flatten_loadout_profiles(loadouts: dict[str, Any]) -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    for group in ("archetypes", "npc_profiles"):
        for profile_id, profile in (loadouts.get(group, {}) or {}).items():
            if isinstance(profile, dict):
                profiles[str(profile_id)] = profile
    return profiles


def parse_resource_packs() -> list[str]:
    options_path = ROOT / "options.txt"
    if not options_path.exists():
        return []
    match = re.search(r"(?m)^resourcePacks:(\[.*\])$", options_path.read_text(encoding="utf-8", errors="replace"))
    if not match:
        return []
    try:
        packs = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []
    return [str(pack) for pack in packs if isinstance(pack, str)]


def mod_presence() -> dict[str, dict[str, Any]]:
    mods = {
        "mca_reborn": "mods/minecraft-comes-alive-reborn.pw.toml",
        "mca_default_medieval_resource_pack": "resourcepacks/mca-default-medieval-by-de4th4sh.pw.toml",
        "easy_npc_bundle": "mods/easy-npc.pw.toml",
        "easy_npc_core": "mods/easy-npc-core.pw.toml",
        "easy_npc_config_ui": "mods/easy-npc-config-ui.pw.toml",
        "customnpcs_unofficial": "mods/customnpcs-unofficial.pw.toml",
        "human_companions": "mods/human-companions.pw.toml",
        "guard_villagers": "mods/guard-villagers.pw.toml",
        "villager_names": "mods/villager-names-serilum.pw.toml",
    }
    return {
        key: {
            "path": rel(ROOT / path),
            "present": (ROOT / path).exists(),
        }
        for key, path in mods.items()
    }


def rel(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def inspect_mca_medieval_pack(resource_packs: list[str]) -> dict[str, Any]:
    configured = (ROOT / "resourcepacks" / "mca-default-medieval-by-de4th4sh.pw.toml").exists()
    active_in_options = MCA_MEDIEVAL_PACK_KEY in resource_packs
    zip_candidates = [
        ACTIVE_INSTANCE / "resourcepacks" / MCA_MEDIEVAL_PACK_FILE,
        ROOT / "resourcepacks" / MCA_MEDIEVAL_PACK_FILE,
    ]
    zip_paths = [path for path in zip_candidates if path.exists()]

    audit: dict[str, Any] = {
        "metadata_present": configured,
        "configured_pack_key": MCA_MEDIEVAL_PACK_KEY,
        "active_in_options": active_in_options,
        "active_instance_path": str(ACTIVE_INSTANCE),
        "zip_paths_found": [str(path) for path in zip_paths],
        "zip_inspected": False,
        "total_zip_entries": 0,
        "png_asset_count": 0,
        "clothing_asset_count": 0,
        "skin_asset_count": 0,
        "profession_asset_counts": {},
        "tone_review_flags": [],
        "sample_assets": [],
    }
    if not zip_paths:
        audit["tone_review_flags"] = ["MCA medieval resource pack zip was not found in source or active instance."]
        return audit

    zip_path = zip_paths[0]
    profession_counts: Counter[str] = Counter()
    tone_flags: list[str] = []
    sample_assets: list[str] = []
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        png_assets = [name for name in names if name.lower().endswith(".png")]
        clothing_assets = [name for name in png_assets if "/skins/clothing/" in name.lower()]
        skin_assets = [name for name in png_assets if "/skins/" in name.lower()]
        for asset in clothing_assets:
            parts = asset.split("/")
            # Expected: assets/mca/skins/clothing/<state>/<gender>/<profession>/<variant>.png
            if len(parts) >= 8 and parts[0] == "assets" and parts[2] == "skins":
                profession_counts[parts[6]] += 1
            lowered = asset.lower()
            if any(term in lowered for term in MODERN_TONE_TERMS):
                tone_flags.append(asset)
            if len(sample_assets) < 16:
                sample_assets.append(asset)
        audit.update(
            {
                "zip_inspected": True,
                "inspected_zip_path": str(zip_path),
                "total_zip_entries": len(names),
                "png_asset_count": len(png_assets),
                "clothing_asset_count": len(clothing_assets),
                "skin_asset_count": len(skin_assets),
                "profession_asset_counts": dict(sorted(profession_counts.items())),
                "tone_review_flags": tone_flags[:50],
                "sample_assets": sample_assets,
            }
        )
    return audit


def bridge_skin_audit(generated_profiles: dict[str, Any]) -> dict[str, Any]:
    profiles = generated_profiles.get("profiles", []) if isinstance(generated_profiles, dict) else []
    expected_ids = {
        str(profile.get("id"))
        for profile in profiles
        if isinstance(profile, dict) and profile.get("skin_texture")
    }
    pack_dir = ROOT / "resourcepacks/ascendant-realms-compat-fixes/assets/customnpcs/textures/entity/ascendant_mca"
    native_dir = ROOT / "customnpcs/assets/customnpcs/textures/entity/ascendant_mca"
    missing: list[str] = []
    for profile_id in sorted(expected_ids):
        for path in (pack_dir / f"{profile_id}.png", native_dir / f"{profile_id}.png"):
            if not path.exists():
                missing.append(rel(path))
    return {
        "expected_profile_skin_count": len(expected_ids),
        "resource_pack_skin_count": len(list(pack_dir.glob("*.png"))) if pack_dir.exists() else 0,
        "customnpcs_native_skin_count": len(list(native_dir.glob("*.png"))) if native_dir.exists() else 0,
        "expected_profile_ids": sorted(expected_ids),
        "missing_bridge_skin_files": missing,
        "resource_pack_dir": rel(pack_dir),
        "customnpcs_native_dir": rel(native_dir),
    }


def collect_loadout_gear_misses(loadout_profiles: dict[str, dict[str, Any]], gear_items: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    misses: list[dict[str, str]] = []
    for profile_id, profile in loadout_profiles.items():
        for equipment in equipment_list(profile):
            item_id = equipment["item_id"]
            if item_id and item_id not in gear_items:
                misses.append({"profile_id": profile_id, "slot": equipment["slot"], "item_id": item_id})
    return misses


def build_silhouettes(
    loadout_profiles: dict[str, dict[str, Any]],
    nameplate_profiles: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    silhouettes: list[dict[str, Any]] = []
    for profession_id in IMPORTANT_PROFESSION_IDS + ["wounded_hunter"]:
        override = dict(SILHOUETTE_OVERRIDES[profession_id])
        profile = loadout_profiles.get(profession_id, {})
        nameplate = nameplate_profiles.get(profession_id, {})
        equipment = equipment_list(profile)
        gear_ids = [entry["item_id"] for entry in equipment if entry.get("item_id")]
        silhouettes.append(
            {
                "profession_id": profession_id,
                "display_name": override["display_name"],
                "role": override["role"],
                "preferred_tool": override["preferred_tool"],
                "silhouette_read": override["silhouette_read"],
                "required_visual_cues": override["required_visual_cues"],
                "avoid_terms": override["avoid_terms"],
                "loadout_profile_id": profession_id if profession_id in loadout_profiles else None,
                "nameplate_profile_id": profession_id if profession_id in nameplate_profiles else None,
                "rank": profile.get("rank") or nameplate.get("rank") or "varies_by_roster",
                "equipment": equipment,
                "gear_item_ids": gear_ids,
                "uses_visual_only_skin": profession_id != "rival_hunter",
                "visual_only_skin_equivalent_item_note": (
                    "Bridge skin is visual identity only; visible gear IDs above are player-obtainable or intentionally curated."
                    if profession_id != "rival_hunter"
                    else "Generic role only. Individual rival entries provide concrete loadout gear and nameplate style."
                ),
                "applies_to_rival_roster_ids": RIVAL_IDS if profession_id == "rival_hunter" else [],
            }
        )
    return silhouettes


def build_rival_roster(
    rivals_json: dict[str, Any],
    loadout_profiles: dict[str, dict[str, Any]],
    nameplate_profiles: dict[str, dict[str, Any]],
    rank_rules: dict[str, Any],
) -> list[dict[str, Any]]:
    source_rivals = {
        str(entry.get("id")): entry
        for entry in rivals_json.get("rivals", [])
        if isinstance(entry, dict) and entry.get("id")
    }
    roster: list[dict[str, Any]] = []
    for rival_id in RIVAL_IDS:
        source = source_rivals.get(rival_id, {})
        loadout = loadout_profiles.get(rival_id, {})
        nameplate = nameplate_profiles.get(rival_id, {})
        rank = str(loadout.get("rank") or nameplate.get("rank") or rank_id(str(source.get("rank", ""))))
        rank_rule = rank_rules.get(rank, {}) if isinstance(rank_rules, dict) else {}
        equipment = equipment_list(loadout)
        roster.append(
            {
                "rival_id": rival_id,
                "name": source.get("name") or nameplate.get("display") or rival_id.replace("_", " ").title(),
                "rank": rank,
                "rank_label": rank_label(rank),
                "class": source.get("class") or nameplate.get("profession"),
                "style": source.get("combat_style") or source.get("class") or nameplate.get("style"),
                "gear_tier": rank_rule.get("max_default_rarity", "manual_review"),
                "allowed_rarities": rank_rule.get("allowed_rarities", []),
                "preferred_regions": source.get("preferred_regions", []),
                "initial_status": source.get("initial_status", "manual_review"),
                "loadout_profile_id": rival_id if rival_id in loadout_profiles else None,
                "nameplate_profile_id": rival_id if rival_id in nameplate_profiles else None,
                "drop_policy": loadout.get("drop_policy", ""),
                "nameplate": nameplate,
                "equipment": equipment,
                "gear_item_ids": [entry["item_id"] for entry in equipment if entry.get("item_id")],
                "visual_language": {
                    "silhouette": SILHOUETTE_OVERRIDES["rival_hunter"]["silhouette_read"],
                    "class_read": source.get("combat_style", ""),
                    "rank_read": f"{rank_label(rank)} palette through nameplates.json",
                },
                "uses_visual_only_skin": bool(loadout),
                "visual_only_skin_equivalent_item_note": (
                    "Rival skin is visual identity only; visible equipment comes from gear_registry-backed item IDs."
                ),
                "drop_policy_note": "Named rivals should use quest rewards, trophies, fragments, or scripted rewards instead of farming full gear.",
            }
        )
    return roster


def validation_summary(
    mca_audit: dict[str, Any],
    bridge_audit: dict[str, Any],
    silhouettes: list[dict[str, Any]],
    rivals: list[dict[str, Any]],
    loadout_gear_misses: list[dict[str, str]],
    loadout_profiles: dict[str, dict[str, Any]],
    nameplate_profiles: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    silhouette_ids = {entry.get("profession_id") for entry in silhouettes}
    missing_silhouettes = sorted(set(IMPORTANT_PROFESSION_IDS) - {str(value) for value in silhouette_ids})
    missing_rival_contracts: list[str] = []
    for rival in rivals:
        if not rival.get("nameplate_profile_id") or not rival.get("loadout_profile_id") or not rival.get("drop_policy"):
            missing_rival_contracts.append(str(rival.get("rival_id")))
    missing_loadout_profiles = sorted(
        profile_id for profile_id in IMPORTANT_PROFESSION_IDS if profile_id != "rival_hunter" and profile_id not in loadout_profiles
    )
    missing_nameplate_profiles = sorted(
        profile_id for profile_id in IMPORTANT_PROFESSION_IDS if profile_id != "rival_hunter" and profile_id not in nameplate_profiles
    )
    visual_note_missing = sorted(
        str(entry.get("profession_id") or entry.get("rival_id"))
        for entry in silhouettes + rivals
        if entry.get("uses_visual_only_skin") and not str(entry.get("visual_only_skin_equivalent_item_note", "")).strip()
    )
    missing_mca = []
    if not mca_audit.get("metadata_present"):
        missing_mca.append("resourcepacks/mca-default-medieval-by-de4th4sh.pw.toml")
    if not mca_audit.get("active_in_options"):
        missing_mca.append(MCA_MEDIEVAL_PACK_KEY)
    if not mca_audit.get("zip_inspected"):
        missing_mca.append("active MCA medieval resource pack zip")
    return {
        "mca_medieval_pack_missing_or_inactive": missing_mca,
        "mca_medieval_pack_active": bool(mca_audit.get("metadata_present") and mca_audit.get("active_in_options")),
        "mca_medieval_clothing_asset_count": int(mca_audit.get("clothing_asset_count") or 0),
        "important_professions_missing_silhouette": missing_silhouettes,
        "important_professions_missing_loadout_profile": missing_loadout_profiles,
        "important_professions_missing_nameplate_profile": missing_nameplate_profiles,
        "rival_missing_nameplate_loadout_or_drop_policy": missing_rival_contracts,
        "loadout_missing_gear_item_ids": loadout_gear_misses,
        "visual_only_skin_without_equivalent_item_note": visual_note_missing,
        "modern_or_unknown_skin_review_flags": mca_audit.get("tone_review_flags", []),
        "generated_bridge_skins_missing": bridge_audit.get("missing_bridge_skin_files", []),
        "important_profession_count": len(IMPORTANT_PROFESSION_IDS),
        "rival_count": len(rivals),
    }


def build_markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


def format_equipment(items: list[dict[str, Any]]) -> str:
    if not items:
        return "None recorded"
    return ", ".join(f"{item['slot']}: `{item['item_id']}`" for item in items)


def write_docs(
    generated_at: str,
    policy: dict[str, Any],
    silhouettes_doc: dict[str, Any],
    roster_doc: dict[str, Any],
) -> None:
    validation = policy["validation"]
    mca = policy["mca_medieval_skin_audit"]
    mods = policy["mod_audit"]
    bridge = policy["customnpcs_bridge_skin_audit"]
    silhouette_rows = [
        [
            entry["display_name"],
            entry["preferred_tool"],
            entry["rank"],
            entry["silhouette_read"],
            format_equipment(entry.get("equipment", [])),
        ]
        for entry in silhouettes_doc["silhouettes"]
    ]
    rival_rows = [
        [
            entry["name"],
            entry["rank_label"],
            entry["class"],
            entry["gear_tier"],
            entry["drop_policy"] or "missing",
            format_equipment(entry.get("equipment", [])),
        ]
        for entry in roster_doc["rivals"]
    ]
    mod_rows = [
        [key, "present" if value["present"] else "missing", value["path"]]
        for key, value in sorted(mods.items())
    ]
    top_professions = Counter(mca.get("profession_asset_counts", {})).most_common(16)

    write_md(
        DOCS_DIR / "NPC_VISUAL_VALIDATION_REPORT.md",
        f"""# NPC Visual Validation Report

Generated: {generated_at}

Status: audit/control scaffold only. This pass did not place NPCs, inject villages, add NPC mods, or enable new world NPC population behavior.

## Summary

- MCA Reborn installed: {mods["mca_reborn"]["present"]}.
- MCA Default Medieval metadata present: {mca["metadata_present"]}.
- MCA Default Medieval active in `options.txt`: {mca["active_in_options"]}.
- MCA medieval clothing PNGs counted: {mca["clothing_asset_count"]}.
- CustomNPC bridged MCA-style skins: {bridge["resource_pack_skin_count"]} in the compatibility resource pack and {bridge["customnpcs_native_skin_count"]} in the CustomNPCs native folder.
- Requested important profession silhouettes covered: {validation["important_profession_count"] - len(validation["important_professions_missing_silhouette"])}/{validation["important_profession_count"]}.
- Rival hunters with loadout, nameplate, and drop policy: {validation["rival_count"] - len(validation["rival_missing_nameplate_loadout_or_drop_policy"])}/{validation["rival_count"]}.
- Loadout item IDs missing from `gear_registry.json`: {len(validation["loadout_missing_gear_item_ids"])}.
- Visual-only skins without an equivalent gear note: {len(validation["visual_only_skin_without_equivalent_item_note"])}.
- Modern/unknown MCA skin filename flags: {len(validation["modern_or_unknown_skin_review_flags"])}.

## Mod And Tool Audit

{build_markdown_table(["Layer", "Status", "Evidence"], mod_rows)}

## Important Profession Silhouettes

{build_markdown_table(["Profession", "Tool", "Rank", "Silhouette", "Visible Gear"], silhouette_rows)}

## Rival Hunter Visual Contract

{build_markdown_table(["Rival", "Rank", "Class", "Gear Tier", "Drop Policy", "Visible Gear"], rival_rows)}

## Validation Notes

- MCA medieval pack status: {"clean" if not validation["mca_medieval_pack_missing_or_inactive"] else ", ".join(validation["mca_medieval_pack_missing_or_inactive"])}.
- Missing important silhouettes: {", ".join(validation["important_professions_missing_silhouette"]) or "none"}.
- Missing rival contracts: {", ".join(validation["rival_missing_nameplate_loadout_or_drop_policy"]) or "none"}.
- Missing bridged skins: {", ".join(validation["generated_bridge_skins_missing"]) or "none"}.
- Unknown or modern-looking MCA asset names: {", ".join(validation["modern_or_unknown_skin_review_flags"][:10]) or "none found by filename scan"}.

## Boundary

Easy NPC remains the preferred tool for social NPCs. CustomNPCs remains the preferred tool for combat-capable rival prototypes and current generated test profiles. Human Companions is still generic hunter/companion review material, not the authored rival roster. Guard Villagers and Villager Names support village identity but are not used here to create new placed NPC content.
""",
    )

    top_profession_rows = [[name, count] for name, count in top_professions]
    write_md(
        DOCS_DIR / "MCA_MEDIEVAL_SKIN_AUDIT.md",
        f"""# MCA Medieval Skin Audit

Generated: {generated_at}

Status: active resource-pack validation and filename-level tone review. This does not prove every in-game MCA villager looks perfect; it proves the medieval clothing pack is present, enabled, and inspectable from the active client instance.

## Evidence

- Pack metadata: `resourcepacks/mca-default-medieval-by-de4th4sh.pw.toml`.
- Expected active pack key: `{MCA_MEDIEVAL_PACK_KEY}`.
- Active in `options.txt`: {mca["active_in_options"]}.
- Active instance checked: `{mca["active_instance_path"]}`.
- Zip inspected: {mca["zip_inspected"]}.
- Zip paths found: {", ".join(f"`{path}`" for path in mca["zip_paths_found"]) or "none"}.
- Total zip entries: {mca["total_zip_entries"]}.
- PNG assets: {mca["png_asset_count"]}.
- MCA skin assets: {mca["skin_asset_count"]}.
- MCA clothing assets: {mca["clothing_asset_count"]}.

## Clothing Asset Breakdown

{build_markdown_table(["Profession Folder", "PNG Count"], top_profession_rows)}

## Tone Review

Filename scan flags for modern/tone-breaking terms: {len(mca["tone_review_flags"])}.

{chr(10).join(f"- `{flag}`" for flag in mca["tone_review_flags"][:50]) if mca["tone_review_flags"] else "- No hoodie/jeans/t-shirt/sneaker/modern/business filename terms were found in the inspected MCA clothing assets."}

## Sample Assets

{chr(10).join(f"- `{asset}`" for asset in mca["sample_assets"]) or "- No sample assets available."}

## Manual Visual Test Still Needed

Create or load a safe MCA village test after terrain acceptance and visually inspect villager clothing. Keep MCA Reborn plus MCA Default Medieval only if normal play stays medieval/fantasy-safe and server behavior is clean.
""",
    )

    write_md(
        DOCS_DIR / "RIVAL_HUNTER_VISUAL_ROSTER.md",
        f"""# Rival Hunter Visual Roster

Generated: {generated_at}

Status: visual identity roster only. No rival placement, village injection, Hunter Board placement, or new NPC behavior was enabled.

## Roster

{build_markdown_table(["Rival", "Rank", "Class", "Style", "Gear Tier", "Nameplate", "Loadout", "Drop Policy"], [
    [
        entry["name"],
        entry["rank_label"],
        entry["class"],
        entry["style"],
        entry["gear_tier"],
        entry["nameplate_profile_id"] or "missing",
        entry["loadout_profile_id"] or "missing",
        entry["drop_policy"] or "missing",
    ]
    for entry in roster_doc["rivals"]
])}

## Equipment Reads

{chr(10).join(f"- **{entry['name']}**: {format_equipment(entry.get('equipment', []))}" for entry in roster_doc["rivals"])}

## Rules

- Rival hunters must communicate rank through `config/ascendant_guild/nameplates.json`.
- Rival hunters must communicate class through visible gear from `config/ascendant_index/gear_registry.json`.
- Named rivals should not drop full gear by default; use quest rewards, fragments, trophies, or scripted post-fight rewards.
- The Black Hound can remain rumor-first, but still needs a rank, nameplate profile, loadout profile, and drop policy so future implementation does not improvise.
""",
    )


def main() -> int:
    generated_at = now_iso()
    loadouts = read_json(OUT_DIR / "npc_loadouts.json", {})
    nameplates = read_json(OUT_DIR / "nameplates.json", {})
    rivals_json = read_json(OUT_DIR / "rival_hunters.json", {})
    generated_profiles = read_json(OUT_DIR / "generated_npc_profiles.json", {})
    gear_registry = read_json(ROOT / "config/ascendant_index/gear_registry.json", {})

    gear_items = load_gear_items(gear_registry if isinstance(gear_registry, dict) else {})
    loadout_profiles = flatten_loadout_profiles(loadouts if isinstance(loadouts, dict) else {})
    nameplate_profiles = nameplates.get("profiles", {}) if isinstance(nameplates, dict) else {}
    if not isinstance(nameplate_profiles, dict):
        nameplate_profiles = {}
    rank_rules = loadouts.get("rank_rules", {}) if isinstance(loadouts, dict) else {}

    resource_packs = parse_resource_packs()
    mca_audit = inspect_mca_medieval_pack(resource_packs)
    bridge_audit = bridge_skin_audit(generated_profiles if isinstance(generated_profiles, dict) else {})
    silhouettes = build_silhouettes(loadout_profiles, nameplate_profiles)
    roster = build_rival_roster(rivals_json if isinstance(rivals_json, dict) else {}, loadout_profiles, nameplate_profiles, rank_rules)
    loadout_gear_misses = collect_loadout_gear_misses(loadout_profiles, gear_items)
    validation = validation_summary(
        mca_audit,
        bridge_audit,
        silhouettes,
        roster,
        loadout_gear_misses,
        loadout_profiles,
        nameplate_profiles,
    )

    policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_control_scaffold_only_no_npc_placement",
        "scope": {
            "places_npcs": False,
            "injects_villages": False,
            "adds_npc_mods": False,
            "changes_spawn_rules": False,
            "changes_structure_generation": False,
        },
        "rules": [
            "No hoodies, jeans, modern civilian skins, or tone-breaking NPCs.",
            "Important NPC professions must have distinct medieval/fantasy silhouettes.",
            "Named rivals must carry rank, class, nameplate, curated loadout, gear tier, and drop policy.",
            "Visible NPC gear should use player-findable gear IDs unless an item is intentionally custom and documented.",
            "Visual-only skins need an equivalent gear or clothing note so skins do not hide progression logic.",
        ],
        "tool_policy": {
            "mca_reborn": "Village population and family layer; depends on MCA Default Medieval staying active and visually safe.",
            "easy_npc": "Preferred for Guild Clerk, Rank Examiner, Bounty Master, Arcanist, Quartermaster, Tavern Keeper, and Village Elder.",
            "customnpcs_unofficial": "Preferred for combat-capable rival prototypes and generated test profiles.",
            "human_companions": "Generic hunter/companion review layer only until visuals are manually accepted.",
            "guard_villagers": "Village defense support; not an authored Guild NPC placement system.",
            "villager_names": "Village identity support; does not replace authored nameplate policy.",
        },
        "mod_audit": mod_presence(),
        "mca_medieval_skin_audit": mca_audit,
        "customnpcs_bridge_skin_audit": bridge_audit,
        "source_files": {
            "loadouts": "config/ascendant_guild/npc_loadouts.json",
            "nameplates": "config/ascendant_guild/nameplates.json",
            "rival_hunters": "config/ascendant_guild/rival_hunters.json",
            "generated_profiles": "config/ascendant_guild/generated_npc_profiles.json",
            "gear_registry": "config/ascendant_index/gear_registry.json",
        },
        "validation": validation,
    }

    silhouettes_doc = {
        "version": 1,
        "generated_at": generated_at,
        "status": "visual_identity_policy_only_no_world_placement",
        "important_profession_ids": IMPORTANT_PROFESSION_IDS,
        "silhouettes": silhouettes,
        "validation": {
            "important_professions_missing_silhouette": validation["important_professions_missing_silhouette"],
            "important_professions_missing_loadout_profile": validation["important_professions_missing_loadout_profile"],
            "important_professions_missing_nameplate_profile": validation["important_professions_missing_nameplate_profile"],
            "visual_only_skin_without_equivalent_item_note": validation["visual_only_skin_without_equivalent_item_note"],
        },
    }

    roster_doc = {
        "version": 1,
        "generated_at": generated_at,
        "status": "visual_roster_only_no_spawn_or_village_injection",
        "rivals": roster,
        "validation": {
            "rival_missing_nameplate_loadout_or_drop_policy": validation["rival_missing_nameplate_loadout_or_drop_policy"],
            "loadout_missing_gear_item_ids": validation["loadout_missing_gear_item_ids"],
            "visual_only_skin_without_equivalent_item_note": [
                rival["rival_id"]
                for rival in roster
                if rival.get("uses_visual_only_skin") and not rival.get("visual_only_skin_equivalent_item_note")
            ],
        },
    }

    write_json(OUT_DIR / "npc_visual_policy.json", policy)
    write_json(OUT_DIR / "npc_profession_silhouettes.json", silhouettes_doc)
    write_json(OUT_DIR / "rival_hunter_roster.json", roster_doc)
    write_docs(generated_at, policy, silhouettes_doc, roster_doc)

    print("Generated Ascendant NPC visual identity scaffold")
    print(f"- MCA medieval clothing assets: {mca_audit.get('clothing_asset_count', 0)}")
    print(f"- important silhouettes: {len(silhouettes)}")
    print(f"- rival hunters: {len(roster)}")
    print(f"- missing loadout gear refs: {len(loadout_gear_misses)}")
    print(f"- modern/unknown filename flags: {len(mca_audit.get('tone_review_flags', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
