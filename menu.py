from gameapp import *

   
class Menu():
    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale
        self.GUIFont = GameFont(self, 'fonts\\vcr.ttf', 6, False)
        self.TestText = GameText(self, self.GUIFont)
        self.MenuBackground = GameImage(self, 'images\\background\\BGE_MenuBackground.png')

        self.Buttons = []

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

     

        self.highlighted = 0


    def on_loop(self):
        pass

    def on_render(self):
        self.MenuBackground.render()
        self.TestText.renderText(f'{self.highlighted}')

        # buttons


        for index in range(0, len(self.Buttons)):
            currentButton = self.Buttons[index]
            if index == self.highlighted:
                currentButton['imgSelected'].render()
            else:
                currentButton['imgNormal'].render()


            

        

    def on_key(self, isDown, key, mod): 
        if isDown:
            if key == K_ESCAPE: # ESC kills game
                self.parent.isRunning = False
            
            # menu navigating
            numItems = len(self.Buttons) - 1
            if key == K_DOWN or key == K_s:
                if self.highlighted < numItems:
                    self.highlighted += 1
                else:
                    self.highlighted = 0
            if key == K_UP or key == K_w:
                if self.highlighted > 0:
                    self.highlighted -= 1
                else:
                    self.highlighted = numItems
            
            # enter key
            if key == K_RETURN:

                self.parent.section = self.Buttons[self.highlighted]['section']

                if self.highlighted == 0:
                    self.parent.level.loadFile()



