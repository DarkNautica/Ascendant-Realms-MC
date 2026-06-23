# Structure Director Rollback

Use rollback only if new worlds show serious structure-regression behavior.

## Disable

Run:

```powershell
.\scripts\disable-structure-director-live-v1.ps1
```

This renames the live OpenLoader datapack folder to `.disabled`, sets `live_structure_policy.enabled=false`, and preserves evidence/candidate files.

## Enable

Run:

```powershell
.\scripts\enable-structure-director-live-v1.ps1
```

Then sync/export again before testing active CurseForge or packaged copies.
