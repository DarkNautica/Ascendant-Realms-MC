# Ascendant Shadow Army

Solo Leveling "shadow soldier" reskins of vanilla mobs. Per the source, shadows are
near-**black smoky warriors with blue glowing parts and eyes** (blue is the default
shadow color; purple is the Monarch's-Domain upgrade, red is high-orcs). Each texture
is the **real vanilla texture, recolored**: luminance is gamma-darkened onto a
black → deep-blue → glowing-blue ramp, so the body stays mostly black and only the
original's highlights glow blue. The mob's **own eyes** (its darkest face pixels, or
its vanilla emissive eye overlay) are lit blue — there are no painted-on eyes, so
nothing doubles up. A faint trace of original hue keeps them varied, not identical.

Drop-in resource pack for Minecraft 1.20.1 (`pack_format` 15).

## Units in this batch (vanilla)

- **Humanoid soldiers** (black body, real eyes lit blue): Zombie, Husk, Drowned,
  Zombie Villager (all profession/biome variants too), Skeleton, Wither Skeleton, Stray.
- **Creeper** (black/green-tinged body; its real eyes lit blue, mouth left dark).
- **Enderman** (black body; eyes baked into the body, emissive overlay blanked so it can't full-body glow).
- **Spider, Cave Spider** (black body; eyes baked into the body, emissive overlay blanked).
- **Wolf, Tame Wolf, Angry Wolf** (black-blue shadow hound).

## Enable it

This pack already lives in your modpack's `resourcepacks/` folder. To turn it on:
- In game: Options > Resource Packs > make **Ascendant Shadow Army** active, set priority.
- Or add it to the `resourcePacks` line of `options.txt`.

It only overrides entity textures, so it stacks cleanly with most packs.

**Important:** this instance runs the **ResourcePackOverrides** mod, which re-applies its
`config/resourcepackoverrides.json` `default_packs` list every launch — any pack not in
that list gets stripped from `options.txt` automatically (this is why the pack kept
"disabling itself"). The pack is now added there (in `default_packs`, last = highest
priority, and in `pack_overrides` with `required: true`), so it's force-enabled and locked
on. A **relaunch** is required for that to take effect (F3+T won't enable a disabled pack).

## See them in-game (spawn commands)

A companion datapack ships at `config/openloader/data/ascendant_realms_shadow/`
(loaded globally by OpenLoader). In any world with cheats/op:

- `/function ascendant_shadow:preview` — lines up one frozen, named copy of every
  shadow mob in front of you, each wrapped in a glowing blue aura (soul-flame
  particles + a blue glowing outline). Also sets night + clear weather so the undead
  don't burn.
- `/function ascendant_shadow:preview_modded` — modded test mobs (Born in Chaos +
  Mowzie's), also frozen with the glowing aura.
- `/function ascendant_shadow:aura` — adds the same glowing aura to any shadow mobs
  within 24 blocks (use it on egg-spawned or naturally-spawned mobs).
- `/function ascendant_shadow:eggs` — puts a spawn egg for each shadow mob in your
  inventory so you can place them yourself.
- `/function ascendant_shadow:clear` — removes the preview line and strips the aura.
- `/function ascendant_shadow:help` — prints the command list in chat.

The aura is a datapack particle effect + glowing outline, so it's toggleable and costs
nothing when no shadow mobs are tagged.

Note: the resource pack reskins *all* mobs of each type, so every zombie/skeleton/etc.
shows the shadow look while the pack is on — there isn't a separate "shadow entity" yet.
If you later want shadow versions as distinct units (some normal, some shadow), that's a
follow-up using name-tag-based texture variants (Entity Texture Features) or a small mod.

### Note on Fresh Animations
Your pack also runs **Fresh Animations** (animated entity *models*). This pack only
supplies *textures* in the standard vanilla UV layout, so it should ride on top fine.
If anything looks misaligned, toggle this pack above/below Fresh Animations and compare.
### Emissive (glowing) eyes
Eyes/glow-parts truly glow via **ETF emissive**: your `entity_texture_features.json` has
`enableEmissiveTextures: true` and `alwaysCheckVanillaEmissiveSuffix: true`, so any
`<texture>_e.png` is rendered emissive. Each shadow mob ships a transparent `_e` map with
**only** the eye/glow pixels colored blue (transparent everywhere else) — that's why the
eyes glow without lighting the whole body. The eyes are also baked into the base texture
so they still read with emissive off. The vanilla native eye overlays (enderman/spider)
are shipped blank, because those render additively (black = invisible) and the earlier
full-body glow came from coloring their background; the `_e` maps replace them.

## Regenerating / tweaking

From the repo root (needs your Minecraft 1.20.1 jar as the texture source — common
CurseForge / .minecraft locations are auto-detected, or pass the path):

```
python scripts/generate-shadow-army-textures.py
python scripts/generate-shadow-army-textures.py "C:\path\to\1.20.1.jar"   # if not auto-found
```

Shadow palette, hue-retention amount, and eye placement are constants at the top of
that script. `PREVIEW_frontview.png` / `PREVIEW_textures.png` are reference images, not
game assets.

## Modded mobs (test batch)
A first modded batch is included (see `/function ascendant_shadow:preview_modded`):
- **Born in Chaos**: Bone Imp, Baby Skeleton, Bloody Gadfly (glowing eyes), Bonescaller,
  Barrel Zombie (pure shadow).
- **Mowzie's**: Frostmaw (icy-blue shadow), Foliaath.

Modded reskins are generated by `scripts/generate-shadow-army-modded.py`, which reads the
real mod jars (defaults to the active instance's `mods/` folder, or pass a folder of
jars). The curated mob list is the `MODDED` constant at the top; mobs with a vanilla-style
`_e` emissive get glowing eyes, the rest are pure shadow. To add more mods/mobs, extend
that list with the body texture path and its emissive overlay (if any).

Named Solo Leveling shadows (Igris, Beru, Tank…) can be done as elite recolors of fitting
mobs next.
