from pyanvil import world
from pyanvil import editor
import math

adderSegment = editor.Schema(
    [[['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', 'Rt ', ' B ', ' B ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' G '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' G ', '   ', '   ', '   ', '   '],],
     [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' B ', '   ', '   ', '   '],
      ['   ', '   ', ' B ', ' B ', ' B ', '   ', '   ', ' G ', ' B ', '   ', '   ', ' B ', ' B ', '   ', '   ', '   '],
      ['   ', '   ', ' B ', ' B ', '   ', ' B ', '   ', ' B ', ' G ', '   ', '   ', ' B ', ' B ', '   ', '   ', '   '],
      ['   ', ' B ', ' B ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', ' B ', ' B ', ' B ', '   ', '   ', '   '],
      [' B ', '   ', ' B ', ' B ', '   ', ' - ', ' - ', 'Rr ', ' B ', '   ', '   ', ' B ', ' B ', ' B ', ' G ', ' - '],
      [' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      [' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' G ', ' - ', ' G ', '   ', '   ', '   '],],
     [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'Rr|', '   ', '   ', '   '],
      ['   ', '   ', ' - ', ' - ', 'Rr ', ' T ', ' G ', ' - ', 'Rr ', 'Rt ', ' T ', ' - ', ' - ', '   ', '   ', '   '],
      ['   ', ' B ', 'Rc ', ' - ', '   ', ' - ', ' B ', 'Rc ', ' - ', ' G ', ' B ', 'Rc ', ' - ', '   ', '   ', '   '],
      [' B ', ' - ', 'Rc ', ' - ', '   ', '   ', '   ', '   ', 'Rt ', ' B ', ' - ', 'Rc ', ' - ', '   ', '   ', '   '],
      ['Rr|', '   ', ' - ', ' - ', 'Rt ', ' B ', '   ', '   ', ' - ', '   ', '   ', ' - ', ' - ', 'Rr ', ' - ', '   '],
      [' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' L ', '   ', '   '],
      [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', '   ', ' - ', ' T ', '   ', '   '],],
     [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
      ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],],],
    {' B ': 'minecraft:magenta_concrete',
     ' G ': 'minecraft:glass',
     ' T ': 'minecraft:target',
     ' L ': 'minecraft:redstone_lamp',
     'Rc ': world.BlockState('minecraft:comparator', {'facing': 'south', 'mode': 'subtract'}),
     'Rr ': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '1', 'locked': 'false'}),
     'Rr|': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '1', 'locked': 'false'}),
     'Rt ': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'north'}),
     ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}), })


