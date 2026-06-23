#!/usr/bin/env python3
"""Generate the Ascendant player progression bridge scaffold."""

from __future__ import annotations

import json
import pathlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "config/ascendant_progression"
DOCS_DIR = ROOT / "docs"

REQUIRED_RANKS = ["unranked", "e_rank", "d_rank", "c_rank", "b_rank", "a_rank", "s_rank"]
RANK_LABELS = {
    "unranked": "Unranked",
    "e_rank": "E-Rank",
    "d_rank": "D-Rank",
    "c_rank": "C-Rank",
    "b_rank": "B-Rank",
    "a_rank": "A-Rank",
    "s_rank": "S-Rank",
}

RANK_GUIDANCE = {
    "unranked": {
        "identity": "A capable survivor, not yet publicly trusted by the Guild.",
        "criteria": [
            "Learn the Ascendant Web and survive local travel.",
            "Complete tutorial, local errand, or first-village work.",
            "Avoid receiving rare-or-better progression gear as routine rewards.",
        ],
        "skill_points": [0, 3],
        "skill_thresholds": [0],
        "threat_range": [0, 1],
        "regions": ["crownlands"],
        "rings": ["center"],
        "gear_rarities": ["common", "uncommon"],
        "spell_tiers": ["tier_0_baseline", "tier_1_early"],
        "bounty_tiers": ["none", "tutorial", "local_errand"],
        "milestones": ["Reach a village safely", "Take the Ascendant Oath", "Clear a small local problem"],
    },
    "e_rank": {
        "identity": "A registered beginner hunter who can handle ordinary danger.",
        "criteria": [
            "Prove basic hostile-mob survival and complete village work.",
            "Show one preferred skill branch instead of raw XP grinding.",
            "Operate mostly in Crownlands and inner-road regions.",
        ],
        "skill_points": [4, 8],
        "skill_thresholds": [0, 4],
        "threat_range": [0, 2],
        "regions": ["crownlands", "verdant_coast"],
        "rings": ["center", "inner"],
        "gear_rarities": ["common", "uncommon", "rare"],
        "spell_tiers": ["tier_1_early", "tier_2_regional"],
        "bounty_tiers": ["village_request", "wildlife_control"],
        "milestones": ["Complete several village contracts", "Survive a night patrol", "Defeat routine hostile pressure"],
    },
    "d_rank": {
        "identity": "A field adventurer trusted with roads, ruins, and regional work.",
        "criteria": [
            "Clear small structures or roadside threats.",
            "Bring back proof from a climate-region trip.",
            "Use rare gear or regional materials without jumping into boss-tier rewards.",
        ],
        "skill_points": [8, 13],
        "skill_thresholds": [0, 4],
        "threat_range": [1, 3],
        "regions": ["crownlands", "verdant_coast", "sunreach", "stoneback_highlands", "frostmarch"],
        "rings": ["inner", "middle"],
        "gear_rarities": ["uncommon", "rare"],
        "spell_tiers": ["tier_2_regional"],
        "bounty_tiers": ["village_request", "road_patrol", "small_ruin"],
        "milestones": ["Clear a minor ruin", "Protect a settlement route", "Return with regional materials"],
    },
    "c_rank": {
        "identity": "A licensed monster hunter who can survive real dungeons and elite pressure.",
        "criteria": [
            "Defeat elite mobs and clear meaningful structures.",
            "Demonstrate mid-tree skill specialization.",
            "Handle region identity rather than staying in starter terrain.",
        ],
        "skill_points": [14, 23],
        "skill_thresholds": [0, 4, 14],
        "threat_range": [2, 4],
        "regions": ["frostmarch", "sunreach", "verdant_coast", "stoneback_highlands", "deep_wilds"],
        "rings": ["middle"],
        "gear_rarities": ["rare", "epic"],
        "spell_tiers": ["tier_2_regional", "tier_3_advanced"],
        "bounty_tiers": ["town_guild_board", "dungeon_contract", "rival_sighting"],
        "milestones": ["Clear a dungeon", "Win an elite hunt", "Earn a rival or town Guild notice"],
    },
    "b_rank": {
        "identity": "An elite hunter capable of major dungeons and named modded threats.",
        "criteria": [
            "Clear serious structures and survive high-pressure regions.",
            "Beat named or miniboss-grade threats.",
            "Earn legendary rewards only from danger that justifies them.",
        ],
        "skill_points": [24, 31],
        "skill_thresholds": [0, 4, 14],
        "threat_range": [3, 5],
        "regions": ["deep_wilds", "dragon_scars", "frostmarch", "sunreach", "stoneback_highlands"],
        "rings": ["middle", "outer"],
        "gear_rarities": ["rare", "epic", "legendary"],
        "spell_tiers": ["tier_3_advanced", "tier_4_boss"],
        "bounty_tiers": ["major_guild_registry", "miniboss_contract", "arcane_recovery"],
        "milestones": ["Clear a major dungeon", "Defeat a named threat", "Recover boss-adjacent material"],
    },
    "a_rank": {
        "identity": "A realm-class fighter trusted with boss hunts and dragon-warning work.",
        "criteria": [
            "Prove capstone skill commitment.",
            "Defeat major bosses or dragon-tier threats.",
            "Operate in outer and hostile dimension-linked regions.",
        ],
        "skill_points": [32, 44],
        "skill_thresholds": [0, 4, 14, 32],
        "threat_range": [4, 6],
        "regions": ["dragon_scars", "deep_wilds", "nether_front", "end_expanse"],
        "rings": ["outer", "edge"],
        "gear_rarities": ["epic", "legendary", "mythic"],
        "spell_tiers": ["tier_4_boss", "tier_5_dragon"],
        "bounty_tiers": ["realm_threat", "dragon_warning", "boss_hunt"],
        "milestones": ["Defeat a major boss", "Survive dragon-tier ecology", "Recover mythic material"],
    },
    "s_rank": {
        "identity": "An ascendant-class anomaly measured by realm-defining achievements.",
        "criteria": [
            "Clear capstone bosses or ascendant outer threats.",
            "Show mastery across multiple systems, not just raw XP.",
            "Receive ascendant rewards only from ascendant-scale danger.",
        ],
        "skill_points": [45, 99],
        "skill_thresholds": [0, 4, 14, 32],
        "threat_range": [5, 6],
        "regions": ["dragon_scars", "nether_front", "end_expanse", "deep_wilds"],
        "rings": ["edge"],
        "gear_rarities": ["legendary", "mythic", "ascendant"],
        "spell_tiers": ["tier_5_dragon", "tier_6_ascendant"],
        "bounty_tiers": ["cataclysmic_threat", "dragon_tier", "ascendant_relic"],
        "milestones": ["Clear a realm-defining boss", "Recover an ascendant relic", "Become a Guild legend"],
    },
}

