from menu import Menu, MenuButton
from gameapp import GameImage, kb

class MainMenu(Menu):   
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/BGE_MenuBackground.png')

        self.Buttons.append(MenuButton(
            name = 'loadmenu',
            menuTab = 0,
            imgNormal = GameImage(self, 'images/gui/GUI_ButtonPlay.png', position=(17, 20)),
            imgSelected = GameImage(self, 'images/gui/GUI_ButtonPlaySelected.png', position=(17, 17))
        ))
        self.Buttons.append(MenuButton(
            name = 'settingsmenu',
            menuTab = 0,
            imgNormal = GameImage(self, 'images/gui/GUI_ButtonSettings.png', position=(17, 60)),
            imgSelected = GameImage(self, 'images/gui/GUI_ButtonSettingsSelected.png', position=(17, 57))
        ))
        self.Buttons.append(MenuButton(
            name = 'quit',
            menuTab = 0,
            imgNormal = GameImage(self, 'images/gui/GUI_ButtonQuit.png', position=(17, 99)),
            imgSelected = GameImage(self, 'images/gui/GUI_ButtonQuitSelected.png', position=(17, 97))
        ))   

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_RETURN:
                # if using the GameButton class, we need to acces the values with . instead of []
                # self.parent.currentSectionName = self.Buttons[self.highlighted].currentSection
                if self.Buttons[self.highlighted].name == 'quit':
                    self.parent.quit()
                else:
                    self.parent.currentSectionName = self.Buttons[self.highlighted].name
            if key == kb.K_ESCAPE:
                self.parent.quit()

