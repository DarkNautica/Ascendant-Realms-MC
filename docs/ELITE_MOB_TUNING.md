# Elite Mob Tuning

Status: Batch L installed and validated; tuning active.

Improved Mobs is installed as the elite normal-mob pressure layer:

- Improved Mobs: `improvedmobs-1.20.1-1.13.6-forge.jar`
- TenshiLib: `tenshilib-1.20.1-1.7.6-forge.jar`

Purpose:

- Make normal enemies feel less flat.
- Add long-term pressure without adding another boss pack.
- Create "oh no" moments from regular mobs without making every night impossible.

## Conservative Defaults

Until Batch L passes:

- Do not raise Improved Mobs settings manually.
- Do not combine max mob buffs with high Scaling Health values.
- Do not add more elite/boss systems.
- Watch enchanted/geared mobs around spawn.
- Watch village survival, especially if raids or storms overlap.

## First Balance Targets

If it feels too hard:

- Lower early-game scaling.
- Reduce special gear/ability chances.
- Keep blights and elite mobs rare.

If it feels too empty or too safe:

- Tune spawn mixture first.
- Then tune elite chance.
- Only then consider raw health/damage changes.

## Validation Notes

Client:

- Fight vanilla zombies, skeletons, spiders, and one or two modded mobs.
- Confirm YDM's MobHealthBar remains readable.
- Confirm Better Combat, Combat Roll, and Simply Swords still feel responsive.

Server:

- Confirm Improved Mobs and TenshiLib are present server-side.
- Join localhost with no mismatch.
- Fight vanilla and modded mobs.
- Disconnect/rejoin.
- Run a 10-minute stability check.
