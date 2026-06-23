#!/usr/bin/env python3
"""Generate the Ascendant recipe progression audit and candidate rewrite plan."""

from __future__ import annotations

import json
import os
import pathlib
import re
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
ACTIVE_INSTANCE = pathlib.Path(
    os.environ.get(
        "ASCENDANT_ACTIVE_INSTANCE",
        r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)",
    )
)
ACTIVE_MODS = ACTIVE_INSTANCE / "mods"

OUT_DIR = ROOT / "config/ascendant_recipes"
DOCS_DIR = ROOT / "docs"
DISABLED_REVIEW_DIR = ROOT / "kubejs/server_scripts_disabled/review/ascendant_recipes"

RARITY_ORDER = {
    "common": 0,
    "uncommon": 1,
    "rare": 2,
    "epic": 3,
    "legendary": 4,
    "mythic": 5,
    "ascendant": 6,
}

RARITY_POLICY = {
    "common": {
        "guild_rank": "unranked",
        "atlas_ring": "center",
        "recipe_tier": "tier_0_baseline",
        "material_tier": "mundane",
    },
    "uncommon": {
        "guild_rank": "e_rank",
        "atlas_ring": "center_to_inner",
        "recipe_tier": "tier_1_early",
        "material_tier": "mundane_to_regional",
    },
    "rare": {
        "guild_rank": "d_rank",
        "atlas_ring": "inner_to_middle",
        "recipe_tier": "tier_2_regional",
        "material_tier": "regional",
    },
    "epic": {
        "guild_rank": "c_rank_to_b_rank",
        "atlas_ring": "middle",
        "recipe_tier": "tier_3_advanced",
        "material_tier": "refined_or_structure",
    },
    "legendary": {
        "guild_rank": "b_rank_to_a_rank",
        "atlas_ring": "outer",
        "recipe_tier": "tier_4_boss",
        "material_tier": "boss_or_rank_proof",
    },
    "mythic": {
        "guild_rank": "a_rank_to_s_rank",
        "atlas_ring": "outer_to_edge",
        "recipe_tier": "tier_5_dragon",
        "material_tier": "dragon_or_capstone",
    },
    "ascendant": {
        "guild_rank": "s_rank",
        "atlas_ring": "edge",
        "recipe_tier": "tier_6_ascendant",
        "material_tier": "ascendant_capstone",
    },
}

