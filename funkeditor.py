from gameapp import *

class Editor():
    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale
        self.EditorBackground = GameImage(self, 'images/background/EditBackground.gif')
        self.LeftArrow = GameImage(self, 'images/funkeditor/ArrowLeftEditor.gif')
        self.DownArrow = GameImage(self, 'images/funkeditor/ArrowDownEditor.gif')
        self.UpArrow = GameImage(self, 'images/funkeditor/ArrowUpEditor.gif')
        self.RightArrow = GameImage(self, 'images/funkeditor/ArrowRightEditor.gif')

    def on_loop(self):
        pass

    def on_render(self):
        self.EditorBackground.render()
        self.LeftArrow.render((8, 15))
        self.DownArrow.render((16, 15))
        self.UpArrow.render((24, 15))
        self.RightArrow.render((32, 15))

    def on_key(self, isDown, key, mod):
        if isDown and key == K_ESCAPE:
            self.parent.section = 'menu'