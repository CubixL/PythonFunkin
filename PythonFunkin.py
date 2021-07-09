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
   
class PythonFunkin(GameApp):               # Main app
    def __init__(self):
        # GameApp variables
        super().__init__(240, 135, 1, scale=4.0) # Screen size + number of the display
        self.fps = 66.666
        self.section = 'menu'
        self.level = Level(self)


        self.menu = MainMenu(self)
        self.editor = Editor(self)

    def on_loop(self): # Main loop
        if self.section == 'level':
            self.level.on_loop()
        elif self.section == 'menu':
            self.menu.on_loop()
        elif self.section == 'editor':
            self.editor.on_loop()

    def on_render(self):  # Blit stuff
        if self.section == 'level':
            self.level.on_render()
        elif self.section == 'menu':
            self.menu.on_render()
        elif self.section == 'editor':
            self.editor.on_render()

    def on_key(self, isDown, key, mod):         # Check inputs
        if self.section == 'level':
            self.level.on_key(isDown, key, mod)
        elif self.section == 'menu':
            self.menu.on_key(isDown, key, mod)
        elif self.section == 'editor':
            self.editor.on_key(isDown, key, mod)

if __name__ == '__main__':

    PythonFunkin().start()
