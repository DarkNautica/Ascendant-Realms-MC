#!/usr/bin/env python3
"""Reorganize the Ascendant Web into an organic radial constellation:
  - root at center; each lane grows its OWN organic branch (seeded, no repeated template);
  - tasks inner, goals mid, challenge capstones outer; wide spacing w/ collision avoidance;
  - connections are UNIDIRECTIONAL prerequisites [parent -> child] = the unlock order
    (every node has exactly one prerequisite chain back to the root).
Also sets the category 'unlocked' connection color so traveled paths glow (single color;
Puffish connection colors are per-state category-wide, not per-lane).
Rewrites skills.json, connections.json, and category.json colors for each category dir passed.
"""
import json, os, sys, math
import numpy as np

LANES = ["warrior", "rogue", "ranger", "arcanist", "engineer", "survivalist", "dragonbound"]
SECTOR = 24.0                      # lane angular half-width (deg); lanes are ~51.4 apart
GATEWAY_R = 240                    # radius of each lane's gateway (depth-0) node
RING_GAP = 195                     # radius added per tree depth (planar tidy tree)
CHILD_CAP = 2                      # max children per node -> branching factor
BAND = {"task": (300, 720), "goal": (820, 1040), "challenge": (1120, 1380)}  # legacy, unused
MIN_DIST = 100                     # legacy, unused (only reported now)
UNLOCK_GLOW = {"fill": "#d4f2ff", "stroke": "#74e4ff"}

def tier_of(defs, k):
    fr = defs[k].get("frame", {}).get("data", {})
    if "frame" in fr:
        return fr["frame"]
    u = fr.get("unlocked", "")
    base = u.split("/")[-1]
    for t, name in (("task", "normal"), ("goal", "notable"), ("challenge", "major")):
        if f"_{name}_" in base:
            return t
    return "task"

def build(defs):
    # Planar radial tidy tree: each lane is its own sub-tree in a fixed angular
    # sector; a node's children fan out WITHIN that node's angular slice at the
    # next radius ring -> edges are short and never cross (readable, uncrossed).
    pos = {"ascendant_oath": (0, 0)}
    parent = {}
    order = {"task": 0, "goal": 1, "challenge": 2}
    for li, lane in enumerate(LANES):
        theta0 = -90 + li * (360.0 / len(LANES))
        nodes = [k for k in defs if k.split("_")[0] == lane]
        nodes.sort(key=lambda k: order.get(tier_of(defs, k), 9))
        # breadth-first B-ary tree (lower tiers shallow/inner, capstones deep/outer)
        gw = nodes[0]
        parent[gw] = "ascendant_oath"
        depth = {gw: 0}
        children = {gw: []}
        queue = [gw]; qi = 0
        for n in nodes[1:]:
            while len(children[queue[qi]]) >= CHILD_CAP:
                qi += 1
            par = queue[qi]
            parent[n] = par; children[par].append(n)
            depth[n] = depth[par] + 1; children[n] = []
            queue.append(n)
        # leaf weights for proportional angular slices
        leaves = {}
        def leafcount(n):
            if not children[n]:
                leaves[n] = 1; return 1
            c = sum(leafcount(x) for x in children[n]); leaves[n] = c; return c
        leafcount(gw)
        # recursive radial placement: node centered in its slice, children divide it
        def place(n, a0, a1):
            ang = (a0 + a1) / 2.0
            r = GATEWAY_R + depth[n] * RING_GAP
            pos[n] = (round(r * math.cos(math.radians(ang))), round(r * math.sin(math.radians(ang))))
            ch = children[n]
            if ch:
                tot = sum(leaves[x] for x in ch); acc = a0
                for x in ch:
                    w = (a1 - a0) * leaves[x] / tot
                    place(x, acc, acc + w); acc += w
        place(gw, theta0 - SECTOR, theta0 + SECTOR)
    conns = [[parent[k], k] for k in parent]            # unidirectional prereq -> dependent
    return pos, conns

def apply(catdir, pos, conns):
    sp = os.path.join(catdir, "skills.json")
    skills = json.load(open(sp, encoding="utf-8"))
    for node, v in skills.items():
        if node in pos: v["x"], v["y"] = pos[node]
    json.dump(skills, open(sp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cp = os.path.join(catdir, "connections.json")
    json.dump({"normal": {"unidirectional": conns}}, open(cp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    catp = os.path.join(catdir, "category.json")
    cat = json.load(open(catp, encoding="utf-8"))
    cat.setdefault("colors", {})["connections"] = {"unlocked": UNLOCK_GLOW}
    json.dump(cat, open(catp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"applied {len(pos)} positions, {len(conns)} unidirectional connections -> {catdir}")

if __name__ == "__main__":
    dirs = sys.argv[1:]
    defs = json.load(open(os.path.join(dirs[0], "definitions.json"), encoding="utf-8"))
    pos, conns = build(defs)
    # reachability from root following direction parent->child
    childmap = {}
    for a, b in conns: childmap.setdefault(a, []).append(b)
    seen = {"ascendant_oath"}; stack = ["ascendant_oath"]
    while stack:
        for n in childmap.get(stack.pop(), []):
            if n not in seen: seen.add(n); stack.append(n)
    missing = set(defs) - seen
    print("reachable from root:", len(seen), "/", len(defs), "| missing:", sorted(missing) if missing else "none")
    if missing: raise SystemExit("ABORT: unreachable nodes")
    # min distance report
    pts = list(pos.values()); mind = 1e9
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            d = ((pts[i][0]-pts[j][0])**2+(pts[i][1]-pts[j][1])**2)**.5; mind = min(mind, d)
    print("min node distance:", round(mind, 1), "px")
    for d in dirs: apply(d, pos, conns)
