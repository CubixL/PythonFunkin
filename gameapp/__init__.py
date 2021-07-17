import os

# load pythonsta libraries
if os.name == 'posix':

    import ios_constants as k
    from .ios_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio, GameSection
    from .apprect import Rect
    
#load pygame libraries
elif os.name == 'nt':
    import pygame
    import pygame.constants as k
    from .rect import Rect
    #from pygame import Rect 
    from .win_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio, GameSection
