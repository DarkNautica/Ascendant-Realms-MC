# Generated NPC System

Status: first generated CustomNPC profile and spawn-set layer is active through Open Loader.

Jayden should not need to hand-build every Guild NPC. The current pass creates a reusable generated set at `config/ascendant_guild/generated_npc_profiles.json` and callable spawn functions under `ascendant_guild:npc/*`.

## Profiles

| Profile | Rank | Level | Role | Preferred Placement |
|---|---:|---:|---|---|
| `guild_clerk` | D-Rank | Lv.18 | Clerk | `village_hunter_board` |
| `bounty_master` | C-Rank | Lv.38 | Contracts | `town_guild_board` |
| `rank_examiner` | B-Rank | Lv.52 | Examiner | `frontier_guild_outpost` |
| `guild_arcanist` | B-Rank | Lv.49 | Arcanist | `frontier_guild_outpost` |
| `hunter_quartermaster` | D-Rank | Lv.24 | Supplies | `town_guild_board` |
| `guard_captain` | C-Rank | Lv.36 | Captain | `village_hunter_board` |
| `tavern_keeper` | D-Rank | Lv.16 | Rumors | `roadside_hunter_camp` |
| `village_elder` | D-Rank | Lv.22 | Elder | `village_hunter_board` |
| `wounded_hunter` | C-Rank | Lv.31 | Hunter | `roadside_hunter_camp` |
| `mira_ash` | C-Rank | Lv.34 | Scout | `roadside_hunter_camp` |
| `darius_crowe` | B-Rank | Lv.47 | Duelist | `town_guild_board` |
| `seren_valehart` | B-Rank | Lv.45 | Arcanist | `frontier_guild_outpost` |

## Spawn Sets

- `/function ascendant_guild:npc/spawn_set/starter_guild_staff`
- `/function ascendant_guild:npc/spawn_set/roadside_rumor_camp`
- `/function ascendant_guild:npc/spawn_set/frontier_guild_outpost`
- `/function ascendant_guild:npc/list`

## Design

- Spawned NPCs are `customnpcs:customnpc` entities.
- The visible name line includes rank, name, level, and role.
- Spawn functions now apply role-specific CustomNPCs skin textures from `customnpcs:textures/entity/ascendant_mca/*.png`.
- The same `ascendant_mca` skin PNGs are stored in both `resourcepacks/ascendant-realms-compat-fixes/assets/customnpcs/textures/entity/ascendant_mca/` and `customnpcs/assets/customnpcs/textures/entity/ascendant_mca/`. The CustomNPCs-native copy exists because the first in-game test showed magenta missing skins when the mod requested the texture through `customnpcs:` before resolving the separate compatibility resource pack.
- The `ascendant_mca` skins are bridge textures: MCA medieval clothing overlays composited onto full CustomNPCs-compatible player skins, so generated NPCs avoid broken overlay-only skins and do not default to Steve.
- Spawn functions pull visible mainhand/offhand/head/chest gear from `config/ascendant_guild/npc_loadouts.json`.
- Gear uses CustomNPCs top-level `Weapons` and `Armor` data plus vanilla `HandItems`/`ArmorItems` fallback data. `NpcInv` is kept empty because CustomNPCs treats it as a drop-table inventory, not the rendered equipment layer.
- Mainhand uses CustomNPCs weapon slot `0`; visible offhand uses slot `2`. Slot `1` is projectile/ammo behavior and should not be used for offhand identity gear.
- Social NPCs use anchored AI defaults so they should not all wander away in the same direction. Combat profiles such as guards and rival hunters use a wider active/walking range, but true cross-mod hostile defense still needs in-game validation and may require the future Ascendant NPC Runtime helper mod.
- The entity stores `ar_profile`, `ar_rank`, `ar_level`, `ar_role`, `ar_name`, `ar_relationship_gate`, `ar_command_policy`, `ar_service_min_relation`, `ar_can_follow`, and `ar_can_take_orders` in `ForgeData.CNPCStoredData`.
- Generated NPCs use relationship-gated dialogue through `customnpcs/scripts/ecmascript/ascendant_npc_identity.js`. Repeated interaction can move a player from stranger to familiar/trusted, but the current generated profiles still cannot follow or take player orders.
- Rank Examiner is the only generated NPC allowed to run a hidden public-service function on interaction. That is rank evaluation, not obedience, and the player should never need to type the function manually.
- `config/CustomNpcs.cfg` disables the generic `Hello @p` fallback line and locks normal edit/command surfaces behind ops so random players cannot use NPC tooling as gameplay.
- This is intentionally data-backed and static for the first generated pass. A future Ascendant NPC Runtime helper mod can read the same data and make levels, schedules, gear, dialogue, relationship rewards, and nameplates fully dynamic.

## Test

1. Load a creative test world with cheats enabled.
2. Run `/function ascendant_guild:npc/list`.
3. Run `/function ascendant_guild:npc/spawn_set/starter_guild_staff`.
4. Confirm the generated NPCs appear with styled rank/level/name/role lines.
5. Confirm generated NPCs use medieval/MCA-style skins rather than Steve or plain CustomNPCs defaults.
6. Confirm mainhand, offhand, helmet/hat, and chest identity gear render on the NPC model where configured.
7. Confirm social NPCs stay near their spawn instead of marching off together.
8. Spawn a vanilla zombie near a combat profile such as Guard Captain or Wounded Hunter and verify behavior. If they still ignore hostiles, treat it as the next runtime/faction scripting task instead of deleting the NPC system.
9. Confirm killing a test copy does not drop the full visible kit.
10. Right-click non-examiner NPCs repeatedly and confirm they give role/relation dialogue instead of a generic hello or command prompt.
11. Confirm non-examiner NPCs do not become followers or accept player orders through this script path.
12. Right-click the Rank Examiner and confirm rank evaluation still runs as the only public-service interaction bridge.
13. Run the roadside and frontier spawn sets away from the first group.
