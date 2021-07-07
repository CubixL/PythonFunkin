from gameapp import *
from playerarrow import PlayerArrow
from targetarrow import TargetArrow

class Level():
    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale        
        self.LevelBackground = GameImage(self, 'images\\background\\testBG.gif', (0, 0))
        self.PlayerArrowL = PlayerArrow(self, type = 'Left')
        self.PlayerArrowD = PlayerArrow(self, type = 'Down')
        self.PlayerArrowU = PlayerArrow(self, type = 'Up')
        self.PlayerArrowR = PlayerArrow(self, type = 'Right')
        self.TargetList = []
        self.PlayerScore = 0


        # font & text
        self.GUIFont = GameFont(self, 'fonts\\vcr.ttf', 6, False)
        self.MSText = GameText(self, self.GUIFont)
        self.FPSText = GameText(self, self.GUIFont)
        self.ScoreText = GameText(self, self.GUIFont)

        self.loadFile()

    def getMilli(self):
        return self.parent.getMillisecondsSinceStart()  - self.milliAtStart

    def on_loop(self):
        currentscore = 0
        
        for target in self.TargetList:
            score = target.calcScore()
            # Check for targets that need to become active
            if target.state == 'hidden' and self.getMilli() >= target.milliseconds:
                target.state = 'active'
            # Check for targets that have passed the input range
            if target.state == 'active' and score < 0:
                target.state = 'played'
                currentscore += score
            target.move() # Move targets up

        self.PlayerScore += currentscore


    def on_render(self):
        self.LevelBackground.render()                                                # 1. Background
        self.PlayerArrowL.render()                                              # 2. Player arrows
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        for target in self.TargetList:                                          # 3. Target arrows (Note, then sustain line, then sustain end)
            target.render()

           
        self.MSText.renderText(f'Game time: {self.getMilli()}')   # 4. GUI (Text)
        self.FPSText.renderText(f'FPS: {self.parent.fps}', position = (0, 6))
        self.ScoreText.renderText(f'Score: {self.PlayerScore}', position = (0, 12))

    def on_key(self, isDown, key, mod): 
        if isDown == True and key == K_ESCAPE: # ESC kills game
            self.isRunning = False
        self.PlayerArrowL.on_key(isDown, key) # Check player arrows to switch sprites
        self.PlayerArrowD.on_key(isDown, key)
        self.PlayerArrowU.on_key(isDown, key)
        self.PlayerArrowR.on_key(isDown, key)

        # Check state of target arrows
        currentscore = 0
        for target in self.TargetList:
            # If target arrow was in score range and correct key was pressed
            if target.calcScore() > 0 and key == target.key and isDown and target.state == 'active':
                target.state = 'played'
                currentscore += target.calcScore()
        
        # If score is still 0, the bad key was pressed
        if currentscore == 0 and key in (K_DOWN, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d) and isDown:
            currentscore = -10
        self.PlayerScore += currentscore

        # Create target arrows (debugging)
        if isDown == True and key == K_j:
            self.TargetList.append(TargetArrow(self, type = 'Left'))
        if isDown == True and key == K_k:
            self.TargetList.append(TargetArrow(self, type = 'Down'))
        if isDown == True and key == K_i:
            self.TargetList.append(TargetArrow(self, type = 'Up'))
        if isDown == True and key == K_l:
            self.TargetList.append(TargetArrow(self, type = 'Right'))

        # R resets the chart
        if key == K_r:
            self.loadFile()


    def loadFile(self): # Load the entire song chart (JSON file stuff)
        # When called, reset score, timer and note list to 0 before loading
        self.PlayerScore = 0
        self.milliAtStart = self.parent.getMillisecondsSinceStart()
        self.TargetList.clear()

        self.TargetList.append(TargetArrow(self, type = 'Left', milliseconds = 500))
        self.TargetList.append(TargetArrow(self, type = 'Right', milliseconds = 700))
        self.TargetList.append(TargetArrow(self, type = 'Down', milliseconds = 900))
        self.TargetList.append(TargetArrow(self, type = 'Left', milliseconds = 1100))
        self.TargetList.append(TargetArrow(self, type = 'Down', milliseconds = 1300))
        self.TargetList.append(TargetArrow(self, type = 'Left', milliseconds = 1500))
        self.TargetList.append(TargetArrow(self, type = 'Down', milliseconds = 1700))
        self.TargetList.append(TargetArrow(self, type = 'Right', milliseconds = 1900))
