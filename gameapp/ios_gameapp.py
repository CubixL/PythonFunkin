import os
from .ios_pygame import Rect
from .ios_constants import *

if os.name == 'nt':
    from win_pythonista import run, Scene, SpriteNode, LabelNode
else:
    from scene import run, Scene, SpriteNode, LabelNode
    
screen_size = (1024,768)
renderImages = []

class GameImage():
    def __init__(self, parent, fileName = None, position = (0,0)):
        self.parent = parent
        if fileName:
           fileName = fileName.replace('\\', '/')
        self.image = None
        self.fileName = fileName
        self.position = Rect(position[0], position[1], 0, 0)
        self.scale = parent.scale

        if self.fileName and not self.image:
            self.image = SpriteNode(self.fileName)
            self.image.scale = parent.scale
            self.image.anchor_point = (0,0)
            

    def render(self, position = None):
        if position:
            if type(position) == Rect:
                self.position = position.copy()
            else:
                self.position.x = position[0]
                self.position.y = position[1]

        self.image.position = (self.position.x * self.scale, screen_size[1] - (self.position.y * self.scale)  - (self.image.size[1] * self.image.scale))
        renderImages.append(self)
       
        

class GameFont():
    def __init__(self, parent, name = 'Helvetica', size = 20, isSys = True):
        self.parent = parent
        self.scale = parent.scale
        self.name = name
        self.size = size
        self.font = None
        self.isSys = isSys


class GameText():
    def __init__(self, parent, font, text = '', position = (0,0), RGB = (0,0,0)):
        self.parent = parent
        self.scale = parent.scale
        self.image = None
        self.position = Rect(position[0], position[1], 0, 0)      
        self.font = font
        self.text = text
        self.color = RGB

        if not self.image:
            self.image = LabelNode(self.text, font = (self.font.name, self.font.size*self.scale), position=(0,0))
            self.image.anchor_point = (0,0)

    def renderText(self, text, position = None):
        self.text = str(text)
        self.render(position)

    def render(self, position = None):
        if position:
            if type(position) == Rect:
                self.position = position.copy()
            else:
                self.position.x  = position[0]
                self.position.y  = position[1]


        self.image.position = (self.position.x * self.scale, screen_size[1] - (self.position.y * self.scale)  - (self.image.size[1]))
        self.image.text = str(self.text)
        renderImages.append(self)
        
        
class MyScene(Scene):
    def setup(self):
        self.isShift = False
    def update(self):
        self.gameapp.milliseconds_since_start += 16.66666666666666666666
        screen_size = self.size
        for image in renderImages:
            image.image.remove_from_parent()

        renderImages.clear()
        self.gameapp.on_render()
        for image in renderImages:
            self.add_child(image.image)

        self.gameapp.on_loop()

    def process_touch(self, touch, isDown):
        
        x = touch.location[0]
        y = touch.location[1]
        
        if y < 200 and x < 350:
            self.isShift = isDown
            
        print(f'touch  {touch.location} {isDown} {self.isShift}')

        if self.isShift:            
            if x < 350 and y > 200 and y < 568:
                self.gameapp.on_key(isDown, K_j, None)
            if x > 674 and y > 200 and y < 568:
                self.gameapp.on_key(isDown, K_l, None)
            if y < 200 and x > 350 and x < 674:
                self.gameapp.on_key(isDown, K_k, None)
            if y > 568 and x > 350 and x < 674:
                self.gameapp.on_key(isDown, K_i, None)
        else:
            if x < 350 and y > 200 and y < 568:
                self.gameapp.on_key(isDown, K_LEFT, None)
            if x > 674 and y > 200 and y < 568:
                self.gameapp.on_key(isDown, K_RIGHT, None)
            if y < 200 and x > 350 and x < 674:
                self.gameapp.on_key(isDown, K_DOWN, None)
            if y > 568 and x > 350 and x < 674:
                self.gameapp.on_key(isDown, K_UP, None)

        
    def touch_began(self, touch):
        self.process_touch(touch, True)
            
            
            
    def touch_ended(self, touch):
        self.process_touch(touch, False)
            
        
class GameApp():
    def __init__(self, width=640, height=480, scale=1.0):
        self.scale = scale
        self.isRunning = True
        self.surface = None
        self.width = width
        self.height = height
        self.isFullScreen = False
        self.fps = 5
        self.keysPressed = []
        self.curUserEventId = USEREVENT 
        self.milliseconds_since_start = 0.0
        self.scene = MyScene()
        self.scene.gameapp = self


        # self.clock = pygame.time.Clock()
        # self.surface = pygame.display.set_mode((self.width, self.height))
        # if self.isFullScreen == True:
        #     pygame.display.toggle_fullscreen()
      
 


    def on_start(self):
        pass
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_event(self, eventId):
        pass
    def on_key(self, isDown, key, mod):
        pass


    def addTimer(self, mili, runOnce = False):
        pass
        # self.curUserEventId += 1
        # pygame.time.set_timer(self.curUserEventId, mili, runOnce)
        # return self.curUserEventId
    
    def start(self):
        gblgameapp = self
        self.on_start()
        run(self.scene)

 
if __name__ == "__main__" :
    print('start')
    app = GameApp()
    
   # app.image.render()
    GameApp().start()
