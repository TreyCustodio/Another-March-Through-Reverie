from . import *

"""
This file contains all the functions necessary
for constructing each room in the game.

The Level Editor will write functions to this file.
"""
def mid_1(obj):
    obj.background = [
        Drawable(vec(0,0), os.path.join("middleground.png"))
    ]
    
    obj.tileset = "mid.png"
    obj.tiles = []
    
    for x in range(0, int(obj.size[0]), 16):
        #   Black Tiles (0,0)   #
        for y in range(int(obj.size[1]), int(obj.size[1] - 64), -16):
            obj.tiles += [
                    Tile(vec(x, y), obj.tileset, (0,0))
                ]
        
        #   Red ground (2,1) + (2,0)    #
        obj.tiles += [
            Tile(vec(x, obj.size[1]- 80), obj.tileset, (2,0), property=0),
            Tile(vec(x, obj.size[1] - 64), obj.tileset, (2,1), property=1)
            ]
    
    for y in range(0, int(obj.size[1])):
        obj.tiles += [
            Tile(vec(-16, y), obj.tileset, (0,1), property=1)
        ]