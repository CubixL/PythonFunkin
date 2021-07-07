from gameapp import *

class Menu():

    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale
        self.GUIFont = GameFont(self, 'fonts\\vcr.ttf', 6, False)
        self.TestText = GameText(self, self.GUIFont, RGB = (125,125,125))
        self.MenuBackground = GameImage(self, 'images\\background\\BGE_MenuBackground.png')

        # concerning menu buttons
        self.ButtonPlay = GameImage(self, 'images\\gui\\GUI_ButtonPlay.png')
        self.ButtonPlaySelected = GameImage(self, 'images\\gui\\GUI_ButtonPlaySelected.png')
        self.ButtonLoad = GameImage(self, 'images\\gui\\GUI_ButtonLoad.png')
        self.ButtonLoadSelected = GameImage(self, 'images\\gui\\GUI_ButtonLoadSelected.png')
        self.ButtonEdit = GameImage(self, 'images\\gui\\GUI_ButtonEdit.png')
        self.ButtonEditSelected = GameImage(self, 'images\\gui\\GUI_ButtonEditSelected.png')
        self.highlighted = 0

    def on_loop(self):
        pass

    def on_render(self):
        self.MenuBackground.render()
        self.TestText.renderText(f'{self.highlighted}', (100,100))

        # buttons
        if self.highlighted == 0:
            self.ButtonPlaySelected.render(position = (17, 17))
            self.ButtonLoad.render(position = (17, 56))
            self.ButtonEdit.render(position = (17, 97))
        if self.highlighted == 1:
            self.ButtonPlay.render(position = (17, 17))
            self.ButtonLoadSelected.render(position = (17, 56))
            self.ButtonEdit.render(position = (17, 97))
        if self.highlighted == 2:
            self.ButtonPlay.render(position = (17, 17))
            self.ButtonLoad.render(position = (17, 56))
            self.ButtonEditSelected.render(position = (17, 97))

    def on_key(self, isDown, key, mod): 
            if isDown == True and key == K_ESCAPE: # ESC kills game
                self.parent.isRunning = False
            
            # menu navigating
            if isDown == True and key == K_DOWN or isDown == True and key == K_s:
                if self.highlighted < 2:
                    self.highlighted += 1
                else:
                    self.highlighted = 0
            if isDown == True and key == K_UP or isDown == True and key == K_w:
                if self.highlighted > 0:
                    self.highlighted -= 1
                else:
                    self.highlighted = 2
            
            # enter key
            if isDown == True and key == K_RETURN:
                if self.highlighted == 0:
                    self.parent.section = 'level'
                if self.highlighted == 1:
                    pass
                if self.highlighted == 2:
                    pass