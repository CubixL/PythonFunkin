from gameapp import *

class MyGame(GameApp):
    def __init__(self):
        super().__init__()
        self.image = GameImage('gameapp/images/redcar.png', (200,200))
        self.image2 = GameImage('gameapp/images/redcar.png', (400,200))

    def on_render(self):
        self.image.render()
        self.image2.render()
        pass



if __name__ == "__main__" :
    MyGame().start()
