// Ascendant Realms JEI aliases for important NBT-backed guide items.
// Runic Grimoire is a Patchouli guide book variant, not a standalone item ID.
// Legacy search target: simplyswords:runic_grimoire.

const ASCENDANT_RUNIC_GRIMOIRE = Item.of('patchouli:guide_book', '{\"patchouli:book\":\"ascendant_codex:ascendant_codex\"}')
const ASCENDANT_RUNIC_GRIMOIRE_SEARCH_ALIAS = 'patchouli:guide_book'

if (Platform.isLoaded('jei')) {
  JEIEvents.addItems(event => {
    // JEI rejects the NBT-backed Patchouli guide stack as an empty runtime ingredient in this stack.
    // Add the base guide item safely, then keep the real Runic Grimoire styling on the actual NBT item.
    event.add(ASCENDANT_RUNIC_GRIMOIRE_SEARCH_ALIAS)
  })
}

ItemEvents.tooltip(event => {
  event.add(ASCENDANT_RUNIC_GRIMOIRE, [
    Text.of('ASCENDANT CODEX').color(0xE6FBFF).bold(true),
    Text.of('Runic Grimoire').color(0xE6FBFF).bold(true)
  ])
  event.add(ASCENDANT_RUNIC_GRIMOIRE_SEARCH_ALIAS, [
    Text.of('ASCENDANT CODEX').color(0xE6FBFF).bold(true),
    Text.of('Runic Grimoire guide variants are Patchouli books.').color(0xBDEFFF)
  ])
})
