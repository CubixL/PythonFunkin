from menu import Menu
from gameapp import GameImage

class MainMenu(Menu):   
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images\\background\\BGE_MenuBackground.png')
        self.Buttons.append( { 
            'section' : 'level',
            'imgNormal' : GameImage(self, 'images\\gui\\GUI_ButtonPlay.png', (17, 20)),
            'imgSelected' : GameImage(self, 'images\\gui\\GUI_ButtonPlaySelected.png', (17, 17)),
        })

        self.Buttons.append( { 
            'section' : 'load',
            'imgNormal' : GameImage(self, 'images\\gui\\GUI_ButtonLoad.png', (17, 58)),
            'imgSelected' : GameImage(self, 'images\\gui\\GUI_ButtonLoadSelected.png', (17, 56)),
        })

        self.Buttons.append( { 
            'section' : 'editor',
            'imgNormal' : GameImage(self, 'images\\gui\\GUI_ButtonEdit.png', (17, 99)),
            'imgSelected' : GameImage(self, 'images\\gui\\GUI_ButtonEditSelected.png', (17, 97)),
        })        

    def doAction(self):
        self.parent.section = self.Buttons[self.highlighted]['section']


        if self.highlighted == 0:
            self.parent.level.loadFile()

