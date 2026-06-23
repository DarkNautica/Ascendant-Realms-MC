# MCA Reborn Medieval Validation

Status: installed and default-enabled for the next import; visual/server validation is still pending.

## Installed Files

| Item | Source | File | Side | Status |
| --- | --- | --- | --- | --- |
| MCA Reborn [Fabric/Forge] | CurseForge | `minecraft-comes-alive-7.6.16+1.20.1-universal.jar` | Both | Installed |
| MCA - Default Medieval | CurseForge | `MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip` | Client | Installed |

## Local Resource-Pack Inspection

The medieval pack was downloaded to a scratch folder and inspected before install.

- Total zip entries: 1169
- Clothing PNGs under `assets/mca/skins/clothing/`: 974
- States covered: normal, burnt, zombie
- Genders covered: female, male, neutral
- Profession/life-stage buckets covered: 23
- Covered buckets: archer, armorer, baby, baker, butcher, cartographer, child, cleric, cultist, farmer, fisherman, fletcher, guard, leatherworker, librarian, mason, miner, nitwit, none, shepherd, toddler, toolsmith, weaponsmith
- No `data/**/skins/**/*.json` files were present; this clothes-only pack is asset-path based.

The root `options.txt` now enables `file/MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip` by default, and `scripts/check-pack.py` errors if MCA Reborn is active while the medieval resource pack is not enabled. Client sync merges only the resource-pack lines into the active CurseForge instance's `options.txt`, so user controls/video/audio settings are preserved.

## Validation Needed

Client test:

- Launch after fresh client import.
- Confirm no missing MCA dependency or startup error.
- Create/load a fresh creative test world.
- Locate or spawn MCA villagers.
- Confirm normal/burnt/zombie MCA clothing stays medieval/fantasy-safe.
- Confirm no modern hoodies, modern shirts, or off-tone skins are common in naturally spawned villagers.
- Confirm MCA GUI, interaction, naming, family/social UI, and villager editor screens open without crashes.
- Confirm JEI/search remains responsive after MCA is installed.

Server test:

- Export server staging.
- Materialize from the active CurseForge client mods folder with `-Clean`.
- Confirm `minecraft-comes-alive` is copied server-side.
- Boot Forge 1.20.1-47.4.20 dedicated server.
- Join localhost.
- Visit a village and interact with MCA villagers.
- Confirm no villager/entity mismatch or server crash.
- Disconnect/rejoin.
- Run a 10-minute stability check near a village.

## Risk Notes

MCA Reborn is a large villager/social overhaul. It can change villager entities, village population feel, interaction menus, family systems, and social progression. Keep this pass isolated from other major installs until the client and dedicated server tests pass.
