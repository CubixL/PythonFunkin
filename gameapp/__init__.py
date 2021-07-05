import os


if os.name == 'posix':
    from .rect import Rect
    from .constants import *
    from .gameapp_pythonista import GameApp, GameText, GameFont, GameImage

elif os.name == 'nt':
    import pygame
    from pygame.locals import *
    from .rect import Rect
    # from pygame import Rect
    from .gameapp import GameApp, GameText, GameFont, GameImage

