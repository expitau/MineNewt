from editor import world
import editor.nbt as nbt
import numpy as np


def setBlock(save_file, block_pos, state):
    chunk_pos = save_file._get_chunk(block_pos)
    chunk = save_file.get_chunk(chunk_pos)
    section = chunk.get_section(block_pos[1])
    block = section.get_block([n % 16 for n in block_pos])

    if state.items is not None:
        for e in chunk.raw_nbt.get('block_entities').children:
            if block_pos == (e.get('x').get(), e.get('y').get(), e.get('z').get()):
                print("Found existing data, removing...")
                chunk.raw_nbt.get(
                    'block_entities').children.remove(e)
        chunk.raw_nbt.get('block_entities').sub_type_id = 10
        chunk.raw_nbt.get('block_entities').add_child(
            nbt.CompoundTag(children=[
                nbt.ByteTag(tag_value=0, tag_name="keepPacked"),
                nbt.IntTag(tag_value=block_pos[0], tag_name="x"),
                nbt.IntTag(tag_value=block_pos[1], tag_name="y"),
                nbt.IntTag(tag_value=block_pos[2], tag_name="z"),
                nbt.ListTag(10, 'Items', [
                    nbt.CompoundTag(children=[
                        nbt.ByteTag(i, 'Slot'),
                        nbt.StringTag(item[0], 'id'),
                        nbt.ByteTag(item[1], 'Count'),
                    ]) for i, item in enumerate(state.items)
                ]),
                nbt.StringTag(tag_value=state.name, tag_name="id")
            ]))
    block.set_state(state)


def getBlock(save_file, block_pos):
    return save_file.get_block(block_pos)


class Schema:
    def __init__(self, data, palette=None):

        self.size = (len(data[0]), len(data), len(data[0][0]))
        tmp = data
        if palette != None:
            for dy, layer in enumerate(data):
                for dx, row in enumerate(layer):
                    for dz, block in enumerate(row):
                        if block in palette:
                            if isinstance(palette[block], str):
                                palette[block] = world.BlockState(
                                    palette[block])
                            block = palette[block]
                        elif not isinstance(block, world.BlockState):
                            if block and not (isinstance(block, str) and block.isspace()):
                                print(
                                    f"WARNING: '{block}' not found in palette")
                            block = None
                        tmp[dy][dx][dz] = block
        self.data = np.array(tmp)

    def __str__(self):
        out = "\n=== Schema ===\n"
        layers = []
        for layer in self.data:
            rows = []
            for row in layer:
                rows.append(
                    ''.join([chr(hash(c) % 58 + ord('A')) if c is not None else ' ' for c in row]))
            layers.append('\n'.join(rows))
        out += '\n---\n'.join(layers)
        out += "\n=============="
        return out

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return type(self) == type(other) and other != None and self.data == other.data

    def join(self, other, offset=(0, 0, 0), force=True):
        outStart = (min(0, offset[0]), min(0, offset[1]), min(0, offset[2]))
        outEnd = (max(self.size[0], other.size[0] + offset[0]), max(self.size[1],
                  other.size[1] + offset[1]), max(self.size[2], other.size[2] + offset[2]))

        selfStart = (max(0, -offset[0]), max(0, -offset[1]), max(0, -offset[2]))
        selfEnd = tuple(a + b for a, b in zip(selfStart, self.size))

        otherStart = (max(0, offset[0]), max(0, offset[1]), max(0, offset[2]))
        otherEnd = tuple(a + b for a, b in zip(otherStart, other.size))

        xStart, yStart, zStart = outStart
        xEnd, yEnd, zEnd = outEnd

        xSize, ySize, zSize = xEnd - xStart, yEnd - yStart, zEnd - zStart

        new_data = np.full((ySize, xSize, zSize), None, dtype=object)

        selfMask = np.full((ySize, xSize, zSize), False, dtype=bool)
        otherMask = np.full((ySize, xSize, zSize), False, dtype=bool)

        selfMask[selfStart[1]:selfEnd[1], selfStart[0]:selfEnd[0], selfStart[2]:selfEnd[2]] = True
        otherMask[otherStart[1]:otherEnd[1], otherStart[0]:otherEnd[0], otherStart[2]:otherEnd[2]] = other.data != None

        new_data[selfMask] = self.data.ravel()
        new_data[otherMask] = other.data[other.data != None]

        return Schema(new_data)

    def clone(self):
        return Schema(self.data)

    def parseRedstone(self):
        print("Normalizing redstone...")
        new_data = [[[None for z in range(self.size[2])] for x in range(
            self.size[0])] for y in range(self.size[1])]

        for y, layer in enumerate(self.data):
            for x, row in enumerate(layer):
                for z, block in enumerate(row):
                    if block is not None and block.name == 'minecraft:redstone_wire':

                        new_data[y][x][z] = world.BlockState(
                            'minecraft:redstone_wire', getSides(self.data, (x, y, z)))
                    else:
                        new_data[y][x][z] = block
        return Schema(new_data)

    def write(self, save_file, pos):
        data = self.parseRedstone().data
        for dy, layer in enumerate(data):
            for dx, row in enumerate(layer):
                print(f"Writing layer {dy}/{len(data)} row {dx}/{len(layer)}")
                for dz, block in enumerate(row):
                    block_pos = (pos[0] - dx, pos[1] + dy, pos[2] + dz)
                    if block is not None:
                        setBlock(save_file, block_pos, block)


def getSides(data, pos):
    sides = ['none', 'none', 'none', 'none']

    for i in range(4):
        sides[i] = getSide(data, pos, i)

    for i in range(4):
        if sides[i] != 'none' and sides[(i + 1) % 4] == 'none' and sides[(i - 1) % 4] == 'none' and sides[(i + 2) % 4] == 'none':
            sides[(i + 2) % 4] = 'side'

    return {'north': sides[0], 'east': sides[1], 'south': sides[2], 'west': sides[3]}


def getSide(data, pos, d):

    def safe_index(data, idx1, idx2, idx3):
        if 0 <= idx1 < len(data) and 0 <= idx2 < len(data[0]) and 0 <= idx3 < len(data[0][0]):
            return data[idx1][idx2][idx3]
        return None
    dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    down = safe_index(data, pos[1] - 1, pos[0] + dirs[d][0], pos[2] + dirs[d][1])
    center = safe_index(data, pos[1], pos[0] + dirs[d][0], pos[2] + dirs[d][1])
    up = safe_index(data, pos[1] + 1, pos[0] + dirs[d][0], pos[2] + dirs[d][1])
    top = safe_index(data, pos[1] + 1, pos[0], pos[2])

    facing = {'south': 0, 'west': 1, 'north': 2, 'east': 3}

    transparent = ['minecraft:air', 'minecraft:glass', 'minecraft:hopper', 'minecraft:redstone_torch', 'minecraft:redstone_wall_torch']

    if up:
        if up.name == 'minecraft:redstone_wire' and (not top or top.name in transparent):
            return 'up'

    if center:
        if center.name in ['minecraft:redstone_wire', 'minecraft:redstone_torch', 'minecraft:redstone_wall_torch', 'minecraft:target', 'minecraft:lever']:
            return 'side'
        if center.name == 'minecraft:repeater':
            if facing[center.props['facing']] == d or facing[center.props['facing']] == (d + 2) % 4:
                return 'side'
        if center.name == 'minecraft:comparator':
            return 'side'
        if center.name == 'minecraft:observer':
            if facing[center.props['facing']] == (d + 2) % 4:
                return 'side'

    if down:
        if down.name == 'minecraft:redstone_wire' and (not center or center.name in transparent):
            return 'side'

    return 'none'
