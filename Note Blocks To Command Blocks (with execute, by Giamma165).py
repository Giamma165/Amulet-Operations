# Operation made by Giamma165
# Not compatible with Bedrock Edition
# Feel free to edit the operation
# Credit to the author is always appreciated.

from amulet.api.selection import SelectionGroup, SelectionBox
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension, BlockCoordinates
from amulet.api.block import Block # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties
from amulet.api.errors import ChunkLoadError, ChunkDoesNotExist
from typing import Tuple, Dict

Sources = ["master", "music", "record", "weather", "block", "hostile", "neutral", "player", "ambient", "voice"]
Instruments = ["banJo","basedrum","bass","bell","bit","chime","cow_bell","didgeridoo","flute","guitar","harp","hat","iron_xylophone","pling","snare","xylophone"]

note_blocks = {
    "minecraft:note_block",
}

def join_with_spaces(*i):
    return " ".join(map(str, i))

def note_to_command(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    if world.level_wrapper.platform != "java":
        raise OperationError("This operation only supports Java Edition worlds.")

    block_platform = "java"
    block_version = (1, 16, 5)

    tag = options["execute as @a with tag"].strip()
    coords = options["Coordinates"].strip()
    volume = options["Volume"]
    minVolume = options["Min. Volume"]
    source = options["Source"].strip()

    ModifyInstrument1 = options["Modify Instrument 1"].strip()
    ModifyInstrument2 = options["Modify Instrument 2"].strip()
    ModifyInstrument3 = options["Modify Instrument 3"].strip()

    ToInstrument1 = options["to Instrument 1"].strip()
    ToInstrument2 = options["to Instrument 2"].strip()
    ToInstrument3 = options["to Instrument 3"].strip()

    CustomVolume1 = options["with custom volume 1"].strip()
    CustomVolume2 = options["with custom volume 2"].strip()
    CustomVolume3 = options["with custom volume 3"].strip()

    if CustomVolume1 != "-":
        if CustomVolume1 != "":
            CustomVolume1 = float(CustomVolume1)
            if CustomVolume1 < 0.0:
                raise ValueError('Custom volume cannot be negative')

    if CustomVolume2 != "-":
        if CustomVolume2 != "":
            CustomVolume2 = float(CustomVolume2)
            if CustomVolume2 < 0.0:
                raise ValueError('Custom volume cannot be negative')

    if CustomVolume3 != "-":
        if CustomVolume3 != "":
            CustomVolume3 = float(CustomVolume3)
            if CustomVolume3 < 0.0:
                raise ValueError('Custom volume cannot be negative')

    volume = float(volume)
    minVolume = float(minVolume)

    for box in selection:
        iter_count = 1
        count = 0

        for c in tag:
            if " " == c:
                raise ValueError('Tag: invalid syntax.')

        SpacesCount = 0
        for a in coords:
            if " " == a:
                SpacesCount += 1

        if SpacesCount != 2:
            raise ValueError('Invalid coordinates.  Syntax must be x y z.')

        NumTest = 0
        if coords != "~ ~ ~":
            for b in coords:
                if " " != b:
                    NumTest += 1
                    float(b)

        if volume < 0.0:
            raise ValueError('Volume cannot be negative')

        if minVolume < 0.0:
            raise ValueError('Min. Volume cannot be negative')

        if minVolume > 1.0:
            raise ValueError('Min. Volume cannot be greater than 1')

        if source not in Sources:
            raise ValueError('Invalid source.   Sources: master, music, record, weather, block, hostile, neutral, player, ambient, voice')

        if ModifyInstrument1 not in Instruments:
            raise ValueError('Invalid Instruments: first group.   Instruments: banjo, basedrum, bass, bell, bit, chime, cow_bell, didgeridoo, flute, guitar, harp, hat, iron_xylophone, pling, snare, xylophone')

        if ModifyInstrument2 not in Instruments:
            raise ValueError('Invalid Instruments: second group.   Instruments: banjo, basedrum, bass, bell, bit, chime, cow_bell, didgeridoo, flute, guitar, harp, hat, iron_xylophone, pling, snare, xylophone')

        if ModifyInstrument3 not in Instruments:
            raise ValueError('Invalid Instruments: third group.   Instruments: banjo, basedrum, bass, bell, bit, chime, cow_bell, didgeridoo, flute, guitar, harp, hat, iron_xylophone, pling, snare, xylophone')

        if ToInstrument1 not in Instruments:
            raise ValueError('Invalid Instruments: first group.   Instruments: banjo, basedrum, bass, bell, bit, chime, cow_bell, didgeridoo, flute, guitar, harp, hat, iron_xylophone, pling, snare, xylophone')

        if ToInstrument2 not in Instruments:
            raise ValueError('Invalid Instruments: second group.   Instruments: banjo, basedrum, bass, bell, bit, chime, cow_bell, didgeridoo, flute, guitar, harp, hat, iron_xylophone, pling, snare, xylophone')

        if ToInstrument3 not in Instruments:
            raise ValueError('Invalid Instruments: third group.   Instruments: banjo, basedrum, bass, bell, bit, chime, cow_bell, didgeridoo, flute, guitar, harp, hat, iron_xylophone, pling, snare, xylophone')

        for x, y, z in box:
            src_block, blockEntity = world.get_version_block(
                x, y, z, dimension, (block_platform, block_version)
                )

            if src_block.namespaced_name in note_blocks:
                print(src_block)
                iter_count += 1

                Instrument = src_block.properties["instrument"]
                volume = options["Volume"]

                if Instrument == ModifyInstrument1:
                    Instrument = ToInstrument1
                    print(Instrument)
                    if CustomVolume1 != "-":
                        if CustomVolume1 != "":
                            volume = CustomVolume1
                            print(volume)


                if Instrument == ModifyInstrument2:
                    Instrument = ToInstrument2
                    print(Instrument)
                    if CustomVolume2 != "-":
                        if CustomVolume2 != "":
                            volume = CustomVolume2
                            print(volume)

                if Instrument == ModifyInstrument3:
                    Instrument = ToInstrument3
                    print(Instrument)
                    if CustomVolume3 != "-":
                        if CustomVolume3 != "":
                            volume = CustomVolume3
                            print(volume)

                instrument = "block.note_block." + Instrument

                if len(coords) == 0:
                    coords = join_with_spaces(x, y, z)

                note = src_block.properties["note"]
                note = str(note)
                note = int(note)
                note = note * 0.08333333
                pitch = 0.5 * 2 ** note

                newCommand = join_with_spaces("execute as @a[tag="+tag+"] at @s run playsound", instrument, source, "@s", coords, volume, pitch, minVolume)
                if tag == "":
                    newCommand = join_with_spaces("execute as @a at @s run playsound", instrument, source, "@s", coords, volume, pitch, minVolume)
                if tag == "-":
                    newCommand = join_with_spaces("execute as @a at @s run playsound", instrument, source, "@s", coords, volume, pitch, minVolume)

                try:
                    block = Block(
                        "minecraft", "command_block", {}
                    )
                    theNBT = TAG_Compound()
                    theNBT["Command"] = TAG_String(newCommand)
                    print(theNBT)
                    blockEntity = BlockEntity(
                        "minecraft", "command_block", x, y, z, NBTFile(theNBT)
                    )
                    world.set_version_block(
                        x, y, z, dimension, (block_platform, block_version), block, blockEntity
                    )

                except ChunkLoadError:
                    print(f"Unable to load chunk {x>>4}, {z>>4} at coordinates {x}, {z}")

                yield count / iter_count

                count += 1

operation_options = {
    "execute as @a with tag": [
        "str",
        "",
    ],
    "Coordinates": [
        "str",
        " ~ ~ ~",
    ],
    "Source": [
        "str",
        "master",
    ],
    "Volume": [
        "str",
        "1.0",
    ],
    "Min. Volume": [
        "str",
        "0.0",
    ],
    "Modify Instrument 1": [
        "str",
        "harp",
    ],
    "to Instrument 1": [
        "str",
        "harp"
    ],
    "with custom volume 1": [
        "str",
        " -"
    ],
    "Modify Instrument 2": [
        "str",
        "bass",
    ],
    "to Instrument 2": [
        "str",
        "bass"
    ],
    "with custom volume 2": [
        "str",
        " -"
    ],
    "Modify Instrument 3": [
        "str",
        "flute",
    ],
    "to Instrument 3": [
        "str",
        "flute"
    ],
    "with custom volume 3": [
        "str",
        " -"
    ]
}

export = {"name": "Note Blocks To Command Blocks (with execute, by Giamma165)", "operation": note_to_command,"options": operation_options}
