from gameapp import *

class Menu():
    def __init__(self, parent):
        self.parent = parent
        
        self.GUIFont = GameFont(self, 'fonts/vcr.ttf', 6, False)
        self.TestText = GameText(self, self.GUIFont, RGB = (255, 0, 0))
        self.TestText2 = GameText(self, self.GUIFont, position = (12, 0), RGB = (255, 0, 0))

        self.Buttons = []
        self.MenuBackground = None
        self.MenuOverlay = None
        self.mousePos = (0, 0)
        self.highlighted = 0
        self.highlightedOverlay = 0


    def on_loop(self):
        pass

    def on_render(self):
        self.MenuBackground.render()
        if self.MenuOverlay:
            self.MenuOverlay.render()
        self.TestText.renderText(f'{self.highlighted}')
        self.TestText2.renderText(f'{self.highlightedOverlay}')

        # buttons
        for index in range(0, len(self.Buttons)):
            currentButton = self.Buttons[index]
            if index == self.highlighted:
                currentButton['imgSelected'].render()
                # for future usage when using GameButton class, 
                # currentButton.imgSelected.render()

            else:
                currentButton['imgNormal'].render()
                # for future usage when using GameButton class, 
                # currentButton.imgNormal.render()

         

        

    def on_key(self, isDown, key, mod): 
        if isDown:
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

            # overlay nav
            menuTabs = 1
            if key == K_RIGHT or key == K_d:
                if self.highlightedOverlay < menuTabs:
                    self.highlightedOverlay += 1
                else:
                    self.highlightedOverlay = 0
            if key == K_LEFT or key == K_a:
                if self.highlightedOverlay > 0:
                    self.highlightedOverlay -= 1
                else:
                    self.highlightedOverlay = menuTabs
            
        self.doAction(isDown, key, mod)

    def on_mouse(self, isDown, key, xcoord, ycoord):
        self.mousePos = (xcoord, ycoord)
        if isDown:
            if key == 1:
                pass


    def doAction(self):
        pass