GEAR_RARITY_RANKS = {
    "common": {
        "minimum_rank": "unranked",
        "routine_rank": "unranked",
        "ceiling_rank": "s_rank",
        "role": "baseline survival, tools, and low-risk rewards",
    },
    "uncommon": {
        "minimum_rank": "unranked",
        "routine_rank": "e_rank",
        "ceiling_rank": "s_rank",
        "role": "starter upgrades and safe village rewards",
    },
    "rare": {
        "minimum_rank": "e_rank",
        "routine_rank": "d_rank",
        "ceiling_rank": "s_rank",
        "role": "regional gear, early dungeons, and ranked village work",
    },
    "epic": {
        "minimum_rank": "c_rank",
        "routine_rank": "c_rank",
        "ceiling_rank": "s_rank",
        "role": "real dungeon rewards, elite drops, and specialized builds",
    },
    "legendary": {
        "minimum_rank": "b_rank",
        "routine_rank": "b_rank",
        "ceiling_rank": "s_rank",
        "role": "major structure, boss-adjacent, and high-rank contract rewards",
    },
    "mythic": {
        "minimum_rank": "a_rank",
        "routine_rank": "a_rank",
        "ceiling_rank": "s_rank",
        "role": "dragon, boss, and outer-region rewards",
    },
    "ascendant": {
        "minimum_rank": "s_rank",
        "routine_rank": "s_rank",
        "ceiling_rank": "s_rank",
        "role": "capstone and ascendant-class rewards only",
    },
}

