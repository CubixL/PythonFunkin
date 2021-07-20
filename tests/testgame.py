
from gameapp import GameImage, Rect, GameApp, GameFont, GameText

class MyRedCar(GameImage):
    def __init__(self):
        super().__init__("images/testBG.gif")
        self.bRightSide = True
        self.t = Rect(0,0,0,0)

    def move(self):
        
        if self.bRightSide:
            self.position.x += 3
        else:
            self.position.x -= 3

        if self.position.x < 0:
            self.position.x = 200
        if self.position.x > 400:
            self.position.x = 200

    def toggle(self):
        self.bRightSide = not self.bRightSide


class TestGame(GameApp):
    def __init__(self):
        super().__init__(width=500, height=500) 
        self.redcar = MyRedCar()
        self.fps = 50
        self.bluecar = GameImage('gameapp/images/bluecar.png', (10,500))
        # self.redcar = 
        self.fontVerdana = GameFont(self)
        self.myText = GameText(self.fontVerdana, 'mart is great', (125, 300), (255, 255, 125))
        self.myText2 = GameText(self.fontVerdana, 'test')


    def on_loop(self):
        pass
        #self.bluecar.position.x = 200
        self.bluecar.position.y -= 5
        if self.bluecar.position.y < 5:
            self.bluecar.position.y  = 500

        self.redcar.move()

    def on_render(self):
       # self.surface.fill((100 ,100,255))
        self.bluecar.render()
        self.redcar.render()
        self.myText.position.x = 100
        self.myText.position.y = 50
        # self.myText.text = str(self.milliseconds_since_start)
        self.myText.render()
        # self.myText2.renderText(self.scene.size)



    def on_event(self, eventId):
        pass

    def on_key(self, isDown, key, mod):
        if isDown == True and key == key.K_LEFT:
            self.isRunning = False

        if isDown == True and key == key.K_RIGHT:

            self.redcar.toggle()


if __name__ == "__main__" :
    app = TestGame()
    app.start()
