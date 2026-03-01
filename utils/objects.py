from pygame import Rect, Surface, image, transform, font

from os import path

from globals import SCREEN_SIZE, vec


"""
    ------- Abstract Drawable Object Class -------
"""
class Drawable(object):
    """A class that represents a Drawable Object"""
    
    def __init__(self, position, image: Surface):
        self.pos = position
        self.image = image

    def draw(self, surf: Surface):
        surf.blit(self.image, self.pos)
    
    def set_pos(self, pos):
        self.pos = pos

    def check_hovering(self, pos):
        return

    def get_hovered(self):
        return False
    
    def get_held(self):
        return False
    
    def get_size(self):
        return self.image.get_size()
    
class Cross(object):
    def __init__(self):
        self.position = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
    
    
"""
    ------- Low-level Drawable Object Classes -------
"""
class Collidable(Drawable):
    """A Drawable oject that can keep track of collisions with other objects"""
    def __init__(self, position, image: Surface):
        self.collision_rect = Rect(self.position, self.image.get_size())
        
        super().__init__(position, image)


class Animated(Drawable):
    def __init__(self, position, frames: list, starting_frame : int = 0):
        self.frames = frames
        self.current_frame = starting_frame
        self.fps = 4
        self.frame_timer = 0.0
        super().__init__(position, self.frames[starting_frame])

    def update(self, seconds):
        self.frame_timer += seconds
        if self.frame_timer >= 1.0 / self.fps:
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            self.image = self.frames[self.current_frame]
            self.frame_timer = 0.0

"""
    ------- Objects with Special Features -------
"""
class Pressable(Drawable):
    def __init__(self, position, frames: list, name: str, starting_frame : int = 0):
        self.frames = frames
        self.name = name
        
        #   States:
        ##  hovered, held, pressed
        self.states = {
            "hovered": False,
            "held": False,
        }

        
        super().__init__(position, self.frames[starting_frame])

    
    def get_hovered(self):
        return self.states["hovered"]
    
    def get_held(self):
        return self.states["held"]

    def check_hovering(self, mouse_pos):
        size = self.image.get_size()

        if mouse_pos[0] >= self.pos[0] and mouse_pos[0] <= self.pos[0] + size[0]:
            if mouse_pos[1] >= self.pos[1] and mouse_pos[1] <= self.pos[1] + size[1]:
                if not self.get_hovered():
                    self.set_hovered()
                return
        
        self.states["hovered"] = False
        self.states["held"] = False
        self.image = self.frames[0]
    
    def hold(self):
        """Set the button to the held state"""
        if not self.get_held():
            self.states["held"] = True
            self.image = self.frames[2]
    
    def release(self):
        """Set the button to the released state"""
        if self.get_held():
            self.states["held"] = False
            self.states["hovered"] = False
            if self.get_hovered():
                self.image = self.frames[1]
            else:
                self.image = self.frames[0]

    def set_hovered(self):
        self.states["hovered"] = True
        self.image = self.frames[1]

    def unset_hovered(self):
        self.states["hovered"] = False
        self.image = self.frames[0]

    def set_held(self):
        self.states["held"] = True
        self.image = self.frames[2]
    
    def unset_held(self):
        self.states["held"] = False
        if self.get_hovered():
            self.image = self.frames[1]
        else:
            self.image = self.frames[0]

    

