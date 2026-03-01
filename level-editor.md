#   First draft of level editor

## Goals
1. Create a simple graphical user interface that allows me to construct levels without having to write any actual code
2. Create a **load** function called whenever a room is loaded
    - defines the background
    - places tiles
    - places collision objects
    - places enemies
    - places the player

## Flow
### Landing
- List of each room
- Click the room you want to edit
- Or create a new room which will be added to the dictionary in `build.py`

### Room editor
1. Implement Scrolling
2. Place a tile with left click
    - map mouse position to the nearest integer value
    - `tiles += [Tile(mouse_position, tileset, offset)]`
3. Remove a tile with right click
4. Save the function
    - the builder function becomes a series of appends to `obj.tiles`