# d:/VSCode/PythonFunkin
#
# Python Funkin'
# The game Friday Night Funkin', originally coded by ninjamuffin99, recreated with Pygame.
#
# Made by CubixL
# YouTube channel: https://www.youtube.com/channel/UCNNHpyTeYJqK9bfFeub3uNw

from gameapp import *
from playerarrow import PlayerArrow
from targetarrow import TargetArrow

   
class PythonFunkin(GameApp):               # Main app
    def __init__(self):
        # GameApp variables
        super().__init__(480, 240, 1) # Screen size + number of the display
        self.fps = 66.666

        # assets
        self.Background = GameImage('images\\background\\testBG.gif', (0, 0))
        self.Background.scale2x()
        self.PlayerArrowL = PlayerArrow(type = 'Left')
        self.PlayerArrowD = PlayerArrow(type = 'Down')
        self.PlayerArrowU = PlayerArrow(type = 'Up')
        self.PlayerArrowR = PlayerArrow(type = 'Right')
        self.TargetList = []
        self.PlayerScore = 0
        self.state = 'level'
        self.loadFile()

        # font & text
        self.GUIFont = GameFont('fonts\\vcr.ttf', 12, False)
        self.MSText = GameText(self.GUIFont)
        self.FPSText = GameText(self.GUIFont)
        self.ScoreText = GameText(self.GUIFont)

    def loadFile(self): # Load the entire song chart (JSON file stuff)
        # When called, reset score, timer and note list to 0 before loading
        self.PlayerScore = 0
        self.milliseconds_since_start = 0
        self.TargetList.clear()

        self.TargetList.append(TargetArrow(parent = self, type = 'Left', milliseconds = 500))
        self.TargetList.append(TargetArrow(parent = self, type = 'Right', milliseconds = 700))
        self.TargetList.append(TargetArrow(parent = self, type = 'Down', milliseconds = 900))
        self.TargetList.append(TargetArrow(parent = self, type = 'Left', milliseconds = 1100))
        self.TargetList.append(TargetArrow(parent = self, type = 'Down', milliseconds = 1300))
        self.TargetList.append(TargetArrow(parent = self, type = 'Left', milliseconds = 1500))
        self.TargetList.append(TargetArrow(parent = self, type = 'Down', milliseconds = 1700))
        self.TargetList.append(TargetArrow(parent = self, type = 'Right', milliseconds = 1900))

    def on_loop(self): # Main loop
        if self.state == 'level':
            self.on_loop_level()
        elif self.state == 'menu':
            self.on_loop_menu()
        

    def on_loop_menu(self): # menu loop
        pass

    def on_loop_level(self): # Main loop (level section)
        currentscore = 0
        
        for target in self.TargetList:
            score = target.calcScore()
            # Check for targets that need to become active
            if target.state == 'hidden' and self.milliseconds_since_start >= target.milliseconds:
                target.state = 'active'
            # Check for targets that have passed the input range
            if target.state == 'active' and score < 0:
                target.state = 'played'
                currentscore += score
            target.move() # Move targets up

        self.PlayerScore += currentscore

    def on_render(self):  # Blit stuff
        if self.state == 'level':
            self.on_render_level()
        if self.state == 'menu':
            self.on_render_menu()


    def on_render_menu(self):
        pass
        
    def on_render_level(self):  # Level rendering phase.                        # Layering order:
        self.Background.render()                                                # 1. Background
        self.PlayerArrowL.render()                                              # 2. Player arrows
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        for target in self.TargetList:                                          # 3. Target arrows (Note, then sustain line, then sustain end)
            target.render()

           
        self.MSText.renderText(f'Game time: {self.milliseconds_since_start}')   # 4. GUI (Text)
        self.FPSText.renderText(f'FPS: {self.fps}', position = (0, 12))
        self.ScoreText.renderText(f'Score: {self.PlayerScore}', position = (0, 24))

    def on_key(self, isDown, key, mod):         # Check inputs
        if self.state == 'level':
            self.on_key_level(isDown, key, mod)
        if self.state == 'menu':
            self.on_key_menu(isDown, key, mod)

    def on_key_menu(self, isDown, key, mod):
        pass

    def on_key_level(self, isDown, key, mod):   # Check inputs (level)
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
            self.TargetList.append(TargetArrow(type = 'Left'))
        if isDown == True and key == K_k:
            self.TargetList.append(TargetArrow(type = 'Down'))
        if isDown == True and key == K_i:
            self.TargetList.append(TargetArrow(type = 'Up'))
        if isDown == True and key == K_l:
            self.TargetList.append(TargetArrow(type = 'Right'))

        # R resets the chart
        if key == K_r:
            self.loadFile()

if __name__ == '__main__':
    PythonFunkin().start()
