from gameapp import GameImage, k
from menu import Menu

class LoadMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/BGE_LoadBackground.png')
        self.MenuOverlay = GameImage(self, 'images/background/BGE_LoadOverlay.png')
        self.menuTabs = 1

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == k.K_ESCAPE:
                self.parent.currentSection = 'mainmenu'
            if key == k.K_LEFT and self.highlightedOverlay == 0:
                self.MenuOverlay.render((0, 0))
            if key == k.K_RIGHT and self.highlightedOverlay == 1:
                self.MenuOverlay.render((176, 0))