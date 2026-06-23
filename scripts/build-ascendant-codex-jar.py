#!/usr/bin/env python3
"""Zip the Ascendant Codex book mod (lowcodefml) from local-mods/ascendant-codex-book/src/
into the jar, and deploy to the active instance mods/ folder."""
import os, zipfile, glob, json, shutil
STAGE="local-mods/ascendant-codex-book/src"
JAR="local-mods/ascendant-codex-book/ascendant-codex-1.0.0.jar"
INST_MODS="/sessions/loving-amazing-gates/mnt/Ascendant Realms (2)/mods"
# validate all json first
bad=0
for p in glob.glob(STAGE+"/**/*.json",recursive=True):
    try: json.load(open(p,encoding="utf-8"))
    except Exception as e: print("BAD JSON",p,e); bad+=1
assert bad==0, "fix json first"
with zipfile.ZipFile(JAR,"w",zipfile.ZIP_DEFLATED) as z:
    for root,_,files in os.walk(STAGE):
        for fn in files:
            full=os.path.join(root,fn); arc=os.path.relpath(full,STAGE).replace("\\","/")
            z.write(full,arc)
shutil.copy(JAR, INST_MODS)
with zipfile.ZipFile(JAR) as z: n=len(z.namelist())
print(f"built + deployed jar ({n} entries, {os.path.getsize(JAR)} bytes) -> {INST_MODS}")
