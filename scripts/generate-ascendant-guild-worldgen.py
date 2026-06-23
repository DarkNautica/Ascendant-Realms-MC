#!/usr/bin/env python3
"""Generate Ascendant Guild NPC, contract, and standalone worldgen data."""

from __future__ import annotations

import json
import pathlib
import shutil
from dataclasses import dataclass
from typing import Any

import nbtlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK_NAMES = [
    "config/openloader/data/ascendant_realms_guild",
    "openloader/data/ascendant_realms_guild",
]
CUSTOMNPCS_IDENTITY_SCRIPT = ROOT / "customnpcs/scripts/ecmascript/ascendant_npc_identity.js"
DATA_VERSION_1_20_1 = 3465


def read_json(relative_path: str) -> Any:
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(relative_path: str, data: Any) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_text(relative_path: str, text: str) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n").strip() + "\n", encoding="utf-8")


def clear_pack(relative_path: str) -> None:
    path = ROOT / relative_path
    if not path.exists():
        return
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            child.rmdir()


def slug(value: str) -> str:
    out = []
    for char in value.lower():
        if char.isalnum():
            out.append(char)
        elif char in (" ", "-", "_", "'", ".", ":"):
            out.append("_")
    text = "".join(out)
    while "__" in text:
        text = text.replace("__", "_")
    return text.strip("_")


def snbt_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def compact_npc_script(value: str) -> str:
    compact_lines: list[str] = []
    for raw_line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if "//" in line:
            line = line.split("//", 1)[0].rstrip()
        if line:
            compact_lines.append(line)
    return " ".join(compact_lines)


def npc_script_nbt() -> str:
    script_text = compact_npc_script(CUSTOMNPCS_IDENTITY_SCRIPT.read_text(encoding="utf-8"))
    return (
        "Scripts:[{"
        f"Script:{snbt_string(script_text)},"
        "Console:[],"
        'ScriptList:[{Line:"ascendant_npc_identity.js"}]'
        "}],"
    )


RANK_COLORS = {
    "Unranked": "\u00a77",
    "E-Rank": "\u00a72",
    "D-Rank": "\u00a7a",
    "C-Rank": "\u00a79",
    "B-Rank": "\u00a76",
    "A-Rank": "\u00a7e",
    "S-Rank": "\u00a7d",
}


NPC_SKINS = {
    "guild_clerk": "customnpcs:textures/entity/ascendant_mca/guild_clerk.png",
    "bounty_master": "customnpcs:textures/entity/ascendant_mca/bounty_master.png",
    "rank_examiner": "customnpcs:textures/entity/ascendant_mca/rank_examiner.png",
    "guild_arcanist": "customnpcs:textures/entity/ascendant_mca/guild_arcanist.png",
    "hunter_quartermaster": "customnpcs:textures/entity/ascendant_mca/hunter_quartermaster.png",
    "guard_captain": "customnpcs:textures/entity/ascendant_mca/guard_captain.png",
    "tavern_keeper": "customnpcs:textures/entity/ascendant_mca/tavern_keeper.png",
    "village_elder": "customnpcs:textures/entity/ascendant_mca/village_elder.png",
    "wounded_hunter": "customnpcs:textures/entity/ascendant_mca/wounded_hunter.png",
    "mira_ash": "customnpcs:textures/entity/ascendant_mca/mira_ash.png",
    "darius_crowe": "customnpcs:textures/entity/ascendant_mca/darius_crowe.png",
    "seren_valehart": "customnpcs:textures/entity/ascendant_mca/seren_valehart.png",
}

ASCENDANT_SKIN_RESOURCE_ROOT = pathlib.Path("assets/customnpcs/textures/entity/ascendant_mca")
ASCENDANT_SKIN_SOURCE_ROOT = (
    ROOT
    / "resourcepacks/ascendant-realms-compat-fixes"
    / ASCENDANT_SKIN_RESOURCE_ROOT
)
ASCENDANT_SKIN_CUSTOMNPCS_ROOT = ROOT / "customnpcs" / ASCENDANT_SKIN_RESOURCE_ROOT

COMBAT_PROFILES = {
    "guard_captain",
    "wounded_hunter",
    "mira_ash",
    "darius_crowe",
    "seren_valehart",
}


def loadout_by_profile() -> dict[str, dict[str, Any]]:
    loadouts = read_json("config/ascendant_guild/npc_loadouts.json")
    profiles: dict[str, dict[str, Any]] = {}
    for section in ("archetypes", "npc_profiles"):
        for profile_id, profile in loadouts.get(section, {}).items():
            profiles[profile_id] = profile
    return profiles


NPC_LOADOUTS = loadout_by_profile()


NPC_PROFILE_SOURCE = [
    {
        "id": "guild_clerk",
        "name": "Guild Clerk",
        "rank": "D-Rank",
        "level": 18,
        "role": "Clerk",
        "placement": "village_hunter_board",
        "spawn_weight": 10,
        "line": "New contracts are posted at dawn and dusk.",
    },
    {
        "id": "bounty_master",
        "name": "Bounty Master",
        "rank": "C-Rank",
        "level": 38,
        "role": "Contracts",
        "placement": "town_guild_board",
        "spawn_weight": 8,
        "line": "Choose the work you can finish. The board remembers failures.",
    },
    {
        "id": "rank_examiner",
        "name": "Rank Examiner",
        "rank": "B-Rank",
        "level": 52,
        "role": "Examiner",
        "placement": "frontier_guild_outpost",
        "spawn_weight": 4,
        "line": "Rank is not a costume. Bring proof.",
    },
    {
        "id": "guild_arcanist",
        "name": "Guild Arcanist",
        "rank": "B-Rank",
        "level": 49,
        "role": "Arcanist",
        "placement": "frontier_guild_outpost",
        "spawn_weight": 4,
        "line": "Magic leaves evidence. Monsters do too.",
    },
    {
        "id": "hunter_quartermaster",
        "name": "Quartermaster",
        "rank": "D-Rank",
        "level": 24,
        "role": "Supplies",
        "placement": "town_guild_board",
        "spawn_weight": 6,
        "line": "Guild Marks buy preparation, not courage.",
    },
    {
        "id": "guard_captain",
        "name": "Guard Captain",
        "rank": "C-Rank",
        "level": 36,
        "role": "Captain",
        "placement": "village_hunter_board",
        "spawn_weight": 5,
        "line": "If the road goes quiet, it is already too late.",
    },
    {
        "id": "tavern_keeper",
        "name": "Tavern Keeper",
        "rank": "D-Rank",
        "level": 16,
        "role": "Rumors",
        "placement": "roadside_hunter_camp",
        "spawn_weight": 8,
        "line": "I hear things before the board writes them down.",
    },
    {
        "id": "village_elder",
        "name": "Village Elder",
        "rank": "D-Rank",
        "level": 22,
        "role": "Elder",
        "placement": "village_hunter_board",
        "spawn_weight": 6,
        "line": "A safe village is made one promise at a time.",
    },
    {
        "id": "wounded_hunter",
        "name": "Wounded Hunter",
        "rank": "C-Rank",
        "level": 31,
        "role": "Hunter",
        "placement": "roadside_hunter_camp",
        "spawn_weight": 3,
        "line": "Do not follow the tracks after moonrise.",
    },
    {
        "id": "mira_ash",
        "name": "Mira Ash",
        "rank": "C-Rank",
        "level": 34,
        "role": "Scout",
        "placement": "roadside_hunter_camp",
        "spawn_weight": 2,
        "line": "I marked three ruins nearby. One is watching back.",
    },
    {
        "id": "darius_crowe",
        "name": "Darius Crowe",
        "rank": "B-Rank",
        "level": 47,
        "role": "Duelist",
        "placement": "town_guild_board",
        "spawn_weight": 2,
        "line": "Try not to make the contract boring.",
    },
    {
        "id": "seren_valehart",
        "name": "Seren Valehart",
        "rank": "B-Rank",
        "level": 45,
        "role": "Arcanist",
        "placement": "frontier_guild_outpost",
        "spawn_weight": 2,
        "line": "The spell residue here is wrong.",
    },
]


SPAWN_SETS = [
    {
        "id": "starter_guild_staff",
        "description": "Core social test group for a fresh Guild board.",
        "members": [
            {"profile": "guild_clerk", "offset": [0, 0, 0]},
            {"profile": "bounty_master", "offset": [2, 0, 1]},
            {"profile": "rank_examiner", "offset": [-2, 0, 1]},
            {"profile": "guard_captain", "offset": [0, 0, 3]},
        ],
    },
    {
        "id": "roadside_rumor_camp",
        "description": "Roadside social/rival test set.",
        "members": [
            {"profile": "tavern_keeper", "offset": [0, 0, 0]},
            {"profile": "wounded_hunter", "offset": [2, 0, 0]},
            {"profile": "mira_ash", "offset": [-2, 0, 1]},
        ],
    },
    {
        "id": "frontier_guild_outpost",
        "description": "Higher-rank outpost NPC set for the first worldgen structures.",
        "members": [
            {"profile": "rank_examiner", "offset": [0, 0, 0]},
            {"profile": "guild_arcanist", "offset": [2, 0, 1]},
            {"profile": "hunter_quartermaster", "offset": [-2, 0, 1]},
            {"profile": "seren_valehart", "offset": [0, 0, 3]},
        ],
    },
]


