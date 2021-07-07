from gameapp import *

class PlayerArrow():                       # Arrows at the top, input by the player
    def __init__(self, type):
        # Set up variables and keys
        self.type = type
        self.isPressed = False
        self.key = None
        self.altkey = None
        self.scale = 2

        # Set up sprites + Y position
        self.img_default = GameImage(f'images\\arrows\\GUI_Arrow{type}Default.png')
        self.img_default.position.y = 10 * self.scale
        self.img_default.scale2x() 
        self.img_pressed = GameImage(f'images\\arrows\\GUI_Arrow{type}Pressed.png')
        self.img_pressed.position.y = 10 * self.scale
        self.img_pressed.scale2x()

        # Determine position
        if self.type == 'Left':
            self.img_default.position.x = 80 * self.scale
            self.img_pressed.position.x = 80 * self.scale
            self.key = K_LEFT
            self.altkey = K_a
        if self.type == 'Down':
            self.img_default.position.x = 101 * self.scale
            self.img_pressed.position.x = 101 * self.scale
            self.key = K_DOWN
            self.altkey = K_s
        if self.type == 'Up':
            self.img_default.position.x = 123 * self.scale
            self.img_pressed.position.x = 123 * self.scale
            self.key = K_UP
            self.altkey = K_w
        if self.type == 'Right':
            self.img_default.position.x = 144 * self.scale
            self.img_pressed.position.x = 144 * self.scale
            self.key = K_RIGHT
            self.altkey = K_d
    
    def render(self):
        if self.isPressed == False:
            self.img_default.render() # Render default sprites if not pressed
        elif self.isPressed == True:
            self.img_pressed.render() # Render pressed sprites if pressed

    def on_key(self, isDown, key):
        # Key and altkeys determine if isPressed is true or not
        if isDown == True and key == self.key or isDown == True and key == self.altkey:
            self.isPressed = True
        elif isDown == False and key == self.key or isDown == False and key == self.altkey:
            self.isPressed = False