import os

# load pythonsta libraries
if os.name == 'posix':

    from .ios_constants import *
    from .ios_gameapp import GameApp, GameText, GameFont, GameImage, Rect, GameAudio
    
#load pygame libraries
elif os.name == 'nt':
    import pygame
    from pygame.locals import *
    # from .rect import Rect
    from pygame import Rect
    from .win_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio

