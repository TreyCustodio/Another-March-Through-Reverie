from . import *

"""
This file contains all the functions necessary
for constructing each room in the game.

The Level Editor will write functions to this file.
"""


""" def mid_1(obj):
    obj.background = [
        Drawable(vec(0,0), os.path.join("middleground.png"))
    ]
    obj.tileset = "mid.png"
    obj.tiles = []
        
    for x in range(0, int(obj.size[0]), 16):
        for y in range(int(obj.floor) + 16, int(obj.size[1]), 16):
            obj.tiles += [
                Tile(vec(x, y), obj.tileset, (0,0))
            ]

        obj.tiles += [
            Tile(vec(x, obj.floor-16), obj.tileset, (2,0)),
            Tile(vec(x, obj.floor), obj.tileset, (2,1))
            ] """

def mid_1(obj):
    obj.background = [
        Drawable(vec(0,0), os.path.join("middleground.png"))
    ]
    obj.tileset = "mid.png"
    obj.tiles = []
        
    # for x in range(0, int(obj.size[0]), 16):
    #     for y in range(int(obj.floor) + 16, int(obj.size[1]), 16):
    #         obj.tiles += [
    #             Tile(vec(x, y), obj.tileset, (0,0))
    #         ]

    #     obj.tiles += [
    #         Tile(vec(x, obj.floor-16), obj.tileset, (2,0)),
    #         Tile(vec(x, obj.floor), obj.tileset, (2,1))
    #         ]