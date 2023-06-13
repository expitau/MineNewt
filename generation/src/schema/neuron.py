from editor import world
from editor import schema
from schema import adder
import math


def activationSegment(clamp):
    return schema.Schema(
        [[['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
          [' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            [' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
          ],
            [[' G ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', ' B ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', ' B ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [[' - ', ' G ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', ' T ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' B ', 'Rrs', ' B ', 'Rcs', 'Hw2', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['Hw1', '   ', ' B ', '   ', 'He1', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['He2', 'Rcn', ' B ', 'Rrn', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [[' G ', ' - ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', 'Rt ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', 'Rtn', ' B ', 'Rts', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', 'B2 ', 'Rre', 'B2 ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', '   ', ' B ', '   ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' B ', ' G ', ' - ', ' G ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [[' - ', ' G ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['Rte', '   ', ' - ', '   ', 'Rte', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', '   ', '   ', '   ', '   '],
             ['B2 ', ' - ', 'B2 ', ' - ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', '   ', '   ', ' T ', '   '],
             ['Rtw', '   ', '   ', '   ', 'Rtw', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', ' - ', '   ', ' - ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [['   ', ' - ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', 'B2 ', '   ', 'B2 ', '   '],
             ['   ', '   ', ' - ', '   ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', '   ', '   ', 'Rt ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', 'Rrs', 'Ro ', ' - ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
         ],
        {' O ': 'minecraft:air',
         ' B ': 'minecraft:yellow_concrete',
         'B2 ': 'minecraft:light_blue_concrete',
         ' G ': 'minecraft:glass',
         ' T ': 'minecraft:target',
         ' L ': 'minecraft:redstone_lamp',
         'Bb ': world.BlockState('minecraft:barrel', {'facing': 'west'}),
         'He1': world.BlockState('minecraft:hopper', {'facing': 'east'}),
         'Hw1': world.BlockState('minecraft:hopper', {'facing': 'west'}),
         'He2': world.BlockState('minecraft:hopper', {'facing': 'east'}, [('minecraft:stick', clamp)]),
         'Hw2': world.BlockState('minecraft:hopper', {'facing': 'west'}, [('minecraft:stick', clamp)]),
         'Rd1': world.BlockState('minecraft:dropper', {'facing': 'south'}),
         'Rd2': world.BlockState('minecraft:dropper', {'facing': 'north'}),
         'Ro ': world.BlockState('minecraft:observer', {'facing': 'south'}),
         'Rcn': world.BlockState('minecraft:comparator', {'facing': 'north', 'mode': 'subtract'}),
         'Rce': world.BlockState('minecraft:comparator', {'facing': 'east', 'mode': 'subtract'}),
         'Rcs': world.BlockState('minecraft:comparator', {'facing': 'south', 'mode': 'subtract'}),
         'Rcw': world.BlockState('minecraft:comparator', {'facing': 'west', 'mode': 'subtract'}),
         'Rre': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '1', 'locked': 'false'}),
         'Rrs': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '2', 'locked': 'false'}),
         'Rrn': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '2', 'locked': 'false'}),
         'Rt ': world.BlockState('minecraft:redstone_torch'),
         'Rte': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'east'}),
         'Rtw': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'west'}),
         'Rtn': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'north'}),
         'Rts': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'south'}),
         'Rl ': world.BlockState('minecraft:lever', {'face': 'wall', 'facing': 'north', 'powered': 'false'}),
         ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}), })


def clockSegment(height=5):
    res = schema.Schema(
        [
            [
                ['   ', '   ', '   '],
                ['   ', '   ', ' T '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', '   ', 'Rt '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', 'Rtn', ' B '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', ' B ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', 'Rt ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', ' B ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', 'Rt ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', ' B ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', 'Rt ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', ' B ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', 'Rt ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', ' B ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', 'Rt ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', ' B ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', ' - ', '   '],
            ],
        ],
        {' O ': 'minecraft:air',
         ' B ': 'minecraft:light_blue_concrete',
         ' G ': 'minecraft:glass',
         ' T ': 'minecraft:target',
         ' L ': 'minecraft:redstone_lamp',
         'Bb ': world.BlockState('minecraft:barrel', {'facing': 'west'}),
         'H1 ': world.BlockState('minecraft:hopper', {'facing': 'east'}),
         'H2 ': world.BlockState('minecraft:hopper', {'facing': 'west'}),
         'Rd1': world.BlockState('minecraft:dropper', {'facing': 'south'}),
         'Rd2': world.BlockState('minecraft:dropper', {'facing': 'north'}),
         'Ro ': world.BlockState('minecraft:observer', {'facing': 'south'}),
         'Rcn': world.BlockState('minecraft:comparator', {'facing': 'north', 'mode': 'subtract'}),
         'Rce': world.BlockState('minecraft:comparator', {'facing': 'east', 'mode': 'subtract'}),
         'Rcs': world.BlockState('minecraft:comparator', {'facing': 'south', 'mode': 'subtract'}),
         'Rcw': world.BlockState('minecraft:comparator', {'facing': 'west', 'mode': 'subtract'}),
         'Rre': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '1', 'locked': 'false'}),
         'Rrs': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '3', 'locked': 'false'}),
         'Rt ': world.BlockState('minecraft:redstone_torch'),
         'Rte': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'east'}),
         'Rtw': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'west'}),
         'Rtn': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'north'}),
         'Rts': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'south'}),
         'Rl ': world.BlockState('minecraft:lever', {'face': 'wall', 'facing': 'north', 'powered': 'false'}),
         ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'})
         })
    for i in range(height - 5):
        res = res.join(schema.Schema(
            [
                [
                    ['   ', '   ', '   '],
                    [' G ', '   ', '   '],
                ],
                [
                    ['   ', '   ', '   '],
                    [' - ', ' G ', '   '],
                ],
                [
                    ['   ', '   ', '   '],
                    ['   ', ' - ', '   '],
                ],
            ],
            {' G ': 'minecraft:glass',
             ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'})
             }), (0, res.size[1] - 1, 0))
    return res


def neuron(weights, bias, height=5):
    print("Generating neuron...")

    inputSize = len(weights)
    res = schema.Schema([[[]]], {})
    for w in weights:
        res = res.join(adder.adder(w, height), (-7, 0, 0))
    res = res.join(adder.adder(bias, height), (-7, 0, 0))
    res = res.join(
        schema.Schema(
            [[[world.BlockState('minecraft:redstone_block')]]]),
        (0, res.size[1] - 3, res.size[2] - 4))
    res = res.join(
        activationSegment(round(math.log2(inputSize))),
        (res.size[0] - 3, res.size[1] - 7, -2))
    res = res.join(clockSegment(height), (res.size[0] - 4, 1, res.size[2] - 5))
    return res
