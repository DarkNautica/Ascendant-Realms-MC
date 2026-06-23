
# Weather And Season Region Policy

Generated: 2026-06-17T04:08:00+00:00

Status: audit/control scaffold only. No weather or season config was changed by this pass.

## Weather Layer Audit

| Layer | Role | Config path | Policy |
| --- | --- | --- | --- |
| Weather2 | major storm/weather layer | config/Weather2/Snow.toml | Keep conservative. Snowstorm buildup must stay blocked outside cold biomes. |
| Serene Seasons | season color and weather-frequency layer | config/sereneseasons/seasons.toml | Season color is welcome, blanket snow/ice generation stays off. |
| Snow Real Magic | snow visual/accumulation layer | config/snowrealmagic-common.yaml | Warm biome melt and winter-only accumulation must remain on. |
| Auroras | night sky atmosphere, strongest in Frostmarch and cold outer regions | none | Visual layer only; do not use it as proof of cold climate correctness. |
| Enhanced Celestials | moon/event atmosphere | none | Use for danger mood but do not let event pressure replace Atlas progression. |

## Snow Guard Evidence

| Guard | Current result |
| --- | --- |
| Weather2 blocks snow buildup outside cold biomes | True |
| Serene Seasons blanket snow/ice conversion disabled | True |
| Snow Real Magic melts snow/ice in warm biomes | True |
| Snow Real Magic accumulation is winter-only | True |
| Snow Real Magic snowfall accumulation disabled | True |

## Regional Rules

- Frostmarch can use snow, cold wind, auroras, frozen ambience, snow roads, and harsh winter presentation.
- Sunreach should remain dry, hot, dusty, and storm-scarred, with no snow or ice buildup.
- Verdant Coast should be wet, lush, stormy, coastal, and humid rather than cold.
- Stoneback Highlands should feel windy, mountainous, echoing, and rocky; do not reintroduce broad snow.
- Hearthlands/Crownlands should stay safe, temperate, readable, and beginner-friendly.
- Outer regions can be oppressive and dangerous, but snow must still follow actual cold biome intent instead of blanket conversion.
