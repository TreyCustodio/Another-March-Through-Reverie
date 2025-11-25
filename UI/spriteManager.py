"""
A Singleton Sprite Manager class
Author: Liz Matthews, 7/21/2023
Modified by Trey Custodio 10/18/2025

Provides on-demand loading of images for a pygame program.
Will load entire sprite sheets if given an offset.

"""

from pygame import image, Surface, Rect, SRCALPHA, transform
from os.path import join
from globals import vec

class SpriteManager(object):
   """A singleton factory class to create and store sprites on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._SM()
      
      return cls._INSTANCE
   
   
      
   # Do not directly instantiate this class!
   class _SM(object):
      """An internal SpriteManager class to contain the actual code. Is a private class."""
      
      # Folder in which images are stored
      _IMAGE_FOLDER = "images"
      

      # Static information about the sprite sizes of particular image sheets.
      _SPRITE_SIZES = {
         #  Text  #
         "textbox.png": (240, 96),

         #  Menu Icons  #
         "pointer.png": (33,16),
         'triangle.png': (32, 16),

         #  Other #
         'celestial.png': (64,64),

         #  Player   #
         'samus.png': (32, 40),

         #  NPCs  #
         'luigi.png': (32, 52),
         
         #  Enemies  #
         'raven_b.png': (22, 18)
      }
      

      # A default sprite size
      _DEFAULT_SPRITE = (16,16)
      

      # A list of images that require to be loaded with transparency
      _TRANSPARENCY = [
                       ]
      

      # A list of images that require to be loaded with a color key
      _COLOR_KEY = []
      

      def __init__(self):
         # Stores the surfaces indexed based on file name
         # The values in _surfaces can be a single Surface
         #  or a two dimentional grid of surfaces if it is an image sheet
         self._surfaces = {}      
      

      def __getitem__(self, key):
         return self._surfaces[key]
   

      def __setitem__(self, key, item):
         self._surfaces[key] = item
      

      def getSize(self, fileName):
         """Return the size of the image"""
         spriteSize = SpriteManager._SM._SPRITE_SIZES.get(fileName,
                                             SpriteManager._SM._DEFAULT_SPRITE)
         return spriteSize
      

      def getSprite(self, fileName, offset=None, enemy = False):
         """Get a sprite from a specified sheet"""
         # If this sprite has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset != None, enemy=enemy)
         
         # If this is an image sheet, return the correctly offset sub surface
         if offset != None:
            return self[fileName][offset[1]][offset[0]]
         
         # Otherwise, return the sheet created
         return self[fileName]

      def _loadImage(self, fileName, sheet=False, enemy = False):
         """Begin loading the image"""
         # Load the full image
         if enemy:
            fullImage = image.load(join(SpriteManager._SM._IMAGE_FOLDER, "enemies", fileName))
         else:
            fullImage = image.load(join(SpriteManager._SM._IMAGE_FOLDER, fileName))

         self._loadRoutine(fullImage, fileName, sheet, enemy=enemy)
         

      def _loadRoutine(self, fullImage, fileName, sheet = False, transparent = True, enemy = False):
         """Get the image from the specified file"""
         # Look up some information about the image to be loaded
         # transparent = fileName in SpriteManager._SM._TRANSPARENCY

         colorKey = fileName in SpriteManager._SM._COLOR_KEY
         
         # Detect if a transparency is needed
         if transparent:
            fullImage = fullImage.convert_alpha()
         else:
            fullImage = fullImage.convert()
         
         # If the image to be loaded is an image sheet, split it up based on the sprite size
         if sheet:
            
            #  Array of sprites
            self[fileName] = []
            
            # Try to get the sprite size, use the default size if it is not stored
            spriteSize = self.getSize(fileName)

            # See how big the sprite sheet is
            sheetDimensions = fullImage.get_size()
            
            # Iterate over the entire sheet, increment by the sprite size
            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               for x in range(0, sheetDimensions[0], spriteSize[0]):
                  
                  # If we need transparency
                  if transparent:
                     sprite = Surface(spriteSize, SRCALPHA, 32)
                  else:
                     sprite = Surface(spriteSize)
                  
                  sprite.blit(fullImage, (0,0), Rect((x,y), spriteSize))
                  
                  # If we need to set the color key
                  if colorKey:
                     sprite.set_colorkey(sprite.get_at((0,0)))
                  
                  # Add the sprite to the end of the current row
                  self[fileName][-1].append(sprite)
         else:
            # Not a sprite sheet, full image is what we wish to store
            self[fileName] = fullImage
               
            # If we need to set the color key
            if colorKey:
               self[fileName].set_colorkey(self[fileName].get_at((0,0)))
            
         