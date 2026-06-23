# Sound And Music

Status: Batch L installed and validated.

Installed:

- AmbientSounds 6: `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar`, client-only.
- CreativeCore: `CreativeCore_FORGE_v2.12.38_mc1.20.1.jar`, client-only dependency for AmbientSounds in this pack.
- Presence Footsteps (Forge): `PresenceFootsteps-1.20.1-1.9.1-beta.1.jar`, client-only.
- Biome Music[Forge/Fabric]: `biomemusic-1.20.1-3.5.jar`, client-only.
- Medieval Music: `MedievalMusic.zip`, client-only resource pack.
- Sound Physics Remastered: `sound-physics-remastered-forge-1.20.1-1.3.1.jar`, client-only.

## Design Intent

- Caves, forests, storms, oceans, and villages should sound more alive.
- Footsteps should help body presence without adding gameplay rules.
- Music should feel fantasy/medieval without fighting every other sound layer.
- Audio should be adjustable because too much ambience gets tiring fast.

## Side Split

Client-only:

- AmbientSounds 6
- CreativeCore
- Presence Footsteps
- Biome Music
- Medieval Music
- Sound Physics Remastered

Do not copy these to the server unless a dedicated server test proves a real server requirement.

## Tuning Notes

- AmbientSounds `v6.1.0` is rejected for this pack because it crashed on startup with CreativeCore `2.12.38` through a `ConfigEventHandler.load` method mismatch. Keep the `v6.3.8` pin unless a newer file is separately tested.
- Sound Physics Remastered is restored after the zero-audio report was traced to headphone/output routing rather than the mod stack. If audio goes silent again, check the Minecraft output device and Windows/Sonar route before removing audio mods.
- If the mix is too loud, lower AmbientSounds and Presence Footsteps first.
- If music triggers too often, tune Biome Music before removing Medieval Music.
- Test with Weather, Storms & Tornadoes because weather audio can dominate.

## Validation Notes

Client:

- Confirm client boots with no missing dependency screen.
- Enter a forest, cave, village, ocean/coast, and storm if practical.
- Confirm footsteps vary by block.
- Confirm medieval music plays and does not drown out combat.
- Confirm vanilla sound works first, then confirm AmbientSounds, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered are audible.

Server:

- Confirm these audio mods are not required server-side.
- Join localhost with no mismatch.
- Fight mobs and trigger weather if practical.
- Run the 10-minute stability check.

Sources checked during Batch L:

- AmbientSounds 6 CurseForge page: https://www.curseforge.com/minecraft/mc-mods/ambientsounds
- Presence Footsteps Forge CurseForge page: https://www.curseforge.com/minecraft/mc-mods/presence-footsteps-forge
- Biome Music CurseForge page: https://www.curseforge.com/minecraft/mc-mods/biome-music
- Medieval Music CurseForge page: https://www.curseforge.com/minecraft/mc-mods/medieval-music
- Sound Physics Remastered Modrinth page: https://modrinth.com/mod/sound-physics-remastered/version/forge-1.20.1-1.3.1
