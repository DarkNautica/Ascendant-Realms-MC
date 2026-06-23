# Mob Danger UI Policy

Generated: 2026-06-17T05:01:19Z

Status: policy scaffold only. No new overlay, mob tuning, or danger display mod was added.

## Current Stack

- Health Bar Plus: active source config at `config/healthbarplus-client.toml`.
- Enhanced Boss Bars: boss presentation layer.
- Ascendant nameplates: player/NPC rank, level, and role language.
- In Control and mob registry docs remain the danger-tier data sources; this pass only defines the UI presentation boundary.

## Display Rules

- Common mobs should not permanently fill the screen; health/name display on hover, damage, visibility, or aggro is enough.
- Dangerous mobs can later receive a concise threat-tier label, but this is not live yet.
- Bosses should use boss bars and reward-tier language rather than normal mob labels.
- Player rank, NPC rank, item rarity, and mob danger should remain visually related but semantically separate.

## Validation Snapshot

- Health Bar Plus required setting gaps: 0
- Boss blacklist gaps: 0
- Threat-tier overlay live: no
