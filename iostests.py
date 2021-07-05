from gameapp import *

class MyGame(GameApp):
    def __init__(self):
        super().__init__()
        self.image = GameImage('spc:PlayerShip1Orange', (200,200))

    def on_render(self):
        self.image.render()
        pass



if __name__ == "__main__" :
    print('start')
    app = GameApp()
    
   # app.image.render()
    GameApp().start()