NPC_BEHAVIOR_POLICY = {
    "guild_clerk": {
        "relationship_gate": "guild_staff",
        "command_policy": "explain_only",
        "service_min_relation": "stranger",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Explains Guild systems and points to boards. Never follows player commands.",
    },
    "bounty_master": {
        "relationship_gate": "contract_broker",
        "command_policy": "board_contracts_only",
        "service_min_relation": "familiar",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Can direct players to work after familiarity, but does not accept field orders.",
    },
    "rank_examiner": {
        "relationship_gate": "public_authority",
        "command_policy": "rank_evaluation_only",
        "service_min_relation": "stranger",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "May run the internal rank-evaluation function as a public Guild service. Not a companion.",
    },
    "guild_arcanist": {
        "relationship_gate": "expert_advisor",
        "command_policy": "lore_and_magic_advice_only",
        "service_min_relation": "familiar",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Provides magic advice and future services by trust/rank, not player command.",
    },
    "hunter_quartermaster": {
        "relationship_gate": "supplier",
        "command_policy": "rank_limited_supply_only",
        "service_min_relation": "familiar",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Future trade/supply access should require rank, currency, and relation.",
    },
    "guard_captain": {
        "relationship_gate": "settlement_guard",
        "command_policy": "settlement_defense_only",
        "service_min_relation": "trusted",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Commands local guards; player respect unlocks warnings, not obedience.",
    },
    "tavern_keeper": {
        "relationship_gate": "rumor_source",
        "command_policy": "rumors_only",
        "service_min_relation": "stranger",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Shares rumors by familiarity. Never follows or fights for the player.",
    },
    "village_elder": {
        "relationship_gate": "settlement_elder",
        "command_policy": "local_needs_only",
        "service_min_relation": "familiar",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Trust comes from protecting the settlement. No command obedience.",
    },
    "wounded_hunter": {
        "relationship_gate": "field_contact",
        "command_policy": "warnings_and_rescue_hooks_only",
        "service_min_relation": "familiar",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Can become a quest/contact later; should not instantly become a follower.",
    },
    "mira_ash": {
        "relationship_gate": "rival_hunter",
        "command_policy": "rival_dialogue_only",
        "service_min_relation": "trusted",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Rival hunter. Cooperation must be earned through rivalry/quests.",
    },
    "darius_crowe": {
        "relationship_gate": "rival_hunter",
        "command_policy": "rival_dialogue_only",
        "service_min_relation": "trusted",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Rival hunter. Does not accept player orders.",
    },
    "seren_valehart": {
        "relationship_gate": "rival_hunter",
        "command_policy": "rival_dialogue_only",
        "service_min_relation": "trusted",
        "can_follow": False,
        "can_take_orders": False,
        "obedience_note": "Rival hunter/arcanist. Advice and cooperation require trust.",
    },
}


def profile_behavior(profile_id: str) -> dict[str, Any]:
    return NPC_BEHAVIOR_POLICY.get(
        profile_id,
        {
            "relationship_gate": "generic_npc",
            "command_policy": "dialogue_only",
            "service_min_relation": "trusted",
            "can_follow": False,
            "can_take_orders": False,
            "obedience_note": "Generic NPCs should never become instant followers.",
        },
    )


def npc_display(profile: dict[str, Any]) -> str:
    color = RANK_COLORS.get(profile["rank"], "\u00a77")
    return f"{color}[{profile['rank']}] \u00a7f{profile['name']} \u00a78| \u00a77Lv.{profile['level']} {color}{profile['role']}"


def snbt_item(item_id: str | None) -> str:
    if not item_id:
        return "{}"
    return f'{{id:"{item_id}",Count:1b}}'


def profile_equipment(profile: dict[str, Any]) -> dict[str, str]:
    loadout = NPC_LOADOUTS.get(profile["id"], {})
    equipment = loadout.get("equipment", {})
    return {slot: str(item["item"]) for slot, item in equipment.items() if item.get("item")}


def npc_inventory_nbt(profile: dict[str, Any]) -> str:
    equipment = profile_equipment(profile)
    mainhand = equipment.get("mainhand")
    offhand = equipment.get("offhand")
    head = equipment.get("head")
    chest = equipment.get("chest")
    legs = equipment.get("legs")
    feet = equipment.get("feet")

    # CustomNPCs reads rendered NPC gear from top-level Weapons/Armor maps.
    # NpcInv is the NPC drop table, so keep it empty to avoid visual kits
    # becoming farmable. Vanilla HandItems/ArmorItems stay as a fallback for
    # other entity equipment readers.
    weapons = []
    if mainhand:
        weapons.append(f'{{Slot:0,id:"{mainhand}",Count:1b}}')
    if offhand:
        weapons.append(f'{{Slot:2,id:"{offhand}",Count:1b}}')
    armor = []
    for slot, item_id in ((0, feet), (1, legs), (2, chest), (3, head)):
        if item_id:
            armor.append(f'{{Slot:{slot},id:"{item_id}",Count:1b}}')

    return (
        "NpcInv:[],"
        f'Weapons:[{",".join(weapons)}],'
        f'Armor:[{",".join(armor)}],'
        "DropChance:[],"
        "LootMode:0,"
        "MinExp:0,"
        "MaxExp:0,"
        f"HandItems:[{snbt_item(mainhand)},{snbt_item(offhand)}],"
        f"ArmorItems:[{snbt_item(feet)},{snbt_item(legs)},{snbt_item(chest)},{snbt_item(head)}],"
        "HandDropChances:[0.0f,0.0f],"
        "ArmorDropChances:[0.0f,0.0f,0.0f,0.0f],"
        "CanPickUpLoot:0b,"
    )


def npc_ai_nbt(profile: dict[str, Any]) -> str:
    is_combat = profile["id"] in COMBAT_PROFILES
    if is_combat:
        return (
            "MovingState:1,"
            "WalkingRange:10,"
            "ActiveRange:32,"
            "MoveSpeed:5,"
            "OnAttack:1,"
            "ReturnToStart:1b,"
            "DirectLOS:1b,"
            "CanSprint:1b,"
            "CanLeap:0b,"
            "AttackInvisible:0b,"
            "npcInteracting:1b,"
            "stopAndInteract:1b,"
        )
    return (
        "MovingState:0,"
        "WalkingRange:1,"
        "ActiveRange:24,"
        "MoveSpeed:3,"
        "OnAttack:1,"
        "ReturnToStart:1b,"
        "DirectLOS:1b,"
        "CanSprint:0b,"
        "CanLeap:0b,"
        "AttackInvisible:0b,"
        "npcInteracting:1b,"
        "stopAndInteract:1b,"
    )


def npc_nbt(profile: dict[str, Any]) -> str:
    display = npc_display(profile)
    custom = json.dumps({"italic": False, "color": "gold", "text": f"ar:{profile['id']}"}, separators=(",", ":"))
    texture = NPC_SKINS.get(profile["id"], "customnpcs:textures/entity/humanmale/guardsteve.png")
    behavior = profile_behavior(profile["id"])
    return (
        "{"
        f'Name:"{display}",'
        'Title:"",'
        f'Texture:"{texture}",'
        'SkinUrl:"",'
        'UsingSkinUrl:0b,'
        'SkinUsername:"",'
        'CloakTexture:"",'
        'GlowTexture:"",'
        "ShowName:0,"
        "ScriptEnabled:1b,"
        f"{npc_script_nbt()}"
        f"{npc_ai_nbt(profile)}"
        f"{npc_inventory_nbt(profile)}"
        f'CustomName:\'{custom}\','
        'Tags:["ar_guild_npc",'
        f'"ar_profile_{profile["id"]}",'
        f'"ar_rank_{slug(profile["rank"])}"],'
        "ForgeData:{CNPCStoredData:{"
        f'ar_profile:"{profile["id"]}",'
        f'ar_name:"{profile["name"]}",'
        f'ar_rank:"{profile["rank"]}",'
        f'ar_role:"{profile["role"]}",'
        f'ar_level:"{profile["level"]}",'
        f'ar_relationship_gate:"{behavior["relationship_gate"]}",'
        f'ar_command_policy:"{behavior["command_policy"]}",'
        f'ar_service_min_relation:"{behavior["service_min_relation"]}",'
        f'ar_can_follow:"{str(behavior["can_follow"]).lower()}",'
        f'ar_can_take_orders:"{str(behavior["can_take_orders"]).lower()}",'
        f'ar_obedience_note:{snbt_string(behavior["obedience_note"])}'
        "}}"
        "}"
    )


