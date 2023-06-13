import math

from editor import world
from editor import schema
from schema import adder, layer


def clockLineSegment():
    return schema.Schema([
        [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            [' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B '],
        ],
        [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', 'Rr4', ' B ', 'Rr3', ' - '],
        ]
    ],
        {
        ' B ': 'minecraft:light_blue_concrete',
        ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
        'Rr3': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '3'}),
        'Rte': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'east'}),
        'Rr4': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '4'}),
    })


def network(newt):
    sizes, networkData = newt
    res = layer.layer(sizes[0], sizes[1], networkData[0])
    clockWire = schema.Schema([[[]]], {})
    for i in range(sizes[1]):
        clockWire = clockWire.join(clockLineSegment(), (0, 0, -adder.ADDER_LENGTH))

    clockWire = clockWire.join(schema.Schema([
        [
            ['   ', '   ', ' B ', ' B ', '   '],
            ['   ', '   ', ' B ', ' B ', ' B ']
        ],
        [
            ['Rln', ' B ', 'Rcn', 'Rrn', ' B '],
            ['   ', '   ', ' - ', 'Rrs', ' - ']
        ],
    ],
        {
        ' B ': 'minecraft:light_blue_concrete',
        ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
        'Rrn': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '3'}),
        'Rrs': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '3'}),
        'Rln': world.BlockState('minecraft:lever', {'facing': 'north', 'face': 'wall'}),
        'Rcn': world.BlockState('minecraft:comparator', {'facing': 'north', 'mode': 'subtract'}),
    }), (0, 0, -5))

    for i in range(len(sizes) - 2):
        l = layer.layer(
            sizes[i + 1],
            sizes[i + 2], networkData[i + 1])
        res = res.join(
            l, (res.size[0] - l.size[0], res.size[1] - 4, 0))
        m = layer.multiplexer(
            sizes[i + 1],
            sizes[i + 2])
        res = res.join(
            m,
            (res.size[0] - m.size[0] - 5, res.size
             [1] - l.size[1] + 1, 2))

    tallySegment = schema.Schema(
        [
            [
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ],
            [
                ['   ', '   ', '   ', '   ', 'B3 ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', ' B ', '   ', ' B ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', ' B ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ],
            [
                ['   ', '   ', '   ', 'B3 ', ' L ', 'B3 ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', 'Rt ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['Hw1', 'Rcn', ' B ', 'Rrn', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['He2', '   ', ' B ', '   ', 'Hw2', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                [' B ', 'Rrs', ' B ', 'Rcs', 'He1', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', ' T ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ],
            [
                ['   ', '   ', '   ', 'B3 ', ' L ', 'B3 ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                [' B ', ' G ', ' - ', ' G ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                [' - ', '   ', ' B ', '   ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', 'B2 ', 'Rrw', 'B2 ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                [' - ', 'Rtn', ' B ', 'Rts', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', '   ', 'B2 ', '   '],
                ['   ', '   ', 'Rt ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', '   '],
                ['   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', '   '],
            ],
            [
                ['   ', '   ', '   ', '   ', 'B3 ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                [' - ', ' - ', '   ', ' - ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['Rte', '   ', '   ', '   ', 'Rte', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['B2 ', ' - ', 'B2 ', ' - ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', '   ', '   ', '   ', '   '],
                ['Rtw', '   ', ' - ', '   ', 'Rtw', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', 'Rrs', 'Ro ', ' - ', '   '],
                ['   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   '],
            ],
            [
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', ' - ', '   ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ],
            [
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ],
        ],
        {' O ': 'minecraft:air',
         ' B ': 'minecraft:yellow_concrete',
         'B2 ': 'minecraft:light_blue_concrete',
         'B3 ': 'minecraft:red_concrete',
         ' G ': 'minecraft:glass',
         ' T ': 'minecraft:target',
         ' L ': 'minecraft:redstone_lamp',
         'Bb ': world.BlockState('minecraft:barrel', {'facing': 'west'}),
         'He1': world.BlockState('minecraft:hopper', {'facing': 'east'}),
         'Hw1': world.BlockState('minecraft:hopper', {'facing': 'west'}),
         'He2': world.BlockState('minecraft:hopper', {'facing': 'east'}, [('minecraft:stick', 15)]),
         'Hw2': world.BlockState('minecraft:hopper', {'facing': 'west'}, [('minecraft:stick', 15)]),
         'Rd1': world.BlockState('minecraft:dropper', {'facing': 'south'}),
         'Rd2': world.BlockState('minecraft:dropper', {'facing': 'north'}),
         'Ro ': world.BlockState('minecraft:observer', {'facing': 'south'}),
         'Rcn': world.BlockState('minecraft:comparator', {'facing': 'north', 'mode': 'subtract'}),
         'Rce': world.BlockState('minecraft:comparator', {'facing': 'east', 'mode': 'subtract'}),
         'Rcs': world.BlockState('minecraft:comparator', {'facing': 'south', 'mode': 'subtract'}),
         'Rcw': world.BlockState('minecraft:comparator', {'facing': 'west', 'mode': 'subtract'}),
         'Rrw': world.BlockState('minecraft:repeater', {'facing': 'west', 'delay': '1', 'locked': 'false'}),
         'Rrs': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '2', 'locked': 'false'}),
         'Rrn': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '2', 'locked': 'false'}),
         'Rt ': world.BlockState('minecraft:redstone_torch'),
         'Rte': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'east'}),
         'Rtw': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'west'}),
         'Rtn': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'north'}),
         'Rts': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'south'}),
         'Rl ': world.BlockState('minecraft:lever', {'face': 'wall', 'facing': 'north', 'powered': 'false'}),
         ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}), })
    
    inputSegment = schema.Schema([
        [
            ['   ', '   ', '   ', '   ', '   '],
            ['   ', ' B ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   '],
        ],
        [
            ['   ', '   ', '   ', '   ', '   '],
            [' B ', ' - ', ' T ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   '],
        ],
        [
            ['   ', '   ', '   ', '   ', '   '],
            ['Rl ', ' B ', 'Rt ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   '],
        ],
        [
            ['   ', ' B ', '   ', '   ', '   '],
            ['   ', ' L ', ' B ', 'Rts', '   '],
            ['   ', ' B ', '   ', '   ', '   '],
        ],
        [
            ['   ', ' B ', '   ', '   ', '   '],
            ['   ', ' L ', ' - ', ' G ', '   '],
            ['   ', ' B ', '   ', '   ', '   '],
        ],
        [
            ['   ', '   ', '   ', '   ', '   '],
            ['   ', ' B ', '   ', ' - ', '   '],
            ['   ', '   ', '   ', '   ', '   '],
        ],
    ], {
        ' B ': 'minecraft:red_concrete',
        ' G ': 'minecraft:glass',
        ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
        ' T ': 'minecraft:target',
        ' L ': 'minecraft:redstone_lamp',
        'Rl ': world.BlockState('minecraft:lever', {'face': 'floor', 'facing': 'south', 'powered': 'false'}),
        'Rt ': world.BlockState('minecraft:redstone_torch'),
        'Rts': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'south'}),
    })
    
    h = res.size[1] - 4
    for i in range(sizes[-1]):
        res = res.join(tallySegment, (res.size[0] - 13, h, i * adder.ADDER_LENGTH))

    res = res.join(clockWire, (res.size[0] - 4, 0, -3))

    for i in range(sizes[0]):
        res = res.join(inputSegment, (res.size[0] - i * adder.ADDER_WIDTH - 13, 2, 1))


    return res
