# Bounty Pool Worklist

Generated: 2026-06-14T15:41:03.2735019-04:00

This worklist groups generated bounty targets into Hunter Board pools. The first live unification pass now writes reviewed, filtered Bountiful pools from these candidates through `scripts/generate-ascendant-guild-worldgen.py`.

| Board | Bounty Tier | Reward Rarity | Targets |
| --- | --- | --- | ---: |
| major_guild_registry | boss | legendary | 36 |
| major_guild_registry | dragon | mythic | 33 |
| town_guild_board | elite | epic | 32 |
| village_hunter_board | dangerous | rare | 209 |

## Active Config Note

The current Bountiful config is no longer generic. Active Open Loader pools now contain:

| Board | Live Targets |
| --- | ---: |
| village_hunter_board | 79 |
| town_guild_board | 23 |
| major_guild_registry | 51 |

The generator filters friendly/tooling namespaces (`customnpcs`, `easy_npc`, `humancompanions`, `mca`, and `geckolib`) so Guild boards do not ask players to kill social NPCs or helper entities. The remaining generated candidates stay available for later manual review, but not every language-key entity is safe as a live contract.
