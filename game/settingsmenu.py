from gameapp import GameImage, GameText, kb
from game.menu import Menu, MenuButton

class SettingsMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/BGE_SettingsBackground.png')
        self.menuTabs = 0

        self.Buttons.append(MenuButton(
            name = 'your mom',
            menuTab = 0,
            imgNormal = GameText(self, self.GUIFont, text = 'Placeholder', position = (10, 20), RGB = (255, 255, 255)),
            imgSelected = GameText(self, self.GUIFont, text = 'Placeholder', position = (10, 20), RGB = (255, 233, 127)),
        ))  
        self.Buttons.append(MenuButton(
            name = 'your dad',
            menuTab = 0,
            imgNormal = GameText(self, self.GUIFont, text = 'Placeholder', position = (10, 30), RGB = (255, 255, 255)),
            imgSelected = GameText(self, self.GUIFont, text = 'Placeholder', position = (10, 30), RGB = (255, 233, 127)),
        ))  

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.parent.currentSectionName = 'mainmenu'