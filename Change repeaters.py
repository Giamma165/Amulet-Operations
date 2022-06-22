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

Repeaters = {
    "minecraft:repeater",
}

def ChangeRepeaters(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):

    block_platform = "java"
    block_version = (1, 16, 5)

    CheckBox = options["Check to add 1 redstone tick, uncheck to remove 1 redstone tick"]
    KeepProportions = options["Keep proportions"]

    for box in selection:
        iter_count = 1
        count = 0

        for x, y, z in box:
            src_block, blockEntity = world.get_version_block(
                x, y, z, dimension, (block_platform, block_version)
            )

            if src_block.namespaced_name in Repeaters:
                print(src_block)
                iter_count += 1

                CurrentDelay = src_block.properties["delay"]
                Facing = src_block.properties["facing"]

                CurrentDelay = str(CurrentDelay)
                CurrentDelay = int(CurrentDelay)

                if CheckBox == True:
                    if CurrentDelay == 4 and KeepProportions == True:
                        raise ValueError("There are repeaters with already the maximum of ticks: this would make you lose the proportions between the comparators")
                    if CurrentDelay != 4:
                        CurrentDelay = CurrentDelay + 1
                    str(CurrentDelay)
                    CurrentDelay = TAG_String(CurrentDelay)

                if CheckBox == False:
                    if CurrentDelay == 1 and KeepProportions == True:
                        raise ValueError("There are repeaters with already the minimum of ticks: this would make you lose the proportions between the comparators")
                    if CurrentDelay != 1:
                        CurrentDelay = CurrentDelay -1
                    str(CurrentDelay)
                    CurrentDelay = TAG_String(CurrentDelay)

                try:
                    block = Block(
                        "minecraft", "repeater", {"facing": Facing, "delay": CurrentDelay}
                    )
                    world.set_version_block(
                        x, y, z, dimension, (block_platform, block_version), block, blockEntity
                    )

                except ChunkLoadError:
                    print(f"Unable to load chunk {x>>4}, {z>>4} at coordinates {x}, {z}")

                yield count / iter_count

                count += 1

operation_options = {
    "Check to add 1 redstone tick, uncheck to remove 1 redstone tick": [
        "bool",
        True,
    ],
    "Keep proportions": [
        "bool",
        True,
    ],
}


export = {"name" : "Change repeaters (by Giamma165)", "operation" : ChangeRepeaters, "options" : operation_options}
