# Prism and GitHub Updates

Ascendant Realms is set up for a packwiz-powered Prism Launcher flow.

## Brother Setup

Send him `Ascendant-Realms-Prism-AutoUpdate.zip`.

In Prism Launcher:

1. Click **Add Instance**.
2. Choose **Import**.
3. Pick the ZIP.
4. Stay on the **Import** tab until clicking **OK**.
5. Launch the instance.

The first launch downloads the pack. Later launches check GitHub and only pull changed files.

## Jayden Update Flow

1. Change the pack in `C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms`.
2. Run `scripts\publish-to-github.ps1`.
3. Brother relaunches the Prism instance.

Default live pack URL:

`https://raw.githubusercontent.com/DarkNautica/Ascendant-Realms-MC/main/pack.toml`

Optional GitHub Pages URL, once Pages is enabled:

`https://darknautica.github.io/Ascendant-Realms-MC/pack.toml`
