from gameapp import GameImage, GameApp

class Rating():
    def __init__(self, parent):
        self.position = (100, 10)
        self.parent = parent
        
        self.img_sick = GameImage(self, 'images/level/sick-pixel.png', position = self.position)
        self.img_good = GameImage(self, 'images/level/good-pixel.png', position = self.position)
        self.img_bad = GameImage(self, 'images/level/bad-pixel.png', position = self.position)
        self.img_shit = GameImage(self, 'images/level/shit-pixel.png', position = self.position)

    def render(self):
        self.img_sick.render()

    def on_timer(self):
        pass