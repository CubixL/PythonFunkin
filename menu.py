from gameapp import *

class Menu():

    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale
        self.GUIFont = GameFont(self, 'fonts\\vcr.ttf', 6, False)
        self.TestText = GameText(self, self.GUIFont, RGB = (125,125,125))

    def on_loop(self):
        pass

    def on_render(self):
        self.TestText.renderText('Start', (100,100))

    def on_key(self, isDown, key, mod): 
        pass