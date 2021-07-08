from gameapp import *

class Rating():
    def __init__(self, parent):
        self.position = (100, 10)
        self.parent = parent
        self.scale = parent.scale
        self.img_sick = GameImage(self, 'images\\score\\sick-pixel.png', position = self.position)
        self.img_good = GameImage(self, 'images\\score\\good-pixel.png', position = self.position)
        self.img_bad = GameImage(self, 'images\\score\\bad-pixel.png', position = self.position)
        self.img_shit = GameImage(self, 'images\\score\\shit-pixel.png', position = self.position)

    def move(self):
        pass

    def render(self):
        self.img_sick.render()