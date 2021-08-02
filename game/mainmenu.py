from game.menu import Menu, MenuButton
from gameapp import GameImage, kb

class MainMenu(Menu):   
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/menu/BGE_MenuBackground.png')

        self.Buttons.append(MenuButton(
            name = 'loadmenu',
            menuTab = 0,
            type = 'image',
            position = (17, 20),
            positionSelected = (17, 17),
            fileName = 'images/gui/GUI_ButtonPlay'
        ))
        self.Buttons.append(MenuButton(
            name = 'settingsmenu',
            menuTab = 0,
            type = 'image',
            position = (17, 60),
            positionSelected = (17, 57),
            fileName = 'images/gui/GUI_ButtonSettings'
        ))
        self.Buttons.append(MenuButton(
            name = 'quit',
            menuTab = 0,
            type = 'image',
            position = (17, 99),
            positionSelected = (17, 97),
            fileName = 'images/gui/GUI_ButtonQuit'
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

