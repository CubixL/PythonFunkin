# d:/VSCode/PythonFunkin
#
# Python Funkin'
# The game Friday Night Funkin', originally coded by ninjamuffin99, recreated with Pygame.
#
# Made by CubixL
# YouTube channel: https://www.youtube.com/channel/UCNNHpyTeYJqK9bfFeub3uNw

from gameapp import GameApp
from level import Level
from mainmenu import MainMenu
from funkeditor import Editor
from loadmenu import LoadMenu
   
class PythonFunkin(GameApp):               # Main app
    def __init__(self):
        # GameApp variables
        super().__init__(240, 135, 1) # Screen size + number of the display
        self.fps = 150
        self.currentSection = 'mainmenu'
        self.sections['level'] = Level(self)
        self.sections['mainmenu'] = MainMenu(self)
        self.sections['editor'] = Editor(self)
        self.sections['loadmenu'] = LoadMenu(self)

        # Timers
        self.addTimer('AnimationTimer', 30, -1)

if __name__ == '__main__':

    PythonFunkin().start()
