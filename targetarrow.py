from gameapp import *

class TargetArrow():                       # Arrows that rise up and hitting them rewards score
    def __init__(self, parent, type, milliseconds):
        # Set up variables
        self.type = type
        self.parent = parent
        self.milliseconds = milliseconds
        self.scale = 2

        # Set up sprites + starting Y position
        self.img = GameImage(f'images\\arrows\\GUI_Arrow{type}Target.png') 
        self.img_sustain = GameImage(f'images\\arrows\\GUI_Arrow{type}TargetHeld.png')
        self.img_sustainend = GameImage(f'images\\arrows\\GUI_Arrow{type}TargetHeldEnd.png')
        self.img.scale2x() 
        self.img.position.y = 110 * self.scale
        self.img_sustain.position.y = 60 * self.scale
        
        # Note characteristics
        self.state = 'hidden'
        self.sustainLength = 0
       
        # X position and keys/altkeys determined by note type. Default is left.
        self.img.position.x = 80 * self.scale
        self.img_sustain.position.x = 80 * self.scale
        self.key = K_LEFT
        self.altkey = K_a
        if self.type == 'Down':
            self.img.position.x = 101 * self.scale
            self.img_sustain.position.x = 101 * self.scale
            self.key = K_DOWN
            self.altkey = K_s
        if self.type == 'Up':
            self.img.position.x = 123 * self.scale
            self.img_sustain.position.x = 123 * self.scale
            self.key = K_UP
            self.altkey = K_w
        if self.type == 'Right':
            self.img.position.x = 144 * self.scale
            self.img_sustain.position.x = 144 * self.scale
            self.key = K_RIGHT
            self.altkey = K_d
    
    def move(self): # Move up the screen every frame
        if self.state == 'active':
            self.img.position.y -= 1 * self.scale

    def calcScore(self, key = None, isDown = True): # Calculate score base on Y position
        score = 0
        if self.img.position.y < -17 * self.scale:      # Off-screen: Miss
            score = -10
        elif self.img.position.y < -6 * self.scale:     # Between -17 and -5: Out of score range but should still be displayed
            score = 0
        elif self.img.position.y < -2 * self.scale:     # Between -5 and -2: SHIT
            score = 50
        elif self.img.position.y < 3 * self.scale:      # Between -2 and 3: BAD
            score = 100
        elif self.img.position.y < 7 * self.scale:      # Between 3 and 7: GOOD!
            score = 200
        elif self.img.position.y < 13 * self.scale:     # Between 7 and 13: SICK!!!
            score = 350
        elif self.img.position.y < 18 * self.scale:     # Between 13 and 18: GOOD!
            score = 200
        elif self.img.position.y < 22 * self.scale:     # Between 18 and 22: BAD
            score = 100
        elif self.img.position.y < 26 * self.scale:     # Between 22 and 26: SHIT
            score = 50
        # If more than 26, out of input range
        return score

    def render(self): # Render only if is currently on the screen.
        if self.state == 'active':
            self.img.render()
        self.img_sustain.render()