MAGIC_TIER_RANKS = {
    "tier_0_baseline": {"minimum_rank": "unranked", "routine_rank": "unranked", "ceiling_rank": "e_rank"},
    "tier_1_early": {"minimum_rank": "unranked", "routine_rank": "e_rank", "ceiling_rank": "d_rank"},
    "tier_2_regional": {"minimum_rank": "d_rank", "routine_rank": "d_rank", "ceiling_rank": "c_rank"},
    "tier_3_advanced": {"minimum_rank": "c_rank", "routine_rank": "c_rank", "ceiling_rank": "b_rank"},
    "tier_4_boss": {"minimum_rank": "b_rank", "routine_rank": "b_rank", "ceiling_rank": "a_rank"},
    "tier_5_dragon": {"minimum_rank": "a_rank", "routine_rank": "a_rank", "ceiling_rank": "s_rank"},
    "tier_6_ascendant": {"minimum_rank": "s_rank", "routine_rank": "s_rank", "ceiling_rank": "s_rank"},
    "not_craftable_or_not_found": {"minimum_rank": "manual_review", "routine_rank": "manual_review", "ceiling_rank": "manual_review"},
}


def load_json(relative: str, default: Any) -> Any:
    path = ROOT / relative
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(relative: str, data: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc(relative: str, text: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def rank_order_map() -> dict[str, int]:
    return {rank_id: index for index, rank_id in enumerate(REQUIRED_RANKS)}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def skill_threshold(skill: dict[str, Any]) -> int:
    value = skill.get("required_spent_points", 0)
    return int(value or 0) if isinstance(value, (int, float)) else 0


def build_skill_inventory() -> tuple[dict[str, dict[str, Any]], dict[int, list[str]], dict[str, str]]:
    definitions = load_json("config/puffish_skills/categories/ascendant/definitions.json", {})
    skills = load_json("config/puffish_skills/categories/ascendant/skills.json", {})
    by_threshold: dict[int, list[str]] = defaultdict(list)
    titles: dict[str, str] = {}
    if not isinstance(definitions, dict):
        return {}, {}, {}
    for skill_id, definition in definitions.items():
        if not isinstance(definition, dict):
            continue
        threshold = skill_threshold(definition)
        by_threshold[threshold].append(str(skill_id))
        titles[str(skill_id)] = str(definition.get("title") or skill_id)
    merged: dict[str, dict[str, Any]] = {}
    for skill_id, definition in definitions.items():
        if not isinstance(definition, dict):
            continue
        position = skills.get(skill_id, {}) if isinstance(skills, dict) else {}
        merged[str(skill_id)] = {
            "id": str(skill_id),
            "title": str(definition.get("title") or skill_id),
            "required_spent_points": skill_threshold(definition),
            "cost": definition.get("cost", 0),
            "frame": definition.get("frame", ""),
            "x": position.get("x") if isinstance(position, dict) else None,
            "y": position.get("y") if isinstance(position, dict) else None,
        }
    return merged, {key: sorted(value) for key, value in by_threshold.items()}, titles


def build_rank_lookup() -> dict[str, dict[str, Any]]:
    rank_progression = load_json("config/ascendant_core/rank_progression.json", {})
    lookup = {rank_id: {"id": rank_id, "display": RANK_LABELS[rank_id], "order": index} for index, rank_id in enumerate(REQUIRED_RANKS)}
    for rank in safe_list(rank_progression.get("rank_ladder", [])) if isinstance(rank_progression, dict) else []:
        if not isinstance(rank, dict):
            continue
        rank_id = str(rank.get("id") or "")
        if rank_id in lookup:
            lookup[rank_id].update(rank)
    return lookup


def build_rank_matrix(rank_lookup: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for rank_id in REQUIRED_RANKS:
        base = rank_lookup.get(rank_id, {})
        guidance = RANK_GUIDANCE[rank_id]
        rows.append(
            {
                "rank_id": rank_id,
                "display_name": base.get("display", RANK_LABELS[rank_id]),
                "order": base.get("order", REQUIRED_RANKS.index(rank_id)),
                "status": "guidance_only_no_hard_lock",
                "identity": guidance["identity"],
                "evaluation_style": "public_guild_evaluation_not_checklist_grind",
                "ascendant_web_level_band": base.get("level_band", []),
                "recommended_spent_skill_points": guidance["skill_points"],
                "recommended_skill_thresholds": guidance["skill_thresholds"],
                "recommended_regions": guidance["regions"],
                "recommended_distance_rings": guidance["rings"],
                "recommended_mob_threat_range": guidance["threat_range"],
                "recommended_gear_rarities": guidance["gear_rarities"],
                "recommended_spell_tiers": guidance["spell_tiers"],
                "recommended_bounty_tiers": guidance["bounty_tiers"],
                "recommended_boss_structure_milestones": guidance["milestones"],
                "gear_ceiling_from_core": base.get("gear_ceiling"),
                "contract_access_from_core": base.get("contract_access", []),
                "criteria": guidance["criteria"],
                "proof_counter_guidance": {
                    "reputation": "counts toward automated bridge but should not be the only rank signal",
                    "bounties_done": "supports rank evaluation once Bountiful contracts are validated",
                    "structures_done": "should come from meaningful structure clears, not trivial repeat farming",
                    "bosses_done": "required for B/A/S style evaluations",
                    "dragons_done": "A/S scale proof only",
                },
            }
        )
    validation = {
        "missing_ranks": sorted(set(REQUIRED_RANKS) - {row["rank_id"] for row in rows}),
        "policy_references_missing_regions": [],
        "gear_rarities_without_rank_policy": [],
        "magic_tiers_without_rank_policy": [],
        "skill_unlock_policy_references_missing_skill_ids": [],
        "starter_region_threat_excess": [],
    }
    return {
        "version": 1,
        "generated_at": GENERATED_AT,
        "status": "audit_control_scaffold_only_no_hard_gates",
        "source": {
            "rank_progression": "config/ascendant_core/rank_progression.json",
            "runtime_rules": "config/ascendant_core/runtime_rules.json",
            "loot_rarity_budget": "config/ascendant_loot/loot_rarity_budget.json",
            "atlas_regions": "config/ascendant_atlas/regions.json",
            "puffish_skills": "config/puffish_skills/categories/ascendant/*.json",
        },
        "rules": [
            "Rank is public evaluation, not raw XP.",
            "Puffish Skills remains personal power growth.",
            "Use rank to guide rewards and expectations without locking existing content yet.",
            "C/B/A/S require real world achievements, not checklist grinding.",
        ],
        "ranks": rows,
        "validation": validation,
        "summary": {
            "rank_count": len(rows),
            "required_rank_count": len(REQUIRED_RANKS),
        },
    }


def build_skill_policy(rank_lookup: dict[str, dict[str, Any]]) -> dict[str, Any]:
    skills, by_threshold, titles = build_skill_inventory()
    milestones: list[dict[str, Any]] = []
    for rank_id in REQUIRED_RANKS:
        guidance = RANK_GUIDANCE[rank_id]
        thresholds = guidance["skill_thresholds"]
        referenced: list[str] = []
        for threshold in thresholds:
            referenced.extend(by_threshold.get(threshold, [])[:10])
        referenced = list(dict.fromkeys(referenced))
        milestones.append(
            {
                "rank_id": rank_id,
                "display_name": rank_lookup.get(rank_id, {}).get("display", RANK_LABELS[rank_id]),
                "status": "recommended_only_no_skill_lock",
                "ascendant_web_level_band": rank_lookup.get(rank_id, {}).get("level_band", []),
                "recommended_spent_points": guidance["skill_points"],
                "recommended_skill_thresholds": thresholds,
                "referenced_skill_ids": referenced,
                "referenced_skill_titles": {skill_id: titles.get(skill_id, skill_id) for skill_id in referenced},
                "player_power_note": "Skill points prove growth direction, while Guild rank measures public achievements.",
            }
        )
    referenced_ids = {skill_id for entry in milestones for skill_id in entry["referenced_skill_ids"]}
    return {
        "version": 1,
        "generated_at": GENERATED_AT,
        "status": "audit_control_scaffold_only_no_hard_skill_gates",
        "source": {
            "definitions": "config/puffish_skills/categories/ascendant/definitions.json",
            "skills": "config/puffish_skills/categories/ascendant/skills.json",
            "progression_runtime": "config/ascendant_progression/progression.json",
        },
        "known_skill_count": len(skills),
        "skill_threshold_counts": {str(key): len(value) for key, value in sorted(by_threshold.items())},
        "rank_skill_milestones": milestones,
        "validation": {
            "missing_skill_ids": sorted(referenced_ids - set(skills)),
            "unreferenced_skill_ids": sorted(set(skills) - referenced_ids),
        },
        "summary": {
            "rank_milestones": len(milestones),
            "referenced_skill_ids": len(referenced_ids),
            "known_skill_ids": len(skills),
        },
    }


def build_region_policy() -> dict[str, Any]:
    atlas = load_json("config/ascendant_atlas/regions.json", {})
    regions = [region for region in safe_list(atlas.get("regions", [])) if isinstance(region, dict)] if isinstance(atlas, dict) else []
    tier_map = {
        0: (["unranked", "e_rank"], [0, 2], ["center"]),
        1: (["e_rank", "d_rank"], [1, 3], ["inner"]),
        2: (["d_rank", "c_rank"], [2, 4], ["middle"]),
        3: (["c_rank", "b_rank"], [3, 5], ["middle", "outer"]),
        4: (["b_rank", "a_rank"], [4, 6], ["outer", "edge"]),
        5: (["a_rank", "s_rank"], [5, 6], ["edge"]),
    }
    entries: list[dict[str, Any]] = []
    for region in regions:
        tier = int(region.get("tier", 0) or 0)
        ranks, threat, rings = tier_map.get(tier, tier_map[5])
        entries.append(
            {
                "region_id": region.get("id"),
                "display_name": region.get("display_name", region.get("id")),
                "atlas_tier": tier,
                "sector": region.get("sector"),
                "recommended_ranks": ranks,
                "recommended_distance_rings": rings,
                "recommended_mob_threat_range": threat,
                "recommended_gear_ceiling": region.get("loot_ceiling", "manual_review"),
                "bounty_tiers": [RANK_GUIDANCE[rank]["bounty_tiers"][-1] for rank in ranks if rank in RANK_GUIDANCE],
                "readiness_notes": [
                    "Guidance only; do not teleport-lock or gate regions yet.",
                    "Use Atlas validation and manual terrain review before promising region pacing.",
                ],
            }
        )
    validation = {
        "policy_references_missing_regions": [],
        "starter_region_threat_excess": [
            entry["region_id"]
            for entry in entries
            if set(entry["recommended_ranks"]) & {"unranked", "e_rank"}
            and int(entry["recommended_mob_threat_range"][1]) > 2
        ],
    }
    return {
        "version": 1,
        "generated_at": GENERATED_AT,
        "status": "audit_control_scaffold_only_no_region_locks",
        "source": {
            "atlas_regions": "config/ascendant_atlas/regions.json",
            "difficulty_rings": "config/ascendant_atlas/difficulty_rings.json",
            "world_regions": "config/ascendant_core/world_regions.json",
        },
        "region_readiness": entries,
        "validation": validation,
        "summary": {
            "region_count": len(entries),
            "starter_region_count": sum(1 for entry in entries if set(entry["recommended_ranks"]) & {"unranked", "e_rank"}),
        },
    }


def build_gear_policy() -> dict[str, Any]:
    gear_registry = load_json("config/ascendant_index/gear_registry.json", {})
    stat_policy = load_json("config/ascendant_balance/stat_policy.json", {})
    rarities = []
    if isinstance(gear_registry, dict):
        rarities = [str(entry.get("id")) for entry in safe_list(gear_registry.get("rarity_tiers", [])) if isinstance(entry, dict) and entry.get("id")]
    policy_entries = []
    for rarity in rarities or list(GEAR_RARITY_RANKS):
        base = GEAR_RARITY_RANKS.get(rarity, {"minimum_rank": "manual_review", "routine_rank": "manual_review", "ceiling_rank": "manual_review", "role": "manual review"})
        policy_entries.append(
            {
                "rarity": rarity,
                "minimum_recommended_rank": base["minimum_rank"],
                "routine_reward_rank": base["routine_rank"],
                "maximum_relevant_rank": base["ceiling_rank"],
                "role": base["role"],
                "policy": "placement_guidance_only_no_stat_or_rarity_change",
            }
        )
    summary = stat_policy.get("summary", {}) if isinstance(stat_policy, dict) else {}
    validation = {
        "gear_rarities_without_rank_policy": sorted(set(rarities) - {entry["rarity"] for entry in policy_entries}),
        "rank_policy_references_missing_ranks": sorted(
            {
                value
                for entry in policy_entries
                for value in (entry["minimum_recommended_rank"], entry["routine_reward_rank"], entry["maximum_relevant_rank"])
                if value != "manual_review" and value not in REQUIRED_RANKS
            }
        ),
    }
    return {
        "version": 1,
        "generated_at": GENERATED_AT,
        "status": "audit_control_scaffold_only_no_gear_gates",
        "source": {
            "gear_registry": "config/ascendant_index/gear_registry.json",
            "stat_policy": "config/ascendant_balance/stat_policy.json",
            "loot_budget": "config/ascendant_loot/loot_rarity_budget.json",
        },
        "rarity_rank_policy": policy_entries,
        "gear_policy_summary": summary,
        "validation": validation,
        "summary": {
            "rarity_policy_entries": len(policy_entries),
            "known_gear_policy_entries": summary.get("balance_policy_entries", 0),
            "outlier_items": summary.get("outlier_items", 0),
        },
    }


def build_magic_policy() -> dict[str, Any]:
    spell_registry = load_json("config/ascendant_magic/spell_progression_registry.json", {})
    item_registry = load_json("config/ascendant_magic/magic_item_progression_registry.json", {})
    magic_entries = []
    if isinstance(spell_registry, dict):
        magic_entries.extend(safe_list(spell_registry.get("spells", [])))
    if isinstance(item_registry, dict):
        magic_entries.extend(safe_list(item_registry.get("magic_items", [])))
    observed_tiers = (
        {
            str(entry.get("allowed_loot_tier"))
            for entry in magic_entries
            if isinstance(entry, dict) and entry.get("allowed_loot_tier")
        }
        | {
            str(entry.get("recipe_tier_if_craftable"))
            for entry in magic_entries
            if isinstance(entry, dict) and entry.get("recipe_tier_if_craftable")
        }
        | set(MAGIC_TIER_RANKS)
    )
    tier_sort_order = {tier: index for index, tier in enumerate(MAGIC_TIER_RANKS)}
    observed_tiers = sorted(observed_tiers, key=lambda tier: (tier_sort_order.get(tier, 999), tier))
    tier_entries = []
    for tier in observed_tiers:
        base = MAGIC_TIER_RANKS.get(tier, {"minimum_rank": "manual_review", "routine_rank": "manual_review", "ceiling_rank": "manual_review"})
        tier_entries.append(
            {
                "magic_tier": tier,
                "minimum_recommended_rank": base["minimum_rank"],
                "routine_reward_rank": base["routine_rank"],
                "maximum_relevant_rank": base["ceiling_rank"],
                "policy": "placement_guidance_only_no_spell_or_recipe_gate",
            }
        )
    band_counts = Counter(
        str(entry.get("progression_band") or "unknown")
        for entry in magic_entries
        if isinstance(entry, dict)
    )
    validation = {
        "magic_tiers_without_rank_policy": sorted(set(observed_tiers) - {entry["magic_tier"] for entry in tier_entries}),
        "rank_policy_references_missing_ranks": sorted(
            {
                value
                for entry in tier_entries
                for value in (entry["minimum_recommended_rank"], entry["routine_reward_rank"], entry["maximum_relevant_rank"])
                if value != "manual_review" and value not in REQUIRED_RANKS
            }
        ),
    }
    return {
        "version": 1,
        "generated_at": GENERATED_AT,
        "status": "audit_control_scaffold_only_no_magic_gates",
        "source": {
            "spell_registry": "config/ascendant_magic/spell_progression_registry.json",
            "magic_item_registry": "config/ascendant_magic/magic_item_progression_registry.json",
        },
        "magic_tier_rank_policy": tier_entries,
        "progression_band_counts": dict(sorted(band_counts.items())),
        "validation": validation,
        "summary": {
            "magic_entries": len(magic_entries),
            "magic_tier_policy_entries": len(tier_entries),
            "observed_magic_tiers": len(observed_tiers),
        },
    }


def compute_combined_validation(
    rank_matrix: dict[str, Any],
    skill_policy: dict[str, Any],
    region_policy: dict[str, Any],
    gear_policy: dict[str, Any],
    magic_policy: dict[str, Any],
) -> dict[str, Any]:
    atlas_regions = {
        str(region.get("id"))
        for region in safe_list(load_json("config/ascendant_atlas/regions.json", {}).get("regions", []))
        if isinstance(region, dict) and region.get("id")
    }
    referenced_regions = {
        str(region_id)
        for rank in rank_matrix.get("ranks", [])
        if isinstance(rank, dict)
        for region_id in safe_list(rank.get("recommended_regions", []))
    }
    known_skills = set(build_skill_inventory()[0])
    referenced_skills = {
        str(skill_id)
        for row in skill_policy.get("rank_skill_milestones", [])
        if isinstance(row, dict)
        for skill_id in safe_list(row.get("referenced_skill_ids", []))
    }
    return {
        "missing_ranks": rank_matrix.get("validation", {}).get("missing_ranks", []),
        "rank_policy_references_missing_regions": sorted(referenced_regions - atlas_regions),
        "gear_rarities_without_rank_policy": gear_policy.get("validation", {}).get("gear_rarities_without_rank_policy", []),
        "magic_tiers_without_rank_policy": magic_policy.get("validation", {}).get("magic_tiers_without_rank_policy", []),
        "skill_unlock_policy_references_missing_skill_ids": sorted(referenced_skills - known_skills),
        "starter_region_threat_excess": region_policy.get("validation", {}).get("starter_region_threat_excess", []),
    }


def update_validation(report: dict[str, Any], combined: dict[str, Any]) -> None:
    validation = report.setdefault("validation", {})
    validation.update(combined)


def build_docs(
    rank_matrix: dict[str, Any],
    skill_policy: dict[str, Any],
    region_policy: dict[str, Any],
    gear_policy: dict[str, Any],
    magic_policy: dict[str, Any],
) -> tuple[str, str, str]:
    rank_rows = []
    for row in rank_matrix["ranks"]:
        rank_rows.append(
            [
                row["display_name"],
                "-".join(str(value) for value in row.get("ascendant_web_level_band", [])),
                ", ".join(row["recommended_regions"]),
                ", ".join(row["recommended_gear_rarities"]),
                ", ".join(row["recommended_spell_tiers"]),
                ", ".join(row["recommended_bounty_tiers"]),
            ]
        )
    rank_table = md_table(
        ["Rank", "Level Band", "Regions", "Gear", "Magic Tiers", "Bounty Work"],
        rank_rows,
    )

    skill_rows = []
    for row in skill_policy["rank_skill_milestones"]:
        skill_rows.append(
            [
                row["display_name"],
                "-".join(str(value) for value in row["recommended_spent_points"]),
                ", ".join(str(value) for value in row["recommended_skill_thresholds"]),
                len(row["referenced_skill_ids"]),
            ]
        )
    skill_table = md_table(["Rank", "Recommended SP", "Skill Thresholds", "Referenced Skills"], skill_rows)

    region_rows = []
    for row in region_policy["region_readiness"]:
        region_rows.append(
            [
                row["display_name"],
                row["atlas_tier"],
                ", ".join(row["recommended_ranks"]),
                "-".join(str(value) for value in row["recommended_mob_threat_range"]),
                row["recommended_gear_ceiling"],
            ]
        )
    region_table = md_table(["Region", "Tier", "Ranks", "Threat", "Gear Ceiling"], region_rows)

    gear_rows = [
        [
            row["rarity"],
            row["minimum_recommended_rank"],
            row["routine_reward_rank"],
            row["role"],
        ]
        for row in gear_policy["rarity_rank_policy"]
    ]
    gear_table = md_table(["Rarity", "Minimum Rank", "Routine Rank", "Role"], gear_rows)

    magic_rows = [
        [
            row["magic_tier"],
            row["minimum_recommended_rank"],
            row["routine_reward_rank"],
            row["maximum_relevant_rank"],
        ]
        for row in magic_policy["magic_tier_rank_policy"]
    ]
    magic_table = md_table(["Magic Tier", "Minimum Rank", "Routine Rank", "Ceiling Rank"], magic_rows)

    summary_lines = [
        "# Ascendant Player Progression",
        "",
        f"Generated: {GENERATED_AT}",
        "",
        "## Status",
        "",
        "This is a progression bridge scaffold only. It does not add mods, lock regions, lock recipes, lock skills, change loot, or stop players from reaching existing content.",
        "",
        "Rank is public Guild evaluation. Puffish Skills is personal power growth. Loot, gear, magic, bounties, Atlas regions, and boss milestones now have a shared policy spine, but enforcement still needs explicit approval.",
        "",
        "## Rank Spine",
        "",
        rank_table,
        "",
        "## Region Readiness",
        "",
        region_table,
        "",
        "## Gear Rank Policy",
        "",
        gear_table,
        "",
        "## Magic Rank Policy",
        "",
        magic_table,
        "",
        "## Design Rules",
        "",
        "- Rank should feel like evaluation, not checklist grinding.",
        "- The player should always have several valid goals at the same time.",
        "- C/B/A/S rank should require real world achievements, not just XP.",
        "- Prefer guidance, rank display, reward pacing, and quest language before hard gates.",
        "- Terrain/water acceptance still comes before civilization, road, village, Hunter Board, or Guild Hall placement work.",
    ]

    matrix_lines = [
        "# Guild Rank Requirement Matrix",
        "",
        f"Generated: {GENERATED_AT}",
        "",
        "This matrix defines what each public Guild rank should mean. It is not a live hard gate.",
        "",
        rank_table,
        "",
        "## Rank Details",
        "",
    ]
    for row in rank_matrix["ranks"]:
        matrix_lines.extend(
            [
                f"### {row['display_name']}",
                "",
                f"- Identity: {row['identity']}",
                f"- Evaluation style: {row['evaluation_style']}.",
                f"- Recommended mob threat range: {row['recommended_mob_threat_range'][0]}-{row['recommended_mob_threat_range'][1]}.",
                f"- Boss/structure milestones: {', '.join(row['recommended_boss_structure_milestones'])}.",
                f"- Criteria: {'; '.join(row['criteria'])}.",
                "",
            ]
        )

    skill_lines = [
        "# Skill Tree Integration Plan",
        "",
        f"Generated: {GENERATED_AT}",
        "",
        "This plan connects the Ascendant Web to public Guild rank without turning skill points into a narrow checklist.",
        "",
        skill_table,
        "",
        "## Policy",
        "",
        "- Skill level and spent points show player growth direction.",
        "- Guild rank should also require bounties, structures, bosses, regional survival, and public proof.",
        "- Do not hard-lock existing skills by rank yet.",
        "- Future FTB Quest rank trials can read this policy after terrain and reward pacing are accepted.",
    ]
    return "\n".join(summary_lines), "\n".join(matrix_lines), "\n".join(skill_lines)


GENERATED_AT = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    rank_lookup = build_rank_lookup()
    rank_matrix = build_rank_matrix(rank_lookup)
    skill_policy = build_skill_policy(rank_lookup)
    region_policy = build_region_policy()
    gear_policy = build_gear_policy()
    magic_policy = build_magic_policy()
    combined = compute_combined_validation(rank_matrix, skill_policy, region_policy, gear_policy, magic_policy)
    for report in (rank_matrix, skill_policy, region_policy, gear_policy, magic_policy):
        update_validation(report, combined)

    write_json("config/ascendant_progression/rank_requirement_matrix.json", rank_matrix)
    write_json("config/ascendant_progression/skill_unlock_policy.json", skill_policy)
    write_json("config/ascendant_progression/region_progression_policy.json", region_policy)
    write_json("config/ascendant_progression/gear_rank_policy.json", gear_policy)
    write_json("config/ascendant_progression/magic_rank_policy.json", magic_policy)

    summary_doc, matrix_doc, skill_doc = build_docs(rank_matrix, skill_policy, region_policy, gear_policy, magic_policy)
    write_doc("docs/ASCENDANT_PLAYER_PROGRESSION.md", summary_doc)
    write_doc("docs/GUILD_RANK_REQUIREMENT_MATRIX.md", matrix_doc)
    write_doc("docs/SKILL_TREE_INTEGRATION_PLAN.md", skill_doc)

    print("Ascendant player progression scaffold generated.")
    print(f"Ranks: {len(rank_matrix['ranks'])}")
    print(f"Skill IDs known: {skill_policy['known_skill_count']}")
    print(f"Atlas regions: {region_policy['summary']['region_count']}")
    print(f"Gear rarity policies: {gear_policy['summary']['rarity_policy_entries']}")
    print(f"Magic tier policies: {magic_policy['summary']['magic_tier_policy_entries']}")


if __name__ == "__main__":
    main()
