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
   
class PythonFunkin(GameApp):               # Main app
    def __init__(self):
        # GameApp variables
        super().__init__(240, 135, 1) # Screen size + number of the display
        self.fps = 66.666
        self.currentSection = 'menu'
        self.sections = {
            'level' : Level(self), 
            'menu' : MainMenu(self), 
            'editor' : Editor(self)
        }

if __name__ == '__main__':

    PythonFunkin().start()
