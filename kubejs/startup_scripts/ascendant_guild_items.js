// Ascendant Realms - Guild currency item concepts.
//
// These are intentionally simple starter items for FTB Quests, Bountiful,
// Guild vendors, and rank rewards. Texture/model polish comes after boot
// validation confirms the KubeJS item IDs are stable.

StartupEvents.registry('item', event => {
  event.create('guild_mark').displayName('Guild Mark')
  event.create('hunter_seal').displayName('Hunter Seal')
  event.create('ascendant_sigil').displayName('Ascendant Sigil')
})
