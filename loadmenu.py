from gameapp import GameImage
from menu import Menu

class LoadMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/BGE_LoadBackground.png')
        self.MenuOverlay = GameImage(self, 'images/background/BGE_LoadOverlay.png')

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == key.K_ESCAPE:
                self.parent.currentSection = 'mainmenu'