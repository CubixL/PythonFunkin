import os

# load pythonsta libraries
if os.name == 'posix':

    import gameapp.ios_constants as k
    from gameapp.ios_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio, GameSection
    from gameapp.rect import Rect
    
#load pygame libraries
elif os.name == 'nt':
    import pygame
    import pygame.constants as k
    from gameapp.rect import Rect
    #from pygame import Rect 
    from gameapp.win_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio, GameSection
