from gameapp import GameFont, GameText, GameImage, kb, GameSection

class Menu(GameSection):
    def __init__(self, parent):
        self.parent = parent
        
        self.GUIFont = GameFont(self, 'fonts/vcr.ttf', 6, False)
        # self.TestText = GameText(self, self.GUIFont, RGB = (255, 0, 0))
        # self.TestText2 = GameText(self, self.GUIFont, position = (12, 0), RGB = (255, 0, 0))

        self.Buttons = []
        self.MenuBackground = GameImage(self)
        self.MenuOverlay = None
        self.mousePos = (0, 0)
        self.highlighted = 0
        self.highlightedOverlay = 0
        self.menuTabs = 0


    def on_loop(self):
        pass

    def on_render(self):
        self.MenuBackground.render()
        if self.MenuOverlay:
            self.MenuOverlay.render()
        # self.TestText.renderText(f'{self.highlighted}')
        # self.TestText2.renderText(f'{self.highlightedOverlay}')

        # buttons
        for index in range(0, len(self.Buttons)):
            currentButton = self.Buttons[index]
            if currentButton['menuTab'] == self.highlightedOverlay:
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
            if key == kb.K_DOWN or key == kb.K_s:
                if self.highlighted < numItems:
                    self.highlighted += 1
                else:
                    self.highlighted = 0
            if key == kb.K_UP or key == kb.K_w:
                if self.highlighted > 0:
                    self.highlighted -= 1
                else:
                    self.highlighted = numItems

            # overlay nav
            if key == kb.K_RIGHT or key == kb.K_d:
                if self.highlightedOverlay < self.menuTabs:
                    self.highlightedOverlay += 1
                    self.highlighted = 0
                else:
                    pass
            if key == kb.K_LEFT or key == kb.K_a:
                if self.highlightedOverlay > 0:
                    self.highlightedOverlay -= 1
                    self.highlighted = 0
                else:
                    pass
            
        self.doAction(isDown, key, mod)

    def on_mouse(self, isDown, key, xcoord, ycoord):
        self.mousePos = (xcoord, ycoord)
        if isDown:
            if key == 1:
                pass


    def doAction(self, isDown, key, mod):
        pass



