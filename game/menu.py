from gameapp import GameFont, GameText, GameImage, kb, GameSection, GameAudio

class MenuButton():
    def __init__(self, name, menuTab, type, position, menuText = None, normalColor = (255, 255, 255), selectedColor = (255, 233, 127), fileName = None, positionSelected = None):
        self.name = name
        self.menuTab = menuTab
        self.type = type
        self.position = position
        self.positionSelected = positionSelected
        if self.positionSelected == None:
            self.positionSelected = self.position
        self.fileName = fileName

        self.isActive = False
        self.menuText = menuText
        self.normalColor = normalColor
        self.selectedColor = selectedColor
        self.GUIFont = GameFont(self, 'fonts/vcr.ttf', 6, False)
        self.update()

    def update(self):
        if self.type == 'text':
            self.imgNormal = GameText(self, self.GUIFont, text = self.menuText, position = self.position, RGB = self.normalColor)
            self.imgSelected = GameText(self, self.GUIFont, text = self.menuText, position = self.positionSelected, RGB = self.selectedColor)
        elif self.type == 'image':
            self.imgNormal = GameImage(self, f'{self.fileName}.png', position = self.position)
            self.imgSelected = GameImage(self, f'{self.fileName}Selected.png', position = self.positionSelected)

class Menu(GameSection):
    def __init__(self, parent):
        self.parent = parent
        self.GUIFont = GameFont(self, 'fonts/vcr.ttf', 6, False)
        self.TitleFont = GameFont(self, 'fonts/vcr.ttf', 10, isSys = False)

        self.Buttons = []
        self.MenuBackground = GameImage(self)
        self.MenuOverlay = None
        self.mousePos = (0, 0)
        self.highlighted = 0
        self.highlightedTab = 0
        self.menuTabs = 0
        self.maxButtons = 1000
        self.scrollAudio = GameAudio('sounds/menuselect')

    def on_loop(self):
        pass

    def on_render(self):
        self.MenuBackground.render()
        if self.MenuOverlay:
            self.MenuOverlay.render()

        # buttons
        for index in range(0, len(self.Buttons)):
            currentButton = self.Buttons[index]
            if currentButton.menuTab == self.highlightedTab:
                if index == self.highlighted:
                    currentButton.imgSelected.render()
                else:
                    currentButton.imgNormal.render()

    def on_key(self, isDown, key, mod): 
        if isDown:
            # menu navigating
            numItems = len(self.Buttons) - 1
            if key == kb.K_DOWN or key == kb.K_s:
                if self.highlighted < numItems:
                    self.highlighted += 1
                    if (self.highlighted % self.maxButtons) == 0:
                        self.highlightedTab += 1
                self.scrollAudio.stop()
                self.scrollAudio.play()
            if key == kb.K_UP or key == kb.K_w:
                if self.highlighted > 0:
                    self.highlighted -= 1
                    if (self.highlighted % self.maxButtons) == self.maxButtons - 1:
                        self.highlightedTab -= 1
                self.scrollAudio.stop()
                self.scrollAudio.play()

        self.doAction(isDown, key, mod)

    def on_mouse(self, isDown, key, xcoord, ycoord):
        self.mousePos = (xcoord, ycoord)
        if isDown:
            if key == 1:
                pass

    def doAction(self, isDown, key, mod):
        pass



