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
SECTOR = 23.0                      # lane angular half-width (deg); lanes are ~51.4 apart
BAND = {"task": (205, 475), "goal": (525, 665), "challenge": (715, 855)}
GATEWAY_R = 205
MIN_DIST = 86                      # min px between any two nodes
CHILD_CAP = 3
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
    rng_global = np.random.default_rng(20260618)
    placed = [("ascendant_oath", 0.0, 0.0)]          # (id, x, y)
    pos = {"ascendant_oath": (0, 0)}
    parent = {}
    def far_enough(x, y):
        return all((x-px)**2 + (y-py)**2 >= MIN_DIST*MIN_DIST for _, px, py in placed)
    for li, lane in enumerate(LANES):
        rng = np.random.default_rng(1000 + li)
        theta0 = -90 + li * (360.0 / len(LANES))
        nodes = [k for k in defs if k.split("_")[0] == lane]
        order = {"task": 0, "goal": 1, "challenge": 2}
        nodes.sort(key=lambda k: order.get(tier_of(defs, k), 9))
        lane_nodes = []   # (id, x, y, r, ang)
        # gateway
        gang = theta0 + float(rng.uniform(-4, 4))
        gx, gy = GATEWAY_R*math.cos(math.radians(gang)), GATEWAY_R*math.sin(math.radians(gang))
        pos[nodes[0]] = (round(gx), round(gy)); parent[nodes[0]] = "ascendant_oath"
        placed.append((nodes[0], gx, gy)); lane_nodes.append((nodes[0], gx, gy, GATEWAY_R, gang))
        childcount = {nodes[0]: 0}
        # counts per tier for radius progression
        tiers = [tier_of(defs, k) for k in nodes]
        idx_in_tier = {}; seen = {}
        for k, t in zip(nodes, tiers):
            seen[t] = seen.get(t, 0); idx_in_tier[k] = seen[t]; seen[t] += 1
        tcount = {t: tiers.count(t) for t in set(tiers)}
        for k in nodes[1:]:
            t = tier_of(defs, k)
            lo, hi = BAND[t]
            prog = idx_in_tier[k] / max(1, tcount[t]-1)
            base_r = lo + prog*(hi-lo)
            best = None
            for attempt in range(28):
                tr = base_r + float(rng.uniform(-35, 45))
                cands = [n for n in lane_nodes if n[3] <= tr-55 and childcount.get(n[0], 0) < CHILD_CAP]
                if not cands:
                    cands = [n for n in lane_nodes if n[3] < tr-10] or [lane_nodes[0]]
                # prefer inner, fewer children, nearer radius
                w = []
                for n in cands:
                    w.append(1.0/(1+childcount.get(n[0],0)) * 1.0/(1+abs(n[3]-tr)/120.0))
                w = np.array(w); w /= w.sum()
                par = cands[int(rng.choice(len(cands), p=w))]
                spread = float(rng.uniform(8, 26))
                ang = par[4] + float(rng.uniform(-spread, spread))
                ang = max(theta0-SECTOR, min(theta0+SECTOR, ang))
                x, y = tr*math.cos(math.radians(ang)), tr*math.sin(math.radians(ang))
                if far_enough(x, y):
                    best = (par, x, y, tr, ang); break
                if best is None or tr > (best[3] if best else 0):
                    best = (par, x, y, tr, ang)   # fallback keep last
            par, x, y, tr, ang = best
            pos[k] = (round(x), round(y)); parent[k] = par[0]
            childcount[par[0]] = childcount.get(par[0], 0) + 1
            childcount.setdefault(k, 0)
            placed.append((k, x, y)); lane_nodes.append((k, x, y, tr, ang))
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
