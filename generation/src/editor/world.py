import sys, math, gzip, zlib, time, os, shutil
from pathlib import Path
import editor.nbt as nbt
import editor.stream as stream
from editor.canvas import Canvas

class BlockState:
    def __init__(self, name, props={}, items=None):
        self.name = name
        self.props = props
        self.items = items
        self.id = None

    def __str__(self):
        return f'BlockState({self.name}, {str(self.props)})'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return type(self) == type(other) and other != None and self.name == other.name and self.props == other.props

    def clone(self):
        return BlockState(self.name, self.props.copy())

class Block:
    def __init__(self, state, block_light, sky_light, dirty=False):
        self._state = state
        self.block_light = 0
        self.sky_light = 0
        self._dirty = dirty

    def __str__(self):
        return f'Block({str(self._state)}, {self.block_light}, {self.sky_light})'

    def set_state(self, state):
        self._dirty = True
        if type(state) is BlockState:
            self._state = state
        else:
            self._state = BlockState(state, {})

    def get_state(self):
        return self._state.clone()

class ChunkSection:
    def __init__(self, blocks, raw_section, y_index):
        self.blocks = blocks
        self.raw_section = raw_section
        self.y_index = y_index
        

    def get_block(self, block_pos):
        x = block_pos[0]
        y = block_pos[1]
        z = block_pos[2]

        return self.blocks[x + z * 16 + y * 16 ** 2]

    def serialize(self):
        # print(f"Serializing section {self.y_index}...")
        serial_section = self.raw_section
        dirty = any([b._dirty for b in self.blocks])
        if dirty:
            self.palette = list(set([ b._state for b in self.blocks ] + [ BlockState('minecraft:air', {}) ]))
            self.palette.sort(key=lambda s: s.name)
            serial_section.add_child(nbt.ByteTag(self.y_index, tag_name='Y'))
            mat_id_mapping = {self.palette[i]: i for i in range(len(self.palette))}
            new_palette = self._serialize_palette()
            serial_section.add_child(nbt.CompoundTag('block_states', [self._serialize_blockstates(mat_id_mapping), new_palette]))
        
        if not serial_section.has('SkyLight'):
            serial_section.add_child(nbt.ByteArrayTag(tag_name='SkyLight', children=[nbt.ByteTag(-1, tag_name='None') for i in range(2048)]))

        if not serial_section.has('BlockLight'):
            serial_section.add_child(nbt.ByteArrayTag(tag_name='BlockLight', children=[nbt.ByteTag(-1, tag_name='None') for i in range(2048)]))

        return serial_section

    def _serialize_palette(self):
        serial_palette = nbt.ListTag(nbt.CompoundTag.clazz_id, tag_name='palette')
        for state in self.palette:
            palette_item = nbt.CompoundTag(tag_name='None', children=[
                nbt.StringTag(state.name, tag_name='Name')
            ])
            if len(state.props) != 0:
                serial_props = nbt.CompoundTag(tag_name='Properties')
                for name, val in state.props.items():
                    serial_props.add_child(nbt.StringTag(str(val), tag_name=name))
                palette_item.add_child(serial_props)
            serial_palette.add_child(palette_item)
        
        return serial_palette
    
    def _serialize_blockstates(self, state_mapping):
        serial_states = nbt.LongArrayTag(tag_name='data')
        width = max(4, math.ceil(math.log(len(self.palette), 2)))
        
        per_long = 64 // width
        blocks_len = len(self.blocks)
        lng_blocks = math.ceil(blocks_len / per_long)
        
        for long_index in range(lng_blocks):
            lng = 0
            end = long_index * per_long
            for i in range(per_long):
                index = end + per_long - i - 1
                if index >= blocks_len:
                    lng <<= width
                else:
                    lng = (lng << width) + state_mapping[self.blocks[index]._state]
            
            lng = int.from_bytes(lng.to_bytes(8, byteorder='big', signed=False), byteorder='big', signed=True)
            serial_states.add_child(nbt.LongTag(lng))

        return serial_states

