# d:/VSCode/PythonFunkin
#
# Python Funkin'
# The game Friday Night Funkin', originally coded by ninjamuffin99, recreated with Pygame.
#
# Made by CubixL
# YouTube channel: https://www.youtube.com/channel/UCNNHpyTeYJqK9bfFeub3uNw

from gameapp import GameApp

from game.level import Level
from game.mainmenu import MainMenu
from game.funkeditor import Editor
from game.loadmenu import LoadMenu
from game.settingsmenu import SettingsMenu

if __name__ == '__main__':
    game = GameApp(width=240, height=135, display_number=1, scale = 5)
    game.set_gbl_anchor_point((0,0))
    game.add_section('mainmenu', MainMenu(game))
    game.add_section('loadmenu', LoadMenu(game))
    game.add_section('level', Level(game))
    game.add_section('editor', Editor(game))
    game.add_section('settingsmenu', SettingsMenu(game))
    game.sections['mainmenu'].active = True
    game.start()
