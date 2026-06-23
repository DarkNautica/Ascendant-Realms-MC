# First Person And Animations

Status: Batch L installed and validated. First-person Model was removed after user feedback.

Installed:

- Not Enough Animations: `notenoughanimations-forge-1.12.3-mc1.20.1.jar`

Delayed:

- First-person Model is removed because Jayden disliked seeing the player body in first person.
- Better Animations Collection is delayed for this pass. It has a clean 1.20.1 Forge file, but it overlaps with Fresh Animations, Entity Model Features, Entity Texture Features, and the existing visual stack. Add it only after Batch L proves stable and only if the mob animation result is worth the conflict risk.

## Side Split

- Not Enough Animations: client-only.
- Do not copy client animation jars into the dedicated server.

## Compatibility Focus

Test these together:

- Better Combat attack animations.
- Combat Roll.
- Simply Swords.
- Shields and Spartan Shields.
- Iron's Spells casting animations.
- IceAndFire riding/mount camera behavior if practical.
- Fresh Animations, EMF, ETF, and shaders.

## Validation Notes

Client:

- Confirm spellcasting and shield use still look usable.
- Confirm third-person animations still look normal.
- Confirm first-person view is back to the normal Minecraft-style view with no visible body overlay.
- Save/reload.

Server:

- Confirm these mods are not required server-side.
- Join localhost with no mismatch.
- Fight a few mobs and cast a basic spell from the client.

Sources checked during Batch L:

- Not Enough Animations Modrinth page: https://modrinth.com/mod/not-enough-animations
