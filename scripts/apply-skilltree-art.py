#!/usr/bin/env python3
"""Rewire the Ascendant Web puffish category to use the Arcane Void custom art:
custom background, lane/tier texture frames, and per-node texture icons.
Run after generate-ascendant-skilltree-art.py. Operates on every category copy passed.
"""
import json, os, sys
LANES = {"warrior","rogue","ranger","arcanist","engineer","survivalist","dragonbound","ascendant"}
TIER = {"task": "normal", "goal": "notable", "challenge": "major"}
NS = "ascendant:textures/skilltree"

def apply(catdir):
    dpath = os.path.join(catdir, "definitions.json")
    defs = json.load(open(dpath, encoding="utf-8"))
    for node, v in defs.items():
        lane = node.split("_")[0]
        if lane not in LANES: lane = "ascendant"
        cur = v.get("frame", {}).get("data", {}).get("frame", "task")
        tier = TIER.get(cur, "normal")
        v["frame"] = {"type": "texture", "data": {
            "unlocked": f"{NS}/frames/{lane}_{tier}_unlocked.png",
            "available": f"{NS}/frames/{lane}_{tier}_available.png"}}
        v["icon"] = {"type": "texture", "data": {"texture": f"{NS}/icons/{node}.png"}}
    json.dump(defs, open(dpath, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cpath = os.path.join(catdir, "category.json")
    cat = json.load(open(cpath, encoding="utf-8"))
    cat["background"] = {"texture": f"{NS}/background.png", "width": 1024, "height": 1024, "position": "fill"}
    cat["icon"] = {"type": "texture", "data": {"texture": f"{NS}/icons/ascendant_oath.png"}}
    json.dump(cat, open(cpath, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("applied:", catdir)

if __name__ == "__main__":
    for c in sys.argv[1:]:
        if os.path.isfile(os.path.join(c, "definitions.json")):
            apply(c)
        else:
            print("skip (no definitions):", c)