def weightSegment(weight):
    return editor.Schema(
        [[
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', ' B ', ' B ', '   ', '   ', ' B ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', ' B ', ' B ', ' B ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', 'B3 ', 'B3 ', 'B3 ', 'B3 ', 'B3 ', '   ', '   '],
            ['   ', 'Rr1', '   ', 'Rr2', '   ', 'Rr3', '   ', 'Rr4', '   ', 'B3 ', '   ', '   ', '   ', 'B3 ', '   ', '   '],
            ['   ', ' - ', 'Bb1', ' - ', '   ', ' - ', 'Bb4', ' - ', '   ', '   ', '   ', ' B ', '   ', 'B3 ', '   ', '   '],
            ['   ', ' - ', 'Rce', ' B ', ' B ', ' - ', 'Rce', ' B ', ' B ', '   ', '   ', ' B ', '   ', 'B3 ', '   ', '   '],
            ['   ', '   ', ' - ', '   ', ' - ', '   ', ' - ', '   ', ' - ', '   ', ' B ', ' B ', '   ', 'B3 ', '   ', '   '],
            ['   ', 'Bb+', 'Rcn', ' B ', 'Rcn', ' B ', 'Rcn', ' B ', 'Rcn', ' - ', 'Rcw', '   ', '   ', 'B3 ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'Bb?', '   ', '   ', 'B3 ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B3 ', '   ', '   '],
        ],
            [
            ['   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', 'B3 ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', ' - ', '   ', ' - ', '   ', ' - ', '   ', ' - ', '   ', ' - ', 'Ro ', 'Rrs', 'Rrs', ' - ', '   ', '   '],
            ['   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', ' B ', '   ', 'Rr2', '   ', '   ', ' B ', ' - ', '   ', '   '],
            ['   ', ' B ', '   ', ' G ', 'Bb2', ' B ', '   ', ' G ', 'Bb8', 'B3 ', 'Rts', ' - ', '   ', 'Rr3', '   ', '   '],
            ['   ', ' B ', '   ', ' - ', 'Rce', '   ', '   ', ' - ', 'Rce', 'B3 ', '   ', 'Rr2', '   ', ' - ', '   ', '   '],
            ['   ', '   ', '   ', '   ', ' B ', '   ', '   ', '   ', ' B ', 'B3 ', ' - ', 'Rrn', ' B ', 'Rr4', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   ', '   '],
        ],
            [
            ['B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'Rtw', '   ', '   ', '   '],
            ['   ', ' - ', '   ', ' - ', '   ', ' - ', '   ', ' - ', '   ', '   ', '   ', '   ', ' - ', ' B ', '   ', '   '],
            ['   ', 'Rcw', '   ', 'Rcw', '   ', 'Rcw', '   ', 'Rcw', '   ', ' - ', '   ', '   ', ' B ', ' B ', '   ', '   '],
            ['   ', ' H ', '   ', ' H ', '   ', ' H ', '   ', ' H ', '   ', ' - ', '   ', '   ', ' B ', ' B ', ' B ', '   '],
            ['   ', 'Rd ', '   ', 'Rd ', '   ', 'Rd ', '   ', 'Rd ', ' B ', ' - ', ' B ', '   ', ' - ', ' B ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', 'Rrn3', 'Rrn4', ' - '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', 'Rcn', ' T ', '   '],
            ['   ', 'Rte', '   ', 'Rte', ' O ', 'Rte', ' O ', 'Rte', '   ', '   ', '   ', '   ', ' - ', 'Rcn', ' - ', ' O '],
            ['   ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' - ', '   ', '   ', '   ', '   ', ' - ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', '   ', '   ', ' O ', ' O ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', ' O ', '   ', 'Rt ', '   '],
            ['   ', '   ', '   ', ' G ', '   ', ' O ', ' O ', ' O ', '   ', '   ', '   ', ' O ', ' O ', ' O ', ' O ', ' O '],
            ['   ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', ' O ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', ' O ', '   ', ' B ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', ' O ', ' O ', ' O '],
            ['   ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', '   ', '   ', '   ', '   ', '   ', ' O ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'Rt ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' B ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', ' O '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' - ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' T ', ' O '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'Rt ', ' O '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
            [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' B ', ' O '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ],
        ],
        {' O ': 'minecraft:air', ' B ': 'minecraft:lime_concrete', 'B2 ': 'minecraft:orange_concrete', 'B3 ': 'minecraft:light_blue_concrete',
         ' G ': 'minecraft:glass', ' T ': 'minecraft:target', ' L ': 'minecraft:redstone_lamp', ' R ': 'minecraft:redstone_block',
         'Bb1': world.BlockState('minecraft:barrel', {'facing': 'west'}, [('minecraft:wooden_shovel', 1) for _ in range(1)]),
         'Bb2': world.BlockState('minecraft:barrel', {'facing': 'west'}, [('minecraft:wooden_shovel', 1) for _ in range(3)]),
         'Bb4': world.BlockState('minecraft:barrel', {'facing': 'west'}, [('minecraft:wooden_shovel', 1) for _ in range(7)]),
         'Bb8': world.BlockState('minecraft:barrel', {'facing': 'west'}, [('minecraft:wooden_shovel', 1) for _ in range(14)]),
         'Bb+': world.BlockState('minecraft:barrel', {'facing': 'west'}, [('minecraft:wooden_shovel', 1) for _ in range(27)]),
         'Bb?': world.BlockState('minecraft:barrel', {'facing': 'west'}, [('minecraft:wooden_shovel', 1) for _ in range(round(weight * 27))]),
         #  'Bb ': world.BlockState('minecraft:barrel', {'facing': 'west'}),
         ' H ': world.BlockState('minecraft:hopper', {'facing': 'west'}),
         'Rd ': world.BlockState('minecraft:dropper', {'facing': 'east'}, [('minecraft:wooden_shovel', 1), ('minecraft:stick', 1)]),
         'Ro ': world.BlockState('minecraft:observer', {'facing': 'south'}),
         'Rcn': world.BlockState('minecraft:comparator', {'facing': 'north', 'mode': 'subtract'}),
         'Rce': world.BlockState('minecraft:comparator', {'facing': 'east', 'mode': 'subtract'}),
         'Rcs': world.BlockState('minecraft:comparator', {'facing': 'south', 'mode': 'subtract'}),
         'Rcw': world.BlockState('minecraft:comparator', {'facing': 'west', 'mode': 'subtract'}),
         'Rr2': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '2', 'locked': 'false'}),
         'Rrn': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '1', 'locked': 'false'}),
         'Rrs': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '1', 'locked': 'false'}),
         'Rre': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '1', 'locked': 'false'}),
         'Rrw': world.BlockState('minecraft:repeater', {'facing': 'west', 'delay': '1', 'locked': 'false'}),
         'Rr1': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '1', 'locked': 'false'}),
         'Rr2': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '2', 'locked': 'false'}),
         'Rr3': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '3', 'locked': 'false'}),
         'Rr4': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '4', 'locked': 'false'}),
         'Rrn3': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '3', 'locked': 'false'}),
         'Rrn4': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '4', 'locked': 'false'}),
         'Rt ': world.BlockState('minecraft:redstone_torch'),
         'Rtw': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'west'}),
         'Rts': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'south'}),
         'Rte': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'east'}),
         'Rtn': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'north'}),
         'Rl ': world.BlockState('minecraft:lever', {'face': 'wall', 'facing': 'north', 'powered': 'false'}),
         ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}), })


