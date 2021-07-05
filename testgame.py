
from gameapp import *

class MyRedCar(GameImage):
    def __init__(self):
        super().__init__("gameapp\\images\\redcar.png", (200, 300))
        self.bRightSide = True
        self.t = Rect(0,0,0,0)

    def move(self):
        
        if self.bRightSide:
            self.position.move_ip(3, 0)
        else:
            self.position.move_ip(-3, 0)

        if self.position.x < 0:
            self.position.x = 200
        if self.position.x > 400:
            self.position.x = 200

    def toggle(self):
        self.bRightSide = not self.bRightSide


class TestGame(GameApp):
    def __init__(self):
        super().__init__(500, 500) 
        self.redcar = MyRedCar()
        self.fps = 50
        self.bluecar = GameImage('gameapp\\images\\bluecar.png', (10,500))
        self.bluecar.scale2x()
        # self.redcar = 
        self.fontVerdana = GameFont('Verdana',50)
        self.myText = GameText(self.fontVerdana, 'mart is great', (125, 300), (255, 255, 125))


    def on_loop(self):
        self.bluecar.position.move_ip(0, -5)
        if self.bluecar.position.y < 5:
            self.bluecar.position.y  = 500

        self.redcar.move()

    def on_render(self):
        self.surface.fill((100 ,100,255))
        self.bluecar.render()
        self.myText.position.x = 10
        self.myText.position.y = 10
        self.myText.text = str(self.milliseconds_since_start)
        self.myText.render()
        self.redcar.render()


    def on_event(self, eventId):
        pass

    def on_key(self, isDown, key, mod):
        if isDown == True and key == K_q:
            self.isRunning = False

        if isDown == True and key == K_t:

            self.redcar.toggle()


if __name__ == "__main__" :
    TestGame().start()
