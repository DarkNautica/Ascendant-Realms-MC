# Ascendant Realms Codex

The in-game **Ascendant Codex** — a Patchouli book and the player's manual for the modpack,
styled as an Arcane Void grimoire (custom GUI, held-book item, colored text via macros).

Active OpenLoader load path: `config/openloader/data/ascendant_realms_codex/`
(mirrored to `datapacks/` and `openloader/`). Grimoire textures live in the always-on
KubeJS resource pack at `kubejs/assets/ascendant_realms/`.

First-edition sample: the **Getting Started** category is fully written (Welcome, Your First
Day, Powers). The other categories (Guild, Hunter Boards, Settlements, Rivals, Paths) are
outline stubs to be expanded. See `codex-art/README.md` and `scripts/generate-ascendant-codex-art.py`.


## IMPORTANT: 1.20 layout
Patchouli 1.20+ enforces resource-pack books. `book.json` stays here (data side) with
`"use_resource_pack": true`, but the **categories/entries must live in assets** at
`kubejs/assets/ascendant_realms/patchouli_books/ascendant_codex/en_us/`. Content placed only
under this datapack's `en_us/` will be silently ignored by Patchouli.
