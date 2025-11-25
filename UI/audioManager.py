"""
A Singleton Sound Manager class
Author: Liz Matthews, 2/17/2024
Modified by Trey Custodio, 10/28/2025

Provides on-demand loading of sounds and music for a pygame program.

"""

import pygame
import os

class Track(object):
        """Represents an ost track"""
        def __init__(self, intro, main, drums, intro_drums):
            self.intro = intro
            self.main = main
            self.drums = drums
            self.intro_drums = intro_drums

        def get_intro(self):
            return self.intro
        
        def get_main(self):
            return self.main
        
        def get_drums(self):
            return self.drums
        
        def get_intro_drums(self):
            return self.intro_drums
        
class AudioManager(object):
    """A singleton factory class to create and store sounds and music on demand."""
    
    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._AM()
        
        return cls._INSTANCE
    
    



    class _AM(object):
        """An internal AudioManager class to contain the actual code."""
        
        #   Paths to relevant directories   #
        _SFX_FOLDER = "sfx"
        _OST_FOLDER = "ost"
        _BGM_FOLDER = "bgm"
        _VOICE_FOLDER = "voices"
        
        def __init__(self):
            self.ost = {} # "track number": [intro, loop, drums]
            self.BGMs = {}
            self.dict = {}

            #   Initialize pygame's mixer
            pygame.mixer.init()

            #   Reserve Channel 4 for menu sfx    #
            pygame.mixer.set_reserved(4)
            self.menu_channel = pygame.mixer.Channel(4)

            #   Reserve Channel 5 for bgm melody    #
            pygame.mixer.set_reserved(5)
            self.bgm_channel = pygame.mixer.Channel(5)

            #   Reserve Channel 6 for bgm drums    #
            pygame.mixer.set_reserved(6)
            self.drum_channel = pygame.mixer.Channel(6)

            #   Booleans    #
            self.currently_playing = False # True if currently playing a track
            self.playing_intro = False # True if an intro to a track is playing
            self.playing_drums = False

        def is_busy(self):
            return pygame.mixer.get_busy()
        
        def get_current_track(self) -> Track:
            return self.ost[self.currently_playing]
        
        def play_ost(self, name, play_intro = False, play_outro = False, play_drums = True, volume = 1.0, fade_in = 0):
            """Play a track from the original soundtrack"""
            if name not in self.ost:
                self._load_ost(name, play_intro, play_outro, play_drums)

            if play_intro:
                self.playing_intro = True
                self.currently_playing = name
                track = self.ost[name]
                if play_drums:
                    self.playing_drums = True
                    self.drum_channel.play(track.get_intro_drums(), 0, fade_ms=fade_in)
                else:
                    self.playing_drums = False
                self.bgm_channel.play(track.get_intro(), 0, fade_ms=fade_in)
            
            else:
                self.currently_playing = name
                track = self.ost[name]
                if play_drums:
                    self.playing_drums = True
                    self.drum_channel.play(track.get_drums(), -1, fade_ms=fade_in)
                else:
                    self.playing_drums = False
                self.bgm_channel.play(track.get_main(), -1, fade_ms=fade_in)

            #   Set the volume  #
            self.bgm_channel.set_volume(volume)
            self.drum_channel.set_volume(volume)





        def playBGM(self, name):
            if self.currently_playing:
                pygame.mixer.music.stop()
                
            self.currently_playing = name
            pygame.mixer.music.load(os.path.join(AudioManager._AM._MUSIC_FOLDER,
                                                 name))        
            pygame.mixer.music.play(-1)


        def fadeout_bgm(self, fadeoutAmount=1000):
            self.bgm_channel.fadeout(fadeoutAmount)
            self.drum_channel.fadeout(fadeoutAmount)

            self.currently_playing = None
            self.playing_intro = False
        
    
        def playSFX(self, name, loops=0):
            if name not in self.dict:
                self._loadSFX(name)
            return self.dict[name].play(loops)
        
        def playText(self, name, loops=0):
            if name not in self.dict:
                self._loadSFX(name)
            return self.menu_channel.play(self.dict[name], loops)
        
        def play_menu_sfx(self, name, loops=0):
            if name not in self.dict:
                self._loadSFX(name)

            return self.menu_channel.play(self.dict[name], loops)
        
        def play_voice(self, name, loops=0):
            """
            Play and load a voice file from the voice directory
            """
            if name not in self.dict:
                self._loadVoice(name)
            return self.dict[name].play(loops)
        
        def playLowSFX(self, name, volume = 0.5, loops=0):
            if name not in self.dict:
                fullname = os.path.join(AudioManager._AM._SFX_FOLDER, name)
                sound = pygame.mixer.Sound(fullname)
                #print(sound.get_volume())
                sound.set_volume(volume)
                self.dict[name] = sound
            return self.dict[name].play(loops)
        
        def _loadSFX(self, name):
            """Loads a sound from a file."""
            fullname = os.path.join(AudioManager._AM._SFX_FOLDER, name)
            sound = pygame.mixer.Sound(fullname)
                
            self.dict[name] = sound
        
        
        def _load_ost(self, name, play_intro = False, play_outro = False, play_drums = False):
            """Load up a track from the ost"""
            track_number = name
            fullname = os.path.join(AudioManager._AM._OST_FOLDER, name)

            if play_intro:
                name = fullname + "_intro.wav"
                intro = pygame.mixer.Sound(name)
            else:
                intro = None

            if play_outro:
                name = fullname + "_outro.wav"
                outro = pygame.mixer.Sound(name)
            else:
                outro = None

            #   Add drums
            if play_drums:
                name = fullname + "_drums.wav"
                drums = pygame.mixer.Sound(name)

                name = fullname + "_drums_intro.wav"
                drums_intro = pygame.mixer.Sound(name)

            else:
                drums = None
                drums_intro = None

            #   Add main
            name = fullname + "_main.wav"
            main = pygame.mixer.Sound(name)

            self.ost[track_number] = Track(intro, main, drums, drums_intro)

        def _loadVoice(self, name):
            """
            Load a voice file from the voice directory
            """
            fullname = os.path.join(AudioManager._AM._VOICE_FOLDER, name)
            sound = pygame.mixer.Sound(fullname)
            self.dict[name] = sound

        def stopSFX(self, name):
            if name in self.dict:
                self.dict[name].stop()

        def playOnce(self, name):
            if name in self.dict:
                return
            else:
                self.playSFX(name)

        def stopAllSFX(self):
            for song, player in self.dict.items():
                if song.endswith(".wav"):
                    player.stop()

        def fadeAllSFX(self, fade_dur = 1000):
            for song, player in self.dict.items():
                if song.endswith(".wav"):
                    player.fadeout(fade_dur)

        def update(self, seconds):
            # print(self.bgm_channel.get_volume())
            if self.playing_intro:
                #   Transition to the track's loop after the intro finishes #
                if not self.bgm_channel.get_busy():
                    self.playing_intro = False
                    self.bgm_channel.play(self.get_current_track().get_main(), -1)
                    if self.playing_drums:
                        self.drum_channel.play(self.get_current_track().get_drums(), -1)
