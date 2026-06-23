# NPC Relationship And Behavior

Status: live v1 for generated CustomNPC Guild/Hunter profiles.

The important shift is this: NPCs are not player tools. A player should be able to talk to an NPC, learn who they are, and use public services like rank evaluation, but ordinary NPCs should not instantly follow commands just because the player clicked them.

## Live Implementation

- `customnpcs/scripts/ecmascript/ascendant_npc_identity.js` now owns first-pass relationship behavior for generated CustomNPC profiles.
- `config/ascendant_guild/npc_relationship_policy.json` records the policy.
- `scripts/generate-ascendant-guild-worldgen.py` stamps generated NPCs with relationship and command-policy metadata.
- `config/CustomNpcs.cfg` is now source-controlled for command safety and removes the generic `Hello @p` fallback line.
- `scripts/check-pack.py` now validates the relationship policy, CustomNPCs safety config, generated NPC profile metadata, embedded spawn functions, and identity script tests.

## Current Relationship Tiers

| Tier | Meaning | What It Allows | What It Blocks |
| --- | --- | --- | --- |
| stranger | The NPC has no real reason to trust the player yet. | Public dialogue, warnings, board direction, Rank Examiner public evaluation. | Following, combat orders, private contracts, guard authority. |
| familiar | The NPC recognizes the player through repeated interaction. | Better rumors, more specific advice, future low-risk service hooks. | Companion behavior, rival obedience, free hireling conversion. |
| trusted | The NPC treats the player as a known contact. | Future quest/intel/cooperation hooks. | Generic follow-me commands and unlimited combat support. |

## Role Rules

- Guild Clerk: explains Guild systems, never follows.
- Bounty Master: points to contract work; future private work should require familiarity/rank.
- Rank Examiner: may run the hidden evaluation function because that is a public Guild service.
- Guild Arcanist: gives magic advice; does not become field artillery.
- Quartermaster: future supplies should require rank, marks, and relation.
- Guard Captain: commands the watch; player respect unlocks warnings, not control.
- Tavern Keeper: rumors only.
- Village Elder: settlement trust, local problems, and future village-state hooks.
- Rival Hunters: rivalry first. Cooperation must be earned through authored encounters, not generic interaction.

## Current Limitations

- This is a CustomNPC script-level gate, not the final full NPC runtime.
- It tracks simple per-NPC/per-player interaction familiarity in NPC stored data.
- It does not yet read full FTB Quest state, village reputation, completed bounties, or rescue outcomes.
- Human Companions remains a generic companion mod under review; it should not become the Guild relationship system without a separate relation gate.
- This pass does not redesign MCA villagers, Guard Villagers, or Human Companions. It prevents generated Guild/Hunter CustomNPCs from behaving like instant command followers and documents the boundary for the rest of the NPC stack.

## Test Route

1. Spawn the starter Guild staff set.
2. Right-click each NPC once and confirm they give a role line rather than a generic hello.
3. Click the same non-examiner NPC several times and confirm relation text moves from stranger to familiar/trusted, but still says they are not a follower.
4. Right-click the Rank Examiner and confirm rank evaluation still runs.
5. Confirm no normal NPC tells the player to type a command.
6. Confirm no normal NPC becomes a follower or accepts orders through this script path.
