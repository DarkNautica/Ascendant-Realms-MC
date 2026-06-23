#!/usr/bin/env python3
"""Generate an AI-facing Ascendant Realms modpack handoff document."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import tomllib


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "AI_MODPACK_HANDOFF.md"


CATEGORY_NOTES = {
    "Audio / Atmosphere": "Feeds biome mood, storm feel, footsteps, sound reverb, ambient music, leaves, particles, and sky/weather presentation.",
    "Cohesion / Recipes / Tags": "Glue layer for recipes, wood sets, tags, material compatibility, structure palette cohesion, and pack-owned data overrides.",
    "Combat / Gear": "Feeds the RPG combat loop, rarity labels, loot tiers, skill synergies, and boss/contract rewards.",
    "Dependency / Library": "Required API/runtime support. Usually do not tune directly, but side and version compatibility matter.",
    "Loot / Contracts": "Feeds Bountiful, loot tables, guide books, bounty objectives, and reward visibility.",
    "Magic": "Feeds spell progression, magical loot, skill hooks, boss rewards, and class fantasy.",
    "Mobs / Bosses": "Adds hostile/passive entity pressure, boss goals, structure inhabitants, drops, and bounty targets.",
    "Performance": "Keeps the large mod stack playable. Treat as infrastructure and verify after shader/UI/worldgen changes.",
    "Resource Pack": "Visual cohesion layer. Order matters because several packs intentionally override mod textures/models.",
    "Shader / Visual Base": "Client visual base: shaders, model features, animation support, particles, and rendering compatibility.",
    "Skills / Difficulty": "Owns player growth, level pressure, difficulty scaling, attributes, and future rank gates.",
    "Storage / QoL": "Convenience features that should not control balance unless linked to loot/progression.",
    "UI / Presentation": "Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity.",
    "Villages / NPCs": "Owns village population, medieval NPC presentation, Guild staff, guards, rivals, companions, and settlement safety.",
    "Worldgen / Structures": "Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces.",
    "Custom / Local": "Pack-owned code/data. This is the highest-priority layer to inspect before changing worldgen or runtime behavior.",
}


SPECIFIC_NOTES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"ascendant-atlas-regions", re.I), "Pack-owned Forge helper. Registers the active coordinate-aware Overworld biome source and must stay aligned with Atlas JSON and OpenLoader dimension overrides."),
    (re.compile(r"terralith", re.I), "Primary biome table provider for Atlas worldgen. Do not classify its biomes by name alone; inspect biome JSON and Terralith climate entries."),
    (re.compile(r"tectonic", re.I), "Terrain/noise shape layer. Atlas controls biome source while Tectonic-style terrain shape must remain intact."),
    (re.compile(r"open.?loader", re.I), "Datapack loader for pack-owned tags, dimension overrides, structures, loot, functions, and integration repairs."),
    (re.compile(r"kubejs", re.I), "Runtime/data glue for Ascendant Core, Atlas status, progression HUD, recipes, tags, JEI aliases, and tooltips."),
    (re.compile(r"in.?control", re.I), "Spawn guardrail layer using Atlas coordinate areas and settlement safety caps."),
    (re.compile(r"sparse.?structures", re.I), "Global structure-spacing pressure valve. Use alongside per-structure-set overrides, not as the only density fix."),
    (re.compile(r"integrated.?villages", re.I), "Village expansion layer with known processor/tag repairs in the world-integration datapack."),
    (re.compile(r"idas|integrated dungeons", re.I), "Large dungeon/structure source. Check biome tags, loot, and density before moving structures."),
    (re.compile(r"towns.?and.?towers", re.I), "Major village/outpost structure provider. Interacts heavily with Integrated Villages, MCA, roads, and Guild settlement tuning."),
    (re.compile(r"moog|mvs|mss|mes", re.I), "Moog structure family. High structure volume; tune density and biome fit before adding more structure mods."),
    (re.compile(r"yung", re.I), "Dungeon/bridge/stronghold/mineshaft/extras overhaul family. Good content, but bridge/road/river seams need field validation."),
    (re.compile(r"structory", re.I), "Ambient structure layer; tune for density and biome identity rather than blanket disabling."),
    (re.compile(r"create.?structures", re.I), "Create-themed structure layer; check loot and mechanical block palette fit with world regions."),
    (re.compile(r"ice.?and.?fire|iceandfire", re.I), "Dragon/mythic ecology plus structures, loot, armor, and ores. Needs boss/biome/rank tuning."),
    (re.compile(r"cataclysm", re.I), "Major boss/dungeon layer. Treat as late-game content and wire rewards to rank/progression."),
    (re.compile(r"mowzie", re.I), "Boss/mob layer with structures. Good for bounty targets and regional danger spikes."),
    (re.compile(r"born.?in.?chaos", re.I), "High-pressure hostile ecology. Interacts with In Control caps, villages, and early-game safety."),
    (re.compile(r"aquamirae", re.I), "Ocean/frozen-ocean structure and mob layer. Surface structure set is overridden to reduce dense spawn clusters."),
    (re.compile(r"alex.?s.?mobs", re.I), "Animal/monster ecology. Spawns are part of regional feel and bounty candidate pool."),
    (re.compile(r"scaling.?health|majrusz|improved.?mobs|spawn.?balance", re.I), "Difficulty/spawn-pressure modifier. Must be balanced against early villages, Guild ranks, and In Control caps."),
    (re.compile(r"better.?combat", re.I), "Core combat animation/hit system. Weapon balance, animation packs, and shields must be tested through it."),
    (re.compile(r"combat.?roll", re.I), "Player mobility layer. Changes encounter difficulty and boss readability."),
    (re.compile(r"simply.?swords|marium|soulslike", re.I), "High-value weapon pool. Indexed for rarity, loot tiers, JEI aliases, and skill hooks."),
    (re.compile(r"spartan.?shields|immersive.?armors|fantasy.?armor", re.I), "Armor/shield pool. Indexed for rarity and NPC/loot identity."),
    (re.compile(r"artifacts|curios", re.I), "Accessory/relic layer. Curios is infrastructure; Artifacts feeds loot, rarity, and build identity."),
    (re.compile(r"iron.?s.?spells|irons", re.I), "Magic progression and spell loot. Needs skill tree hooks, rank gates, and boss/structure rewards."),
    (re.compile(r"puffish|attributes", re.I), "Skill/attribute foundation. Ascendant Web and HUD bridge depend on it."),
    (re.compile(r"bountiful", re.I), "Bounty/contract system. Receives generated Guild objectives and reward pools."),
    (re.compile(r"patchouli", re.I), "Ascendant Codex guidebook surface through OpenLoader data."),
    (re.compile(r"ftb", re.I), "Quest/rank/team infrastructure for future formal rank trials and Guild progression."),
    (re.compile(r"minecraft.?comes.?alive|mca", re.I), "Village NPC identity layer. Medieval clothing/resource pack is required for tone."),
    (re.compile(r"easy.?npc|customnpcs|human.?companions|guard.?villagers|villager.?names", re.I), "NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety."),
    (re.compile(r"create(?!.*structures)|farmer.?s.?delight|alex.?s.?delight|slice.?and.?dice", re.I), "Crafting/food/mechanical economy. Recipe/tag unification and reward pacing matter."),
    (re.compile(r"almost.?unif|every.?compat|polymorph|quark|supplementaries|zeta", re.I), "Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs."),
    (re.compile(r"macaw", re.I), "Decorative/building palette. Bridges are especially relevant to future Atlas road/river seam fixes."),
    (re.compile(r"weather|serene.?seasons|snow.?real", re.I), "Weather/season/snow behavior. Atlas guards prevent warm-region snow and keep Frostmarch identity regional."),
    (re.compile(r"enhanced.?celestials", re.I), "Event/moon pressure layer; can affect mob danger and atmosphere."),
    (re.compile(r"aurora|ambient|sound.?physics|falling.?leaves|biome.?music|particular|subtle", re.I), "Atmosphere layer tied to biome feel, weather, and shader/performance testing."),
    (re.compile(r"embeddium|oculus|modernfix|ferrite|entity.?culling|dynamic.?lights", re.I), "Client/performance/rendering stack. Verify after shaders, particles, animations, or large worldgen changes."),
    (re.compile(r"resource.?pack.?overrides", re.I), "Forces resource-pack order so visual fallbacks and UI packs load reliably."),
    (re.compile(r"fancy.?menu|drippy", re.I), "Main-menu/loading presentation. Depends on packaged assets and resource-pack order."),
    (re.compile(r"traveler|titles", re.I), "Biome/dimension title presentation and region flavor."),
    (re.compile(r"item.?borders|legendary.?tooltips|mob.?health|overflowing|stylish|loot.?beam|loot.?journal|jei|xaero", re.I), "Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback."),
    (re.compile(r"fresh.?animations|entity.?model|entity.?texture|3d.?skin|visual.?workbench|enchanted.?books|icon|stoneborn|vanilla experience|excalibur|cubic", re.I), "Visual resource/model polish. Order and client-only side metadata matter."),
    (re.compile(r"sophisticated", re.I), "Storage QoL. Make sure storage access does not trivialize intended loot pacing."),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def source_from_toml(data: dict) -> str:
    update = data.get("update", {})
    if isinstance(update, dict):
        if "modrinth" in update:
            return "Modrinth"
        if "curseforge" in update:
            return "CurseForge"
    download = data.get("download", {})
    if isinstance(download, dict) and download.get("url"):
        return "Direct URL"
    return "Local/unknown"


def parse_universal_index() -> dict[str, dict[str, str]]:
    path = ROOT / "docs" / "UNIVERSAL_MOD_INDEX.md"
    if not path.exists():
        return {}
    rows: dict[str, dict[str, str]] = {}
    for line in read_text(path).splitlines():
        if not line.startswith("| ") or "`" not in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8 or cells[0] == "Name" or cells[0].startswith("---"):
            continue
        name, kind, category, side, source, rarity, target, metadata = cells[:8]
        metadata_path = metadata.strip("`")
        rows[metadata_path] = {
            "name": name,
            "kind": kind,
            "category": category,
            "side": side,
            "source": source,
            "rarity": rarity,
            "target": target,
        }
    return rows


def fallback_category(name: str, rel: str) -> str:
    value = f"{name} {rel}".lower()
    rules = [
        ("Villages / NPCs", ["mca", "minecraft-comes-alive", "easy npc", "customnpcs", "human companions", "guard villager", "villager names"]),
        ("Worldgen / Structures", ["terralith", "tectonic", "yung", "struct", "village", "idas", "moog", "dungeon", "tower", "ship", "bridge", "aquamirae"]),
        ("Mobs / Bosses", ["mobs", "boss", "cataclysm", "chaos", "mowzie", "dragon", "iceandfire", "alex"]),
        ("Combat / Gear", ["combat", "sword", "weapon", "shield", "armor", "projectile", "artifact"]),
        ("Magic", ["spell", "magic", "irons"]),
        ("Skills / Difficulty", ["skill", "difficulty", "health", "attribute", "improved"]),
        ("UI / Presentation", ["menu", "hud", "tooltip", "title", "minimap", "healthbar", "jei", "border", "plaque", "loading"]),
        ("Audio / Atmosphere", ["sound", "music", "weather", "season", "celestial", "aurora", "leaves", "snow", "ambient", "particle", "subtle"]),
        ("Shader / Visual Base", ["shader", "oculus", "embeddium", "animation", "texture", "model", "visual", "skin", "cubic", "icon", "stoneborn", "fresh"]),
        ("Performance", ["modernfix", "ferrite", "culling", "sodium", "dynamic"]),
        ("Cohesion / Recipes / Tags", ["create", "delight", "quark", "supplement", "macaw", "unify", "compat", "polymorph", "kubejs", "open-loader"]),
        ("Loot / Contracts", ["bountiful", "loot", "patchouli", "quest", "rank", "ftb"]),
        ("Storage / QoL", ["backpack", "storage", "appleskin"]),
        ("UI / Presentation", ["boss bar", "spiffyhud", "stylish", "item border", "overflowing", "healthbar", "jei", "tooltip", "resource pack overrides"]),
        ("Dependency / Library", ["api", "lib", "core", "cloth", "kotlin", "rhino", "gecko", "architectury", "citadel", "cupboard", "resourceful", "moonlight", "zeta", "iceberg", "collective", "watermedia"]),
    ]
    for category, tokens in rules:
        if any(token in value for token in tokens):
            return category
    if rel.startswith("resourcepacks/"):
        return "Resource Pack"
    if rel.startswith("shaderpacks/"):
        return "Shader / Visual Base"
    return "Mod"


def clean_name(name: str) -> str:
    cleaned = (
        name.replace("âœ¨", "")
        .replace("â›„", "")
        .replace("🥝", "")
        .replace("✨", "")
        .replace("⛄", "")
        .strip()
    )
    return re.sub(r"\s+", " ", cleaned)


def interaction_note(name: str, rel: str, category: str) -> str:
    value = f"{name} {rel}"
    matches: list[str] = []
    for pattern, note in SPECIFIC_NOTES:
        if pattern.search(value):
            matches.append(note)
    if matches:
        return " ".join(dict.fromkeys(matches))
    return CATEGORY_NOTES.get(category, "Installed pack entry; inspect its config/data surfaces before changing balance.")


def load_pack_entries(universal: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for folder in ["mods", "resourcepacks", "shaderpacks"]:
        for path in sorted((ROOT / folder).glob("*.pw.toml")):
            rel = path.relative_to(ROOT).as_posix()
            data = tomllib.loads(read_text(path))
            indexed = universal.get(rel, {})
            name = clean_name(str(data.get("name") or indexed.get("name") or path.stem))
            fallback = fallback_category(name, rel)
            indexed_category = indexed.get("category")
            category = fallback if not indexed_category or indexed_category == "Mod" else indexed_category
            kind = indexed.get("kind") or ("Resource Pack" if folder == "resourcepacks" else "Shader Pack" if folder == "shaderpacks" else "Mod")
            side = str(data.get("side") or indexed.get("side") or "unknown")
            source = indexed.get("source") or source_from_toml(data)
            entries.append(
                {
                    "name": name,
                    "kind": kind,
                    "category": category,
                    "side": side,
                    "source": source,
                    "filename": str(data.get("filename") or ""),
                    "metadata": rel,
                    "role": interaction_note(name, rel, category),
                }
            )

    helper = ROOT / "mods" / "ascendant-atlas-regions-0.1.0.jar"
    if helper.exists():
        entries.append(
            {
                "name": "Ascendant Atlas Regions",
                "kind": "Local Forge helper mod",
                "category": "Custom / Local",
                "side": "both",
                "source": "Local source",
                "filename": helper.name,
                "metadata": "mods/ascendant-atlas-regions-0.1.0.jar",
                "role": interaction_note("ascendant-atlas-regions", "mods/ascendant-atlas-regions-0.1.0.jar", "Custom / Local"),
            }
        )
    return entries


def registry_counts() -> dict[str, str]:
    counts: dict[str, str] = {}
    paths = {
        "indexed_mobs": ROOT / "config" / "ascendant_index" / "mob_registry.json",
        "indexed_structures": ROOT / "config" / "ascendant_index" / "structure_registry.json",
        "gear_registry": ROOT / "config" / "ascendant_index" / "gear_registry.json",
        "spawn_groups": ROOT / "config" / "ascendant_index" / "spawn_tuning_worklist.json",
        "worldgen_audit": ROOT / "docs" / "generated" / "worldgen_content_audit.json",
    }
    for key, path in paths.items():
        if not path.exists():
            continue
        data = json.loads(read_text(path))
        if key == "indexed_mobs":
            counts[key] = str(len(data.get("mobs", [])))
        elif key == "indexed_structures":
            counts[key] = str(len(data.get("structures", [])))
        elif key == "gear_registry":
            pieces = []
            for field in ["weapons", "armor", "shields", "magic_items", "spells", "accessories_relics"]:
                pieces.append(f"{field}={len(data.get(field, []))}")
            counts[key] = ", ".join(pieces)
        elif key == "spawn_groups":
            counts[key] = str(len(data.get("spawn_groups", [])))
        elif key == "worldgen_audit":
            raw = data.get("counts", {})
            counts[key] = ", ".join(f"{name}={raw.get(name)}" for name in ["biomes", "structures", "structure_sets", "templates", "mobs_with_json_spawn_evidence"])
    return counts


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def build_doc(entries: list[dict[str, str]]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    by_category: dict[str, list[dict[str, str]]] = defaultdict(list)
    for entry in sorted(entries, key=lambda row: (row["category"], row["name"].casefold(), row["metadata"])):
        by_category[entry["category"]].append(entry)
    category_counts = Counter(entry["category"] for entry in entries)
    side_counts = Counter(entry["side"] for entry in entries)
    kind_counts = Counter(entry["kind"] for entry in entries)
    counts = registry_counts()

    lines: list[str] = []
    lines.extend(
        [
            "# AI Modpack Handoff",
            "",
            f"Generated: {generated}",
            "",
            "Purpose: give another AI enough context to inspect or continue Ascendant Realms without rediscovering the modpack from scratch.",
            "",
            "## Pack Facts",
            "",
            "- Pack: Ascendant Realms `0.1.0-alpha`.",
            "- Minecraft: `1.20.1`; Forge: `47.4.20`; Java target: `17`.",
            "- Pack manager: Packwiz `pack-format = \"packwiz:1.1.0\"`.",
            "- Active test instance path used in recent work: `C:\\Users\\Jayden\\curseforge\\minecraft\\Instances\\Ascendant Realms (2)`.",
            "- Do not treat `dist/server-pack-staging/` as source. It is generated export output.",
            f"- Pack entries in this handoff: {len(entries)} total.",
            f"- Kind counts: {', '.join(f'{k}={v}' for k, v in sorted(kind_counts.items()))}.",
            f"- Side counts: {', '.join(f'{k}={v}' for k, v in sorted(side_counts.items()))}.",
            "",
            "## Registry Snapshot",
            "",
        ]
    )
    if counts:
        for key, value in counts.items():
            lines.append(f"- `{key}`: {value}.")
    else:
        lines.append("- Registry counts unavailable; regenerate the Ascendant indexes before major balance work.")

    lines.extend(
        [
            "",
            "## First-Read Source Order For Another AI",
            "",
            "1. `docs/CURRENT_STATUS.md` for the newest live state, latest fixes, and retest checklist.",
            "2. `docs/DOCS_INDEX.md` for which docs are authoritative versus generated or historical.",
            "3. `docs/ASCENDANT_ATLAS_WORLDGEN.md` before touching biomes, regions, snow, structures, roads, or finite-world rules.",
            "4. `docs/SYSTEM_ECOSYSTEM_OVERVIEW.md` for the broad layer map.",
            "5. `docs/WORLDGEN_CONTENT_AUDIT.md` and `docs/generated/worldgen_content_audit.json` before classifying biomes or structures.",
            "6. `config/ascendant_index/*.json` for machine-readable mobs, structures, gear, spawn worklists, and integration thresholds.",
            "",
            "## Core Architecture",
            "",
            "- Ascendant Core is the pack-owned contract layer under `config/ascendant_core/`; KubeJS reads it and mirrors shared state into scoreboards.",
            "- Ascendant Atlas is the region/worldgen layer under `config/ascendant_atlas/`; the local `ascendant_atlas_regions` helper jar owns the active regional biome source.",
            "- OpenLoader carries datapack overrides, tags, functions, structure repairs, Guild structures, Codex data, and the Overworld dimension override.",
            "- KubeJS carries runtime glue, tooltip/JEI polish, recipe/tag glue, rank/proof mirroring, and Atlas/progression bridge behavior.",
            "- In Control applies coordinate-area spawn guardrails; it should follow Atlas regions instead of fighting them.",
            "- Resource Pack Overrides controls visual pack order; do not assume a resource pack is active just because its file exists.",
            "",
            "## Critical Interaction Hotspots",
            "",
            "| Hotspot | Main Mods/Data | What Another AI Must Know |",
            "|---|---|---|",
            "| Atlas worldgen | `ascendant_atlas_regions`, Terralith, Tectonic, OpenLoader, KubeJS, In Control | Atlas chooses regional biome tables and biases climate; Tectonic-style terrain shape must remain. Do not pick biomes by name only. Use the audit JSON and live chunk evidence. |",
            "| Warm-region snow | Weather2, Snow Real Magic, Serene Seasons, Terralith, Atlas configs | Recent bug: `terralith:gravel_desert` looked like a desert but had temperature `0.14` and accepted snow. Source configs now block snow buildup outside cold biomes and disable global seasonal snow/ice conversion. |",
            "| Structure density | Sparse Structures, YUNG suite, IDAS, Integrated Villages, Towns and Towers, Structory, Moog structures, Aquamirae, Guild structures | The pack has enough structure volume. Tune density, spacing, biome fit, and loot before adding more structure mods. Aquamirae surface set is overridden wider. |",
            "| Villages/NPCs | MCA Reborn, MCA Default Medieval, Easy NPC, CustomNPCs, Human Companions, Guard Villagers, Villager Names, Bountiful, Patchouli, FTB | The goal is a Guild/Hunter RPG spine. NPC visuals, guards, rivals, boards, and contracts must feel medieval/fantasy and survive hostile pressure. |",
            "| Spawn pressure | In Control, Spawn Balance Utility, Scaling Health, Majrusz, Improved Mobs, Born in Chaos, Alex's Mobs, IceAndFire, Cataclysm, Mowzie, Aquamirae | Danger mods stay installed; tune pressure using regional caps and spawn groups rather than removing content first. Settlement safety is a known concern. |",
            "| Combat/progression | Better Combat, Combat Roll, Simply Swords, Marium, Spartan Shields, Immersive/Fantasy Armor, Artifacts, Iron's Spells, Puffish Skills/Attributes | Gear and skills are indexed for rarity and future rank gates. Balance reward pacing with combat feel and mobility. |",
            "| Recipes/materials | Create, Farmer's Delight, Alex's Delight, Slice & Dice, Every Compat, Almost Unified, Quark, Supplementaries, Macaw family, Polymorph | This is the material and recipe cohesion layer. Avoid adding recipes that bypass intended rank/loot progression. |",
            "| UI clarity | Item Borders, Legendary Tooltips, JEI, Loot Beams, Loot Journal, Health Bar Plus, Overflowing Bars, Traveler's Titles, FancyMenu, Drippy | UI should tell the RPG story: rarity, levels, biomes, loot feedback, and title/menu polish. Test visual overlap after changes. |",
            "| Rendering/performance | Embeddium, Oculus, ModernFix, FerriteCore, Entity Culling, Sodium Dynamic Lights, EMF/ETF, Fresh Animations, shaders/resource packs | Large worldgen/content stack depends on this staying stable. Run client launch and visual checks after shader/resource changes. |",
            "",
            "## Category Counts",
            "",
            "| Category | Count | Role |",
            "|---|---:|---|",
        ]
    )
    for category, count in sorted(category_counts.items()):
        lines.append(f"| {md_escape(category)} | {count} | {md_escape(CATEGORY_NOTES.get(category, 'Installed pack layer.'))} |")

    lines.extend(
        [
            "",
            "## Complete Pack Entry Breakdown",
            "",
            "This table is generated from root Packwiz metadata plus the local Atlas helper jar. `Role / interaction` is intentionally practical: it tells the next AI what each entry touches in this pack.",
            "",
        ]
    )
    for category in sorted(by_category):
        lines.extend(
            [
                f"### {category}",
                "",
                "| Entry | Side | Source | File | Role / interaction |",
                "|---|---|---|---|---|",
            ]
        )
        for entry in by_category[category]:
            file_label = entry["filename"] or entry["metadata"]
            lines.append(
                "| "
                + " | ".join(
                    [
                        md_escape(entry["name"]),
                        md_escape(entry["side"]),
                        md_escape(entry["source"]),
                        f"`{md_escape(file_label)}`",
                        md_escape(entry["role"]),
                    ]
                )
                + " |"
            )
        lines.append("")

    lines.extend(
        [
            "## Operational Rules For The Next AI",
            "",
            "- Before changing worldgen, regenerate or inspect `docs/WORLDGEN_CONTENT_AUDIT.md`; biome names are not reliable enough.",
            "- Before changing structures, inspect structure sets, template pools, block palettes, and biome tags. Do not assume by structure name only.",
            "- Before changing mobs, inspect biome spawns, structure spawn overrides, In Control rules, and settlement safety pressure.",
            "- Prefer datapack/config/KubeJS fixes when they are enough. Use helper mods only for behavior that data cannot express safely.",
            "- Never sync into the active CurseForge instance while Minecraft is running.",
            "- Fresh world or ungenerated chunks are required to judge worldgen changes; existing chunks keep old terrain and placed blocks.",
            "- Run `python scripts\\check-pack.py` after edits. Run the Atlas generator/audit/build scripts after worldgen edits.",
            "",
            "## Generated From",
            "",
            "- `pack.toml` and `index.toml`.",
            "- Root `mods/*.pw.toml`, `resourcepacks/*.pw.toml`, and `shaderpacks/*.pw.toml`.",
            "- Local helper jar `mods/ascendant-atlas-regions-0.1.0.jar`.",
            "- `docs/UNIVERSAL_MOD_INDEX.md` category and integration-target rows.",
            "- `config/ascendant_index/*.json` registry counts.",
            "- `docs/generated/worldgen_content_audit.json` worldgen audit counts.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    universal = parse_universal_index()
    entries = load_pack_entries(universal)
    OUTPUT.write_text(build_doc(entries), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(entries)} pack entries.")


if __name__ == "__main__":
    main()