def write_npc_functions(base: str) -> None:
    profiles_by_id = {profile["id"]: profile for profile in NPC_PROFILE_SOURCE}
    for profile in NPC_PROFILE_SOURCE:
        write_text(
            f"{base}/data/ascendant_guild/functions/npc/spawn_{profile['id']}.mcfunction",
            "\n".join(
                [
                    f"# Generated profile: {profile['id']}",
                    f"summon customnpcs:customnpc ~ ~ ~ {npc_nbt(profile)}",
                    f'tellraw @p[distance=..16] [{{"text":"Spawned Guild NPC: ","color":"gold"}},{{"text":"{profile["name"]}","color":"white"}},{{"text":" ({profile["rank"]} Lv.{profile["level"]})","color":"gray"}}]',
                ]
            ),
        )

    for spawn_set in SPAWN_SETS:
        lines = [f"# Generated NPC set: {spawn_set['id']}"]
        for member in spawn_set["members"]:
            profile = profiles_by_id[member["profile"]]
            x, y, z = member["offset"]
            lines.append(
                f"execute positioned {relative_coord(x)} {relative_coord(y)} {relative_coord(z)} run function ascendant_guild:npc/spawn_{profile['id']}"
            )
        write_text(f"{base}/data/ascendant_guild/functions/npc/spawn_set/{spawn_set['id']}.mcfunction", "\n".join(lines))

    write_text(
        f"{base}/data/ascendant_guild/functions/npc/list.mcfunction",
        "\n".join(
            [
                'tellraw @s {"text":"Ascendant generated NPC spawn functions:","color":"gold","bold":true}',
                'tellraw @s {"text":"/function ascendant_guild:npc/spawn_set/starter_guild_staff","color":"aqua"}',
                'tellraw @s {"text":"/function ascendant_guild:npc/spawn_set/roadside_rumor_camp","color":"aqua"}',
                'tellraw @s {"text":"/function ascendant_guild:npc/spawn_set/frontier_guild_outpost","color":"aqua"}',
                'tellraw @s {"text":"Individual profiles are under ascendant_guild:npc/spawn_<profile>.","color":"gray"}',
            ]
        ),
    )


def relative_coord(value: int) -> str:
    if value == 0:
        return "~"
    return f"~{value}"


def make_state(name: str, properties: dict[str, str] | None = None) -> dict[str, Any]:
    state = {"Name": name}
    if properties:
        state["Properties"] = properties
    return state


def tag_int_list(values: list[int]) -> nbtlib.List[nbtlib.Int]:
    return nbtlib.List[nbtlib.Int]([nbtlib.Int(value) for value in values])


def make_compound(data: dict[str, Any]) -> nbtlib.Compound:
    result = nbtlib.Compound()
    for key, value in data.items():
        if isinstance(value, (nbtlib.Compound, nbtlib.List, nbtlib.String, nbtlib.Byte, nbtlib.Int, nbtlib.Long)):
            result[key] = value
        elif isinstance(value, str):
            result[key] = nbtlib.String(value)
        elif isinstance(value, dict):
            result[key] = make_compound(value)
        elif isinstance(value, list):
            if not value:
                result[key] = nbtlib.List([])
            elif all(isinstance(item, str) for item in value):
                result[key] = nbtlib.List[nbtlib.String]([nbtlib.String(item) for item in value])
            elif all(isinstance(item, dict) for item in value):
                result[key] = nbtlib.List[nbtlib.Compound]([make_compound(item) for item in value])
            else:
                raise TypeError(f"Unsupported NBT list for {key}: {value!r}")
        elif isinstance(value, bool):
            result[key] = nbtlib.Byte(1 if value else 0)
        elif isinstance(value, int):
            result[key] = nbtlib.Int(value)
        else:
            raise TypeError(f"Unsupported NBT value for {key}: {value!r}")
    return result


@dataclass(frozen=True)
class StructureSpec:
    id: str
    size: tuple[int, int, int]
    spacing: int
    separation: int
    salt: int
    biomes: list[str]
    note: str


def set_block(
    blocks: dict[tuple[int, int, int], dict[str, Any]],
    x: int,
    y: int,
    z: int,
    name: str,
    properties: dict[str, str] | None = None,
    block_nbt: dict[str, Any] | None = None,
) -> None:
    blocks[(x, y, z)] = {"state": make_state(name, properties), "nbt": block_nbt}


def fill(blocks: dict[tuple[int, int, int], dict[str, Any]], start: tuple[int, int, int], end: tuple[int, int, int], name: str, properties: dict[str, str] | None = None) -> None:
    x1, y1, z1 = start
    x2, y2, z2 = end
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                set_block(blocks, x, y, z, name, properties)


def item_stack_nbt(item_id: str, slot: int | None = None, count: int = 1, tag: dict[str, Any] | None = None) -> nbtlib.Compound:
    data: dict[str, Any] = {"id": item_id, "Count": nbtlib.Byte(count)}
    if slot is not None:
        data["Slot"] = nbtlib.Byte(slot)
    if tag:
        data["tag"] = tag
    return make_compound(data)


def written_book_tag(title: str, lines: list[str]) -> dict[str, Any]:
    page_text = "\n".join(lines)
    return {
        "title": title[:32],
        "author": "Ascendant Guild",
        "pages": [json.dumps({"text": page_text}, separators=(",", ":"))],
    }


def notice_board_nbt(title: str, lines: list[str], item_id: str = "minecraft:written_book") -> dict[str, Any]:
    book = item_stack_nbt(item_id, slot=0, tag=written_book_tag(title, lines))
    return {
        "id": "supplementaries:notice_board",
        "PageNumber": 0,
        "Items": nbtlib.List[nbtlib.Compound]([book]),
        "TextHolder": {
            "has_glowing_text": nbtlib.Byte(0),
            "color": "black",
            "message": [json.dumps({"text": line}, separators=(",", ":")) for line in lines],
            "has_antique_ink": nbtlib.Byte(0),
        },
    }


def container_loot_nbt(block_id: str, loot_table: str) -> dict[str, Any]:
    return {"id": block_id, "LootTable": loot_table}


def build_hunter_board() -> tuple[StructureSpec, dict[tuple[int, int, int], dict[str, Any]]]:
    blocks: dict[tuple[int, int, int], dict[str, Any]] = {}
    spec = StructureSpec(
        id="hunter_board_village_standard",
        size=(13, 6, 5),
        spacing=192,
        separation=80,
        salt=1730141,
        biomes=[
            "minecraft:plains",
            "minecraft:sunflower_plains",
            "minecraft:meadow",
            "minecraft:forest",
            "minecraft:birch_forest",
            "minecraft:taiga",
            "minecraft:savanna",
            "minecraft:desert",
            "minecraft:snowy_plains",
            "minecraft:cherry_grove",
        ],
        note="Small standalone village-facing Hunter Board with one Bountiful board and a multi-board Guild notice roster.",
    )
    fill(blocks, (0, 0, 0), (12, 0, 4), "minecraft:spruce_planks")
    fill(blocks, (1, 1, 4), (11, 4, 4), "minecraft:dark_oak_planks")
    fill(blocks, (0, 1, 4), (0, 5, 4), "minecraft:stripped_dark_oak_log", {"axis": "y"})
    fill(blocks, (12, 1, 4), (12, 5, 4), "minecraft:stripped_dark_oak_log", {"axis": "y"})
    fill(blocks, (0, 5, 3), (12, 5, 4), "minecraft:spruce_slab", {"type": "bottom", "waterlogged": "false"})
    set_block(blocks, 6, 2, 3, "bountiful:bountyboard")
    set_block(
        blocks,
        2,
        2,
        3,
        "supplementaries:notice_board",
        {"facing": "north", "has_book": "true"},
        notice_board_nbt("Guild Ranks I", ["S: Black Hound", "A: Kael Vorn", "B: Darius Crowe", "B: Seren Valehart"]),
    )
    set_block(
        blocks,
        4,
        2,
        3,
        "supplementaries:notice_board",
        {"facing": "north", "has_book": "true"},
        notice_board_nbt("Guild Ranks II", ["C: Mira Ash", "C: Guard Captain", "C: Wounded Hunter", "D: Quartermaster"]),
    )
    set_block(
        blocks,
        8,
        2,
        3,
        "supplementaries:notice_board",
        {"facing": "north", "has_book": "true"},
        notice_board_nbt("Board Rules", ["Proof beats talk.", "Bring trophies.", "No lone dragon hunts.", "Report village threats."]),
    )
    set_block(
        blocks,
        10,
        2,
        3,
        "supplementaries:notice_board",
        {"facing": "north", "has_book": "true"},
        notice_board_nbt("Local Work", ["Take board contracts.", "Earn Guild Marks.", "Return at dawn.", "Ask clerks for leads."]),
    )
    set_block(blocks, 1, 1, 1, "minecraft:barrel", {"facing": "up", "open": "false"}, container_loot_nbt("minecraft:barrel", "ascendant_guild:chests/village_hunter_board"))
    set_block(blocks, 11, 1, 1, "minecraft:barrel", {"facing": "up", "open": "false"}, container_loot_nbt("minecraft:barrel", "ascendant_guild:chests/village_hunter_board"))
    set_block(blocks, 4, 1, 1, "minecraft:campfire", {"facing": "north", "lit": "true", "signal_fire": "false", "waterlogged": "false"})
    set_block(blocks, 1, 3, 3, "mcwlights:tavern_wall_lantern", {"facing": "north"})
    set_block(blocks, 11, 3, 3, "mcwlights:tavern_wall_lantern", {"facing": "north"})
    set_block(blocks, 6, 5, 2, "minecraft:yellow_banner", {"rotation": "8"})
    return spec, blocks


