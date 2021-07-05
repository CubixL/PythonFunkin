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
        self.xpos = 25
        self.ypos = 10
        self.key = None

        if self.type == "Left":
            self.xpos = 80
            self.key = K_a
        if self.type == "Down":
            self.xpos = 101
            self.key = K_s
        if self.type == "Up":
            self.xpos = 123
            self.key = K_w
        if self.type == "Right":
            self.xpos = 144
            self.key = K_d

        self.img_default = GameImage(f"images\\GUI_Arrow{type}Default.png", (self.xpos*2, self.ypos*2))
        self.img_default.scale2x() 
        self.img_pressed = GameImage(f"images\\GUI_Arrow{type}Pressed.png", (self.xpos*2, self.ypos*2))
        self.img_pressed.scale2x()
    
    def render(self):
        if self.isPressed == False:
            self.img_default.render()
        elif self.isPressed == True:
            self.img_pressed.render() 

    def on_key(self, isDown, key):
        if isDown == True and key == self.key:
            self.isPressed = True
        elif isDown == False and key == self.key:
            self.isPressed = False

class TargetArrow():
    def __init__(self, type):
        self.type = type
        self.xpos = 25
        self.ypos = 110

        if self.type == "Left":
            self.xpos = 80
        if self.type == "Down":
            self.xpos = 101
        if self.type == "Up":
            self.xpos = 123
        if self.type == "Right":
            self.xpos = 144
    
        self.img = GameImage(f"images\\GUI_Arrow{type}Target.png", (self.xpos*2, self.ypos*2))
        self.img.scale2x() 
    
    def move(self):
        self.ypos -= 1
        if self.ypos <= 10
    def render(self):
        self.img.render()
    
class PythonFunkin(GameApp):
    def __init__(self):
        super().__init__(480,240)
        self.fps = 66.666

        self.Background = GameImage("images\\BGE_Week6BackgroundScaled.png", (0, 0))
        self.Background.scale2x()
        self.PlayerArrowL = PlayerArrow(type = "Left")
        self.PlayerArrowD = PlayerArrow(type = "Down")
        self.PlayerArrowU = PlayerArrow(type = "Up")
        self.PlayerArrowR = PlayerArrow(type = "Right")
        self.TargetDummy = TargetArrow(type = "Left")

    def on_loop(self):
        # self.TargetDummy.move()
        pass

    def on_render(self):
        self.Background.render()
        self.PlayerArrowL.render()
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        self.TargetDummy.render()
    
    def on_event(self, eventId):
        pass

    def on_key(self, isDown, key, mod):
        if isDown == True and key == K_ESCAPE:
            self.isRunning = False
        self.PlayerArrowL.on_key(isDown, key)
        self.PlayerArrowD.on_key(isDown, key)
        self.PlayerArrowU.on_key(isDown, key)
        self.PlayerArrowR.on_key(isDown, key)

if __name__ == "__main__":
    PythonFunkin().start()