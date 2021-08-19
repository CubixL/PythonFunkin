from gameapp import GameImage, kb
import os, json

class PlayerArrow():                       # Arrows at the top, input by the player
    def __init__(self, parent, type):
        # Set up variables and keys
        self.parent = parent
        self.type = type
        self.isPressed = False
        self.key = None
        self.altkey = None
        
        # load save file for altkeybinds
        self.saveFile = {}
        self.saveFile['settings'] = {}
        
        with open('saveFile.json') as json_file:
            self.saveFile = json.load(json_file)

        # Set up sprites + Y position
        self.img_default = GameImage(self, f'images/arrows/GUI_Arrow{type}Default.png')
        self.img_default.position.y = 10 
        self.img_pressed = GameImage(self, f'images/arrows/GUI_Arrow{type}Pressed.png')
        self.img_pressed.position.y = 10 

        self.img_enemy = GameImage(self, f'images/arrows/GUI_Arrow{type}Default.png')
        self.img_enemy.position.y = 10
        
        # Determine position
        if self.type == 'Left':
            self.img_default.position.x = 144
            self.img_pressed.position.x = 144
            self.img_enemy.position.x = 17
            self.key = kb.K_LEFT
            self.altkey = self.saveFile['settings']['LeftKeybind']
        if self.type == 'Down':
            self.img_default.position.x = 165
            self.img_pressed.position.x = 165
            self.img_enemy.position.x = 38
            self.key = kb.K_DOWN
            self.altkey = self.saveFile['settings']['DownKeybind']
        if self.type == 'Up':
            self.img_default.position.x = 186
            self.img_pressed.position.x = 186 
            self.img_enemy.position.x = 59
            self.key = kb.K_UP
            self.altkey = self.saveFile['settings']['UpKeybind']
        if self.type == 'Right':
            self.img_default.position.x = 207
            self.img_pressed.position.x = 207
            self.img_enemy.position.x = 80
            self.key = kb.K_RIGHT
            self.altkey = self.saveFile['settings']['RightKeybind']
    
    def render(self):
        if self.isPressed == False:
            self.img_default.render() # Render default sprites if not pressed
        elif self.isPressed == True:
            self.img_pressed.render() # Render pressed sprites if pressed
        self.img_enemy.render()

    def on_key(self, isDown, key):
        # Key and altkeys determine if isPressed is true or not
        if isDown == True and key == self.key or isDown == True and key == self.altkey:
            self.isPressed = True
        elif isDown == False and key == self.key or isDown == False and key == self.altkey:
            self.isPressed = False