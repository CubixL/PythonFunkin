from gameapp import GameImage, kb
import json


from gameapp.win_gameapp import GameApp

class TargetArrow():                       # Arrows that rise up and hitting them rewards score
    def __init__(self, parent, type, milliseconds, isEnemy, sustainLength):
        # Set up variables
        self.type = type
        self.parent = parent
        self.milliseconds = milliseconds
        self.sustainLength = sustainLength
        self.sustainMilli = self.milliseconds + self.sustainLength
        self.sustainTop = 140
        self.sustainBottom = 140
        self.sustainShaftLength = int((130 * self.sustainLength) / self.parent.totalMoveTime)
        
        self.isEnemy = isEnemy

        # settings for keybinds
        self.saveFile = {}
        self.saveFile['settings'] = {}
        
        with open('saveFile.json') as json_file:
            self.saveFile = json.load(json_file)

        # Set up sprites + starting Y position
        self.img = GameImage(f'images/arrows/GUI_Arrow{type}Target.png') 
        self.img_sustain = GameImage(f'images/arrows/GUI_Arrow{type}TargetHeld.png')
        self.img_sustainend = GameImage(f'images/arrows/GUI_Arrow{type}TargetHeldEnd.png')
        self.initialypos = 140
        self.perfectypos = 10
        self.img.position.y = self.initialypos
        
        self.img_sustain.position.y = self.initialypos + 6
        self.img_sustainend.position.y = self.initialypos + 6

        # Note characteristics
        self.state = 'hidden'
        self.endstate = 'hidden'
        self.finishedResize = False
       
        # if self.sustainLength != 0:
        #     x = x + 1

        # X position and keys/altkeys determined by note type. Default is left.
        if self.isEnemy == False:
            self.img.position.x = 144
            self.img_sustain.position.x = 150
            self.img_sustainend.position.x = 150
            self.key = kb.K_LEFT
            self.altkey = self.saveFile['settings']['LeftKeybind']
            if self.type == 'Down':
                self.img.position.x = 165
                self.img_sustain.position.x = 170
                self.img_sustainend.position.x = 170
                self.key = kb.K_DOWN
                self.altkey = self.saveFile['settings']['DownKeybind']
            if self.type == 'Up':
                self.img.position.x = 186
                self.img_sustain.position.x = 190
                self.img_sustainend.position.x = 190
                self.key = kb.K_UP
                self.altkey = self.saveFile['settings']['UpKeybind']
            if self.type == 'Right':
                self.img.position.x = 207
                self.img_sustain.position.x = 213
                self.img_sustainend.position.x = 213
                self.key = kb.K_RIGHT
                self.altkey = self.saveFile['settings']['RightKeybind']
        else:
            self.img.position.x = 17
            self.img_sustain.position.x = 23
            self.img_sustainend.position.x = 23
            self.key = kb.K_LEFT
            self.altkey = self.saveFile['settings']['LeftKeybind']
            if self.type == 'Down':
                self.img.position.x = 38
                self.img_sustain.position.x = 43
                self.img_sustainend.position.x = 43
                self.key = kb.K_DOWN
                self.altkey = self.saveFile['settings']['DownKeybind']
            if self.type == 'Up':
                self.img.position.x = 59
                self.img_sustain.position.x = 64
                self.img_sustainend.position.x = 64
                self.key = kb.K_UP
                self.altkey = self.saveFile['settings']['UpKeybind']
            if self.type == 'Right':
                self.img.position.x = 80
                self.img_sustain.position.x = 86
                self.img_sustainend.position.x = 86
                self.key = kb.K_RIGHT
                self.altkey = self.saveFile['settings']['RightKeybind']
    
    def move(self): # Move up the screen every frame

        # Total number of pixels to move from bottom to top
        totalMoveDist = self.initialypos - self.perfectypos
        # Total time for a note to move from bottom to top. If speed is default then it's 1500
        # totalMoveTime = 1500 / self.parent.JSONspeed
        # Time since last frame
        lastFrameTime = self.parent.gameapp.get_lastframe_MS()
        # Number of pixels to move in this frame
        moveDist = totalMoveDist * lastFrameTime / self.parent.totalMoveTime

        if self.state == 'active':
            self.img.position.y -= moveDist
            self.img_sustain.position.y -= moveDist
        if self.endstate == 'active':
            self.img_sustainend.position.y -= moveDist

    # def updateLength(self):
    #     # self.sustainShaftLength = int(self.img_sustainend.position.y) - int(self.img.position.y)
    #     self.img_sustain.resize(width = 7, height = self.sustainShaftLength, in_place = True)
    
    def calcScore(self, key = None, isDown = True): # Calculate score base on Y position
        score = 0
        if self.isEnemy == False:
            if self.img.position.y < -17 :      # Off-screen: Miss
                score = -10
            elif self.img.position.y < -6 :     # Between -17 and -5: Out of score range but should still be displayed
                score = 0
            elif self.img.position.y < -4 :     # Between -5 and -2: SHIT
                score = 50
            elif self.img.position.y < -2 :      # Between -2 and 2: BAD
                score = 100
            elif self.img.position.y < 2 :      # Between 2 and 7: GOOD!
                score = 200
            elif self.img.position.y < 19 :     # Between 7 and 13: SICK!!!
                score = 350
            elif self.img.position.y < 23 :     # Between 13 and 19: GOOD!
                score = 200
            elif self.img.position.y < 25 :     # Between 19 and 22: BAD
                score = 100
            elif self.img.position.y < 27 :     # Between 22 and 25: SHIT
                score = 50
        # If more than 26, out of input range
        return score

    def render(self): # Render only if is currently on the screen.
        if self.endstate == 'active':
            self.img_sustainend.render()
        if self.state == 'active':
            if self.sustainLength != 0:
                self.img_sustain.render()
            self.img.render()
        elif self.state == 'played':
            if self.sustainLength != 0 and self.finishedResize == False:
                # Total number of pixels to move from bottom to top
                totalMoveDist = self.initialypos - self.perfectypos
                # Total time for a note to move from bottom to top. If speed is default then it's 1500
                # totalMoveTime = 1500 / self.parent.JSONspeed
                # Time since last frame
                lastFrameTime = self.parent.gameapp.get_lastframe_MS()
                # Number of pixels to move in this frame
                moveDist = totalMoveDist * lastFrameTime / self.parent.totalMoveTime
                self.sustainShaftLength -= moveDist
                if self.sustainShaftLength <= 0:
                    self.finishedResize = True
                else:
                    self.img_sustain.position.y = 19
                    self.img_sustain.resize(width = 7, height = int(self.sustainShaftLength), in_place = True)
                    self.img_sustain.render()