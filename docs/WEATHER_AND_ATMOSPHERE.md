# Weather And Atmosphere

Batch K is installed and validated. Batch L adds ambience, footsteps, and music on top of the same Weather2 path and has also passed playtest validation.

## Recommendation

Choose exactly one major weather path for Batch K:

Installed path: **Weather, Storms & Tornadoes + CoroUtil**.

Reason: it has a clear Minecraft 1.20.1 Forge/NeoForge file, is required on both client and server, and has a simple dependency chain. It is riskier for gameplay because storms and tornadoes can affect bases and server load, so it must start with conservative configs.

Delayed path: **Simple Clouds / Project Atmosphere**.

Reason: Simple Clouds has a clean 1.20.1 Forge file but is explicitly open beta and warns about bugs, crashes, and instability. Project Atmosphere has 1.20.1 Forge files and strong Serene Seasons appeal, but current 1.20.1 Forge metadata shows Simple Clouds and Gabou's Libs as dependencies, and there is a recent public crash report involving Simple Clouds loaded with Project Atmosphere. This is a prettier but less conservative next step.

## Candidate Status

| Candidate | Source | 1.20.1 Forge status | Side | Batch K decision |
|---|---|---|---|---|
| Weather, Storms & Tornadoes | Modrinth/CurseForge | Installed: `weather2-1.20.1-2.8.3.jar` | Both | Installed |
| CoroUtil | Modrinth/CurseForge | Installed: `coroutil-forge-1.20.1-1.3.7.jar` | Both | Required by Weather2 |
| Sound Physics Remastered | Modrinth/CurseForge | Installed: `sound-physics-remastered-forge-1.20.1-1.3.1.jar` | Client | Installed; restored after headphone/output route fix |
| AmbientSounds 6 | CurseForge | Installed: `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar` | Client | Batch L installed client-only; `v6.1.0` startup crash fixed |
| CreativeCore | CurseForge | Installed: `CreativeCore_FORGE_v2.12.38_mc1.20.1.jar` | Client | Batch L dependency for AmbientSounds |
| Presence Footsteps | CurseForge | Installed: `PresenceFootsteps-1.20.1-1.9.1-beta.1.jar` | Client | Batch L installed client-only |
| Biome Music | CurseForge | Installed: `biomemusic-1.20.1-3.5.jar` | Client | Batch L installed client-only |
| Medieval Music | CurseForge | Installed: `MedievalMusic.zip` | Client | Batch L installed client-only resource pack |
| Simple Clouds | Modrinth/CurseForge | Verified: `0.7.3+1.20.1-forge` supports 1.20.1 Forge | Both best installed on both | Delay |
| Project Atmosphere | Modrinth/CurseForge | Verified 1.20.1 Forge files exist | Both | Delay |
| Immersive Storms | Modrinth/CurseForge | Current visible project is Fabric/Quilt and newer-version focused | Client | Reject/delay |
| Better Clouds | Modrinth | Current 1.20.1 file is Fabric and requires Fabric API | Client | Reject |

Sources:

- Weather, Storms & Tornadoes: https://modrinth.com/mod/weather-storms-tornadoes/version/1.20.1-2.8.3
- Simple Clouds: https://modrinth.com/mod/simple-clouds/version/mcVeYqAI
- Project Atmosphere: https://modrinth.com/mod/project-atmosphere/version/Forge-0.7.0.0
- Simple Clouds and Project Atmosphere crash report: https://github.com/nonamecrackers2/simple-clouds/issues/250
- Immersive Storms: https://modrinth.com/mod/immersive-storms/versions
- Better Clouds: https://modrinth.com/project/5srFLIaK
- AmbientSounds 6: https://www.curseforge.com/minecraft/mc-mods/ambientsounds
- Presence Footsteps (Forge): https://www.curseforge.com/minecraft/mc-mods/presence-footsteps-forge
- Biome Music: https://www.curseforge.com/minecraft/mc-mods/biome-music
- Medieval Music: https://www.curseforge.com/minecraft/mc-mods/medieval-music
- Sound Physics Remastered: https://modrinth.com/mod/sound-physics-remastered/version/forge-1.20.1-1.3.1

## Weather2 Config Direction

Start conservative:

- Reduce tornado/storm frequency if config exposes frequency controls.
- Disable or reduce destructive block effects if config exposes damage/grief controls.
- Keep early-base safety in mind until the real survival world begins.
- Test with Complementary Reimagined, Auroras, Serene Seasons, and Enhanced Celestials.
- Watch TPS during storms and chunk generation.

Weather2 generates TOML config categories after first boot. Review generated storm/tornado settings before a committed world; do not stack another major cloud/weather system with it.

Atlas climate guardrails now ship source configs for Weather2, Snow Real Magic, and Serene Seasons. Weather2 snow buildup is disabled outside cold biomes, Snow Real Magic melts snow/ice in warm biomes and limits accumulation to winter, and Serene Seasons no longer performs blanket winter snow/ice generation. This keeps Frostmarch snowy without painting Sunreach, Hearthlands, or warm seam chunks white.

## Batch M Lighting Direction

Batch M does not add a second weather system.

- Sodium Dynamic Lights is client-only and should be tested with Weather, Storms & Tornadoes plus Complementary Reimagined because storm darkness, lanterns, torches, fire, and shader lighting can interact visually.
- Amendments, Macaw's Lights and Lamps, and Decorative Blocks are both-side decorative/block additions. They should not affect storm logic, but they need block placement and save/reload validation.
- If lighting looks wrong during storms, isolate shader settings and Sodium Dynamic Lights before changing Weather2.

## Sound Physics Direction

Sound Physics Remastered is installed client-only again. The zero-audio report was traced to headphone/output routing, while the latest client log showed OpenAL starting successfully on `SteelSeries Sonar - Gaming` with Minecraft volume sliders at 100%. If silence returns, inspect Minecraft's output device and the Windows/Sonar routing path before changing the mod stack.

## Batch L Audio Direction

Batch L keeps all new audio/music/body-presence presentation client-only:

- AmbientSounds 6 and CreativeCore are client-only in this pack.
- Presence Footsteps is client-only.
- Biome Music and Medieval Music are client-only.
- Sound Physics Remastered is client-only.
- Weather, Storms & Tornadoes remains the only major weather system; do not add Simple Clouds or Project Atmosphere on top of it.

Tune volume before removing mods. If the world sounds too busy, lower AmbientSounds and Presence Footsteps first, then Biome Music/Medieval Music.

## Testing Plan

Client:

- Confirm client boots with no missing dependency screen.
- Confirm weather visuals work with Complementary Reimagined enabled.
- Confirm storms do not make the screen unreadable.
- Confirm vanilla sound is audible before judging ambience or music.
- Confirm AmbientSounds, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered do not drown out combat or weather.
- Confirm Auroras and Enhanced Celestials still render sensibly at night.

Server:

- Confirm no mod mismatch.
- Confirm Weather, Storms & Tornadoes and CoroUtil are present server-side.
- Confirm AmbientSounds, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered are not required server-side unless testing proves otherwise.
- Generate a fresh test world.
- Trigger or wait for weather if practical.
- Watch TPS/logs during weather.
- Disconnect/rejoin.
- Run a 10-minute stability check.