VANILLA_NAMESPACES = {"minecraft"}
LOW_TIER_VANILLA_ITEMS = {
    "minecraft:stick",
    "minecraft:flint",
    "minecraft:string",
    "minecraft:leather",
    "minecraft:feather",
    "minecraft:paper",
    "minecraft:book",
    "minecraft:bone",
    "minecraft:glass",
    "minecraft:coal",
    "minecraft:charcoal",
    "minecraft:copper_ingot",
    "minecraft:iron_ingot",
    "minecraft:gold_ingot",
    "minecraft:redstone",
    "minecraft:lapis_lazuli",
    "minecraft:amethyst_shard",
    "minecraft:quartz",
    "minecraft:blaze_rod",
    "minecraft:ender_pearl",
}
HIGH_TIER_TERMS = (
    "ancient",
    "ascendant",
    "awakened",
    "boss",
    "dragon",
    "dragonbone",
    "dragonsteel",
    "echo_shard",
    "elytra",
    "empowered",
    "heart",
    "legendary",
    "mythic",
    "nether_star",
    "netherite",
    "phylactery",
    "relic",
    "rune",
    "seal",
    "sigil",
    "soul",
    "wither",
)
MATERIAL_TERMS = re.compile(
    r"(^raw_|_ingot$|_nugget$|_gem$|_dust$|_scrap$|_ore$|_crystal$|_shard$|_scale$|_bone$|_plate$|_rod$|_sheet$|_wire$|_gear$)"
)
DIRECT_DUPLICATE_MATERIAL_TERMS = re.compile(r"(_ingot$|_nugget$|_gem$|_dust$|_plate$|_rod$|_sheet$|_wire$|_gear$)")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def safe_rel(path: pathlib.Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def namespace(value: str) -> str:
    return value.split(":", 1)[0] if ":" in value else ""


def local_id(value: str) -> str:
    return value.split(":", 1)[-1]


def is_item_id(value: object) -> bool:
    return isinstance(value, str) and bool(re.match(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$", value))


def is_material_like(item_id: str) -> bool:
    return bool(MATERIAL_TERMS.search(local_id(item_id).lower()))


def is_direct_duplicate_material(item_id: str) -> bool:
    local = local_id(item_id).lower()
    return bool(DIRECT_DUPLICATE_MATERIAL_TERMS.search(local)) and not local.startswith("crushed_raw")


def has_high_tier_term(value: str) -> bool:
    lower = value.lower()
    return any(term in lower for term in HIGH_TIER_TERMS)


def load_registries() -> tuple[dict[str, Any], dict[str, str], dict[str, set[str]], dict[str, str]]:
    gear_registry = read_json(ROOT / "config/ascendant_index/gear_registry.json")
    rarity_by_item: dict[str, str] = {}
    domains_by_item: dict[str, set[str]] = defaultdict(set)
    mod_by_namespace: dict[str, str] = {}
    for collection in ("weapons", "armor", "shields", "magic_items", "spells", "accessories_relics"):
        for entry in gear_registry.get(collection, []):
            item_id = str(entry.get("id") or "")
            if not item_id:
                continue
            rarity = str(entry.get("rarity") or "common").lower()
            rarity_by_item[item_id] = rarity
            domain_value = entry.get("domains") or entry.get("domain") or collection
            if isinstance(domain_value, str):
                domain_parts = re.split(r"[,;/ ]+", domain_value)
            elif isinstance(domain_value, list):
                domain_parts = [str(part) for part in domain_value]
            else:
                domain_parts = [collection]
            for domain in domain_parts:
                if domain:
                    domains_by_item[item_id].add(domain.strip())
            domains_by_item[item_id].add(collection.rstrip("s"))
            mod_id = str(entry.get("mod_id") or namespace(item_id))
            source_mod = str(entry.get("source_mod") or mod_id)
            if mod_id:
                mod_by_namespace.setdefault(mod_id, source_mod)
    return gear_registry, rarity_by_item, domains_by_item, mod_by_namespace


def canonical_materials() -> dict[str, dict[str, Any]]:
    path = ROOT / "config/ascendant_core/materials.json"
    if not path.exists():
        return {}
    data = read_json(path)
    materials = data.get("canonical_materials", {})
    return materials if isinstance(materials, dict) else {}


def parse_kubejs_items() -> set[str]:
    item_ids: set[str] = set()
    startup_dir = ROOT / "kubejs/startup_scripts"
    if not startup_dir.exists():
        return item_ids
    for script in startup_dir.glob("*.js"):
        text = script.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"event\.create\(['\"]([^'\"]+)['\"]\)", text):
            raw = match.group(1)
            item_ids.add(raw if ":" in raw else f"kubejs:{raw}")
    return item_ids


def collect_known_items_from_jars() -> tuple[set[str], set[str]]:
    items: set[str] = set()
    namespaces: set[str] = {"minecraft", "kubejs"}
    if not ACTIVE_MODS.exists():
        return items, namespaces
    for jar_path in sorted(ACTIVE_MODS.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar_path) as jar:
                for name in jar.namelist():
                    if name.startswith("assets/") and "/models/item/" in name and name.endswith(".json"):
                        parts = name.split("/")
                        if len(parts) >= 5:
                            ns = parts[1]
                            item_name = pathlib.PurePosixPath(name).stem
                            namespaces.add(ns)
                            items.add(f"{ns}:{item_name}")
                    elif name.startswith("data/"):
                        parts = name.split("/")
                        if len(parts) > 1:
                            namespaces.add(parts[1])
        except zipfile.BadZipFile:
            continue
    return items, namespaces


def output_entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []

    def add(item_id: object, count: object = None) -> None:
        if is_item_id(item_id):
            amount = 1
            if isinstance(count, int):
                amount = count
            elif isinstance(count, float):
                amount = int(count)
            outputs.append({"item_id": str(item_id), "count": amount})

    result = payload.get("result")
    if isinstance(result, str):
        add(result, payload.get("count"))
    elif isinstance(result, dict):
        add(result.get("item") or result.get("id"), result.get("count"))

    for key in ("results", "outputs", "output"):
        value = payload.get(key)
        if isinstance(value, list):
            for entry in value:
                if isinstance(entry, dict):
                    add(entry.get("item") or entry.get("id"), entry.get("count") or entry.get("amount"))
                elif isinstance(entry, str):
                    add(entry)
        elif isinstance(value, dict):
            add(value.get("item") or value.get("id"), value.get("count") or value.get("amount"))
        elif isinstance(value, str):
            add(value)

    return outputs


def collect_recipe_refs(node: Any, item_refs: set[str], tag_refs: set[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in {"item", "content"} and is_item_id(value):
                item_refs.add(str(value))
            elif key in {"tag", "tagKey"} and isinstance(value, str):
                tag_refs.add(value.removeprefix("#"))
            elif key in {"items"}:
                if isinstance(value, str) and is_item_id(value):
                    item_refs.add(value)
                elif isinstance(value, list):
                    for item in value:
                        if is_item_id(item):
                            item_refs.add(str(item))
            else:
                collect_recipe_refs(value, item_refs, tag_refs)
    elif isinstance(node, list):
        for entry in node:
            collect_recipe_refs(entry, item_refs, tag_refs)


def ingredient_summary(payload: dict[str, Any], outputs: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    item_refs: set[str] = set()
    tag_refs: set[str] = set()
    collect_recipe_refs(payload, item_refs, tag_refs)
    for output in outputs:
        item_refs.discard(output["item_id"])
    return sorted(item_refs), sorted(tag_refs)


def iter_jar_recipes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not ACTIVE_MODS.exists():
        return rows
    for jar_path in sorted(ACTIVE_MODS.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar_path) as jar:
                for name in jar.namelist():
                    parts = name.split("/")
                    if len(parts) < 4 or parts[0] != "data" or parts[2] != "recipes" or not name.endswith(".json"):
                        continue
                    recipe_namespace = parts[1]
                    after = "/".join(parts[3:])[:-5]
                    recipe_id = f"{recipe_namespace}:{after}"
                    try:
                        payload = json.loads(jar.read(name).decode("utf-8-sig"))
                        invalid = None
                    except Exception as exc:  # noqa: BLE001
                        payload = {}
                        invalid = str(exc)
                    outputs = output_entries(payload) if isinstance(payload, dict) else []
                    ingredients, tags = ingredient_summary(payload, outputs) if isinstance(payload, dict) else ([], [])
                    rows.append(
                        {
                            "recipe_id": recipe_id,
                            "namespace": recipe_namespace,
                            "source_kind": "installed_mod_jar",
                            "source_file": f"{jar_path.name}!/{name}",
                            "jar": jar_path.name,
                            "payload": payload,
                            "recipe_type": payload.get("type") if isinstance(payload, dict) else None,
                            "outputs": outputs,
                            "ingredient_items": ingredients,
                            "ingredient_tags": tags,
                            "invalid_json": invalid,
                        }
                    )
        except zipfile.BadZipFile:
            continue
    return rows


def iter_repo_recipes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    roots = [
        ROOT / "config/openloader/data",
        ROOT / "openloader/data",
        ROOT / "datapacks",
        ROOT / "kubejs/data",
    ]
    seen: set[pathlib.Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.glob("**/data/*/recipes/**/*.json")):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            marker_positions = [
                i
                for i, part in enumerate(path.parts)
                if part == "data" and len(path.parts) > i + 2 and path.parts[i + 2] == "recipes"
            ]
            if not marker_positions:
                continue
            marker = marker_positions[-1]
            recipe_namespace = path.parts[marker + 1]
            after = "/".join(path.parts[marker + 3 :])[:-5]
            recipe_id = f"{recipe_namespace}:{after}"
            try:
                payload = read_json(path)
                invalid = None
            except Exception as exc:  # noqa: BLE001
                payload = {}
                invalid = str(exc)
            outputs = output_entries(payload) if isinstance(payload, dict) else []
            ingredients, tags = ingredient_summary(payload, outputs) if isinstance(payload, dict) else ([], [])
            rows.append(
                {
                    "recipe_id": recipe_id,
                    "namespace": recipe_namespace,
                    "source_kind": "repo_datapack_or_openloader",
                    "source_file": safe_rel(path),
                    "jar": "",
                    "payload": payload,
                    "recipe_type": payload.get("type") if isinstance(payload, dict) else None,
                    "outputs": outputs,
                    "ingredient_items": ingredients,
                    "ingredient_tags": tags,
                    "invalid_json": invalid,
                }
            )
    return rows


def infer_rarity(item_id: str, rarity_by_item: dict[str, str]) -> str:
    if item_id in rarity_by_item:
        return rarity_by_item[item_id]
    local = local_id(item_id).lower()
    if any(term in local for term in ("ascendant", "annihilator", "incinerator")):
        return "ascendant"
    if any(term in local for term in ("dragonsteel", "dragonbone", "mythic")):
        return "mythic"
    if any(term in local for term in ("legendary", "netherite", "totem", "boss", "sigil")):
        return "legendary"
    if any(term in local for term in ("diamond", "artifact", "relic", "arcane", "ancient")):
        return "epic"
    if any(term in local for term in ("gold", "ender", "rune", "scroll", "spell_book", "plate")):
        return "rare"
    if any(term in local for term in ("iron", "copper", "gear", "shaft", "cogwheel")):
        return "uncommon"
    return "common"


def output_domain(item_id: str, domains_by_item: dict[str, set[str]]) -> str:
    domains = domains_by_item.get(item_id, set())
    if any(domain in domains for domain in ("weapon", "weapons")):
        return "weapon"
    if any(domain in domains for domain in ("armor", "shield", "shields")):
        return "armor_or_shield"
    if any(domain in domains for domain in ("magic_item", "magic_items", "spell", "spells")):
        return "magic_or_spell"
    if any(domain in domains for domain in ("accessory_relic", "accessories_relics")):
        return "accessory_or_relic"
    ns = namespace(item_id)
    local = local_id(item_id).lower()
    if ns in {"farmersdelight", "alexsdelight", "sliceanddice"} or any(
        term in local for term in ("stew", "soup", "pie", "sandwich", "burger", "meal", "cake", "food")
    ):
        return "food_economy"
    if ns in {"create", "createbigcannons"} or any(
        term in local
        for term in (
            "cogwheel",
            "shaft",
            "andesite_alloy",
            "brass",
            "precision_mechanism",
            "mechanical",
            "deployer",
            "press",
            "belt",
        )
    ):
        return "create_component"
    if ns.startswith("sophisticated") or any(term in local for term in ("backpack", "storage", "upgrade", "shulker")):
        return "storage_qol"
    if is_material_like(item_id) or any(term in local for term in ("dragonbone", "dragonsteel", "arcane_ingot")):
        return "material"
    return "general"


def ingredient_max_rarity(ingredients: list[str], rarity_by_item: dict[str, str]) -> str:
    best = "common"
    for item_id in ingredients:
        rarity = infer_rarity(item_id, rarity_by_item)
        if RARITY_ORDER.get(rarity, 0) > RARITY_ORDER.get(best, 0):
            best = rarity
    return best


def vanilla_only_low_tier(ingredients: list[str], tags: list[str]) -> bool:
    if not ingredients and tags:
        return False
    if any(namespace(item_id) not in VANILLA_NAMESPACES for item_id in ingredients):
        return False
    if any(has_high_tier_term(item_id) for item_id in ingredients):
        return False
    if any(has_high_tier_term(tag) for tag in tags):
        return False
    return True


def canonical_conflicts(items: list[str], tags: list[str], materials: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    conflicts: list[dict[str, str]] = []
    for material_name, info in materials.items():
        canonical = str(info.get("canonical") or "")
        status = str(info.get("status") or "")
        if not canonical or status == "planned":
            continue
        for value in items:
            local = local_id(value).lower()
            if (
                value != canonical
                and namespace(value) != namespace(canonical)
                and material_name.lower() in local
                and is_direct_duplicate_material(value)
            ):
                conflicts.append(
                    {
                        "material": material_name,
                        "canonical_item": canonical,
                        "observed_reference": value,
                    }
                )
    return conflicts


def classify_recipe_status(
    output: str,
    rarity: str,
    domain: str,
    ingredients: list[str],
    tags: list[str],
    materials: dict[str, dict[str, Any]],
    rarity_by_item: dict[str, str],
) -> tuple[str, str, list[dict[str, str]], str | None]:
    conflicts = canonical_conflicts(ingredients + [output], tags, materials)
    ing_rarity = ingredient_max_rarity(ingredients, rarity_by_item)
    high_output = RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["legendary"]
    epic_output = RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["epic"]
    low_recipe = RARITY_ORDER.get(ing_rarity, 0) <= RARITY_ORDER["rare"] and not any(
        has_high_tier_term(value) for value in ingredients + tags
    )
    if high_output and vanilla_only_low_tier(ingredients, tags):
        return (
            "bypass",
            "High-rarity output is craftable from low-tier vanilla-only materials.",
            conflicts,
            "Add boss, dragon, structure, or Guild-rank proof materials; keep disabled until reviewed.",
        )
    if high_output and low_recipe:
        return (
            "too_cheap",
            "High-rarity output does not require enough high-tier ingredients.",
            conflicts,
            "Raise ingredients to match boss/dragon/rank tier or convert to loot-only progression.",
        )
    if conflicts:
        return (
            "duplicate",
            "Recipe references noncanonical or duplicate material families.",
            conflicts,
            "Prefer canonical material tags/items after Almost Unified review.",
        )
    if epic_output and domain in {"weapon", "armor_or_shield", "magic_or_spell", "accessory_or_relic"}:
        return (
            "needs_manual_review",
            "Progression-sensitive crafted gear or magic item.",
            conflicts,
            "Confirm JEI path matches Guild rank and Atlas ring before enabling changes.",
        )
    if domain == "storage_qol" and RARITY_ORDER.get(rarity, 0) >= RARITY_ORDER["rare"]:
        return (
            "needs_manual_review",
            "Storage/QoL item can affect exploration pacing.",
            conflicts,
            "Keep useful, but verify upgrade path does not skip loot pacing.",
        )
    if domain == "food_economy":
        return (
            "okay",
            "Food recipes stay generous unless combat balance is affected.",
            conflicts,
            None,
        )
    return ("okay", "Recipe fits current broad policy.", conflicts, None)


def compact_ingredients(items: list[str], tags: list[str], limit: int = 18) -> list[str]:
    values = items + [f"#{tag}" for tag in tags]
    return values[:limit] + ([f"+{len(values) - limit} more"] if len(values) > limit else [])


def build_recipe_entries(
    recipes: list[dict[str, Any]],
    rarity_by_item: dict[str, str],
    domains_by_item: dict[str, set[str]],
    mod_by_namespace: dict[str, str],
    materials: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    invalid_json = []
    by_status = Counter()
    by_domain = Counter()
    by_rarity = Counter()
    high_risk = []

    for recipe in recipes:
        if recipe.get("invalid_json"):
            invalid_json.append({"recipe_id": recipe["recipe_id"], "error": recipe["invalid_json"]})
        outputs = recipe.get("outputs", [])
        if not outputs:
            continue
        for output in outputs:
            output_id = output["item_id"]
            rarity = infer_rarity(output_id, rarity_by_item)
            policy = RARITY_POLICY.get(rarity, RARITY_POLICY["common"])
            domain = output_domain(output_id, domains_by_item)
            status, reason, conflicts, proposed = classify_recipe_status(
                output_id,
                rarity,
                domain,
                recipe["ingredient_items"],
                recipe["ingredient_tags"],
                materials,
                rarity_by_item,
            )
            entry = {
                "item_id": output_id,
                "recipe_id": recipe["recipe_id"],
                "source_mod": mod_by_namespace.get(recipe["namespace"], recipe["namespace"]),
                "source_namespace": recipe["namespace"],
                "source_kind": recipe["source_kind"],
                "source_file": recipe["source_file"],
                "recipe_type": recipe.get("recipe_type"),
                "current_ingredients": compact_ingredients(recipe["ingredient_items"], recipe["ingredient_tags"]),
                "ingredient_items": recipe["ingredient_items"],
                "ingredient_tags": recipe["ingredient_tags"],
                "output_count": output.get("count", 1),
                "gear_material_rarity": rarity,
                "output_domain": domain,
                "intended_guild_rank": policy["guild_rank"],
                "intended_atlas_distance_ring": policy["atlas_ring"],
                "intended_recipe_tier": policy["recipe_tier"],
                "material_tier": policy["material_tier"],
                "recipe_status": status,
                "reason": reason,
                "canonical_material_conflicts": conflicts,
                "material_tag_references": [
                    tag
                    for tag in recipe["ingredient_tags"]
                    if any(material_name.lower() in tag.lower() for material_name in materials)
                ],
                "proposed_replacement": proposed,
            }
            entries.append(entry)
            by_status[status] += 1
            by_domain[domain] += 1
            by_rarity[rarity] += 1
            if status in {"too_cheap", "bypass", "duplicate"}:
                high_risk.append(entry)
                candidates.append(
                    {
                        "candidate_id": f"candidate/{recipe['recipe_id'].replace(':', '/')}",
                        "recipe_id": recipe["recipe_id"],
                        "item_id": output_id,
                        "issue": status,
                        "current_ingredients": entry["current_ingredients"],
                        "proposed_replacement": proposed or "Manual review required before writing a replacement.",
                        "review_status": "unreviewed",
                        "enabled": False,
                    }
                )

    summary = {
        "total_recipe_outputs": len(entries),
        "by_status": dict(sorted(by_status.items())),
        "by_domain": dict(sorted(by_domain.items())),
        "by_rarity": dict(sorted(by_rarity.items())),
        "high_risk_count": len(high_risk),
        "invalid_json_count": len(invalid_json),
        "invalid_json": invalid_json[:100],
        "high_risk_examples": [
            {
                "recipe_id": entry["recipe_id"],
                "item_id": entry["item_id"],
                "status": entry["recipe_status"],
                "rarity": entry["gear_material_rarity"],
                "ingredients": entry["current_ingredients"],
            }
            for entry in high_risk[:100]
        ],
    }
    return entries, summary, candidates


def build_indexed_item_policy(
    gear_registry: dict[str, Any],
    recipe_entries: list[dict[str, Any]],
    rarity_by_item: dict[str, str],
    domains_by_item: dict[str, set[str]],
) -> tuple[list[dict[str, Any]], list[str]]:
    recipes_by_output: dict[str, list[str]] = defaultdict(list)
    for entry in recipe_entries:
        recipes_by_output[entry["item_id"]].append(entry["recipe_id"])

    indexed: list[dict[str, Any]] = []
    missing_policy: list[str] = []
    for collection in ("weapons", "armor", "shields", "magic_items", "spells", "accessories_relics"):
        for item in gear_registry.get(collection, []):
            item_id = str(item.get("id") or "")
            if not item_id:
                continue
            rarity = rarity_by_item.get(item_id, "common")
            policy = RARITY_POLICY.get(rarity, RARITY_POLICY["common"])
            recipes = sorted(set(recipes_by_output.get(item_id, [])))
            status = "crafting_policy_assigned" if recipes else "no_recipe_found_loot_or_drop_only"
            indexed.append(
                {
                    "item_id": item_id,
                    "name": item.get("name"),
                    "collection": collection,
                    "source_mod": item.get("source_mod"),
                    "rarity": rarity,
                    "domains": sorted(domains_by_item.get(item_id, [])),
                    "recipe_ids": recipes,
                    "recipe_policy_status": status,
                    "intended_guild_rank": policy["guild_rank"],
                    "intended_atlas_distance_ring": policy["atlas_ring"],
                    "intended_recipe_tier": policy["recipe_tier"],
                }
            )
            if not recipes and RARITY_ORDER.get(rarity, 0) <= RARITY_ORDER["rare"]:
                missing_policy.append(item_id)
    return indexed, missing_policy


def missing_item_references(recipe_entries: list[dict[str, Any]], known_items: set[str], active_namespaces: set[str]) -> list[dict[str, str]]:
    missing: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for entry in recipe_entries:
        for item_id in entry["ingredient_items"] + [entry["item_id"]]:
            if item_id in known_items:
                continue
            ns = namespace(item_id)
            if ns in active_namespaces:
                continue
            key = (entry["recipe_id"], item_id)
            if key in seen:
                continue
            seen.add(key)
            missing.append({"recipe_id": entry["recipe_id"], "item_id": item_id})
    return missing


def rarity_contradictions(recipe_entries: list[dict[str, Any]], rarity_by_item: dict[str, str]) -> list[dict[str, str]]:
    contradictions = []
    for entry in recipe_entries:
        item_id = entry["item_id"]
        registry_rarity = rarity_by_item.get(item_id)
        if registry_rarity and registry_rarity != entry["gear_material_rarity"]:
            contradictions.append(
                {
                    "recipe_id": entry["recipe_id"],
                    "item_id": item_id,
                    "recipe_rarity": entry["gear_material_rarity"],
                    "registry_rarity": registry_rarity,
                }
            )
    return contradictions


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    def cell(value: Any) -> str:
        text = str(value if value is not None else "")
        return text.replace("|", "\\|").replace("\n", " ")

    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)


def write_docs(policy: dict[str, Any], gates: dict[str, Any], high_risk: dict[str, Any], candidates: dict[str, Any]) -> None:
    summary = policy["summary"]
    audit_rows = []
    for entry in policy["major_recipe_entries"][:350]:
        audit_rows.append(
            [
                entry["item_id"],
                entry["recipe_id"],
                entry["source_mod"],
                entry["output_domain"],
                entry["gear_material_rarity"],
                entry["intended_guild_rank"],
                entry["recipe_status"],
            ]
        )

    write_text(
        DOCS_DIR / "RECIPE_PROGRESSION_AUDIT.md",
        f"""# Recipe Progression Audit

Generated: {policy['generated_at']}

This audit scans active installed jar recipes plus repo OpenLoader/datapack recipes. It assigns each major output a rarity, Guild rank, Atlas ring, recipe tier, and review status. No active recipe rewrites are enabled by this pass.

## Summary

{markdown_table(
            ['Metric', 'Count'],
            [
                ['Recipe outputs audited', summary['total_recipe_outputs']],
                ['Installed mod jar recipes', policy['scan_inputs']['installed_mod_jar_recipes']],
                ['Repo datapack/OpenLoader recipes', policy['scan_inputs']['repo_datapack_recipes']],
                ['High-risk recipes', summary['high_risk_count']],
                ['Candidate rewrites generated', len(candidates['candidates'])],
                ['Indexed gear/magic/relic policies', len(policy['indexed_item_policy'])],
            ],
        )}

## Status Counts

{markdown_table(['Status', 'Count'], [[k, v] for k, v in summary['by_status'].items()])}

## Domain Counts

{markdown_table(['Domain', 'Count'], [[k, v] for k, v in summary['by_domain'].items()])}

## Recipe Assignment Preview

Only the first 350 rows are shown here; the complete machine-readable audit is in `config/ascendant_recipes/recipe_progression_policy.json`.

{markdown_table(['Item ID', 'Recipe ID', 'Mod', 'Domain', 'Rarity', 'Guild Rank', 'Status'], audit_rows)}
""",
    )

    write_text(
        DOCS_DIR / "CRAFTING_GATE_PLAN.md",
        f"""# Crafting Gate Plan

Generated: {policy['generated_at']}

This is a planning scaffold only. It does not enable hard gates yet.

## Gate Ladder

{markdown_table(
            ['Rarity', 'Guild Rank', 'Atlas Ring', 'Recipe Tier', 'Material Tier'],
            [
                [rarity, data['guild_rank'], data['atlas_ring'], data['recipe_tier'], data['material_tier']]
                for rarity, data in gates['rarity_gate_ladder'].items()
            ],
        )}

## Rules

- Legendary, mythic, and ascendant gear cannot be craftable from basic vanilla-only materials.
- High-tier magic should require high-tier materials, boss drops, structures, or rank progression.
- Duplicate material recipes should prefer canonical materials from `config/ascendant_core/materials.json`.
- Endgame weapons should not be craftable before their loot/danger tier.
- Storage and QoL remain useful, but high-tier upgrades need review if they trivialize exploration pacing.
- Food recipes stay generous unless they directly break combat balance.

## Live Enforcement

No hard gates are enabled. Candidate rewrites are generated under `kubejs/server_scripts_disabled/review/ascendant_recipes/` and in `config/ascendant_recipes/candidate_recipe_rewrites.json`.
""",
    )

    high_rows = []
    for entry in high_risk["entries"][:200]:
        high_rows.append(
            [
                entry["item_id"],
                entry["recipe_id"],
                entry["recipe_status"],
                entry["gear_material_rarity"],
                ", ".join(entry["current_ingredients"][:8]),
                entry.get("proposed_replacement") or "manual review",
            ]
        )
    write_text(
        DOCS_DIR / "BROKEN_OR_EASY_RECIPE_REPORT.md",
        f"""# Broken Or Easy Recipe Report

Generated: {policy['generated_at']}

This report lists recipe outputs that appear too cheap, bypass progression, or use duplicate/noncanonical materials. It is evidence for future manual rewrites, not an enabled change list.

## Summary

{markdown_table(
            ['Metric', 'Count'],
            [
                ['High-risk recipes', high_risk['summary']['high_risk_count']],
                ['Too cheap', high_risk['summary']['by_status'].get('too_cheap', 0)],
                ['Bypass', high_risk['summary']['by_status'].get('bypass', 0)],
                ['Duplicate/noncanonical material', high_risk['summary']['by_status'].get('duplicate', 0)],
                ['Malformed recipe JSON', high_risk['summary']['invalid_json_count']],
            ],
        )}

## High-Risk Recipes

{markdown_table(['Item ID', 'Recipe ID', 'Issue', 'Rarity', 'Current Ingredients', 'Proposed Replacement'], high_rows)}
""",
    )


def update_docs_index() -> None:
    path = DOCS_DIR / "DOCS_INDEX.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    additions = [
        "- [RECIPE_PROGRESSION_AUDIT.md](RECIPE_PROGRESSION_AUDIT.md) - Generated recipe progression audit summary.",
        "- [CRAFTING_GATE_PLAN.md](CRAFTING_GATE_PLAN.md) - Authoritative candidate crafting gate plan.",
        "- [BROKEN_OR_EASY_RECIPE_REPORT.md](BROKEN_OR_EASY_RECIPE_REPORT.md) - Generated high-risk recipe report.",
    ]
    missing = [line for line in additions if line not in text]
    if not missing:
        return
    marker = "## Generated Or Registry-Like Docs"
    if marker in text:
        text = text.replace(marker, marker + "\n\n" + "\n".join(missing), 1)
    else:
        text += "\n\n## Recipe Economy Docs\n\n" + "\n".join(missing) + "\n"
    path.write_text(text, encoding="utf-8")


def update_current_status(summary: dict[str, Any]) -> None:
    path = DOCS_DIR / "CURRENT_STATUS.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    block = f"""## Recipe Progression Control Scaffold

- Status: generated audit/candidate scaffold only; no hard crafting gates or broad recipe rewrites are enabled.
- Recipe outputs audited: {summary['total_recipe_outputs']}.
- High-risk recipes: {summary['high_risk_count']}.
- Malformed recipe JSON: {summary['invalid_json_count']}.
- Authoritative docs/configs: `docs/RECIPE_PROGRESSION_AUDIT.md`, `docs/CRAFTING_GATE_PLAN.md`, `docs/BROKEN_OR_EASY_RECIPE_REPORT.md`, and `config/ascendant_recipes/*.json`.
- Candidate rewrites live only in disabled review paths until explicitly approved.
"""
    heading = "## Recipe Progression Control Scaffold"
    if heading in text:
        start = text.index(heading)
        next_heading = text.find("\n## ", start + 1)
        if next_heading == -1:
            text = text[:start].rstrip() + "\n\n" + block
        else:
            text = text[:start].rstrip() + "\n\n" + block + "\n" + text[next_heading + 1 :].lstrip()
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_disabled_candidates(candidates: dict[str, Any]) -> None:
    lines = [
        "// Ascendant recipe rewrite candidates.",
        "// Disabled review artifact only. Do not rename to .js or move into active server_scripts without approval.",
        "//",
    ]
    for candidate in candidates["candidates"][:80]:
        lines.append(f"// {candidate['issue']}: {candidate['recipe_id']} -> {candidate['item_id']}")
        lines.append(f"// Current: {', '.join(candidate.get('current_ingredients', []))}")
        lines.append(f"// Proposed: {candidate.get('proposed_replacement')}")
        lines.append("// event.remove({ id: '" + candidate["recipe_id"] + "' })")
        lines.append("")
    write_text(DISABLED_REVIEW_DIR / "candidate_recipe_rewrites.js.txt", "\n".join(lines))
    write_text(
        DISABLED_REVIEW_DIR / "README.md",
        f"""# Ascendant Recipe Rewrite Candidates

This folder is intentionally disabled. Minecraft and KubeJS should ignore it.

Candidate count: {len(candidates['candidates'])}

Do not enable these candidates as a batch. Review recipe-by-recipe after terrain and loot signoff.
""",
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = now_iso()
    gear_registry, rarity_by_item, domains_by_item, mod_by_namespace = load_registries()
    materials = canonical_materials()
    jar_known_items, active_namespaces = collect_known_items_from_jars()
    known_items = set(jar_known_items) | set(rarity_by_item) | parse_kubejs_items()

    jar_recipes = iter_jar_recipes()
    repo_recipes = iter_repo_recipes()
    recipes = jar_recipes + repo_recipes
    for recipe in recipes:
        for output in recipe.get("outputs", []):
            known_items.add(output["item_id"])
        known_items.update(recipe.get("ingredient_items", []))

    recipe_entries, summary, candidates_list = build_recipe_entries(
        recipes,
        rarity_by_item,
        domains_by_item,
        mod_by_namespace,
        materials,
    )
    indexed_policy, low_rarity_no_recipe_policy = build_indexed_item_policy(
        gear_registry,
        recipe_entries,
        rarity_by_item,
        domains_by_item,
    )
    missing_refs = missing_item_references(recipe_entries, known_items, active_namespaces)
    contradictions = rarity_contradictions(recipe_entries, rarity_by_item)

    high_risk_entries = [
        entry for entry in recipe_entries if entry["recipe_status"] in {"too_cheap", "bypass", "duplicate"}
    ]
    high_risk = {
        "version": 1,
        "generated_at": generated_at,
        "summary": {
            "high_risk_count": len(high_risk_entries),
            "by_status": dict(sorted(Counter(entry["recipe_status"] for entry in high_risk_entries).items())),
            "invalid_json_count": summary["invalid_json_count"],
        },
        "entries": high_risk_entries,
    }

    gates = {
        "version": 1,
        "generated_at": generated_at,
        "status": "candidate_plan_only_no_hard_gates_enabled",
        "rarity_gate_ladder": RARITY_POLICY,
        "rules": [
            "Legendary/mythic/ascendant gear cannot be craftable from basic vanilla-only materials.",
            "High-tier magic requires high-tier materials, boss drops, structures, or rank progression.",
            "Duplicate material recipes should use Ascendant canonical materials after Almost Unified review.",
            "Endgame weapons should not be craftable before their corresponding loot/danger tier.",
            "Storage/QoL should remain useful but not trivialize exploration and loot pacing.",
            "Food recipes can remain generous unless they break combat balance or progression.",
        ],
    }

    candidates = {
        "version": 1,
        "generated_at": generated_at,
        "status": "disabled_review_only",
        "enabled_candidates": 0,
        "candidates": candidates_list,
    }

    policy = {
        "version": 1,
        "generated_at": generated_at,
        "status": "audit_and_candidate_scaffold_only",
        "no_enabled_rewrites": True,
        "scan_inputs": {
            "active_instance_mods": str(ACTIVE_MODS),
            "installed_mod_jars": len(list(ACTIVE_MODS.glob("*.jar"))) if ACTIVE_MODS.exists() else 0,
            "installed_mod_jar_recipes": len(jar_recipes),
            "repo_datapack_recipes": len(repo_recipes),
        },
        "source_registries": {
            "gear": "config/ascendant_index/gear_registry.json",
            "materials": "config/ascendant_core/materials.json",
            "recipe_policy": "config/ascendant_core/recipe_policy.json",
            "loot_economy": "config/ascendant_loot/loot_policy.json",
        },
        "canonical_materials": materials,
        "rules": gates["rules"],
        "major_recipe_entries": recipe_entries,
        "indexed_item_policy": indexed_policy,
        "validation": {
            "high_rarity_low_tier_recipes": [
                entry for entry in high_risk_entries if entry["recipe_status"] in {"too_cheap", "bypass"}
            ][:200],
            "noncanonical_duplicate_material_recipes": [
                entry for entry in high_risk_entries if entry["recipe_status"] == "duplicate"
            ][:200],
            "indexed_items_without_recipe_policy": [],
            "low_rarity_indexed_items_without_recipe": low_rarity_no_recipe_policy[:200],
            "missing_item_references": missing_refs[:200],
            "rarity_contradictions": contradictions[:200],
            "unreviewed_rewrite_candidates": [
                candidate for candidate in candidates_list if candidate.get("review_status") != "reviewed"
            ][:200],
        },
        "known_item_ids": sorted(known_items),
        "summary": summary,
    }

    write_json(OUT_DIR / "recipe_progression_policy.json", policy)
    write_json(OUT_DIR / "crafting_gate_registry.json", gates)
    write_json(OUT_DIR / "high_risk_recipes.json", high_risk)
    write_json(OUT_DIR / "candidate_recipe_rewrites.json", candidates)
    write_docs(policy, gates, high_risk, candidates)
    update_docs_index()
    update_current_status(summary)
    write_disabled_candidates(candidates)

    print("Generated Ascendant recipe progression scaffold.")
    print(f"Recipe outputs audited: {summary['total_recipe_outputs']}")
    print(f"High-risk recipes: {summary['high_risk_count']}")
    print(f"Candidate rewrites: {len(candidates_list)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
