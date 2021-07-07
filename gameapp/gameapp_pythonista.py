import os

from .ios_constants import *
from .ios_pygame import pygame

if os.name == 'nt':
    from win_pythonista import Path, run, Scene, SpriteNode, LabelNode, ShapeNode

else:
    from scene import SpriteNode, Scene, run, LabelNode, ShapeNode
    from ui import Path
    
from .ios_pygame import Rect

screen_size = (1024,768)
renderImages = []
gblgameapp = None

class GameImage():
    def __init__(self, parent, fileName = None, position = (0,0)):
        self.parent = parent
        if fileName:
           fileName = fileName.replace('\\', '/')
        self.image = None
        self.fileName = fileName
        self.position = Rect(position[0], position[1], 0, 0)

        if self.fileName and not self.image:
            self.image = SpriteNode(self.fileName)
            self.image.anchor_point = (0,0)
            

    def render(self, position = None):
        if position:
            self.position.x = position[0]
            self.position.y = position[1]

        self.image.position = (self.position.x, screen_size[1] - self.position.y  - (self.image.size[1] * self.image.scale))
        renderImages.append(self)
       


        

class GameFont():
    def __init__(self, name = 'Helvetica', size = 20, isSys = True):
        self.name = 'Helvetica'#name
        self.size = size
        self.font = None
        self.isSys = isSys

        


class GameText():
    def __init__(self, font, text = '', position = (0,0), RGB = (0,0,0)):
        self.position = Rect(position[0], position[1], 0, 0)      
        self.font = font
        self.text = text
        self.color = RGB

        self.image = LabelNode(self.text, position=(0,0))
        self.image.anchor_point = (0,0)

            
    def renderText(self, text, position = None):
        self.text = str(text)
        self.render(position)

    def render(self, position = None):
        if position:
            self.position.x = position[0]
            self.position.y = position[1]

        self.image.position = (self.position.x, screen_size[1] - self.position.y  - self.image.size[1])
        self.image.text = str(self.text)
        renderImages.append(self)

class VirtualKey():
    def __init__(self, parent, label, key, position):
        
        self.parent = parent
        self.label = label
        self.key = key
        self.position = position
        self.circle =  ShapeNode(Path.oval(position[0], position[1], 50, 50))
        self.text = GameText(parent.defaultFont, label, position)



    def render(self):
        self.circle.position = (self.position.x, screen_size[1] - self.position.y  - (self.image.size[1] * self.image.scale))
        renderImages.append(self)


    def render(self):
        surf = pygame.display.get_surface()
        pygame.draw.circle(surf, (255,255,255), self.position, 20)
        self.text.render()        
        
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
    def __init__(self, width=640, height=480):
        gblgameapp = self
        
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
        self.virtualKeys = []


        # pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.width, self.height))
        if self.isFullScreen == True:
            pygame.display.toggle_fullscreen()
      
        self.defaultFont = GameFont('Helvetica', 20) 



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


    def cleanup(self):
        pygame.quit()
 
    def addTimer(self, mili, runOnce = False):
        self.curUserEventId += 1
        pygame.time.set_timer(self.curUserEventId, mili, runOnce)
        return self.curUserEventId
    
    def start(self):
        gblgameapp = self

        self.virtualKeys.append(VirtualKey(self, 'L', K_LEFT, (300,200)))
        self.virtualKeys.append(VirtualKey(self, 'R', K_RIGHT, (400,200)))
        self.virtualKeys.append(VirtualKey(self, 'U', K_UP, (350,150)))
        self.virtualKeys.append(VirtualKey(self, 'D', K_DOWN, (350,200)))


        self.on_start()

        
        run(self.scene)


        # while( self.isRunning ):
        #     print('loop')
        #     self.keysPressed = pygame.key.get_pressed()
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.isRunning = False

        #         self.on_event(event.type)

        #         if event.type == KEYDOWN:
        #             self.on_key(True, event.key, event.mod)
        #         if event.type == KEYUP:
        #             self.on_key(False, event.key, event.mod)
                


        #     self.on_loop()
        #     self.on_render()

        #     pygame.display.update()
        #     self.milliseconds_since_start += self.clock.get_time()
        #     self.clock.tick(self.fps)
 

if __name__ == "__main__" :
    print('start')
    app = GameApp()
    
   # app.image.render()
    GameApp().start()