def build_roadside_camp() -> tuple[StructureSpec, dict[tuple[int, int, int], dict[str, Any]]]:
    blocks: dict[tuple[int, int, int], dict[str, Any]] = {}
    spec = StructureSpec(
        id="roadside_hunter_camp",
        size=(11, 5, 9),
        spacing=224,
        separation=96,
        salt=1730142,
        biomes=[
            "minecraft:plains",
            "minecraft:forest",
            "minecraft:birch_forest",
            "minecraft:dark_forest",
            "minecraft:taiga",
            "minecraft:old_growth_pine_taiga",
            "minecraft:savanna",
            "minecraft:meadow",
            "minecraft:stony_peaks",
        ],
        note="Roadside camp for wounded hunters, tavern rumors, and scout/rival encounters.",
    )
    fill(blocks, (2, 0, 2), (8, 0, 6), "minecraft:coarse_dirt")
    fill(blocks, (3, 1, 7), (7, 3, 7), "minecraft:dark_oak_planks")
    set_block(blocks, 5, 2, 6, "bountiful:bountyboard")
    set_block(
        blocks,
        3,
        2,
        6,
        "supplementaries:notice_board",
        {"facing": "north", "has_book": "true"},
        notice_board_nbt("Road Rumors", ["Tracks after moonrise.", "Blue flame in ruins.", "Mira marked 3 sites.", "Pay for fresh leads."]),
    )
    set_block(
        blocks,
        7,
        2,
        6,
        "supplementaries:notice_board",
        {"facing": "north", "has_book": "true"},
        notice_board_nbt("Camp Roster", ["Tavern Keeper: D", "Wounded Hunter: C", "Mira Ash: C", "Rest before night."]),
    )
    set_block(blocks, 5, 1, 3, "minecraft:campfire", {"facing": "north", "lit": "true", "signal_fire": "true", "waterlogged": "false"})
    set_block(blocks, 2, 1, 3, "minecraft:red_bed", {"facing": "east", "occupied": "false", "part": "foot"})
    set_block(blocks, 3, 1, 3, "minecraft:red_bed", {"facing": "east", "occupied": "false", "part": "head"})
    set_block(blocks, 8, 1, 3, "minecraft:barrel", {"facing": "up", "open": "false"}, container_loot_nbt("minecraft:barrel", "ascendant_guild:chests/roadside_hunter_camp"))
    set_block(blocks, 8, 1, 4, "minecraft:chest", {"facing": "north", "type": "single", "waterlogged": "false"}, container_loot_nbt("minecraft:chest", "ascendant_guild:chests/roadside_hunter_camp"))
    for x, z in [(2, 2), (8, 2), (2, 6), (8, 6)]:
        set_block(blocks, x, 1, z, "minecraft:oak_fence", {"east": "false", "north": "false", "south": "false", "waterlogged": "false", "west": "false"})
        set_block(blocks, x, 2, z, "minecraft:lantern", {"hanging": "false", "waterlogged": "false"})
    return spec, blocks


def build_frontier_outpost() -> tuple[StructureSpec, dict[tuple[int, int, int], dict[str, Any]]]:
    blocks: dict[tuple[int, int, int], dict[str, Any]] = {}
    spec = StructureSpec(
        id="frontier_guild_outpost",
        size=(15, 7, 9),
        spacing=288,
        separation=128,
        salt=1730143,
        biomes=[
            "minecraft:plains",
            "minecraft:meadow",
            "minecraft:windswept_hills",
            "minecraft:stony_peaks",
            "minecraft:forest",
            "minecraft:taiga",
            "minecraft:savanna",
            "minecraft:badlands",
            "minecraft:snowy_plains",
        ],
        note="Small Guild outpost prototype for Rank Examiner, Arcanist, and Quartermaster placement.",
    )
    fill(blocks, (0, 0, 0), (14, 0, 8), "minecraft:stone_bricks")
    fill(blocks, (1, 1, 7), (13, 4, 7), "minecraft:dark_oak_planks")
    fill(blocks, (0, 1, 7), (0, 5, 7), "minecraft:deepslate_bricks")
    fill(blocks, (14, 1, 7), (14, 5, 7), "minecraft:deepslate_bricks")
    fill(blocks, (0, 5, 5), (14, 5, 8), "minecraft:dark_oak_slab", {"type": "bottom", "waterlogged": "false"})
    set_block(blocks, 7, 2, 6, "bountiful:bountyboard")
    for x, title, lines in [
        (2, "Examiner Desk", ["B Rank exams.", "Bring boss proof.", "No borrowed trophies.", "Trials reset weekly."]),
        (4, "Arcanist Notes", ["Spell residue: blue.", "Portal class restricted.", "Carry scroll proof.", "Report moon events."]),
        (10, "Frontier Watch", ["Dragon signs: rare.", "Cataclysm relics: S.", "Aquamirae coast watch.", "Do not travel alone."]),
        (12, "Supply Ledger", ["Marks buy prep.", "Seals unlock stock.", "Return broken gear.", "Keep roads lit."]),
    ]:
        set_block(
            blocks,
            x,
            2,
            6,
            "supplementaries:notice_board",
            {"facing": "north", "has_book": "true"},
            notice_board_nbt(title, lines),
        )
    set_block(blocks, 2, 1, 2, "minecraft:barrel", {"facing": "up", "open": "false"}, container_loot_nbt("minecraft:barrel", "ascendant_guild:chests/frontier_guild_outpost"))
    set_block(blocks, 12, 1, 2, "minecraft:barrel", {"facing": "up", "open": "false"}, container_loot_nbt("minecraft:barrel", "ascendant_guild:chests/frontier_guild_outpost"))
    set_block(blocks, 7, 1, 3, "minecraft:smithing_table")
    set_block(blocks, 6, 1, 3, "minecraft:cartography_table")
    set_block(blocks, 8, 1, 3, "minecraft:bookshelf")
    set_block(blocks, 1, 3, 6, "mcwlights:covered_wall_lantern", {"facing": "north"})
    set_block(blocks, 13, 3, 6, "mcwlights:covered_wall_lantern", {"facing": "north"})
    set_block(blocks, 7, 5, 4, "minecraft:blue_banner", {"rotation": "8"})
    return spec, blocks


