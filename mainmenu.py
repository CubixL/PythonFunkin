from menu import Menu
from gameapp import *

#  for future usage when we need a more intelligent button, like adding visual effect 
# class GameButton():
#     def __init__(self, section, imgNormal, imgSelected):
#         self.type = 'text' 'image'
#         self.currentSection = section
#         self.imgNormal = imgNormal
#         self.imgSelected = imgSelected
#         self.isActive = False




class MainMenu(Menu):   
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/BGE_MenuBackground.png')

        # for future usage example on how to use the GameButton class instead of a dictionary
        # self.Buttons.append(GameButton(
        #                         'level',
        #                         GameImage(self, 'images/gui/GUI_ButtonPlay.png', (17, 20)),
        #                         GameImage(self, 'images/gui/GUI_ButtonPlaySelected.png', (17, 17))
        #                     )
        # )


        # self.Buttons.append( { 
        #     'section' : 'level2',
        #     'imgNormal' : GameText(self, GameFont(self), 'play', (17, 5)),
        #     'imgSelected' : GameText(self, GameFont(self), 'play', (17, 5), RGB=(255,1,1)),
        # })
        self.Buttons.append( { 
            'section' : 'level',
            'imgNormal' : GameImage(self, 'images/gui/GUI_ButtonPlay.png', (17, 20)),
            'imgSelected' : GameImage(self, 'images/gui/GUI_ButtonPlaySelected.png', (17, 17)),
        })

        self.Buttons.append( { 
            'section' : 'loadmenu',
            'imgNormal' : GameImage(self, 'images/gui/GUI_ButtonLoad.png', (17, 58)),
            'imgSelected' : GameImage(self, 'images/gui/GUI_ButtonLoadSelected.png', (17, 56)),
        })

        self.Buttons.append( { 
            'section' : 'editor',
            'imgNormal' : GameImage(self, 'images/gui/GUI_ButtonEdit.png', (17, 99)),
            'imgSelected' : GameImage(self, 'images/gui/GUI_ButtonEditSelected.png', (17, 97)),
        })        

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == K_RETURN:
                # if using the GameButton class, we need to acces the values with . instead of []
                # self.parent.currentSection = self.Buttons[self.highlighted].currentSection
                self.parent.currentSection = self.Buttons[self.highlighted]['section']


                if self.highlighted == 0:
                    self.parent.sections['level'].loadFile()
            
            if key == K_ESCAPE:
                self.parent.quit()

