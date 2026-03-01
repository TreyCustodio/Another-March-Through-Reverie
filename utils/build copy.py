from . import *

"""
This file loads rooms by calling each room's builder function
contained in functions.py

The level editor will add functions to room_data.
"""

# Load a room from the dictionary of functions
def load_room(room):
    return room_data[room.name](room)

# Dictionary of rooms mapped to their builder functions
## Entries to this dictionary will be appended after saving a room's data in the level editor
room_data = {
    'mid_1' : mid_1,
}