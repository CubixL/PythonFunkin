# d:/VSCode/PythonFunkin
#
# Python Funkin'
# The game Friday Night Funkin', originally coded by ninjamuffin99, recreated with Pygame.
#
# Made by CubixL
# YouTube channel: https://www.youtube.com/channel/UCNNHpyTeYJqK9bfFeub3uNw

from gameapp import *
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
        self.sections = {
            'level' : Level(self), 
            'mainmenu' : MainMenu(self), 
            'editor' : Editor(self),
            'loadmenu' : LoadMenu(self)
        }

if __name__ == '__main__':

    PythonFunkin().start()
