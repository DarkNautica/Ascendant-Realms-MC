# Enemy Threat UI

Batch K is installed and validated. Batch L adds Majrusz's Progressive Difficulty and Improved Mobs, so threat UI and difficulty scaling are now tuned together during long-form survival tuning.

Latest multiplayer playtest finding: enemy numeric levels were not visible. Scaling Health is still useful for scaling difficulty, but the inspected configs do not expose a clean always-readable enemy-level nameplate. Treat numeric enemy levels as a future client-overlay or verified HUD-mod task, not a finished config toggle.

## Goal

Make enemies readable without turning the screen into noise. Normal mobs should communicate health when targeted or recently damaged; true bosses should still rely on Enhanced Boss Bars.

## Recommended Mods

| Candidate | Source | 1.20.1 Forge status | Side | Batch K decision |
|---|---|---|---|---|
| YDM's MobHealthBar | Modrinth/CurseForge | Installed: `mobhealthbar-forge-1.20.x-2.3.0.jar` | Client | Installed |
| Scaling Health | Modrinth/CurseForge | Installed: `ScalingHealth-1.20.1-8.0.2+9.jar` | Both | Installed, conservative config required |
| Silent Lib | CurseForge/Modrinth | Installed: `silent-lib-1.20.1-8.0.0.jar` | Both | Required by Scaling Health |
| Health Indicators | Modrinth | Current visible 1.20.1 platforms are Fabric/NeoForge/Quilt, not Forge | Client | Reject/delay |
| Champions | Modrinth | Current visible project is Fabric-oriented; do not use in this Forge pack | Both if ever replaced | Reject/delay |

Sources:

- YDM's MobHealthBar: https://modrinth.com/project/wtk2r10e
- Scaling Health: https://modrinth.com/mod/scaling-health/version/OTsI95Em
- Silent Lib: https://www.curseforge.com/minecraft/mc-mods/silent-lib
- Health Indicators: https://modrinth.com/mod/health-indicators/versions
- Champions: https://modrinth.com/project/z8QdexpL

## YDM's MobHealthBar Config Direction

Use health bars as combat feedback, not a permanent overlay:

- Hide passive mobs if the config exposes a passive/blacklist option.
- Show normal hostile mobs only when targeted, damaged, aggressive, or hovered.
- Keep render distance modest for normal mobs.
- Allow stronger mobs and miniboss-like threats to show longer if the config supports entity/category rules.
- Keep Enhanced Boss Bars as the boss presentation layer.

The generated YDM's MobHealthBar config was inspected after first boot. `config/mobhealthbar-client.toml` now locks the intended behavior:

- `hovered_only = true`
- `damaged_only = true`
- `on_aggro = true`
- `render-distance = 64`
- `blacklist = "minecraft:ender_dragon,minecraft:wither"`

The mod's render gate treats these as an OR condition: show when hovered, damaged, or aggressive. With any of those gates enabled, the proximity-only fallback is skipped, so nearby mobs should not show bars just because the player is close. Ender Dragon and Wither stay blacklisted so Enhanced Boss Bars owns true boss presentation.

## Scaling Health Config Direction

Scaling Health should make the world more legible and scalable, not punish early exploration:

- Start with conservative difficulty growth.
- Keep blights rare.
- Avoid early-game health walls.
- Do not sharply boost enemies near spawn before final survival tuning.
- Watch interaction with Pufferfish's Attributes, Simply Swords, Iron's Spells, Artifacts, and boss loot.
- Watch interaction with Majrusz's Progressive Difficulty and Improved Mobs from Batch L.
- Treat any heart-container or player-health progression as balance-sensitive.

Scaling Health config should be generated and reviewed after first client/server boot. Do not tune by memory; inspect the generated `config/scalinghealth/` files before changing difficulty, blight, or health scaling values.

## Enemy Level Display Gap

Current installed pieces:

- YDM's MobHealthBar handles health bars.
- Scaling Health handles difficulty/health scaling.
- Enhanced Boss Bars owns true boss presentation.

Still missing:

- A visible numeric `Level X` enemy nameplate/HUD layer.

Safe next options:

- Find and test a Forge 1.20.1 enemy-level display mod that can coexist with YDM's MobHealthBar and Enhanced Boss Bars.
- Build a small custom client overlay if we need exact Scaling Health difficulty/level data shown above mobs.
- Do not replace the health bar stack just to chase enemy levels unless the replacement is verified in the current pack.

## Testing Plan

Client:

- Confirm mob health bars render.
- Confirm passive mobs are hidden or minimally noisy.
- Confirm normal hostile mobs show health only when targeted/damaged/aggressive if possible.
- Confirm health bars do not appear from proximity alone.
- Confirm boss bars still come from Enhanced Boss Bars.
- Confirm Scaling Health does not crash with vanilla and modded mobs.
- Confirm shader-on visibility remains readable.

Server:

- Confirm no mod mismatch.
- Confirm Scaling Health and Silent Lib are present server-side.
- Confirm YDM's MobHealthBar is not required on the dedicated server unless testing proves otherwise.
- Fight vanilla mobs and several modded mobs.
- Confirm scaling/blights are conservative.
- Disconnect/rejoin.
- Run a 10-minute stability check.
