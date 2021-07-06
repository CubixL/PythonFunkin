# d:/VSCode/PythonFunkin
#
# Python Funkin'
# The game Friday Night Funkin', originally coded by ninjamuffin99, recreated with Pygame.
#
# Made by CubixL
# YouTube channel: https://www.youtube.com/channel/UCNNHpyTeYJqK9bfFeub3uNw

from gameapp import *
import os, sys, random, time, math, getopt


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
        self.img_pressed.scale2x()
        self.img_pressed.position.y = 10 * self.scale

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
    def __init__(self, type,):
        self.type = type
        self.scale = 2
        self.img = GameImage(f"images\\GUI_Arrow{type}Target.png") 
        self.img.scale2x() 
        self.img.position.y = 110 * self.scale
        

        if self.type == "Left":
            self.img.position.x = 80 * self.scale
        if self.type == "Down":
            self.img.position.x = 101 * self.scale
        if self.type == "Up":
            self.img.position.x = 123 * self.scale
        if self.type == "Right":
            self.img.position.x = 144 * self.scale
    
    def move(self):
        self.img.position.y -= 1 * self.scale
        if self.img.position.y <= 10 * self.scale:
            self.img.position.y = 110 * self.scale


    def render(self):
    # if self.parent.MilliTimer.currentTime >= self.milli:
        self.img.render()
    
class PythonFunkin(GameApp):
    def __init__(self):
        # misc
        super().__init__(480,240)
        self.fps = 66.666

        # assets
        self.Background = GameImage("images/testBG.gif", (0, 0))
        self.Background.scale2x()
        self.PlayerArrowL = PlayerArrow(type = "Left")
        self.PlayerArrowD = PlayerArrow(type = "Down")
        self.PlayerArrowU = PlayerArrow(type = "Up")
        self.PlayerArrowR = PlayerArrow(type = "Right")
        self.TargetList = []

        # font & text
        self.GUIFont = GameFont('fonts\\vcr.ttf', 12, False)
        self.MSText = GameText(self.GUIFont)



    def on_loop(self):
        for target in self.TargetList:
            target.move()
        

    def on_render(self):                    # Layering order:
        self.Background.render()            # 1. Background
        self.PlayerArrowL.render()          # 2. Player arrows
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        for target in self.TargetList:      # 3. Target arrows
            target.render()
        
        self.MSText.renderText(self.milliseconds_since_start)

    
    def on_event(self, eventId):
        pass

    def on_key(self, isDown, key, mod):
        if isDown == True and key == K_ESCAPE:
            self.isRunning = False
        self.PlayerArrowL.on_key(isDown, key)
        self.PlayerArrowD.on_key(isDown, key)
        self.PlayerArrowU.on_key(isDown, key)
        self.PlayerArrowR.on_key(isDown, key)
        if isDown == True and key == K_j:
            self.TargetList.append(TargetArrow(type = "Left"))
        if isDown == True and key == K_k:
            self.TargetList.append(TargetArrow(type = "Down"))
        if isDown == True and key == K_i:
            self.TargetList.append(TargetArrow(type = "Up"))
        if isDown == True and key == K_l:
            self.TargetList.append(TargetArrow(type = "Right"))

if __name__ == "__main__":
    PythonFunkin().start()
