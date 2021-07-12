import os
from .ios_pygame import Rect
from .ios_constants import *
import platform

if os.name == 'nt':
    from win_pythonista import run, Scene, SpriteNode, LabelNode, ShapeNode, Path, sound
else:
    from scene import run, Scene, SpriteNode, LabelNode, ShapeNode
    from ui import Path
    import sound
    
gblScale = 1
gblScene = None
renderImages = []



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
            global gblScale
           # print(f'glbS {gblScale}')
            
            global renderImages  
            #print(f'renderIm {renderImages}')

            self.image.anchor_point = (0,0)
            


    def render(self, position = None):
        global gblScale
        self.image.scale = gblScale
       # print('render')
        if position:
            if type(position) == Rect:
                self.position = position.copy()
            else:
                self.position.x = position[0]
                self.position.y = position[1]
        #screen_height = screen_size[1] 
        global gblScene
        #global gblScale
        screen_height = gblScene.size[1] 
        self.image.position = (self.position.x * gblScale, screen_height - (self.position.y * gblScale)  - (self.image.size[1] * self.image.scale))
        global renderImages

      #  print(f'renderIm {renderImages}')
        renderImages.append(self)
       
        

class GameFont():
    def __init__(self, parent, name = 'Helvetica', size = 20, isSys = True):
        self.parent = parent
        self.name = name
        self.size = size
        self.font = None
        self.isSys = isSys


class GameText():
    def __init__(self, parent, font, text = '', position = (0,0), RGB = (0,0,0)):
        self.parent = parent
        self.image = None
        self.position = Rect(position[0], position[1], 0, 0)      
        self.font = font
        self.text = text
        self.color = RGB

        if not self.image:
            self.image = LabelNode(self.text, font = (self.font.name, self.font.size*gblScale), position=(0,0))
            self.image.color = RGB
            #self.image.stroke_color = 'black'
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

        global gblScene
        self.image.position = (self.position.x * gblScale, gblScene.size[1] - (self.position.y * gblScale)  - (self.image.size[1]))
        self.image.text = str(self.text)
        #self.image.color = 'black'
        global renderImages
        renderImages.append(self)


class VirtualKey():
    def __init__(self, parent, label, key, colrow):
        self.parent = parent
        self.label = label
        self.key = key
        self.diameter = 50
        self.spacing = 5
        self.distance = (self.diameter) + (self.spacing)       


        if parent and colrow:
            xpos = self.diameter + self.spacing
            global gblScene
            ypos  = gblScene.size[1] - (self.distance * 3) + self.spacing
            self.position = Rect(xpos + (colrow[0]*self.distance), ypos + (colrow[1]*self.distance), 0, 0)

            self.circle =  ShapeNode(Path.oval(0,0, self.diameter, self.diameter))
            self.circle.position = (self.position.x, gblScene.size[1] - self.position.y)
            self.text = GameText(self, GameFont(self), label, (self.position.x,self.position.y-self.spacing), (0,0,0))
            self.text.image.anchor_point = (0.5,0)


    def render(self):
        global renderImages
        renderImages.append(self.text)
        

        
class MyScene(Scene):
    def setup(self):
        self.isShift = False
    def update(self):
        self.gameapp._milliseconds_since_start += 16.66666666666666666666
        global renderImages
      #  print(f'render im sc {renderImages}')

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
            vk.text.render()
            self.add_child(vk.circle)
            self.add_child(vk.text.image)
            

        self.gameapp.on_loop()

    def process_touch(self, touch, isDown):
        #print(f'touch  {touch.location} {isDown}')
        
        pos = touch.location
        for vk in self.gameapp.virtualKeys:
            vk: VirtualKey 
            if (pos[0] > vk.circle.position.x - vk.diameter/2) and (pos[0] < vk.circle.position.x + vk.diameter/2) and \
               (pos[1] > vk.circle.position.y - vk.diameter/2) and (pos[1] < vk.circle.position.y + vk.diameter/2):
                self.gameapp.on_key(isDown, vk.key, None)




        
    def touch_began(self, touch):
        self.process_touch(touch, True)

    def touch_ended(self, touch):
        self.process_touch(touch, False)
        
    def did_change_size(self):
        global gblScale
        gblScale = min(self.size[0] / 240, self.size[1] / 135)        

        

class GameAudio():
    def __init__(self):
        self.effect = None
        self.fileName = None
        
    def play(self, loop = 0):
    
        print(f'playing {self.fileName}')
        self.effect = sound.play_effect(self.fileName)
       
    def load(self, fileName):
        print(f'loading {fileName}')
        if self.effect:
            self.effect.stop()
        if fileName:

            fileName = str(f'{fileName}.caf').replace('\\', '/')
            self.fileName = fileName
        

    def unload(self):
        if self.effect:
           self.effect.stop()
    def pause(self):
        pass
    def unpause(self):
        pass
    def stop(self):
        if self.effect:
           self.effect.stop()
                    
        
class GameApp():
    def __init__(self, width=640, height=480, display=0):
        self.plat = 'ios'
        self.scene = MyScene()
        global gblScale

        # if os.name == 'nt':
        #     gblScale = 4.0

        # if platform.machine()[:6] == 'iPhone':
        gblScale = min(self.scene.size[0] / 240, self.scene.size[1] / 135)        
        
        self.isRunning = True
        self.surface = None
        self.width = width
        self.height = height
        self.isFullScreen = False
        self.fps = 5
        self.keysPressed = []
        self.curUserEventId = USEREVENT 
        self._milliseconds_since_start = 0.0

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
    
    def on_event(self, eventId):
        pass
        
    def on_loop(self):
        if self.currentSection:
            self.sections[self.currentSection].on_loop()
    def on_render(self):
        if self.currentSection:
            self.sections[self.currentSection].on_render()
    def on_key(self, isDown, key, mod):
        if self.currentSection:
            self.sections[self.currentSection].on_key(isDown, key, mod)
    def on_mouse(self, isDown, key, xcoord, ycoord):
        if self.currentSection:    
            self.sections[self.currentSection].on_mouse(isDown, key, xcoord, ycoord)


    def addTimer(self, mili, runOnce = False):
        pass
        # self.curUserEventId += 1
        # pygame.time.set_timer(self.curUserEventId, mili, runOnce)
        # return self.curUserEventId
    
    def start(self):
        
       
        self.on_start()
        global gblScene
        gblScene = self.scene
        
        self.virtualKeys.append(VirtualKey(self, 'L', K_LEFT, (2,1)))
        self.virtualKeys.append(VirtualKey(self, 'R', K_RIGHT, (4,1)))
        self.virtualKeys.append(VirtualKey(self, 'U', K_UP, (3,0)))
        self.virtualKeys.append(VirtualKey(self, 'D', K_DOWN, (3,1)))
        self.virtualKeys.append(VirtualKey(self, 'R', K_r, (0,2)))
        self.virtualKeys.append(VirtualKey(self, 'ESC', K_ESCAPE, (0,0)))
        self.virtualKeys.append(VirtualKey(self, 'OK', K_RETURN, (6,2)))    
        
     
        
        run(self.scene)
        
    def quit(self):
        self.scene.view.close()

 
if __name__ == "__main__" :
    print('start')
    app = GameApp()
    
   # app.image.render()
    GameApp().start()
