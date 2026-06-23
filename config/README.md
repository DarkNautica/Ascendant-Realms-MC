# Config Folder

Reviewed config files go here after the version/loader decision and first generated instance.

Do not invent config formats before mods generate known-good files.

Current reviewed configs:

- `lootbeams-client.toml` tunes Loot Beams for E2: one combined look-at-item tooltip, rarity-colored beams, max native render distance, and non-common rarity filtering.
- `healthbarplus-client.toml` tunes Health Bar Plus: no proximity-only bars, show bars only for looked-at or recently damaged mobs, and leave true bosses to Enhanced Boss Bars.
- `obscuria/loot_journal-client.toml` keeps Loot Journal's pickup notification UI enabled.
- `incontrol/spawn.json` applies conservative E1 mob caps.
- `puffish_skills/` loads the unified Ascendant Web custom skill tree globally through Pufferfish's Skills so new worlds do not need a manual datapack copy.
- `openloader/` is the active OpenLoader config path. OpenLoader Forge 1.20.1 injects datapacks from `config/openloader/data/`; the world-integration crash fix must be present there, not only under repo-level `openloader/data/`.
