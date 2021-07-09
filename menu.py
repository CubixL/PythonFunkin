from gameapp import *

class Menu():
    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale
        self.GUIFont = GameFont(self, 'fonts\\vcr.ttf', 6, False)
        self.TestText = GameText(self, self.GUIFont)

        self.Buttons = []
        self.MenuBackground = None

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
                self.parent.quit()
            
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
                self.doAction()


    def doAction(self):
        pass



