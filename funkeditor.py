from gameapp import *

class Editor():
    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale
        self.EditorBackground = GameImage(self, 'images\\background\\EditBackground.gif')

    def on_loop(self):
        pass

    def on_render(self):
        self.EditorBackground.render()
    
    def on_key(self, isDown, key, mod):
        if isDown and key == K_ESCAPE:
            self.parent.section = 'menu'