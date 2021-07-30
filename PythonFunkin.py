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
   
class PythonFunkin(GameApp):               # Main app
    def __init__(self):
        # GameApp variables
        super().__init__(width=240, height=135, displayNumber=1, fps = 80) # Screen size + number of the display
        self.currentSectionName = 'mainmenu'
        self.sections['level'] = Level(self)
        self.sections['mainmenu'] = MainMenu(self)
        self.sections['editor'] = Editor(self)
        self.sections['loadmenu'] = LoadMenu(self)
        self.sections['settingsmenu'] = SettingsMenu(self)

        # Timers

if __name__ == '__main__':
    PythonFunkin().start()
