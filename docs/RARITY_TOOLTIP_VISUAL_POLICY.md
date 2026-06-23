# Rarity Tooltip Visual Policy

Generated: 2026-06-17T05:01:19Z

Status: policy scaffold only. No tooltip rewrite or visual mod change was enabled.

## Canonical Palette

| Rarity | Color | Use |
| --- | --- | --- |
| Common | `#9CA3AF` | Item Borders, rarity tooltip line, loot-value language |
| Uncommon | `#55FF55` | Item Borders, rarity tooltip line, loot-value language |
| Rare | `#55AAFF` | Item Borders, rarity tooltip line, loot-value language |
| Epic | `#D966FF` | Item Borders, rarity tooltip line, loot-value language |
| Legendary | `#FFE66D` | Item Borders, rarity tooltip line, loot-value language |
| Mythic | `#FF3B00` | Item Borders, rarity tooltip line, loot-value language |
| Ascendant | `#E6FBFF` | Item Borders, rarity tooltip line, loot-value language |

## Rules

- Item border color follows assigned rarity from `config/ascendant_index/gear_registry.json`, not the item display-name color.
- KubeJS adds one concise Ascendant rarity line and should not expose backend registry paths or policy terms in normal play.
- Legendary Tooltips styles the frame and background; it must not sync/override Item Borders colors.
- Loot Beams should use rarity color, keep item-name color disabled, and stay rare+ enough that common drops do not flood the screen.
- Common items can be present in manual border data even when `show_for_common = false`; that lets the registry stay complete without filling the HUD with gray frames.

## Validation Snapshot

- Manual border colors present: #55AAFF, #55FF55, #9CA3AF, #D966FF, #E6FBFF, #FF3B00, #FFE66D
- Tangible item IDs with borders: 1460/1460
- Border color mismatches: 0
- Tangible tooltip gaps: 0
- Legacy rarity color drift rows: 7
