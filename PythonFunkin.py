# d:/VSCode/PythonFunkin
#
# Python Funkin'
# The game Friday Night Funkin', originally coded by ninjamuffin99, recreated with Pygame.
#
# Made by CubixL
# YouTube channel: https://www.youtube.com/channel/UCNNHpyTeYJqK9bfFeub3uNw

from gameapp import *

class PlayerArrow():
    def __init__(self, type):
        self.type = type
        self.isPressed = False
        self.key = None
        self.altkey = None
        self.scale = 2
        self.img_default = GameImage(f"images/GUI_Arrow{type}Default.png")
        self.img_default.position.y = 10 * self.scale
        self.img_default.scale2x() 
        self.img_pressed = GameImage(f"images\\GUI_Arrow{type}Pressed.png")
        self.img_pressed.position.y = 10 * self.scale
        self.img_pressed.scale2x()

        if self.type == "Left":
            self.img_default.position.x = 80 * self.scale
            self.img_pressed.position.x = 80 * self.scale
            self.key = K_LEFT
            self.altkey = K_a
        if self.type == "Down":
            self.img_default.position.x = 101 * self.scale
            self.img_pressed.position.x = 101 * self.scale
            self.key = K_DOWN
            self.altkey = K_s
        if self.type == "Up":
            self.img_default.position.x = 123 * self.scale
            self.img_pressed.position.x = 123 * self.scale
            self.key = K_UP
            self.altkey = K_w
        if self.type == "Right":
            self.img_default.position.x = 144 * self.scale
            self.img_pressed.position.x = 144 * self.scale
            self.key = K_RIGHT
            self.altkey = K_d
    
    def render(self):
        if self.isPressed == False:
            self.img_default.render()
        elif self.isPressed == True:
            self.img_pressed.render() 

    def on_key(self, isDown, key):
        if isDown == True and key == self.key or isDown == True and key == self.altkey:
            self.isPressed = True
        elif isDown == False and key == self.key or isDown == False and key == self.altkey:
            self.isPressed = False

class TargetArrow():
    def __init__(self, parent, type, milliseconds):
        self.type = type
        self.parent = parent
        self.milliseconds = milliseconds
        self.scale = 2
        self.img = GameImage(f"images\\GUI_Arrow{type}Target.png") 
        self.img.scale2x() 
        self.img.position.y = 110 * self.scale
        self.state = "hidden"
       
        # Left by default
        self.img.position.x = 80 * self.scale
        self.key = K_LEFT
        self.altkey = K_a
        if self.type == "Down":
            self.img.position.x = 101 * self.scale
            self.key = K_DOWN
            self.altkey = K_s
        if self.type == "Up":
            self.img.position.x = 123 * self.scale
            self.key = K_UP
            self.altkey = K_w
        if self.type == "Right":
            self.img.position.x = 144 * self.scale
            self.key = K_RIGHT
            self.altkey = K_d
    
    def move(self):
        if self.state == "active":
            self.img.position.y -= 1 * self.scale

    def calcScore(self, key = None, isDown = True):
        # calculate score base on y coordinate
        score = 0
        if self.img.position.y < 10:
            score = -10
        elif self.img.position.y < 20:
            score = 200
        elif self.img.position.y < 30:
            score = 350
        elif self.img.position.y < 40:
            score = 200
        
        return score

    def render(self):
        if self.state == "active":
            self.img.render()
    
class PythonFunkin(GameApp):
    def __init__(self):
        # misc
        super().__init__(480, 240) # screen size
        self.fps = 66.666

        # assets
        self.Background = GameImage("images\\BGE_Week6BackgroundScaled.png", (0, 0))
        self.Background.scale2x()
        self.PlayerArrowL = PlayerArrow(type = "Left")
        self.PlayerArrowD = PlayerArrow(type = "Down")
        self.PlayerArrowU = PlayerArrow(type = "Up")
        self.PlayerArrowR = PlayerArrow(type = "Right")
        self.TargetList = []
        self.PlayerScore = 0
        self.loadFile()

        # font & text
        self.GUIFont = GameFont('fonts\\vcr.ttf', 12, False)
        self.MSText = GameText(self.GUIFont)
        self.FPSText = GameText(self.GUIFont)
        self.ScoreText = GameText(self.GUIFont)


    def loadFile(self):
        self.PlayerScore = 0
        self.milliseconds_since_start = 0
        self.TargetList.clear()
        self.TargetList.append(TargetArrow(parent = self, type = "Left", milliseconds = 500))
        self.TargetList.append(TargetArrow(parent = self, type = "Right", milliseconds = 700))
        self.TargetList.append(TargetArrow(parent = self, type = "Down", milliseconds = 900))
        self.TargetList.append(TargetArrow(parent = self, type = "Left", milliseconds = 1100))
        self.TargetList.append(TargetArrow(parent = self, type = "Down", milliseconds = 1300))
        self.TargetList.append(TargetArrow(parent = self, type = "Left", milliseconds = 1500))
        self.TargetList.append(TargetArrow(parent = self, type = "Down", milliseconds = 1700))
        self.TargetList.append(TargetArrow(parent = self, type = "Right", milliseconds = 1900))


    def on_loop(self):
        currentscore = 0
        
        for target in self.TargetList:
            target.move()
            score = target.calcScore()
            if target.state == "hidden" and self.milliseconds_since_start >= target.milliseconds:
                target.state = "active"
            if target.state == "active" and score < 0:
                target.state = "played"
                currentscore += score

        self.PlayerScore += currentscore

            
        

    def on_render(self):                                                        # Layering order:
        self.Background.render()                                                # 1. Background
        self.PlayerArrowL.render()                                              # 2. Player arrows
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        for target in self.TargetList:                                          # 3. Target arrows
            target.render()

           
        self.MSText.renderText(f"Game time: {self.milliseconds_since_start}")   # 4. GUI
        self.FPSText.renderText(f"FPS: {self.fps}", position = (0, 12))
        self.ScoreText.renderText(f"Score: {self.PlayerScore}", position = (0, 24))

    
    def on_event(self, eventId):
        pass

    def on_key(self, isDown, key, mod):
        if isDown == True and key == K_ESCAPE:
            self.isRunning = False
        self.PlayerArrowL.on_key(isDown, key)
        self.PlayerArrowD.on_key(isDown, key)
        self.PlayerArrowU.on_key(isDown, key)
        self.PlayerArrowR.on_key(isDown, key)

        currentscore = 0
        for target in self.TargetList:
            # If target arrow was in score range and correct key was pressed
            if target.calcScore() > 0 and key == target.key and isDown:
                target.state = "played"
                currentscore += target.calcScore()
        
        # If score is still 0, the bad key was pressed
        if currentscore == 0 and key in (K_DOWN, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d):
            currentscore == -10
        self.PlayerScore += currentscore

        if isDown == True and key == K_j:
            self.TargetList.append(TargetArrow(type = "Left"))
        if isDown == True and key == K_k:
            self.TargetList.append(TargetArrow(type = "Down"))
        if isDown == True and key == K_i:
            self.TargetList.append(TargetArrow(type = "Up"))
        if isDown == True and key == K_l:
            self.TargetList.append(TargetArrow(type = "Right"))

        if key == K_r:
            self.loadFile()

if __name__ == "__main__":
    PythonFunkin().start()