class Bar(Pressable):
    """"""
    def __init__(self, position, bar_num = 1, instrument = None, bpm=80, notes=None, full = False):

        #   The Bar's States    #
        self.states = {
            "hovered": False,
            "held": False,
            "full" : full
        }

        #   Data about Note to be Created on Click    #
        self.instrument = instrument # Instrument() object
        self.pitch = None # Float frequency value of the note to be created
        self.duration = get_quarter(bpm) # The duration of the note that will be created
        
        #   Bar Data    #
        self.bpm = bpm
        self.bar_length = len(sine_wave(0, get_measure(bpm)))
        self.total_length = 0.0 # Sum of the duration of all the notes in the bar

        #   Load necessary images   #
        scale = 8
        self.scale = scale

        img1 = image.load(path.join("UI", "images", "composer", "bar_1.png"))
        img = image.load(path.join("UI", "images", "composer", "bar_2.png"))
        size = img.get_size()
        self.img1 = transform.scale(img1, (size[0] * scale, size[1] * scale))
        self.image = transform.scale(img, (size[0] * scale, size[1] * scale))
        self.frames = [self.image, transform.scale(image.load(path.join("UI", "images", "composer", "bar_3.png")), (1 * scale, 42 * scale)), self.image]

        #   Image Data  #
        self.pos = position
        self.width = WIDTH // 2 - 16
        self.bar_num = bar_num

        #   Note Buttons   #
        frames = load_row(image.load(path.join("UI", "images", "composer", "notes.png")), (16,16), 4, 5, 2)
        self.note = frames[3]
        self.note.set_alpha(200)
        self.note_pos = vec(self.pos[0] + 16, self.pos[1] + 16)

        if notes:
            self.notes = notes
            self.note_buttons = []
            self.note_lengths = []

            for n in notes:
                frames = load_row(image.load(path.join("UI", "images", "composer", "notes.png")), (16,16), 4, 5, 2)
                #   How do we determine Y pos ??    #
                pitch = n.pitch

                if pitch == C2:
                    y = 16
                
                elif pitch == B2:
                    y = 40
                
                elif pitch == A2:
                    y = 56

                elif pitch == G2:
                    y = 80
                
                elif pitch == F2:
                    y = 96

                elif pitch == E2:
                    y = 120
                
                elif pitch == D2:
                    y = 136
                
                elif pitch == C2:
                    y = 160
                
                elif pitch == B1:
                    y = 176
                
                elif pitch == A1:
                    y = 200
                
                elif pitch == G1:
                    y = 216
                
                elif pitch == F1:
                    y = 240
                
                elif pitch == E1:
                    y = 256
                
                elif pitch == D1:
                    y = 280

                elif pitch == C1:
                    y = 296

                else:
                    y = self.note_pos[1]

                
                img = Pressable(vec(self.note_pos[0], y), frames)
                self.note_buttons.append(img)
                
                self.note_lengths.append(len(n))

                self.note_pos[0] += 64
        else:
            self.notes = [] # The waveforms that represent the notes
            self.note_buttons = [] # The buttons of each note on the bar
            self.note_lengths = [] # The lengths of each note


    def get_notes(self):
        return self.notes
    
    def draw(self, surf):
        #   Display the Bar Background  #
        surf.blit(self.img1, self.pos)
        for i in range(1, self.width+1):
            surf.blit(self.image, (self.pos[0] + i, self.pos[1]))

        #   Display the Bar Number  #
        name = font.SysFont(None, 36).render("Bar " + str(self.bar_num), True, (0,0,0))
        surf.blit(name, (self.pos[0] + 16, self.pos[1]))

        #   Display transparent notes   #
        if self.get_hovered() and not self.states["full"]:
            surf.blit(self.note, self.note_pos)

        #   Display notes   #
        for n in self.note_buttons:
            n.draw(surf)


        #   Print for test  #
        # print("Quarter note length:", len(sine_wave(C1, get_quarter(self.bpm))))
        # for i in range(len(self.notes)):
        #     print("Note", i, "\nLength:", len(self.notes[i]),"\n")


    def check_hovering(self, mouse_pos):    
        pos = mouse_pos

        #   Update the state of hovered and the note_pos    #
        if pos[0] >= self.pos[0] and pos[0] <= self.pos[0] + (self.image.get_size()[0] + self.width):
            if pos[1] >= self.pos[1] and pos[1] <= self.pos[1] + self.image.get_size()[1]:
                ##   The Mouse is inside the Bar #

                ##  Set hovered to True #
                if not self.get_hovered():
                    self.states["hovered"] = True
                    self.image = self.frames[1]  # Change to hovered frame

                ##  Check if any notes are hovered  #
                if self.notes:
                    for n in self.note_buttons:
                        n.check_hovering(pos)


                ##  Update note_pos #
                if pos[1] < 145:
                    #pos[1] >= 105 and 
                    ### G
                    self.note_pos[1] = 80
                    self.pitch = G2
                    
                
                elif pos[1] >= 145 and pos[1] < 165:
                    ### F
                    self.note_pos[1] = 96
                    self.pitch = F2

                    # prev + 16
                
                elif pos[1] >= 165 and pos[1] < 185:
                    ### E
                    self.note_pos[1] = 120
                    self.pitch = E2
                    
                    # prev + 24

                elif pos[1] >= 185 and pos[1] < 205:
                    ### D
                    self.note_pos[1] = 136
                    self.pitch = D2
                    # prev + 16

                elif pos[1] >= 205 and pos[1] < 225:
                    ### C
                    self.note_pos[1] = 160
                    self.pitch = C2
                    # prev + 24

                elif pos[1] >= 225 and pos[1] < 245:
                    ### B
                    self.note_pos[1] = 176
                    self.pitch = B1
                    # + 16

                elif pos[1] >= 245 and pos[1] < 265:
                    ### A
                    self.note_pos[1] = 200
                    self.pitch = A1
                    # + 24

                elif pos[1] >= 265 and pos[1] < 285:
                    ### G
                    self.note_pos[1] = 216
                    self.pitch = G1
                    # + 16

                elif pos[1] >= 285 and pos[1] < 305:
                    ### F
                    self.note_pos[1] = 240
                    self.pitch = F1
                    # + 24

                elif pos[1] >= 305 and pos[1] < 325:
                    ### E
                    self.note_pos[1] = 256
                    self.pitch = E1
                    # + 16

                elif pos[1] >= 325 and pos[1] > 345:
                    #and pos[1] < 345:

                    ### D
                    self.note_pos[1] = 280
                    self.pitch = D1
                    # + 24

                elif pos[1] >= 345:
                    ### C
                    self.note_pos[1] = 296
                    self.pitch = C1
                    # + 16

                else:
                    ### Default Pos
                    self.note_pos = vec(self.note_pos[0], 80)
                
                return
        
        self.states["hovered"] = False
        self.states["held"] = False
        self.image = self.frames[0]
        self.note.set_alpha(200)

    def hold(self):
        if not self.get_held() and not self.states["full"]:
            self.states["held"] = True
            self.note.set_alpha(255)

    def release(self):
        if self.get_held():
            #   Adjust the state    #
            self.states["held"] = False

            #   Add the note to the list of notes   #
            note = self.instrument.note(self.pitch, self.duration)
            self.notes.append(note)
            
            #   Track the length    #
            self.total_length += self.duration
            self.note_lengths.append(len(note))

            #   Add the note's button to the list of notes  #
            frames = load_row(image.load(path.join("UI", "images", "composer", "notes.png")), (16,16), 4, 5, 2)
            img = Pressable(vec(self.note_pos[0], self.note_pos[1]), frames)
            self.note_buttons.append(img)

            #   Check if the measure is full    #
            if self.total_length >= self.bar_length:
                if self.total_length > self.bar_length:
                    pass
                    #print("BAR LENGTH WARNING: The current bar exceeds the maximum bar length")
                    
                self.states["full"] = True
                return
            
            self.note_pos[0] += 64
            self.note.set_alpha(200)


    def right_down(self, event):
        if self.notes:
            pos = event.__dict__['pos']
            for n in self.note_buttons:
                if pos[0] >= n.pos[0] and pos[0] <= n.pos[0] + n.get_size()[0]:
                    if pos[1] >= n.pos[1] and pos[1] <= n.pos[1] + n.get_size()[1]:
                        n.hold()

    def right_up(self, event):
        if self.notes:
            index = 0
            for n in self.note_buttons:
                if n.get_held():
                    #   Adjust successive note positions   #
                    notes = self.note_buttons[index:]
                    for n in notes:
                        n.pos[0] -= 64

                    #   Pop the note from the lists  #
                    self.notes.pop(index)
                    self.note_buttons.pop(index)

                    #   Adjust and check the length   #
                    self.total_length -= self.note_lengths[index]
                    if self.states["full"]:
                        self.states["full"] = False
                    else:
                        self.note_pos[0] -= 64

                    #   Reset the indicator's alpha #
                    self.note.set_alpha(200)

                    return

                index += 1