class Chunk:
    def __init__(self, xpos, zpos, sections, raw_nbt, orig_size):
        self.xpos = xpos
        self.zpos = zpos
        self.sections = sections
        self.raw_nbt = raw_nbt
        
        self.orig_size = orig_size
        
    def get_block(self, block_pos):
        block = self.get_section(block_pos[1]).get_block([n % 16 for n in block_pos])
        tileData = []
        for e in self.raw_nbt.get('block_entities').children:
            if block_pos == (e.get('x').get(), e.get('y').get(), e.get('z').get()):
                tileData.append(e)
        return (block, tileData)

    def get_section(self, y):
        key = int(y/16)
        if key not in self.sections:
            self.sections[key] = ChunkSection(
                [Block(BlockState('minecraft:air', {}), 0, 0, dirty=True) for i in range(4096)],
                nbt.CompoundTag(),
                key
            )
        return self.sections[key]

    def find_like(self, string):
        results = []
        for sec in self.sections:
            section = self.sections[sec]
            for x1 in range(16):
                for y1 in range(16):
                    for z1 in range(16):
                        if string in section.get_block((x1, y1, z1))._state.name:
                            results.append((
                                (x1 + self.xpos * 16, y1 + sec * 16, z1 + self.zpos * 16), 
                                section.get_block((x1, y1, z1))
                            ))
        return results

    # Blockstates are packed based on the number of values in the pallet. 
    # This selects the pack size, then splits out the ids
    def unpack(raw_nbt):

        sections = {}
        for section in raw_nbt.get('sections').children:
            if section.has('block_states') and section.get('block_states').has('data'):
                num_states = len(section.get('block_states').get('palette').children)
                pack_size = max(4, math.ceil(math.log(num_states, 2)))
                # print(f"num_states {num_states}")
                num_flatstates = math.ceil(16**3 / (64 // pack_size))
                flatstates = [c.get() for c in section.get('block_states').get('data').children[:num_flatstates]]
                states = [
                    Chunk._read_width_from_loc(flatstates, pack_size, i) for i in range(16**3)
                ]
            else:
                # Sections which contain only air have no states.
                states = []
            if section.has('block_states') and section.get('block_states').has('palette'):
                palette = [ 
                    BlockState(
                        state.get('Name').get(),
                        state.get('Properties').to_dict() if state.has('Properties') else {}
                    ) for state in section.get('block_states').get('palette').children
                ]
            else:
                # Nor any palette entries.
                palette = None
            block_lights = Chunk._divide_nibbles(section.get('BlockLight').get()) if section.has('BlockLight') else None
            sky_lights = Chunk._divide_nibbles(section.get('SkyLight').get()) if section.has('SkyLight') else None
            blocks = []
            for i in range(len(states)):
                state = palette[states[i]]
                block_light = block_lights[i] if block_lights else 0
                sky_light = sky_lights[i] if sky_lights else 0
                blocks.append(Block(state, block_light, sky_light))

            if len(blocks) == 0:
                # print(f"0 found... filling with {palette[0].name}")
                blocks = [Block(BlockState(palette[0].name, {}), 0, 0, dirty=True) for i in range(4096)]
            elif len(blocks) < 4096:
                raise Exception("Not enough blocks in section")
            sections[section.get('Y').get()] = ChunkSection(blocks, section, section.get('Y').get())
        return sections

    def _divide_nibbles(arry):
        rtn = []
        f2_mask = 2**4-1
        f1_mask = f2_mask << 4
        for s in arry:
            rtn.append(s & f1_mask)
            rtn.append(s & f2_mask)

        return rtn

    def pack(self):
        print(f"Serializing chunk ({self.xpos}, {self.zpos})")
        
        new_sections = nbt.ListTag(nbt.CompoundTag.clazz_id, tag_name='sections', children=[
            self.sections[sec].serialize() for sec in self.sections
        ])
        new_nbt = self.raw_nbt.clone()
        new_nbt.add_child(new_sections)

        return new_nbt

    def _read_width_from_loc(long_list, width, possition):
        per_long = 64 // width
        index = possition // per_long
        offset = possition % per_long
        # print(f"Reading {possition} from {index} {offset} of {len(long_list)} {per_long}")
        comp = Chunk._read_bits(long_list[index], width, width * offset)
        return comp


    def _read_bits(num, width, start):
        # create a mask of size 'width' of 1 bits
        mask = (2 ** width) - 1
        # shift it out to where we need for the mask
        mask = mask << start
        # select the bits we need
        comp = num & mask
        # move them back to where they should be
        comp = comp >> start

        return comp

    def __str__(self):
        return f'Chunk({str(self.xpos)},{str(self.zpos)})'

class World:
    def __init__(self, world_folder, save_location=None, debug=False, read=True, write=True):
        self.debug = debug
        if save_location is not None:
            self.world_folder = Path(save_location) / world_folder
        else:
            self.world_folder = Path(world_folder)
        if not self.world_folder.is_dir():
            raise FileNotFoundError(f'No such folder \"{self.world_folder}\"')
        self.chunks = {}

    def __enter__(self):
        return self
    
    def __exit__(self, typ, val, trace):
        if typ is None:
            self.close()

    def flush(self):
        self.close()
        self.chunks = {}

    def close(self, output):
        shutil.rmtree(output)
        shutil.copytree(self.world_folder, output)

        chunks_by_region = {}
        for chunk_pos, chunk in self.chunks.items():
            region = self._get_region_file(chunk_pos)
            if region not in chunks_by_region:
                chunks_by_region[region] = []
            chunks_by_region[region].append(chunk)

        for region_name, chunks in chunks_by_region.items():
            with open(Path(output) / 'region' / region_name, mode='r+b') as region:
                region.seek(0)
                locations = [[
                            int.from_bytes(region.read(3), byteorder='big', signed=False) * 4096, 
                            int.from_bytes(region.read(1), byteorder='big', signed=False) * 4096
                        ] for i in range(1024) ]

                timestamps = [int.from_bytes(region.read(4), byteorder='big', signed=False) for i in range(1024)]

                data_in_file = bytearray(region.read())

                chunks.sort(key=lambda chunk: locations[((chunk.xpos % 32) + (chunk.zpos % 32) * 32)][0])
                # print("writing chunks", [str(c) + ":" + str(locations[((chunk.xpos % 32) + (chunk.zpos % 32) * 32)][0]) for c in chunks])

                for chunk in chunks:
                    strm = stream.OutputStream()
                    chunkNBT = chunk.pack()
                    chunkNBT.serialize(strm)
                    data = zlib.compress(strm.get_data())
                    datalen = len(data)
                    block_data_len = math.ceil((datalen + 5)/4096.0)*4096
                    # Constuct new data block
                    data = (datalen + 1).to_bytes(4, byteorder='big', signed=False) + \
                        (2).to_bytes(1, byteorder='big', signed=False) + \
                        data + \
                        (0).to_bytes(block_data_len - (datalen + 5), byteorder='big', signed=False)

                    timestamps[((chunk.xpos % 32) + (chunk.zpos % 32) * 32)] = int(time.time())

                    loc = locations[((chunk.xpos % 32) + (chunk.zpos % 32) * 32)]
                    original_sector_length = loc[1]
                    data_len_diff = block_data_len - original_sector_length
                    if data_len_diff != 0 and self.debug:
                        print(f'Danger: Diff is {data_len_diff}, shifting required!')

                    locations[((chunk.xpos % 32) + (chunk.zpos % 32) * 32)][1] = block_data_len

                    if loc[0] == 0 or loc[1] == 0:
                        print('Chunk not generated', chunk)
                        sys.exit(0)

                    # Adjust sectors after this one that need their locations recalculated
                    for i, other_loc in enumerate(locations):
                        if other_loc[0] > loc[0]:
                            locations[i][0] = other_loc[0] + data_len_diff

                    header_length = 2*4096
                    data_in_file[(loc[0] - header_length):(loc[0] + original_sector_length - header_length)] = data
                    if self.debug:
                        print(f'Saving {chunk} with', {'loc': loc, 'new_len': datalen, 'old_len': chunk.orig_size, 'sector_len': block_data_len})

                # rewrite entire file with new chunks and locations recorded
                region.seek(0)

                for c_loc in locations:
                    region.write(int(c_loc[0]/4096).to_bytes(3, byteorder='big', signed=False))
                    region.write(int(c_loc[1]/4096).to_bytes(1, byteorder='big', signed=False))

                for ts in timestamps:
                    region.write(ts.to_bytes(4, byteorder='big', signed=False))

                region.write(data_in_file)

                required_padding = (math.ceil(region.tell()/4096.0) * 4096) - region.tell()

                region.write((0).to_bytes(required_padding, byteorder='big', signed=False))

    def get_block(self, block_pos):
        chunk_pos = self._get_chunk(block_pos)
        chunk = self.get_chunk(chunk_pos)
        return chunk.get_block(block_pos)

    def get_chunk(self, chunk_pos):
        if chunk_pos not in self.chunks:
            self._load_chunk(chunk_pos)

        return self.chunks[chunk_pos]

    def get_canvas(self):
        return Canvas(self)

    def _load_chunk(self, chunk_pos):
        with open(self.world_folder / 'region' / self._get_region_file(chunk_pos), mode='rb') as region:
            locations = [[
                        int.from_bytes(region.read(3), byteorder='big', signed=False) * 4096, 
                        int.from_bytes(region.read(1), byteorder='big', signed=False) * 4096
                    ] for i in range(1024) ]

            timestamps = region.read(4096)

            loc = locations[((chunk_pos[0] % 32) + (chunk_pos[1] % 32) * 32)]
            if self.debug:
                print('Loading', chunk_pos,'from', region.name)
            chunk = self._load_binary_chunk_at(region, loc[0], loc[1])
            self.chunks[chunk_pos] = chunk

    def _load_binary_chunk_at(self, region_file, offset, max_size):
        region_file.seek(offset)
        datalen = int.from_bytes(region_file.read(4), byteorder='big', signed=False)
        compr = region_file.read(1)
        # print(region_file.tell()-5, datalen)
        decompressed = zlib.decompress(region_file.read(datalen-1))
        data = nbt.parse_nbt(stream.InputStream(decompressed))
        chunk_pos = (data.get('xPos').get(), data.get('zPos').get())
        chunk = Chunk(
            chunk_pos[0],
            chunk_pos[1],
            Chunk.unpack(data),
            data,
            datalen
        )
        return chunk

    def _get_region_file(self, chunk_pos):
        return 'r.' + '.'.join([str(x) for x in self._get_region(chunk_pos)]) + '.mca'

    def _get_chunk(self, block_pos):
        return (math.floor(block_pos[0] / 16), math.floor(block_pos[2] / 16))

    def _get_region(self, chunk_pos):
        return (math.floor(chunk_pos[0] / 32), math.floor(chunk_pos[1] / 32))
