# Skill Tree Implementation Plan

Status: implemented as a unified Ascendant Web, playtest passed, tuning active.

## Active Load Paths

Primary config path:

```text
config/puffish_skills/
```

Fallback/source datapack:

```text
datapacks/ascendant_realms_skills/
```

Open Loader legacy/source datapack mirror:

```text
openloader/data/ascendant_realms_skills/
```

All three paths are generated from:

```text
scripts/generate-ascendant-skill-web.js
```

Run the generator after any large node/layout edits, then run Packwiz refresh and the pack checker.

## Active Decision

The old seven-tab custom tree was replaced with one `Ascendant Web` category because Jayden wanted one large upgrade web where players can pick and choose across branches.

Default Skill Trees stays removed.

## Implemented Scope

- 113 generated nodes.
- 196 generated connections after the readability pass.
- One central root node.
- Seven cleaner branch lanes inside one category.
- Styled tooltips with exact `Effect:` lines.
- Shift metadata for cost, branch, requirements, loaded mods, and pack links.
- Direct attribute rewards using confirmed vanilla, Pufferfish's Attributes, Iron's Spells, and Projectile Damage Attribute attributes.
- Shared XP source from killed mob dropped XP plus killed mob max health.
- 2 starting points.
- Level limit 120.
- Expression-based XP curve: `min(55 + level ^ 1.82 * 11, 2400)`.

## Not Yet Implemented

- Boss-kill unlock gates.
- Dragon-kill unlock gates.
- Bountiful contract skill XP.
- Create milestone unlocks.
- Title rewards.
- KubeJS live progression scripting.
- Custom art beyond item icons and the Puffish web layout.
- Animated frames/backgrounds beyond the Puffish Skills UI surface.
- True second HUD skill-XP bar tied directly to Puffish internals.

## Update Process

1. Edit `scripts/generate-ascendant-skill-web.js`.
2. Run `node scripts\generate-ascendant-skill-web.js`.
3. Run `packwiz refresh`.
4. Run `python scripts\check-pack.py`.
5. Export client and server staging.
6. Validate in a fresh creative test world before treating the skill gate as passed.
