# Atlas Tectonic Integration Risk

Generated: 2026-06-17

Status: risk assessment updated after the failed Option C post-generation block-fill prototype and the new source natural density-bias prototype. Tectonic, Terralith, structures, roads, villages, mobs, ores, loot, recipes, magic, and civilization systems are still untouched.

## Current Integration

Ascendant Atlas currently works by replacing the Overworld biome source with `ascendant_atlas_regions:regional_multi_noise` while leaving the generator as `minecraft:noise` and the settings as `minecraft:overworld`.

That means:

- Atlas controls biome identity.
- Tectonic/Terratonic still controls terrain shape.
- Terralith still contributes biome content.
- The water-basin bug sits below biome selection.

## Risk Summary

| Option | Risk | Tectonic feel | Rollback | Notes |
| --- | --- | --- | --- | --- |
| Keep biome-source-only Atlas | Low | Preserved | Already live | Proven insufficient for south/west ocean basins. |
| Tectonic config tuning | Low | Preserved | Simple | No useful active config knobs found beyond `legacy_mode`. |
| Add datapack density overrides | Medium-high | Partial/uncertain | Remove datapack | Easy to prototype, but can accidentally fork Tectonic/Terratonic terrain globally. |
| Atlas land-bias density override | Medium | Intended preserved | Remove continents override and restore previous helper jar | Current source prototype; targets `minecraft:overworld/continents` only and leaves `final_density`, `depth`, aquifers, generator type, and noise settings alone. |
| Custom noise-settings preset | High | Uncertain | Restore dimension override | Can bypass injected Tectonic resources if copied incorrectly. |
| Probe-only land/water classifier | Low | Preserved | Disable policy or restore old helper jar | Implemented and used as evidence; proved the blocker is below biome selection. |
| Option C fresh-chunk basin correction | Failed | Poor visual result | Source helper `E9597A745` disables terrain_correction | Rejected. It kept `minecraft:noise` and `minecraft:overworld`, but edited fresh chunks after generation and produced artificial Stoneback/Sunreach shelves. |
| Region-aware chunk generator wrapper | High | Best if delegate-based | Restore old helper jar and dimension override | Most correct path for an actual fix, but requires careful Java implementation and fresh-world testing. |
| Post-generate terrain repair | Very high | Poor | Hard | Can break structures, caves, aquifers, fluids, lighting, and performance. Not preferred. |

## Tectonic/Terratonic Pack-Order Risk

Tectonic registers its worldgen resources as a server datapack. With Terralith installed, the Terratonic branch is expected to be active.

Risk:

- A custom datapack override may load before or after Tectonic/Terratonic differently than expected.
- If the override wins, it may replace more Tectonic logic than intended.
- If it loses, the prototype may appear to do nothing.

Mitigation:

- Keep datapack prototypes disabled until explicitly testing.
- Record exact datapack order from a live log before judging any datapack override.
- Prefer a helper-side generator wrapper when region-specific behavior is required.

## Density Function Risk

The tempting files to override are also the dangerous files:

- `overworld/noise_router/continents`
- `overworld/noise_router/depth`
- `overworld/noise_router/final_density`
- `overworld/noise_router/fluid_level_floodedness`
- `overworld/noise_router/fluid_level_spread`
- `tectonic:overworld/continents`
- `tectonic:overworld/depth`
- `tectonic:overworld/aquifer_parameters`

Risk:

- Continentalness changes can affect every region, including Verdant Coast and Frostmarch.
- Depth/final-density changes can flatten mountains, cliffs, caves, and valleys.
- Aquifer changes can break underground water and cave behavior.
- Vanilla density functions are not naturally aware of Atlas region names unless coordinate math is encoded or the helper participates.

Mitigation:

- Current source prototype overrides only `minecraft:overworld/continents`, preserving vanilla shifted continentalness and adding `ascendant_atlas_regions:atlas_land_bias`.
- Do not directly override `final_density` as a first prototype.
- If a datapack prototype is used, start with a narrow continents/aquifer experiment in a disposable test world.
- Validate with fresh chunks only.

## Chunk Generator Wrapper Risk

A region-aware wrapper is the most correct direction because it can ask Atlas which region a chunk belongs to. It is also a real code change.

Potential files/classes touched:

- `local-mods/ascendant-atlas-regions/src/main/java/.../AscendantAtlasRegions.java`
- helper registry/bootstrap classes
- a new generator codec/serializer class
- a terrain policy loader for `config/ascendant_atlas/terrain_noise_policy.json`
- Atlas region math utilities already used by the biome source
- the Overworld dimension override, only if the wrapper becomes the generator type

Risks:

- Startup codec errors can prevent world creation.
- Incorrect delegation can bypass Tectonic terrain.
- Post-processing can cause lag or chunk lighting/fluid issues.
- Old chunks cannot prove the result.

Mitigation:

- Add a feature flag.
- Keep the existing biome source as the stable baseline.
- Prototype debug/report mode before mutating terrain.
- Delegate to the active `minecraft:noise` generator and `minecraft:overworld` settings instead of reimplementing terrain from scratch.
- Keep rollback as replacing the helper jar and restoring the current dimension override.

## Performance Risk

The water-body classifier already proved that broad live sampling can lag the game. A terrain wrapper must avoid doing neighborhood scans during normal chunk generation.

Performance guardrails:

- Use region math that is cheap and deterministic.
- Avoid wide radius scans inside chunk generation.
- If basin detection needs neighborhood context, precompute or limit it to debug commands first.
- Use `/ascatlas sample_land_water 30000 5000` for the current probe pass instead of rerunning `classify_water_bodies`.
- Do not put the probe's surrounding-grid scan inside normal chunk generation.

## Rollback Plan

Fast rollback:

1. Close Minecraft.
2. Restore the previous known-good `ascendant-atlas-regions-0.1.0.jar`.
3. Restore the current Overworld override shape:
   - `generator.type = minecraft:noise`
   - `generator.settings = minecraft:overworld`
   - `generator.biome_source.type = ascendant_atlas_regions:regional_multi_noise`
4. Remove or disable any prototype datapack overrides.
5. Create a fresh world before retesting.

## Risk Verdict

The fresh-chunk-only Option C correction failed visual validation. It preserved the Tectonic path technically, but it did not preserve natural Tectonic/Terralith terrain visually because it filled finished chunks with replacement blocks. Keep it disabled. The current source path is a narrower Atlas land-bias density override; if that fails, move to the delegate generator-wrapper path instead of post-generation repair.
