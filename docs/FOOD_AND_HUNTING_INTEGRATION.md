# Food And Hunting Integration

Status: Batch N installed and validated.

Installed:

- Alex's Delight: `alexsdelight-1.5.jar`
- Create Slice & Dice: `sliceanddice-forge-3.6.0.jar`

Existing foundations:

- Alex's Mobs
- Farmer's Delight
- Create
- Bountiful
- custom Survivalist, Ranger, Engineer, and Dragonbound skill branches

Design intent:

- Alex's Mobs hunting should feed Farmer's Delight survival.
- Bountiful contracts can later request cooked foods, monster foods, and rare ingredients.
- Survivalist should benefit from seasons, travel, food, and field cooking.
- Ranger should connect to Alex's Mobs, Born in Chaos, IceAndFire CE, and bounty trophies.

Why Alex's Delight was chosen:

- It directly bridges Alex's Mobs and Farmer's Delight.
- It resolved cleanly through CurseForge for Minecraft 1.20.1.
- The alternate "Alex's Mobs Delight" naming is treated as a search/candidate alias, not the installed file.

Validation notes:

- Confirm Alex's Delight items appear in JEI.
- Confirm its recipes reference Alex's Mobs and Farmer's Delight correctly.
- Confirm food items do not crash tooltips or JEI.
- Confirm dedicated server joins with no mod mismatch.
