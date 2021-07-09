import os
from .ios_pygame import Rect
from .ios_constants import *

if os.name == 'nt':
    from win_pythonista import run, Scene, SpriteNode, LabelNode, ShapeNode, Path
else:
    from scene import run, Scene, SpriteNode, LabelNode, ShapeNode
    from ui import Path
    
screen_size = (1024,768)
renderImages = []

def convertY(y):
    return screen_size[1] - y

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


class VirtualKey():
    def __init__(self, parent, label, key, colrow):
        self.parent = parent
        self.scale = 1
        self.label = label
        self.key = key
        self.diameter = 50
        self.spacing = 5
        self.distance = (self.diameter*2) + (self.spacing * 2)       


        if parent and colrow:
            xpos = self.diameter + self.spacing
            ypos  = (self.distance * 3) + self.diameter + self.spacing
            self.position = Rect(xpos + (colrow[0]*self.distance), ypos + (colrow[1]*self.distance), 0, 0)

            self.circle =  ShapeNode(Path.oval(self.position[0], self.position[1], self.diameter, self.diameter))
            self.circle.position = (self.position.x, screen_size[1] - self.position.y + self.diameter)
            self.text = GameText(self, GameFont(self), label, self.position)



    def render(self):
        renderImages.append(self)

        
class MyScene(Scene):
    def setup(self):
        self.isShift = False
    def update(self):
        self.gameapp._milliseconds_since_start += 16.66666666666666666666
        screen_size = self.size
        for image in renderImages:
            image.image.remove_from_parent()
        for vk in self.gameapp.virtualKeys:
            vk.text.image.remove_from_parent()   
            vk.circle.remove_from_parent()     
            
            

        renderImages.clear()
        self.gameapp.on_render()
        for image in renderImages:
            self.add_child(image.image)
            
        for vk in self.gameapp.virtualKeys:
            self.add_child(vk.text.image)
            self.add_child(vk.circle)
            

        self.gameapp.on_loop()

    def process_touch(self, touch, isDown):
        print(f'touch  {touch.location} {isDown}')
        
        pos = touch.location
        for vk in self.gameapp.virtualKeys:
            vk: VirtualKey 
            if (pos[0] > vk.position.x - vk.diameter) and (pos[0] < vk.position.x + vk.diameter) and \
               (pos[1] > vk.position.y - vk.diameter) and (pos[1] < vk.position.y + vk.diameter):
                self.gameapp.on_key(isDown, vk.key, None)


        # x = touch.location[0]
        # y = touch.location[1]

        # if y < 200 and x < 350:
        #     self.isShift = isDown
            

        # if self.isShift:            
        #     if x < 350 and y > 200 and y < 568:
        #         self.gameapp.on_key(isDown, K_j, None)
        #     if x > 674 and y > 200 and y < 568:
        #         self.gameapp.on_key(isDown, K_l, None)
        #     if y < 200 and x > 350 and x < 674:
        #         self.gameapp.on_key(isDown, K_k, None)
        #     if y > 568 and x > 350 and x < 674:
        #         self.gameapp.on_key(isDown, K_r, None)
        # else:
        #     if x < 350 and y > 200 and y < 568:
        #         self.gameapp.on_key(isDown, K_LEFT, None)
        #     if x > 674 and y > 200 and y < 568:
        #         self.gameapp.on_key(isDown, K_RIGHT, None)
        #     if y < 200 and x > 350 and x < 674:
        #         self.gameapp.on_key(isDown, K_DOWN, None)
        #     if y > 568 and x > 350 and x < 674:
        #         self.gameapp.on_key(isDown, K_UP, None)

        
    def touch_began(self, touch):
        self.process_touch(touch, True)

    def touch_ended(self, touch):
        self.process_touch(touch, False)


        

class GameAudio():
    def __init__(self, fileName = None):
       pass
    def play(self, loop = 0):
       pass
    def load(self, fileName):
       pass
    def unload(self):
       pass
    def pause(self):
       pass
    def unpause(self):
       pass
    def stop(self):
       pass
                    
        
class GameApp():
    def __init__(self, width=640, height=480, display=0, scale=1.0):
        self.platform = 'ios'
        self.scale = scale
        self.isRunning = True
        self.surface = None
        self.width = width
        self.height = height
        self.isFullScreen = False
        self.fps = 5
        self.keysPressed = []
        self.curUserEventId = USEREVENT 
        self._milliseconds_since_start = 0.0
        self.scene = MyScene()
        self.scene.gameapp = self
        self.virtualKeys = []


        # self.clock = pygame.time.Clock()
        # self.surface = pygame.display.set_mode((self.width, self.height))
        # if self.isFullScreen == True:
        #     pygame.display.toggle_fullscreen()
      
 
    def getMillisecondsSinceStart(self):
        return self._milliseconds_since_start

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
        
        self.virtualKeys.append(VirtualKey(self, 'L', K_LEFT, (5,1)))
        self.virtualKeys.append(VirtualKey(self, 'R', K_RIGHT, (7,1)))
        self.virtualKeys.append(VirtualKey(self, 'U', K_UP, (6,0)))
        self.virtualKeys.append(VirtualKey(self, 'D', K_DOWN, (6,1)))
        self.virtualKeys.append(VirtualKey(self, 'R', K_r, (1,2)))
        self.virtualKeys.append(VirtualKey(self, 'ESC', K_ESCAPE, (1,0)))
        self.virtualKeys.append(VirtualKey(self, 'OK', K_RETURN, (9,2)))    

        self.on_start()
        run(self.scene)

 
if __name__ == "__main__" :
    print('start')
    app = GameApp()
    
   # app.image.render()
    GameApp().start()
