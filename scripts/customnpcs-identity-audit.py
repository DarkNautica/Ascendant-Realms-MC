#!/usr/bin/env python3
"""Audit and repair Ascendant Realms CustomNPC identity data in a world save.

This repairs the actual per-entity CustomNPCs data, including the embedded
script copy stored inside each authored NPC. Updating the script file alone is
not enough because CustomNPCs serializes scripts into the NPC entity.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import math
import shutil
import struct
import subprocess
import sys
import time
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import nbtlib
except Exception as exc:  # pragma: no cover - actionable CLI error
    raise SystemExit(
        "Missing Python package nbtlib. Install with: python -m pip install nbtlib"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INSTANCES_ROOT = Path(r"C:\Users\Jayden\curseforge\minecraft\Instances")
SCRIPT_PATH = ROOT / "customnpcs/scripts/ecmascript/ascendant_npc_identity.js"
NAMEPLATES_PATH = ROOT / "config/ascendant_guild/nameplates.json"

SECTION = "\u00a7"
RANKS = {
    "unranked": ("Unranked", "7"),
    "e_rank": ("E-Rank", "2"),
    "d_rank": ("D-Rank", "a"),
    "c_rank": ("C-Rank", "9"),
    "b_rank": ("B-Rank", "6"),
    "a_rank": ("A-Rank", "e"),
    "s_rank": ("S-Rank", "d"),
}
STYLE_IDS = {"guild_staff"}


def latest_ascendant_instance() -> Path:
    instances = [
        path
        for path in DEFAULT_INSTANCES_ROOT.glob("Ascendant Realms*")
        if path.is_dir()
    ]
    if not instances:
        return DEFAULT_INSTANCES_ROOT / "Ascendant Realms"
    return max(instances, key=lambda path: path.stat().st_mtime)


@dataclass
class ChunkRecord:
    path: Path
    local_x: int
    local_z: int
    nbt: nbtlib.File
    dirty: bool = False


def read_chunk(path: Path, local_x: int, local_z: int) -> nbtlib.File | None:
    with path.open("rb") as handle:
        header = handle.read(8192)
        index = 4 * (local_x + local_z * 32)
        offset = int.from_bytes(header[index : index + 3], "big")
        if offset == 0:
            return None
        handle.seek(offset * 4096)
        length = struct.unpack(">I", handle.read(4))[0]
        compression = handle.read(1)[0]
        payload = handle.read(length - 1)
    if compression == 1:
        data = gzip.decompress(payload)
    elif compression == 2:
        data = zlib.decompress(payload)
    elif compression == 3:
        data = payload
    else:
        raise ValueError(f"{path} chunk {local_x},{local_z} uses unknown compression {compression}")
    return nbtlib.File.parse(io.BytesIO(data))


def write_chunk(record: ChunkRecord) -> None:
    raw = io.BytesIO()
    record.nbt.write(raw, byteorder="big")
    compressed = zlib.compress(raw.getvalue())
    chunk_blob = struct.pack(">I", len(compressed) + 1) + bytes([2]) + compressed
    sectors_needed = math.ceil(len(chunk_blob) / 4096)
    chunk_blob += bytes(sectors_needed * 4096 - len(chunk_blob))

    with record.path.open("r+b") as handle:
        header = bytearray(handle.read(8192))
        index = 4 * (record.local_x + record.local_z * 32)
        old_offset = int.from_bytes(header[index : index + 3], "big")
        old_sectors = header[index + 3]

        if old_offset and sectors_needed <= old_sectors:
            offset = old_offset
        else:
            handle.seek(0, 2)
            offset = math.ceil(handle.tell() / 4096)
            handle.seek(offset * 4096)

        if sectors_needed > 255:
            raise ValueError(f"Chunk too large to write into region header: {record.path} {record.local_x},{record.local_z}")

        header[index : index + 3] = offset.to_bytes(3, "big")
        header[index + 3] = sectors_needed
        timestamp_index = 4096 + index
        header[timestamp_index : timestamp_index + 4] = int(time.time()).to_bytes(4, "big")

        handle.seek(0)
        handle.write(header)
        handle.seek(offset * 4096)
        handle.write(chunk_blob)


def minecraft_running() -> bool:
    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "Get-Process javaw -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return False
    return bool(output.strip())


def load_profiles() -> dict[str, dict[str, str]]:
    data = json.loads(NAMEPLATES_PATH.read_text(encoding="utf-8-sig"))
    profiles: dict[str, dict[str, str]] = {}
    for profile_id, profile in data.get("profiles", {}).items():
        rank_id = str(profile.get("rank", "unranked"))
        rank_label, color_code = RANKS.get(rank_id, ("Unranked", "7"))
        profiles[profile_id] = {
            "id": profile_id,
            "name": str(profile.get("display", profile_id)),
            "rank": rank_label,
            "role": str(profile.get("profession", "")),
            "level": normalize_level(profile.get("level", "1")),
            "color_code": color_code,
        }
    return profiles


def normalize_level(value: Any) -> str:
    text = str(value)
    if "." in text:
        text = text.split(".", 1)[0]
    return text if text and text.lower() not in {"nan", "none", "null", "undefined"} else "1"


def tag_string(value: str) -> nbtlib.String:
    return nbtlib.String(value)


def tag_int(value: int) -> nbtlib.Int:
    return nbtlib.Int(value)


def ensure_compound(parent: nbtlib.Compound, key: str) -> nbtlib.Compound:
    if key not in parent or not isinstance(parent[key], nbtlib.Compound):
        parent[key] = nbtlib.Compound()
    return parent[key]


def strip_formatting(value: str) -> str:
    output: list[str] = []
    skip = False
    for char in value:
        if skip:
            skip = False
            continue
        if char == SECTION:
            skip = True
            continue
        output.append(char)
    return "".join(output)


def clean_key(value: str) -> str:
    text = strip_formatting(value).lower()
    for before, after in [
        ("ar:", ""),
        ("\\r", "_"),
        ("\\n", "_"),
        ("\r", "_"),
        ("\n", "_"),
        (" ", "_"),
        ("-", "_"),
        ("[", ""),
        ("]", ""),
        ("|", "_"),
        (".", ""),
    ]:
        text = text.replace(before, after)
    return text


def profile_from_entity(entity: nbtlib.Compound, profiles: dict[str, dict[str, str]]) -> str | None:
    forge_data = entity.get("ForgeData", nbtlib.Compound())
    stored = forge_data.get("CNPCStoredData", nbtlib.Compound()) if isinstance(forge_data, nbtlib.Compound) else {}
    candidates = [
        str(stored.get("ar_profile", "")) if hasattr(stored, "get") else "",
        str(entity.get("CustomName", "")),
        str(entity.get("Name", "")),
    ]
    for candidate in candidates:
        key = clean_key(candidate)
        for profile_id, profile in profiles.items():
            compact = profile_id.replace("_", "")
            display_key = clean_key(profile["name"])
            if profile_id in key or compact in key or display_key in key:
                return profile_id
    return None


def format_name(profile: dict[str, str]) -> str:
    color = profile["color_code"]
    return (
        f"{SECTION}{color}[{profile['rank']}] "
        f"{SECTION}f{profile['name']} "
        f"{SECTION}8| {SECTION}7Lv.{profile['level']} "
        f"{SECTION}{color}{profile['role']}"
    )


def expected_custom_name(profile_id: str) -> str:
    color = "gold" if profile_id == "rank_examiner" else "aqua"
    return json.dumps({"italic": False, "color": color, "text": f"ar:{profile_id}"}, separators=(",", ":"))


def update_scripts(entity: nbtlib.Compound, script_text: str) -> bool:
    changed = False
    scripts = entity.get("Scripts")
    if not scripts:
        entity["Scripts"] = nbtlib.List[nbtlib.Compound](
            [
                nbtlib.Compound(
                    {
                        "Script": tag_string(script_text),
                        "Console": nbtlib.List[nbtlib.Compound]([]),
                        "ScriptList": nbtlib.List[nbtlib.Compound]([nbtlib.Compound({"Line": tag_string("ascendant_npc_identity.js")})]),
                    }
                )
            ]
        )
        return True
    first = scripts[0]
    if str(first.get("Script", "")) != script_text:
        first["Script"] = tag_string(script_text)
        changed = True
    if "ScriptList" not in first or "ascendant_npc_identity.js" not in str(first.get("ScriptList", "")):
        first["ScriptList"] = nbtlib.List[nbtlib.Compound]([nbtlib.Compound({"Line": tag_string("ascendant_npc_identity.js")})])
        changed = True
    if "Console" not in first:
        first["Console"] = nbtlib.List[nbtlib.Compound]([])
        changed = True
    return changed


def audit_entity(entity: nbtlib.Compound, profiles: dict[str, dict[str, str]], script_text: str, apply: bool) -> tuple[list[str], bool]:
    issues: list[str] = []
    changed = False
    profile_id = profile_from_entity(entity, profiles)
    if not profile_id:
        return issues, changed

    profile = profiles[profile_id]
    expected_name = format_name(profile)
    current_name = str(entity.get("Name", ""))
    current_title = str(entity.get("Title", ""))
    current_custom_name = str(entity.get("CustomName", ""))
    forge_data = ensure_compound(entity, "ForgeData")
    stored = ensure_compound(forge_data, "CNPCStoredData")

    expected_fields = {
        "Name": expected_name,
        "Title": "",
        "CustomName": expected_custom_name(profile_id),
    }
    for key, expected in expected_fields.items():
        if str(entity.get(key, "")) != expected:
            issues.append(f"{profile_id}: {key} {str(entity.get(key, ''))!r} -> {expected!r}")
            if apply:
                entity[key] = tag_string(expected)
                changed = True

    if int(entity.get("ShowName", 0)) != 0:
        issues.append(f"{profile_id}: ShowName {entity.get('ShowName')} -> 0")
        if apply:
            entity["ShowName"] = tag_int(0)
            changed = True

    if int(entity.get("ScriptEnabled", 0)) != 1:
        issues.append(f"{profile_id}: ScriptEnabled {entity.get('ScriptEnabled')} -> 1")
        if apply:
            entity["ScriptEnabled"] = nbtlib.Byte(1)
            changed = True

    stored_expected = {
        "ar_profile": profile_id,
        "ar_name": profile["name"],
        "ar_rank": profile["rank"],
        "ar_role": profile["role"],
        "ar_level": profile["level"],
    }
    for key, expected in stored_expected.items():
        if str(stored.get(key, "")) != expected:
            issues.append(f"{profile_id}: CNPCStoredData.{key} {str(stored.get(key, ''))!r} -> {expected!r}")
            if apply:
                stored[key] = tag_string(expected)
                changed = True

    if str(stored.get("ar_rank", "")) in STYLE_IDS:
        issues.append(f"{profile_id}: stale style id stored as rank: {stored.get('ar_rank')}")

    scripts = entity.get("Scripts")
    embedded_script = str(scripts[0].get("Script", "")) if scripts else ""
    if embedded_script != script_text:
        issues.append(f"{profile_id}: embedded script is stale")
        if apply:
            changed = update_scripts(entity, script_text) or changed

    return issues, changed


def iter_chunk_records(world: Path) -> list[ChunkRecord]:
    records: list[ChunkRecord] = []
    entities_dir = world / "entities"
    if not entities_dir.exists():
        return records
    for region_path in sorted(entities_dir.glob("r.*.*.mca")):
        for local_x in range(32):
            for local_z in range(32):
                try:
                    nbt = read_chunk(region_path, local_x, local_z)
                except Exception as exc:
                    print(f"warning: failed to read {region_path.name} chunk {local_x},{local_z}: {exc}", file=sys.stderr)
                    continue
                if nbt is not None and "Entities" in nbt:
                    records.append(ChunkRecord(region_path, local_x, local_z, nbt))
    return records


def backup_region(path: Path, backup_root: Path) -> None:
    backup_root.mkdir(parents=True, exist_ok=True)
    target = backup_root / path.name
    if not target.exists():
        shutil.copy2(path, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", default=str(latest_ascendant_instance() / "saves/New World"))
    parser.add_argument("--apply", action="store_true", help="repair matching CustomNPC entities")
    parser.add_argument("--force", action="store_true", help="allow writes even if Minecraft appears to be running")
    args = parser.parse_args()

    world = Path(args.world)
    if not world.exists():
        raise SystemExit(f"World not found: {world}")
    if args.apply and minecraft_running() and not args.force:
        raise SystemExit(
            "Minecraft is running. Close the world/client before applying offline entity repairs, "
            "or rerun with --force if you intentionally accept overwrite risk."
        )

    profiles = load_profiles()
    script_text = SCRIPT_PATH.read_text(encoding="utf-8")
    script_hash = hashlib.sha256(script_text.encode("utf-8")).hexdigest()[:12]
    print(f"World: {world}")
    print(f"Identity script: {SCRIPT_PATH} ({script_hash})")

    records = iter_chunk_records(world)
    total_entities = 0
    matched_entities = 0
    issue_count = 0
    changed_regions: set[Path] = set()

    for record in records:
        entities = record.nbt.get("Entities", [])
        total_entities += len(entities)
        for entity in entities:
            if str(entity.get("id", "")) != "customnpcs:customnpc":
                continue
            issues, changed = audit_entity(entity, profiles, script_text, args.apply)
            if not issues and not changed:
                continue
            matched_entities += 1
            issue_count += len(issues)
            pos = str(entity.get("Pos", "unknown"))
            print(f"\nCustomNPC at {record.path.name} chunk {record.local_x},{record.local_z} pos={pos}")
            for issue in issues:
                print(f"- {issue}")
            if changed:
                record.dirty = True
                changed_regions.add(record.path)

    if args.apply:
        backup_root = world / "ascendant_backups" / f"customnpcs_identity_{int(time.time())}"
        for region_path in sorted(changed_regions):
            backup_region(region_path, backup_root)
        for record in records:
            if record.dirty:
                write_chunk(record)
        print(f"\nApplied repairs to {sum(1 for record in records if record.dirty)} chunks.")
        if changed_regions:
            print(f"Backups written under: {backup_root}")
    else:
        print("\nDry run only. Re-run with --apply after closing Minecraft to repair the world save.")

    print(f"Scanned {total_entities} entities; matched {matched_entities} CustomNPC identity records; issues={issue_count}.")
    return 1 if issue_count and not args.apply else 0


if __name__ == "__main__":
    raise SystemExit(main())