def write_structure_nbt(relative_path: str, size: tuple[int, int, int], blocks: dict[tuple[int, int, int], dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)

    palette: list[dict[str, Any]] = []
    palette_keys: dict[str, int] = {}
    block_entries = []
    for pos, block in sorted(blocks.items(), key=lambda item: (item[0][1], item[0][2], item[0][0])):
        state = block["state"]
        key = json.dumps(state, sort_keys=True)
        if key not in palette_keys:
            palette_keys[key] = len(palette)
            palette.append(state)
        entry = nbtlib.Compound(
            {
                "pos": tag_int_list([pos[0], pos[1], pos[2]]),
                "state": nbtlib.Int(palette_keys[key]),
            }
        )
        if block.get("nbt"):
            entry["nbt"] = make_compound(block["nbt"])
        block_entries.append(entry)

    root = nbtlib.Compound(
        {
            "DataVersion": nbtlib.Int(DATA_VERSION_1_20_1),
            "size": tag_int_list(list(size)),
            "palette": nbtlib.List[nbtlib.Compound]([make_compound(state) for state in palette]),
            "blocks": nbtlib.List[nbtlib.Compound](block_entries),
            "entities": nbtlib.List[nbtlib.Compound]([]),
        }
    )
    nbtlib.File(root).save(path, gzipped=True)


def write_worldgen(base: str) -> list[StructureSpec]:
    structures = [build_hunter_board(), build_roadside_camp(), build_frontier_outpost()]
    specs = []
    for spec, blocks in structures:
        specs.append(spec)
        structure_id = f"ascendant_guild:{spec.id}"
        pool_id = f"ascendant_guild:guild/{spec.id}"
        structure_location = f"ascendant_guild:guild/{spec.id}"

        write_structure_nbt(
            f"{base}/data/ascendant_guild/structures/guild/{spec.id}.nbt",
            spec.size,
            blocks,
        )
        write_json(
            f"{base}/data/ascendant_guild/worldgen/template_pool/guild/{spec.id}.json",
            {
                "name": pool_id,
                "fallback": "minecraft:empty",
                "elements": [
                    {
                        "weight": 1,
                        "element": {
                            "location": structure_location,
                            "processors": "minecraft:empty",
                            "projection": "rigid",
                            "element_type": "minecraft:legacy_single_pool_element",
                        },
                    }
                ],
            },
        )
        write_json(
            f"{base}/data/ascendant_guild/worldgen/structure/{spec.id}.json",
            {
                "type": "minecraft:jigsaw",
                "biomes": f"#ascendant_guild:has_structure/{spec.id}",
                "step": "surface_structures",
                "terrain_adaptation": "beard_thin",
                "spawn_overrides": {},
                "start_pool": pool_id,
                "size": 1,
                "start_height": {"absolute": 0},
                "project_start_to_heightmap": "WORLD_SURFACE_WG",
                "max_distance_from_center": 80,
                "use_expansion_hack": False,
            },
        )
        write_json(
            f"{base}/data/ascendant_guild/worldgen/structure_set/{spec.id}.json",
            {
                "structures": [{"structure": structure_id, "weight": 1}],
                "placement": {
                    "type": "minecraft:random_spread",
                    "spacing": spec.spacing,
                    "separation": spec.separation,
                    "salt": spec.salt,
                },
            },
        )
        write_json(
            f"{base}/data/ascendant_guild/tags/worldgen/biome/has_structure/{spec.id}.json",
            {"replace": False, "values": spec.biomes},
        )
    return specs


def loot_entry(item_id: str, weight: int = 1, count: tuple[int, int] | None = None) -> dict[str, Any]:
    entry: dict[str, Any] = {"type": "minecraft:item", "name": item_id, "weight": weight}
    if count:
        entry["functions"] = [
            {
                "function": "minecraft:set_count",
                "count": {"type": "minecraft:uniform", "min": count[0], "max": count[1]},
            }
        ]
    return entry


def write_loot_tables(base: str) -> None:
    loot_tables = {
        "village_hunter_board": [
            loot_entry("minecraft:bread", 5, (1, 3)),
            loot_entry("minecraft:arrow", 4, (4, 12)),
            loot_entry("minecraft:torch", 4, (2, 8)),
            loot_entry("minecraft:emerald", 2, (1, 3)),
            loot_entry("kubejs:guild_mark", 2, (1, 2)),
            loot_entry("minecraft:paper", 1, (1, 4)),
        ],
        "roadside_hunter_camp": [
            loot_entry("minecraft:cooked_beef", 5, (1, 4)),
            loot_entry("minecraft:arrow", 5, (6, 18)),
            loot_entry("minecraft:torch", 4, (3, 10)),
            loot_entry("minecraft:iron_ingot", 2, (1, 3)),
            loot_entry("kubejs:guild_mark", 3, (1, 4)),
            loot_entry("minecraft:experience_bottle", 1, (1, 3)),
        ],
        "frontier_guild_outpost": [
            loot_entry("minecraft:iron_ingot", 5, (2, 6)),
            loot_entry("minecraft:experience_bottle", 4, (2, 6)),
            loot_entry("kubejs:guild_mark", 4, (3, 8)),
            loot_entry("kubejs:hunter_seal", 2, (1, 2)),
            loot_entry("irons_spellbooks:common_ink", 2, (1, 3)),
            loot_entry("minecraft:diamond", 1, (1, 2)),
        ],
    }
    for table_id, entries in loot_tables.items():
        write_json(
            f"{base}/data/ascendant_guild/loot_tables/chests/{table_id}.json",
            {
                "type": "minecraft:chest",
                "pools": [
                    {
                        "rolls": {"type": "minecraft:uniform", "min": 2, "max": 4},
                        "entries": entries,
                    }
                ],
            },
        )


def clean_target(target: dict[str, Any]) -> bool:
    target_id = str(target.get("target_id", ""))
    name = str(target.get("name", ""))
    namespace = target_id.split(":", 1)[0]
    blocked_ids = {
        # Bountiful rejected this generated language-key entity at runtime; use confirmed dragon entities instead.
        "iceandfire:black_frost_dragon",
        "iceandfire:fire_dragon_charge",
        "iceandfire:ice_dragon_charge",
        "iceandfire:lightning_dragon_charge",
    }
    blocked_namespaces = {
        "customnpcs",
        "easy_npc",
        "geckolib",
        "humancompanions",
        "mca",
    }
    blocked_pieces = [
        "abyss_blast",
        "abyss_mine",
        "abyss_orb",
        "air_combustion",
        "ancient_ancient",
        "arrow",
        "ashen_breath",
        "axe_blade",
        "blackflame_explosion",
        "blackflame_snake",
        "blast",
        "blood",
        "bomb",
        "boulder",
        "breath",
        "chakra",
        "controlled",
        "copy",
        "corpse",
        "dummy",
        "earthquake",
        "egg",
        "entity",
        "explosion",
        "fireball",
        "flame_jet",
        "flame_pillar",
        "flame_strike",
        "fog",
        "ghost_glaive",
        "head",
        "holy_moonlight_pillar",
        "jet",
        "lantern",
        "lightning",
        "magic",
        "mine",
        "minion",
        "not_despawn",
        "orb",
        "part",
        "phantom_halberd",
        "pillar",
        "projectile",
        "sculptor",
        "segment",
        "shot",
        "skull",
        "slash",
        "spear_entity",
        "spit",
        "stele",
        "storm",
        "summoned",
        "vortex",
        "warmth",
        "wave",
        "wither_skull",
    ]
    if not target_id or target_id in blocked_ids or namespace in blocked_namespaces:
        return False
    return not any(piece in target_id for piece in blocked_pieces) and "§" not in name


BOARD_NAMESPACE_ALLOW = {
    "village_hunter_board": {
        "alexsmobs",
        "aquamirae",
        "artifacts",
        "born_in_chaos_v1",
        "irons_spellbooks",
        "majruszsdifficulty",
        "minecraft",
        "mowziesmobs",
        "quark",
    },
    "town_guild_board": {
        "alexsmobs",
        "born_in_chaos_v1",
        "cataclysm",
        "irons_spellbooks",
        "majruszsdifficulty",
        "mowziesmobs",
        "quark",
        "soulsweapons",
    },
    "major_guild_registry": {
        "alexsmobs",
        "block_factorys_bosses",
        "born_in_chaos_v1",
        "cataclysm",
        "iceandfire",
        "irons_spellbooks",
        "mowziesmobs",
        "soulsweapons",
    },
}


def pick_targets(targets: list[dict[str, Any]], board: str, limit: int | None = None) -> list[dict[str, Any]]:
    picked = []
    seen_mods: set[str] = set()
    allowed_namespaces = BOARD_NAMESPACE_ALLOW.get(board, set())
    for target in targets:
        if target.get("recommended_board") != board or not clean_target(target):
            continue
        mod_key = str(target.get("target_id", "")).split(":", 1)[0]
        if allowed_namespaces and mod_key not in allowed_namespaces:
            continue
        if limit is not None and mod_key in seen_mods and len(picked) < limit // 2:
            continue
        picked.append(target)
        seen_mods.add(mod_key)
        if limit is not None and len(picked) >= limit:
            break
    if limit is not None and len(picked) < limit:
        for target in targets:
            if target.get("recommended_board") == board and clean_target(target) and target not in picked:
                mod_key = str(target.get("target_id", "")).split(":", 1)[0]
                if allowed_namespaces and mod_key not in allowed_namespaces:
                    continue
                picked.append(target)
                if len(picked) >= limit:
                    break
    return picked


def entity_objective(prefix: str, target: dict[str, Any], index: int, amount: tuple[int, int], unit_worth: int, weight: float, rarity: str | None = None) -> dict[str, Any]:
    objective = {
        "type": "entity",
        "timeMult": 7.5,
        "content": target["target_id"],
        "amount": {"min": amount[0], "max": amount[1]},
        "unitWorth": unit_worth,
        "weightMult": weight,
    }
    if rarity:
        objective["rarity"] = rarity
    return {f"{prefix}_{index:02d}_{slug(target['name'])}": objective}


def item_reward(content: str, amount: tuple[int, int], unit_worth: int, weight: float, rarity: str | None = None) -> dict[str, Any]:
    reward = {
        "type": "item",
        "content": content,
        "amount": {"min": amount[0], "max": amount[1]},
        "unitWorth": unit_worth,
        "weightMult": weight,
    }
    if rarity:
        reward["rarity"] = rarity
    return reward


def target_objective_profile(target: dict[str, Any], board: str, spec: dict[str, Any]) -> tuple[tuple[int, int], int, float, str]:
    threat = str(target.get("threat_tier", "")).lower()
    reward_rarity = str(target.get("reward_rarity", spec["rarity"])).upper()
    if board == "village_hunter_board":
        if threat in {"elite", "boss", "dragon_tier"}:
            return (1, 1), 1400, 0.22, "RARE"
        return (1, 2), 900, 0.55, "UNCOMMON"
    if board == "town_guild_board":
        if threat == "boss":
            return (1, 1), 4200, 0.18, "EPIC"
        return (1, 1), 2600, 0.38, "RARE"
    if threat == "dragon_tier":
        return (1, 1), 11000, 0.08, "LEGENDARY"
    if threat == "boss":
        return (1, 1), 7600, 0.15, "EPIC"
    return spec["amount"], spec["unit"], spec["weight"], reward_rarity


def write_bountiful_data(base: str) -> dict[str, Any]:
    bounty_data = read_json("config/ascendant_guild/generated_bounty_targets.json")
    targets = bounty_data.get("bounty_targets", [])
    selected = {
        "village_hunter_board": pick_targets(targets, "village_hunter_board"),
        "town_guild_board": pick_targets(targets, "town_guild_board"),
        "major_guild_registry": pick_targets(targets, "major_guild_registry"),
    }

    pool_specs = {
        "village_hunter_board": {
            "objective_name": "ar_village_hunter_objs",
            "reward_name": "ar_village_hunter_rews",
            "prefix": "village_hunt",
            "amount": (1, 2),
            "unit": 900,
            "weight": 0.55,
            "rarity": "UNCOMMON",
            "rewards": {
                "ar_rew_guild_mark": item_reward("kubejs:guild_mark", (1, 4), 700, 1.2, "UNCOMMON"),
                "ar_rew_emeralds": item_reward("minecraft:emerald", (3, 12), 1000, 1.0),
                "ar_rew_arrows": item_reward("minecraft:arrow", (8, 24), 120, 0.55),
                "ar_rew_cooked_beef": item_reward("minecraft:cooked_beef", (2, 8), 180, 0.4),
                "ar_rew_experience_bottle": item_reward("minecraft:experience_bottle", (1, 4), 450, 0.35, "UNCOMMON"),
            },
        },
        "town_guild_board": {
            "objective_name": "ar_town_guild_objs",
            "reward_name": "ar_town_guild_rews",
            "prefix": "town_contract",
            "amount": (1, 1),
            "unit": 2500,
            "weight": 0.4,
            "rarity": "RARE",
            "rewards": {
                "ar_rew_hunter_seal": item_reward("kubejs:hunter_seal", (1, 2), 2200, 0.8, "RARE"),
                "ar_rew_guild_marks": item_reward("kubejs:guild_mark", (4, 10), 700, 0.8, "UNCOMMON"),
                "ar_rew_iron": item_reward("minecraft:iron_ingot", (4, 16), 250, 0.35),
                "ar_rew_xp_bottle": item_reward("minecraft:experience_bottle", (3, 12), 600, 0.4, "RARE"),
                "ar_rew_gold": item_reward("minecraft:gold_ingot", (3, 10), 500, 0.28, "RARE"),
                "ar_rew_ender_pearl": item_reward("minecraft:ender_pearl", (1, 3), 900, 0.16, "RARE"),
            },
        },
        "major_guild_registry": {
            "objective_name": "ar_major_guild_objs",
            "reward_name": "ar_major_guild_rews",
            "prefix": "major_contract",
            "amount": (1, 1),
            "unit": 7000,
            "weight": 0.18,
            "rarity": "EPIC",
            "rewards": {
                "ar_rew_ascendant_sigil": item_reward("kubejs:ascendant_sigil", (1, 1), 8500, 0.5, "LEGENDARY"),
                "ar_rew_hunter_seals": item_reward("kubejs:hunter_seal", (2, 5), 2200, 0.6, "RARE"),
                "ar_rew_diamond": item_reward("minecraft:diamond", (1, 4), 3000, 0.25, "EPIC"),
                "ar_rew_totem": item_reward("minecraft:totem_of_undying", (1, 1), 4500, 0.12, "LEGENDARY"),
                "ar_rew_netherite_scrap": item_reward("minecraft:netherite_scrap", (1, 2), 5200, 0.08, "LEGENDARY"),
                "ar_rew_echo_shard": item_reward("minecraft:echo_shard", (1, 3), 4000, 0.1, "EPIC"),
            },
        },
    }

    summary = {"selected_counts": {}, "selected_targets": {}}
    for board, spec in pool_specs.items():
        objective_content: dict[str, Any] = {}
        for index, target in enumerate(selected[board], start=1):
            amount, unit_worth, weight, rarity = target_objective_profile(target, board, spec)
            objective_content.update(
                entity_objective(
                    spec["prefix"],
                    target,
                    index,
                    amount,
                    unit_worth,
                    weight,
                    rarity,
                )
            )
        write_json(
            f"{base}/data/bountiful/bounty_pools/ascendant_guild/{spec['objective_name']}.json",
            {"content": objective_content},
        )
        write_json(
            f"{base}/data/bountiful/bounty_pools/ascendant_guild/{spec['reward_name']}.json",
            {"content": spec["rewards"]},
        )
        write_json(
            f"{base}/data/bountiful/bounty_decrees/ascendant_guild/{board}.json",
            {
                "objectives": [spec["objective_name"]],
                "rewards": [spec["reward_name"], "_all_rews"],
            },
        )
        summary["selected_counts"][board] = len(selected[board])
        summary["registry_candidates_seen"] = len(targets)
        summary["friendly_namespaces_filtered"] = ["customnpcs", "easy_npc", "humancompanions", "mca", "geckolib"]
        summary["selected_targets"][board] = [
            {
                "target_id": target["target_id"],
                "name": target["name"],
                "threat_tier": target["threat_tier"],
                "reward_rarity": target.get("reward_rarity", ""),
                "source_mod": target.get("source_mod", ""),
            }
            for target in selected[board]
        ]
    return summary


def write_pack(base: str) -> dict[str, Any]:
    clear_pack(base)
    write_json(
        f"{base}/pack.mcmeta",
        {"pack": {"pack_format": 15, "description": "Ascendant Realms generated Guild NPC, contract, and worldgen slice"}},
    )
    write_text(
        f"{base}/README.md",
        "# Ascendant Realms Guild Datapack\n\n"
        "Generated by `scripts/generate-ascendant-guild-worldgen.py`.\n\n"
        "This pack adds generated CustomNPC spawn functions, Ascendant Bountiful contract pools, and the first standalone Guild/Hunter worldgen structures. It does not inject pieces into third-party village pools yet.\n",
    )
    write_npc_functions(base)
    structures = write_worldgen(base)
    write_loot_tables(base)
    bounty_summary = write_bountiful_data(base)
    return {"structures": structures, "bounties": bounty_summary}


def write_config_files(summary: dict[str, Any]) -> None:
    profiles = []
    for profile in NPC_PROFILE_SOURCE:
        enriched = dict(profile)
        behavior = profile_behavior(profile["id"])
        enriched["generated_name"] = npc_display(profile)
        enriched["entity_type"] = "customnpcs:customnpc"
        enriched["skin_texture"] = NPC_SKINS.get(profile["id"], "customnpcs:textures/entity/humanmale/guardsteve.png")
        enriched["equipment"] = profile_equipment(profile)
        enriched["relationship_gate"] = behavior["relationship_gate"]
        enriched["command_policy"] = behavior["command_policy"]
        enriched["service_min_relation"] = behavior["service_min_relation"]
        enriched["can_follow"] = behavior["can_follow"]
        enriched["can_take_orders"] = behavior["can_take_orders"]
        enriched["obedience_note"] = behavior["obedience_note"]
        enriched["data_backed"] = True
        enriched["manual_build_required"] = False
        profiles.append(enriched)
    write_json(
        "config/ascendant_guild/generated_npc_profiles.json",
        {
            "version": 1,
            "status": "generated CustomNPC profile set; spawn functions are live through Open Loader",
            "source": "scripts/generate-ascendant-guild-worldgen.py",
            "profiles": profiles,
        },
    )
    write_json(
        "config/ascendant_guild/generated_npc_spawn_sets.json",
        {
            "version": 1,
            "status": "generated sets for non-manual Guild NPC placement tests",
            "source": "scripts/generate-ascendant-guild-worldgen.py",
            "spawn_sets": SPAWN_SETS,
        },
    )
    write_json(
        "config/ascendant_guild/live_bountiful_pools.json",
        {
            "version": 1,
            "status": "live Open Loader Bountiful pool summary for Ascendant Guild contracts",
            "source": "config/openloader/data/ascendant_realms_guild/data/bountiful",
            **summary["config"]["bounties"],
        },
    )

    settlement = read_json("config/ascendant_settlements/settlement_unification.json")
    settlement["status"] = "standalone generated Guild/Hunter worldgen test active; no third-party village-pool injection yet"
    settlement["active_worldgen_changes"] = [
        {
            "id": structure.id,
            "type": "standalone_jigsaw_structure",
            "namespace": "ascendant_guild",
            "locate": f"/locate structure ascendant_guild:{structure.id}",
            "spacing": structure.spacing,
            "separation": structure.separation,
            "policy": "approved standalone test only; do not inject into vanilla or modded village pools until validation passes",
        }
        for structure in summary["config"]["structures"]
    ]
    settlement["first_blueprints"] = [
        {
            "id": structure.id,
            "status": "generated standalone structure active for fresh-world test",
            "locate": f"/locate structure ascendant_guild:{structure.id}",
            "note": structure.note,
        }
        for structure in summary["config"]["structures"]
    ]
    write_json("config/ascendant_settlements/settlement_unification.json", settlement)


def mirror_customnpcs_skin_assets() -> None:
    """Mirror generated MCA-style skins into CustomNPCs' own resource surface.

    The same files also remain in the compatibility resource pack. CustomNPCs
    can request `customnpcs:textures/entity/...` before the separate pack has
    been accepted by the client, so this native copy prevents magenta missing
    skins while keeping one visible texture namespace.
    """

    write_json(
        "customnpcs/pack.mcmeta",
        {
            "pack": {
                "pack_format": 15,
                "description": "Ascendant Realms CustomNPCs resources",
            }
        },
    )
    write_json("customnpcs/assets/customnpcs/sounds.json", {})
    ASCENDANT_SKIN_CUSTOMNPCS_ROOT.mkdir(parents=True, exist_ok=True)
    for profile_id in sorted(NPC_SKINS):
        source = ASCENDANT_SKIN_SOURCE_ROOT / f"{profile_id}.png"
        destination = ASCENDANT_SKIN_CUSTOMNPCS_ROOT / f"{profile_id}.png"
        if not source.exists():
            raise FileNotFoundError(f"Missing source CustomNPCs MCA-style skin: {source}")
        shutil.copyfile(source, destination)


def write_docs(summary: dict[str, Any]) -> None:
    structure_rows = "\n".join(
        f"| `ascendant_guild:{structure.id}` | {structure.spacing}/{structure.separation} | `{structure.note}` | `/locate structure ascendant_guild:{structure.id}` |"
        for structure in summary["config"]["structures"]
    )
    npc_rows = "\n".join(
        f"| `{profile['id']}` | {profile['rank']} | Lv.{profile['level']} | {profile['role']} | `{profile['placement']}` |"
        for profile in NPC_PROFILE_SOURCE
    )
    bounty_rows = "\n".join(
        f"| `{board}` | {count} |"
        for board, count in summary["config"]["bounties"]["selected_counts"].items()
    )

    write_text(
        "docs/GENERATED_NPC_SYSTEM.md",
        f"""# Generated NPC System

Status: first generated CustomNPC profile and spawn-set layer is active through Open Loader.

Jayden should not need to hand-build every Guild NPC. The current pass creates a reusable generated set at `config/ascendant_guild/generated_npc_profiles.json` and callable spawn functions under `ascendant_guild:npc/*`.

## Profiles

| Profile | Rank | Level | Role | Preferred Placement |
|---|---:|---:|---|---|
{npc_rows}

## Spawn Sets

- `/function ascendant_guild:npc/spawn_set/starter_guild_staff`
- `/function ascendant_guild:npc/spawn_set/roadside_rumor_camp`
- `/function ascendant_guild:npc/spawn_set/frontier_guild_outpost`
- `/function ascendant_guild:npc/list`

## Design

- Spawned NPCs are `customnpcs:customnpc` entities.
- The visible name line includes rank, name, level, and role.
- Spawn functions now apply role-specific CustomNPCs skin textures from `customnpcs:textures/entity/ascendant_mca/*.png`.
- The same `ascendant_mca` skin PNGs are stored in both `resourcepacks/ascendant-realms-compat-fixes/assets/customnpcs/textures/entity/ascendant_mca/` and `customnpcs/assets/customnpcs/textures/entity/ascendant_mca/`. The CustomNPCs-native copy exists because the first in-game test showed magenta missing skins when the mod requested the texture through `customnpcs:` before resolving the separate compatibility resource pack.
- The `ascendant_mca` skins are bridge textures: MCA medieval clothing overlays composited onto full CustomNPCs-compatible player skins, so generated NPCs avoid broken overlay-only skins and do not default to Steve.
- Spawn functions pull visible mainhand/offhand/head/chest gear from `config/ascendant_guild/npc_loadouts.json`.
- Gear uses CustomNPCs top-level `Weapons` and `Armor` data plus vanilla `HandItems`/`ArmorItems` fallback data. `NpcInv` is kept empty because CustomNPCs treats it as a drop-table inventory, not the rendered equipment layer.
- Mainhand uses CustomNPCs weapon slot `0`; visible offhand uses slot `2`. Slot `1` is projectile/ammo behavior and should not be used for offhand identity gear.
- Social NPCs use anchored AI defaults so they should not all wander away in the same direction. Combat profiles such as guards and rival hunters use a wider active/walking range, but true cross-mod hostile defense still needs in-game validation and may require the future Ascendant NPC Runtime helper mod.
- The entity stores `ar_profile`, `ar_rank`, `ar_level`, `ar_role`, `ar_name`, `ar_relationship_gate`, `ar_command_policy`, `ar_service_min_relation`, `ar_can_follow`, and `ar_can_take_orders` in `ForgeData.CNPCStoredData`.
- Generated NPCs use relationship-gated dialogue through `customnpcs/scripts/ecmascript/ascendant_npc_identity.js`. Repeated interaction can move a player from stranger to familiar/trusted, but the current generated profiles still cannot follow or take player orders.
- Rank Examiner is the only generated NPC allowed to run a hidden public-service function on interaction. That is rank evaluation, not obedience, and the player should never need to type the function manually.
- `config/CustomNpcs.cfg` disables the generic `Hello @p` fallback line and locks normal edit/command surfaces behind ops so random players cannot use NPC tooling as gameplay.
- This is intentionally data-backed and static for the first generated pass. A future Ascendant NPC Runtime helper mod can read the same data and make levels, schedules, gear, dialogue, relationship rewards, and nameplates fully dynamic.

## Test

1. Load a creative test world with cheats enabled.
2. Run `/function ascendant_guild:npc/list`.
3. Run `/function ascendant_guild:npc/spawn_set/starter_guild_staff`.
4. Confirm the generated NPCs appear with styled rank/level/name/role lines.
5. Confirm generated NPCs use medieval/MCA-style skins rather than Steve or plain CustomNPCs defaults.
6. Confirm mainhand, offhand, helmet/hat, and chest identity gear render on the NPC model where configured.
7. Confirm social NPCs stay near their spawn instead of marching off together.
8. Spawn a vanilla zombie near a combat profile such as Guard Captain or Wounded Hunter and verify behavior. If they still ignore hostiles, treat it as the next runtime/faction scripting task instead of deleting the NPC system.
9. Confirm killing a test copy does not drop the full visible kit.
10. Right-click non-examiner NPCs repeatedly and confirm they give role/relation dialogue instead of a generic hello or command prompt.
11. Confirm non-examiner NPCs do not become followers or accept player orders through this script path.
12. Right-click the Rank Examiner and confirm rank evaluation still runs as the only public-service interaction bridge.
13. Run the roadside and frontier spawn sets away from the first group.
""",
    )

    write_text(
        "docs/ASCENDANT_GUILD_WORLDGEN.md",
        f"""# Ascendant Guild Worldgen

Status: standalone generated worldgen test is active. This is the first custom Ascendant worldgen layer.

This pass does not inject directly into vanilla, Integrated Villages, Towns and Towers, IDAS, or other third-party village pools. It adds standalone Guild/Hunter structures that can be located and tested in fresh chunks first.

## Generated Structures

| Structure | Spacing/Separation | Purpose | Test Command |
|---|---:|---|---|
{structure_rows}

## Why Standalone First

Standalone structures let us prove that custom NBT, Bountiful boards, written notice boards, loot containers, biome placement, and server sync work before touching modded village pools. If a structure has a bad block state or worldgen issue, it is isolated to the Ascendant Guild datapack instead of crashing every village generator.

## Current Tuning Notes

- Village Hunter Boards were widened and moved from `42/18` to `96/40`, then to `192/80`, after a test village produced too many board structures nearby.
- Roadside Hunter Camps moved from `54/22` to `128/56`, then to `224/96`.
- Frontier Guild Outposts moved from `72/30` to `160/64`, then to `288/128`.
- Notice boards are still part of the design, but the roster is split across several written boards so each board stays readable.
- Notice boards are generated facing outward after the first test found them rotated into their support wall.
- Roadside and frontier containers now use `ascendant_guild:chests/*` loot tables instead of empty default containers.
- Wall-adjacent lanterns use Macaw's Lights wall lantern blocks where the structure has a wall behind the lantern.
- The roadside camp lantern supports use real oak fence posts and standing lanterns, not floating hanging lanterns.

## Test Plan

Client creative/system test:

- Create a fresh creative test world.
- Run each `/locate structure ascendant_guild:<id>` command.
- Teleport to each result and inspect the structure.
- Confirm Bountiful bounty boards and multiple written Supplementaries notice boards render.
- Confirm notice boards show readable rank, roster, rumor, rule, or frontier text.
- Confirm notice boards face outward rather than into the wall.
- Confirm wall-mounted lanterns on Hunter/Frontier structures use Macaw wall lanterns, while freestanding roadside post lanterns remain standing lanterns.
- Confirm camp/outpost containers are not empty.
- Confirm camp/outpost blocks do not cause missing-block or block-entity errors.
- Spawn generated NPC sets near the structures.
- Save and reload.

Dedicated server test:

- Sync the latest client files.
- Export server staging.
- Materialize server mods from the active client instance.
- Boot the Forge 47.4.20 server.
- Join localhost or LAN.
- Generate fresh chunks and locate each Ascendant Guild structure.
- Let the server run 10 minutes.

## Next Gate

Only after this passes should we inject rare Guild pieces into village pools. If datapack pool injection proves too brittle, build the `Ascendant Settlements` Forge helper mod rather than removing village functionality.
""",
    )

    write_text(
        "docs/BOUNTIFUL_GUILD_CONTRACTS.md",
        f"""# Bountiful Guild Contracts

Status: first live Ascendant Guild Bountiful pools are generated through Open Loader.

The source candidate list is `config/ascendant_guild/generated_bounty_targets.json`. This pass selects a controlled subset and writes Bountiful pools into `config/openloader/data/ascendant_realms_guild/data/bountiful/`.

## Active Board Pools

| Board | Selected Targets |
|---|---:|
{bounty_rows}

## Reward Spine

- Village Hunter Boards reward `kubejs:guild_mark`, emeralds, arrows, and food.
- Town Guild Boards reward `kubejs:hunter_seal`, Guild Marks, iron, and XP bottles.
- Major Guild Registries reward `kubejs:ascendant_sigil`, Hunter Seals, diamonds, and rare totems.

## Safety Rules

- Technical entities, eggs, projectiles, CustomNPC internals, and Easy NPC internals are filtered out.
- This pass does not force every generated target live at once.
- Boss and dragon contracts are rare/major-board targets and still need balance tuning after worldgen validation.
""",
    )


def patch_docs() -> None:
    replacements = [
        (
            "README.md",
            "config/ascendant_guild/generated_bounty_targets.json` - generated Guild/Hunter bounty target candidates.",
            "config/ascendant_guild/generated_bounty_targets.json` - generated Guild/Hunter bounty target candidates.\n- `config/ascendant_guild/generated_npc_profiles.json` - generated CustomNPC profile set for non-manual Guild NPC placement.\n- `config/ascendant_guild/generated_npc_spawn_sets.json` - generated spawn groups for Guild staff, roadside rumor camps, and frontier outposts.\n- `config/ascendant_guild/live_bountiful_pools.json` - active Bountiful Guild contract pool summary.\n- `docs/GENERATED_NPC_SYSTEM.md` - generated NPC profile/spawn-set test plan.\n- `docs/ASCENDANT_GUILD_WORLDGEN.md` - first standalone Ascendant Guild worldgen test plan.\n- `docs/BOUNTIFUL_GUILD_CONTRACTS.md` - active Bountiful Guild contract pool notes.",
        ),
        (
            "docs/VILLAGE_AND_CITY_INTEGRATION.md",
            "- Actual board structures and NPC placements are not authored yet.",
            "- Actual board structures and NPC placements now have a first generated test layer: `ascendant_guild:hunter_board_village_standard`, `ascendant_guild:roadside_hunter_camp`, and `ascendant_guild:frontier_guild_outpost` generate as standalone structures through Open Loader. NPCs are generated from `config/ascendant_guild/generated_npc_profiles.json` and spawn sets under `/function ascendant_guild:npc/spawn_set/*`.",
        ),
        (
            "docs/STRUCTURE_DENSITY_TUNING.md",
            "Do not add more structure packs or village overhauls until Jayden approves another worldgen/structure batch. Revisit Sparse Structures only during the later full tuning pass after the larger content stack has proven stable.",
            "Do not add more structure packs or village overhauls until Jayden approves another worldgen/structure batch. The approved custom Ascendant Guild worldgen test adds only standalone Guild/Hunter structures, not another external structure pack. Revisit Sparse Structures only during the later full tuning pass after the larger content stack has proven stable.",
        ),
        (
            "docs/GUILD_HUNTER_IMPLEMENTATION_STATUS.md",
            "- `config/ascendant_guild/tool_audit.json` records installed tools and delayed pieces.",
            "- `config/ascendant_guild/tool_audit.json` records installed tools and delayed pieces.\n- `config/ascendant_guild/generated_npc_profiles.json` and `generated_npc_spawn_sets.json` now create non-manual Guild NPC spawn sets.\n- `config/ascendant_guild/live_bountiful_pools.json` records the active Bountiful contract pool slice.\n- `config/openloader/data/ascendant_realms_guild/` now carries generated NPC functions, Bountiful contract pools, and standalone Guild/Hunter structures.",
        ),
        (
            "docs/CUSTOM_HERO_SYSTEM_AUTOMATION.md",
            "Keep fixing root causes in place. Do not remove NPC, village, or UI functionality unless a mod or system proves unfixable after focused repair attempts.",
            "Keep fixing root causes in place. Do not remove NPC, village, or UI functionality unless a mod or system proves unfixable after focused repair attempts.\n\nGenerated NPC update: `docs/GENERATED_NPC_SYSTEM.md` is now the preferred first test path. Use generated spawn functions for Guild staff and rivals before hand-authoring individual CustomNPCs.",
        ),
        (
            "docs/KNOWN_RISKS.md",
            "- NPC loadouts and nameplates are formal data contracts, not live auto-equipment yet. They should guide Easy NPC and CustomNPCs templates until a custom Forge helper mod is justified.",
            "- NPC loadouts and nameplates are formal data contracts. The first generated CustomNPC spawn layer is now active, but it still uses static data-backed NPCs rather than a full runtime scheduler/equipment AI. A custom Forge helper mod is still likely for animated nameplates, dynamic levels, schedules, and automatic settlement role assignment.",
        ),
    ]
    for relative_path, old, new in replacements:
        path = ROOT / relative_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if old in text and new not in text:
            text = text.replace(old, new)
            path.write_text(text, encoding="utf-8")

    testing = ROOT / "docs/TESTING_CHECKLIST.md"
    if testing.exists():
        text = testing.read_text(encoding="utf-8", errors="replace")
        marker = "## Custom Hero / NPC Identity Test"
        addition = """## Ascendant Guild Worldgen And Generated NPC Test

Status: pending Jayden in-game validation.

- Create a fresh creative test world.
- Run `/function ascendant_guild:npc/list`.
- Run `/function ascendant_guild:npc/spawn_set/starter_guild_staff`.
- Confirm generated NPCs show rank, level, name, and role without manual editing.
- Run `/locate structure ascendant_guild:hunter_board_village_standard`.
- Run `/locate structure ascendant_guild:roadside_hunter_camp`.
- Run `/locate structure ascendant_guild:frontier_guild_outpost`.
- Teleport to each structure in fresh chunks.
- Confirm Bountiful bounty boards and Supplementaries notice boards render.
- Confirm no startup, datapack, or chunk-generation errors.
- On dedicated server, repeat locate/generate/join/rejoin and 10-minute stability checks.

"""
        if "## Ascendant Guild Worldgen And Generated NPC Test" not in text:
            text = text.replace(marker, addition + marker) if marker in text else text + "\n\n" + addition
            testing.write_text(text, encoding="utf-8")

    server = ROOT / "docs/SERVER_SETUP.md"
    if server.exists():
        text = server.read_text(encoding="utf-8", errors="replace")
        addition = """## Ascendant Guild Worldgen Server Test

After syncing/exporting the latest pack, test the standalone Guild worldgen layer on a fresh server world:

1. Join the server.
2. Run `/locate structure ascendant_guild:hunter_board_village_standard`.
3. Run `/locate structure ascendant_guild:roadside_hunter_camp`.
4. Run `/locate structure ascendant_guild:frontier_guild_outpost`.
5. Teleport to each result and confirm chunks generate cleanly.
6. Run `/function ascendant_guild:npc/spawn_set/starter_guild_staff` near one structure.
7. Disconnect/rejoin and let the server run 10 minutes.

"""
        if addition.strip() not in text:
            text += "\n\n" + addition
            server.write_text(text, encoding="utf-8")


def main() -> int:
    mirror_customnpcs_skin_assets()
    pack_summaries = {}
    for pack in PACK_NAMES:
        pack_summaries[pack] = write_pack(pack)

    summary = {
        "config": pack_summaries["config/openloader/data/ascendant_realms_guild"],
        "mirror": pack_summaries["openloader/data/ascendant_realms_guild"],
    }
    write_config_files(summary)
    write_docs(summary)
    patch_docs()
    print("Generated Ascendant Guild NPC profiles, Bountiful pools, and standalone worldgen structures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