def activationSegment(clamp):
    return editor.Schema(
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
             ['   ', '   ', 'Rre', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', '   ', ' B ', '   ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' B ', ' G ', ' - ', ' G ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [[' - ', ' G ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' T ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['Rte', '   ', ' - ', '   ', 'Rte', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', '   ', '   ', '   ', '   '],
             ['Rtw', '   ', '   ', '   ', 'Rtw', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', ' - ', '   ', ' - ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [['   ', ' - ', ' - ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', ' B ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', 'B2 ', '   ', 'B2 ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ],
            [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
             ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'B2 ', 'Rrs', 'Ro ', ' - ', 'B2 '],
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
    res = editor.Schema(
        [
            [
                ['   ', '   ', '   '],
                [' B ', '   ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                ['Rt ', '   ', '   '],
            ],
            [
                ['   ', '   ', '   '],
                [' T ', 'Rts', '   '],
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
                ['   ', ' - ', ' G '],
            ],
            [
                ['   ', '   ', '   '],
                ['   ', '   ', ' - '],
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
        res = res.join(editor.Schema(
            [
                [
                    ['   ', '   ', '   '],
                    ['   ', '   ', ' G '],
                ],
                [
                    ['   ', '   ', '   '],
                    ['   ', ' G ', ' - '],
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


def adder(weight, height=5):
    res = adderSegment
    for i in range(height - 1):
        res = res.join(adderSegment, (0, -2, 0))
    res = res.join(
        weightSegment(weight), (0, -5, 0),
        force=True)
    res = res.join(
        editor.Schema(
            [[['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', ' O ', ' O ', '   ', ' O ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              [' O ', '   ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              [' O ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              [' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   '],],
             [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   '],
              ['   ', ' O ', ' O ', ' O ', '   ', ' O ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   ', '   '],
              [' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              [' O ', '   ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              [' O ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              [' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', ' O ', '   ', '   ', '   ', '   ', '   '],],
             [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', '   ', '   ', '   ', '   ', ' O ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', ' O ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
              ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],],],
            {' O ': 'minecraft:air'}),
        (0, res.size[1] - 3, 0),
        force=True)
    return res


def neuron(weights, bias, height=5):
    inputSize = len(weights)
    res = editor.Schema([[[]]], {})
    for w in weights:
        res = res.join(adder(w, height), (-7, 0, 0))
    res = res.join(adder(bias, height), (-7, 0, 0))
    res = res.join(
        editor.Schema(
            [[[world.BlockState('minecraft:redstone_block')]]]),
        (0, res.size[1] - 2, res.size[2] - 4),
        force=True)
    res = res.join(
        activationSegment(round(math.log2(inputSize))),
        (res.size[0] - 3, res.size[1] - 6, -2),
        force=True)
    res = res.join(clockSegment(height), (0, 1, res.size[2] - 3), force=True)
    return res


def outLineSegment(active=False):
    return editor.Schema(
        [
            [['   '], [' B '], [' B '], ['   '], ['   '], [' B '], [' B ']],
            [[' B '], ['Rr4'], ['Rr3'], [' B '], [' B '], [' - '], [' - ']],
            [['Rt ' if active else '   '], ['   '], ['   '], [' - '], [' - '], ['   '], ['   ']]],
        {' B ': 'minecraft:yellow_concrete',
         ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
         'Rr3': world.BlockState('minecraft:repeater', {'facing': 'west', 'delay': '3'}),
         'Rr4': world.BlockState('minecraft:repeater', {'facing': 'west', 'delay': '4'}),
         'Rt ': world.BlockState('minecraft:redstone_torch')})


def inLineSegment(flipDir=False):
    return editor.Schema(
        [[[' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ']],
         [[' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', 'Rrs4' if flipDir else 'Rrn4', 'Rrs3'
           if flipDir else 'Rrn3', ' - ']]],
        {' B ': 'minecraft:orange_concrete', ' - ': world.BlockState(
            'minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
         'Rrn3': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '3'}),
         'Rrn4': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '4'}),
         'Rrs3': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '3'}),
         'Rrs4': world.BlockState('minecraft:repeater', {'facing': 'south', 'delay': '4'}), })


def clockLineSegment():
    return editor.Schema([
        [
            [' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B ', ' B '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']
        ],
        [
            [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', 'Rr4', ' B ', 'Rr3', ' - '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'Rtw', '   ', '   ']
        ]
    ],
        {
        ' B ': 'minecraft:light_blue_concrete',
        ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
        'Rr3': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '3'}),
        'Rtw': world.BlockState('minecraft:redstone_wall_torch', {'facing': 'west'}),
        'Rr4': world.BlockState('minecraft:repeater', {'facing': 'north', 'delay': '4'}),
    })


def multiplexer(inputSize, outputSize):
    print("Generating multiplexer...")

    res = editor.Schema(
        [[['   '] * adderSegment.size[2] *
          outputSize] * adderSegment.size[0] *
         inputSize] * 4, {})
    for i in range(inputSize):
        print(f"Generating input line ({i + 1}/{inputSize})")
        for j in range(
                max(inputSize, outputSize)):
            if j < inputSize:
                res = res.join(
                    outLineSegment(i == j),
                    (i * adderSegment.size[0],
                     0, j * adderSegment.size
                     [2]),
                    force=True)
            res = res.join(
                inLineSegment(i > j),
                (i * adderSegment.size[0],
                 3, j * adderSegment.size[2]),
                force=True)

    print("Done generating multiplexer")
    return res


def layer(inputSize, outputSize, layerData):
    print("Generating layer...")
    res = editor.Schema([[[]]], {})
    for i in range(outputSize):
        print("Generating neuron...")
        res = res.join(
            neuron(layerData[i][1:], layerData[i][0], max(5, round(2 + math.log2(inputSize + 1)))), (0, 0, -adderSegment.size[2]))
    return res


def network(sizes, networkData):
    res = layer(sizes[0], sizes[1], networkData[0])
    clockWire = editor.Schema([[[]]], {})
    for i in range(sizes[1]):
        clockWire = clockWire.join(clockLineSegment(), (0, 0, -adderSegment.size[2]))

    clockWire = clockWire.join(editor.Schema([
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
        l = layer(
            sizes[i + 1],
            sizes[i + 2], networkData[i + 1])
        res = res.join(
            l, (res.size[0] - l.size[0], res.size[1] - 4, 0), force=True)
        m = multiplexer(
            sizes[i + 1],
            sizes[i + 2])
        res = res.join(
            m,
            (res.size[0] - m.size[0] - 5, res.size
             [1] - l.size[1] + 1, 2), force=True)

    res = res.join(clockWire, (0, 1, -3), force=True)

    # Top layer clock for activation
    topClockWireSegment = editor.Schema([
        [[' B '], [' B '], [' B '], [' B '], [' B '], [' B '], [' B '], [' B ']],
        [[' - '], [' - '], ['Rr3'], ['Rr4'], [' - '], [' - '], [' - '], [' - ']]
    ], {
        ' B ': 'minecraft:light_blue_concrete',
        ' - ': world.BlockState('minecraft:redstone_wire', {'north': 'side', 'south': 'side', 'east': 'side', 'west': 'side'}),
        'Rr3': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '3'}),
        'Rr4': world.BlockState('minecraft:repeater', {'facing': 'east', 'delay': '4'}),
    })
    topClockWire = editor.Schema([[[]]], {})
    for i in range(sizes[-2] + 1):
        topClockWire = topClockWire.join(topClockWireSegment, (-adderSegment.size[0], 0, 0))
    topClockWire = topClockWire.join(editor.Schema([[[' B ']], [['Rt ']], [[' B ']]], {
        ' B ': 'minecraft:light_blue_concrete',
        'Rt ': world.BlockState('minecraft:redstone_torch'),
    }), (0, -1, 0), force=True)
    for nz in range(sizes[-1]):
        res = res.join(topClockWire, (1, res.size[1] - 3, (adderSegment.size[2] * nz) + adderSegment.size[2] + 2), force=True)

    return res
