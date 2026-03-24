import os

import pygame
from pygame import event, font
from pygame.locals import *

from . import room_data
from globals import vec, UPSCALED
from objects import room, Player, Room

from . import Pressable, load_room, Tile


"""
The level editor will:
(1) write functions to functions.py
(2) add the function to the map room_data in build.py

-------------------------------------------------------

Some notes on writing/appending to files:
(1) Append writes to the final line of the file;
    does not make a new line
(2) start modifying room_data on lines[16]
"""

# A mapping of input actions to on/off states
ACTIONS = {
    "pressingL": False,
    "pressingR": False,

}

class RoomX(object):
    """The editor's representation of a room"""
    def __init__(self):
        self.name = ""
        self.size = vec(UPSCALED[0] * 20, UPSCALED[1])
        self.floor = UPSCALED[1] - UPSCALED[1] // 4

        # (1) Background: List[Drawable/Animated]
        self.background = []

        # (2) Tileset: "Str"
        self.tileset = ""

        # (3) Tiles: List[Tiles]
        self.tiles = []

        # (4) Npcs: List[Npcs]
        self.npcs = []

        # (5) Enemies: List[Enemies]
        self.enemies = []

        # (6) Player: Player
        self.player = None

        # (7) Foreground: List[Drawable/Animated]
        self.foreground = []

    def set_name(self, name):
        self.name = name

    def draw(self, drawSurf):
        Room.draw(self, drawSurf, draw_player=False, draw_collision = True)
    
class Editor:
    """Container class for the level editor UI"""
    def __init__(self):
        # states:
        ## landing, editing
        self.state = "landing"

        # Objects to display
        self.display_objects = []

        # Current room being edited
        self.current_room = ""

        # Objective representation of the current room
        self.room = RoomX() # only 1 should be instantiated
        
        # Boolean that determines whether to draw the grid or not
        self.grid_on = True

        self.title_offset = (1,1)
        
        # 0 for empty space; 1 for filled space
        self.GRID = [[0 for i in range(0, int(UPSCALED[0] * 20), 16)] for j in range(0, int(UPSCALED[1]), 16)] 

    def load(self):
        """Gather display objects"""
        # position to display each room name
        pos = vec(64, 32)

        for r in room_data:
            fnt = font.Font(os.path.join("UI", "fonts", 'PressStart2P.ttf'), 16)
            img0 = fnt.render(r, False, (255, 255, 255), (0,0,0))
            img1 = fnt.render(r, False, (255, 255, 0), (0,0,0))
            img2 = fnt.render(r, False, (255, 0, 0), (0,0,0))

            button = Pressable(pos.copy(), [img0, img1, img2], r)
            self.display_objects.append(button)

            pos[0] += (img0.get_width() + 16)

    def start(self, o):
        ## this assumes that we are transitioning from Landing -> Editing
        self.current_room = o.name
        self.state = "editing"
        self.display_objects = []

        self.room.set_name(self.current_room)

        load_room(self.room)

        # Add some buttons
        ## Draw grid button
        surf0 = pygame.Surface((16, 16), pygame.SRCALPHA)
        surf0.fill((0,255,0))
        surf1 = pygame.Surface((16, 16), pygame.SRCALPHA)
        surf1.fill((255,255,0))
        surf2 = pygame.Surface((16, 16), pygame.SRCALPHA)
        surf2.fill((255,0,0))

        obj = Pressable((0,0), [surf0, surf1, surf2], "grid")

        self.display_objects.append(obj)
        
    def write_function():
        """Write a function to the functions file"""
        with open("functions.py", 'a') as file:
            return

    def save_function(name):
        """Save a function to the dictionary"""
        # Open the file and read the lines
        with open("build.py", 'r') as file:
            lines = file.readlines()
            file.close()

        # Insert the desired line of code into the dictionary
        lines.insert(17, "und_1 : hey\n")
        
        # Finish writing and close the file
        with open("build.py", "w") as file:
            file.writelines(lines)
            file.close()

        return
    
    def add_tile(self, position):
        # Convert the position to an int
        position = vec(int(position[0]), int(position[1]))

        # Find the corresponding location in the grid
        x = int(position[0] // 16)
        y = int(position[1] // 16)
        print(x)
        print(y)

        # Ensure no tile with the same position is in the list
        if self.GRID[x][y] == 1:
            print("Tile already exists at this location")

        else:
            self.GRID[x][y] = 1
            self.room.tiles += [Tile(vec(x, y), self.room.tileset, self.title_offset)]

        print("Tile added at", position)

        return
    
    def remove_tile(self, position):
        position = vec(int(position[0]), int(position[1]))

        # Need to find this exact tile in memory
        for t in self.room.tiles:
            if t.position[0] == position[0] and t.position[1] == position[1]:
                self.room.tiles.remove(t)
                print("Tile at", position, "removed")
        print("No tile at", position)
    
    def handle_events(self):
        """Handle events in the queue.
        Return False if the UI should die"""
        for ev in event.get():
            if ev.type == QUIT:
                return False
            
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    return False
            
            # Check for pressable buttons
            for o in self.display_objects:
                o.check_hovering(pygame.mouse.get_pos())

                if o.get_hovered() and ev.type == MOUSEBUTTONDOWN:
                    o.hold()
                
                # Release the button and perform its function
                elif o.get_held() and ev.type == MOUSEBUTTONUP:
                    o.release()
                    if self.state == "landing":
                        self.start(o)
                        return True
                    
                    else:
                        if o.name == "grid":
                            self.grid_on = not self.grid_on

                    o.check_hovering(pygame.mouse.get_pos())

            if self.state == "editing":
                # Mouse events
                if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                    ACTIONS["pressingL"] = True

                elif ev.type == MOUSEBUTTONDOWN and ev.button == 3:
                    ACTIONS["pressingR"] = True
                    
                elif ev.type == MOUSEBUTTONUP and ev.button == 1:
                    ACTIONS["pressingL"] = False
                
                elif ev.type == MOUSEBUTTONUP and ev.button == 3:
                    ACTIONS["pressingR"] = False


                if ACTIONS["pressingL"]:
                    self.add_tile(pygame.mouse.get_pos())

                elif ACTIONS["pressingR"]:
                    self.remove_tile(pygame.mouse.get_pos())

        return True

    def draw(self, drawSurf):
        """Draw the editor's display"""
        # Draw white background color
        drawSurf.fill((255,255,255))

        # Draw landing page
        if self.state == "landing":
            for o in self.display_objects:
                o.draw(drawSurf)

        # Draw editing page
        elif self.state == "editing":
            self.room.draw(drawSurf)
            if self.grid_on:
                self.draw_grid(drawSurf, self.room.size)
            
            for o in self.display_objects:
                o.draw(drawSurf)
        return
    
    def draw_grid(self, drawSurf, room_size):
        size = (16,16)
        for x in range(0, int(room_size[0]), size[0]):
            for y in range(0, int(room_size[1]), size[1]):
                pygame.draw.rect(drawSurf, (255,255,255, 70), pygame.Rect((x,y), size), width=1, border_radius = -1)

    def update(self, seconds):
        """Update the editor's state"""
        for o in self.display_objects:
            pass
        return

    def main():
        """Run the GUI"""
        # RUNNING = True
        # while RUNNING:
        #     pass
        # save_function("ice_1")
        return
    
if __name__ == '__main__':
    Editor.main()