# Custom Hero System Automation

Status: automated script tests and saved-world audit tooling are active.

Latest repair result: applied to the active `New World` save after Minecraft was closed. The saved Rank Examiner prototype now has the B-Rank visible identity, no stale close-range title, and the current embedded script copy. The follow-up dry-run audit found `0` stale CustomNPC identity records.

## What This Covers

The Custom Hero system currently uses CustomNPCs for authored guild NPCs, rival hunters, and important role NPCs. The baseline visible identity is one always-visible line:

`[B-Rank] Rank Examiner | Lv.52 Examiner`

This is intentionally a safe bridge before building the final animated Ascendant Nameplates client overlay.

## Root Cause Found

CustomNPCs embeds a full copy of the script inside each placed NPC entity. Updating `customnpcs/scripts/ecmascript/ascendant_npc_identity.js` updates new NPC authoring, but it does not automatically update NPCs that already exist in a save.

The first Rank Examiner prototype had stale saved data:

- Visible name was `[Unranked] Rank Examiner`.
- Title held a close-range level line instead of the always-visible fallback.
- The embedded CustomNPC script copy was stale.

The script now treats saved `Unranked` as stale when the profile baseline has a real rank, so profile-backed NPCs fall back to the intended rank.

## Automated Test Loop

Run from the pack root:

`powershell -ExecutionPolicy Bypass -File scripts\check-custom-hero-system.ps1 -SyncClient`

This syncs current client-side files into the active CurseForge instance, tests the identity script logic, audits the active world save, and runs the full pack checker.

When Minecraft is closed, run the full repair loop:

`powershell -ExecutionPolicy Bypass -File scripts\check-custom-hero-system.ps1 -SyncClient -Apply`

The apply mode repairs matching CustomNPC entities in the active world, including:

- `Name`
- `Title`
- `ShowName`
- `CustomName`
- `ForgeData.CNPCStoredData`
- embedded `Scripts[0].Script`

The repair script writes backups under the world save before it edits region files.

## Manual Checks Left

Automation can verify the saved NBT and script logic. The remaining checks are visual/gameplay checks:

- The NPC label is readable in-world.
- The nameplate does not overlap badly with armor, hats, or helmets.
- The finished NPC can be cloned and respawned cleanly.
- Friendly/rival combat behavior feels correct.

## Current Direction

Keep fixing root causes in place. Do not remove NPC, village, or UI functionality unless a mod or system proves unfixable after focused repair attempts.

Generated NPC update: `docs/GENERATED_NPC_SYSTEM.md` is now the preferred first test path. Use generated spawn functions for Guild staff and rivals before hand-authoring individual CustomNPCs.

Generated NPC root-cause repair: new generated NPCs no longer depend on hand-authored CustomNPC templates for skins or gear. The generator now emits bridged MCA-style CustomNPC skins, visible CustomNPCs `Weapons`/`Armor` data, anchored social AI defaults, and wider combat-profile AI defaults. If combat-capable NPCs still ignore modded enemies during testing, the next fix should be a faction/script/runtime layer, not deleting the NPC system.
