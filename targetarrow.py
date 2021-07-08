from gameapp import *

class TargetArrow():                       # Arrows that rise up and hitting them rewards score
    def __init__(self, parent, type, milliseconds, isEnemy):
        # Set up variables
        self.type = type
        self.parent = parent
        self.milliseconds = milliseconds
        self.scale = parent.scale
        self.isEnemy = isEnemy

        # Set up sprites + starting Y position
        self.img = GameImage(self, f'images\\arrows\\GUI_Arrow{type}Target.png') 
        self.img_sustain = GameImage(self, f'images\\arrows\\GUI_Arrow{type}TargetHeld.png')
        self.img_sustainend = GameImage(self, f'images\\arrows\\GUI_Arrow{type}TargetHeldEnd.png')
        self.img.position.y = 110 
        self.img_sustain.position.y = 60
        
        # Note characteristics
        self.state = 'hidden'
        self.sustainLength = 0
       
        # X position and keys/altkeys determined by note type. Default is left.
        if self.isEnemy == False:
            self.img.position.x = 144
            self.img_sustain.position.x = 150
            self.key = K_LEFT
            self.altkey = K_a
            if self.type == 'Down':
                self.img.position.x = 165
                self.img_sustain.position.x = 171
                self.key = K_DOWN
                self.altkey = K_s
            if self.type == 'Up':
                self.img.position.x = 186
                self.img_sustain.position.x = 191
                self.key = K_UP
                self.altkey = K_w
            if self.type == 'Right':
                self.img.position.x = 207
                self.img_sustain.position.x = 213
                self.key = K_RIGHT
                self.altkey = K_d
        else:
            self.img.position.x = 17
            self.img_sustain.position.x = 23
            self.key = K_LEFT
            self.altkey = K_a
            if self.type == 'Down':
                self.img.position.x = 38
                self.img_sustain.position.x = 44
                self.key = K_DOWN
                self.altkey = K_s
            if self.type == 'Up':
                self.img.position.x = 59
                self.img_sustain.position.x = 65
                self.key = K_UP
                self.altkey = K_w
            if self.type == 'Right':
                self.img.position.x = 80
                self.img_sustain.position.x = 86
                self.key = K_RIGHT
                self.altkey = K_d
    
    def move(self): # Move up the screen every frame
        if self.state == 'active':
            self.img.position.y -= 1 

    def calcScore(self, key = None, isDown = True): # Calculate score base on Y position
        score = 0
        if self.isEnemy == False:
            if self.img.position.y < -17 :      # Off-screen: Miss
                score = -10
            elif self.img.position.y < -6 :     # Between -17 and -5: Out of score range but should still be displayed
                score = 0
            elif self.img.position.y < -2 :     # Between -5 and -2: SHIT
                score = 50
            elif self.img.position.y < 3 :      # Between -2 and 3: BAD
                score = 100
            elif self.img.position.y < 7 :      # Between 3 and 7: GOOD!
                score = 200
            elif self.img.position.y < 13 :     # Between 7 and 13: SICK!!!
                score = 350
            elif self.img.position.y < 18 :     # Between 13 and 18: GOOD!
                score = 200
            elif self.img.position.y < 22 :     # Between 18 and 22: BAD
                score = 100
            elif self.img.position.y < 26 :     # Between 22 and 26: SHIT
                score = 50
        # If more than 26, out of input range
        return score

    def render(self): # Render only if is currently on the screen.
        if self.state == 'active':
            self.img.render()
        self.img_sustain.render()