# type: ignore
import os, time
from gameapp.rect import Rect, Point
import gameapp.ios_constants as kb
import platform
import math
from typing import Optional

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
    def __init__(self, parent, fileName = None, *, position = (0,0), anchor_point = (0,0), rotation = 0.0, scale = 1.0):
        self.parent = parent
        if fileName:
           fileName = fileName.replace('\\', '/')
        self.image:SpriteNode
        self.fileName = fileName
        self.position = Point(position[0], position[1])
        self.anchor_point = anchor_point
        self.rotation = rotation
        self.scale = scale
        # self.rect = Rect(position[0], position[1], 0, 0)
        

        if self.fileName and not self.image:
            self.load(self.fileName)

    def load(self, fileName):
            self.image = SpriteNode(self.fileName)
            # global gblScale
            # global renderImages  
            self.image.anchor_point = self.anchor_point
            


    def render(self, position = None):
        global gblScale
        self.image.scale = self.scale * gblScale
       # print('render')
        if position:
            if type(position) == Point:
                self.position = Point(position.x, position.y)
            else:
                self.position.moveTo(position[0], position[1])

        #screen_height = screen_size[1] 
        global gblScene
        screen_height = gblScene.size[1] 
        self.image.position = (self.position.x * gblScale, screen_height - (self.position.y * gblScale)  - (self.image.size[1] * self.image.scale))
        self.image.rotation = self.rotation
        global renderImages
      #  print(f'renderIm {renderImages}')
        renderImages.append(self)
       
    def rotoZoom(self, angle=0, scale=0):
        pass
        # self.image = pygame.transform.rotozoom(self.image, angle, scale)

    def moveAngle(self, dist, angle):
        ang = math.radians(angle)
        dx = dist * math.cos(ang)
        dy = dist * math.sin(ang)

        self.position.x += dx
        self.position.y -= dy

    def moveTo(self, dist, position):
        dx = (position[0] - self.position.x)
        dy = -(position[1] - self.position.y)
        
        ang = math.degrees(math.atan(dy/dx))

        if dx < 0:
            ang += 180

        self.moveAngle(dist, ang)


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
        self.position = Point(position[0], position[1])
        self.font = font
        self.text = text
        self.color = RGB

        if not self.image:
            self.image = LabelNode(self.text, font = (self.font.name, self.font.size*gblScale), position=(0,0))
            #self.image.color =  RGB
            self.image.color = (RGB[0]/255, RGB[1]/255, RGB[2]/255)
            self.image.anchor_point = (0,0)

    def renderText(self, text, position = None):
        self.text = str(text)
        self.render(position)

    def render(self, position = None):
        if position:
            # if type(position) == Rect:
            #     self.position = position.copy()
            # else:
                self.position = Point(position[0], position[1])

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
        self.colrow = colrow  

        global gblScale


        xpos = self.diameter + self.spacing
        global gblScene
        ypos  = gblScene.size[1] - (self.distance * 3) + self.spacing
        
        self.position = Rect(xpos + (colrow[0]*self.distance), ypos + (colrow[1]*self.distance), 0, 0)

        self.circle =  ShapeNode(Path.oval(0,0, self.diameter, self.diameter))
        self.circle.position = (self.position.x, gblScene.size[1] - self.position.y)
        

        self.text = GameText(self, GameFont(self, size=10), label)
        
        self.text.image.anchor_point = (0.5,0)

  

    def setPos(self):
        global  gblScale

        xpos = self.diameter + self.spacing
        global gblScene
        ypos  = gblScene.size[1] - (self.distance * 3) + self.spacing
        
        self.position = Point(xpos + (self.colrow[0]*self.distance), ypos + (self.colrow[1]*self.distance))

        self.circle =  ShapeNode(Path.oval(0,0, self.diameter, self.diameter))
        self.circle.position = (self.position.x, gblScene.size[1] - self.position.y)
        
            
        self.text.position.x = self.position.x/gblScale
        self.text.position.y = (self.position.y-self.spacing)/gblScale       

        
class MyScene(Scene):
    def setup(self):
        self.isShift = False
    def update(self):
        for timer in self.gameapp.timers.values():
            if timer.active and self.gameapp._milliseconds_since_start > timer.getNextRunMS():
                timer.numLoopsPerformed += 1
                self.gameapp.on_timer(timer.name)
                #check if last loop
                #if not infinite timer
                if timer.numRepeats >= 0 and timer.numLoopsPerformed > timer.numRepeats:
                    timer.active = False



        curTime = time.time() * 1000
        self.gameapp._milliseconds_since_last_frame = curTime - self.gameapp._milliseconds_since_start
        self.gameapp._milliseconds_since_start =  curTime
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
            vk.setPos()
            vk.text.render()
            self.add_child(vk.circle)
            self.add_child(vk.text.image)
            
        self.gameapp.on_after_render()
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
        gblScale = min(self.size[0] / self.gameapp.width, self.size[1] / self.gameapp.height)        

        

class GameAudio():
    def __init__(self, fileName = None, volume = 1):
        self.effect = None
        self.fileName = None
        self.played = False
        
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

    def set_volume(self, volume = 1):
        self.effect.volume = volume

class GameSection:
    def __init__(self):
        pass

    def on_start(self):
        pass

    def on_event(self, eventId):
        pass
    
    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_after_render(self):
        pass

    def on_key(self, isDown, key, mod):
        pass

    def on_mouse(self, isDown, key, xcoord, ycoord):
        pass

    def on_timer(self, name):
        pass


class GameTimer():
    def __init__(self, parent, name:str, id:int, milliseconds:float, numRepeats:int, delayMS:float=0.0):
        self.active: bool = True
        self.parent = parent
        self.name:str = name
        self.id:int = id
        self.milliseconds:float = milliseconds
        self.numRepeats:int = numRepeats
        self.msAtStart:float = 0.0
        self.numLoopsPerformed:int = 0
        self.delayMS:float = delayMS

    def getNextRunMS(self):
        return self.msAtStart + self.delayMS + ((self.numLoopsPerformed + 1) * self.milliseconds)

class GameApp():
    def __init__(self, width=640, height=480, displayNumber=0):
        self.platform = 'ios'
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
        self.curUserEventId = kb.USEREVENT 
        self._milliseconds_since_start = 0.0
        self._milliseconds_since_last_frame = 0.0

        self.scene.gameapp = self
        self.virtualKeys = []

        self.currentSectionName = ''
        self.sections: Dict[str, GameSection] = {}
        self.virtualKeys: List[VirtualKey] = []
        self.timers: Dict[str, GameTimer] = {}

 
    def getMS(self):
        return self._milliseconds_since_start

    def getLastFrameMS(self):
        return self._milliseconds_since_last_frame         

    def on_start(self):
        pass
    
    def on_event(self, eventId):
        pass
        
    def on_loop(self):
        if self.currentSectionName:
            self.sections[self.currentSectionName].on_loop()
    def on_render(self):
        if self.currentSectionName:
            self.sections[self.currentSectionName].on_render()

    def on_after_render(self):
        if self.currentSectionName:
            self.sections[self.currentSectionName].on_after_render()

    def on_key(self, isDown, key, mod):
        if self.currentSectionName:
            self.sections[self.currentSectionName].on_key(isDown, key, mod)
    def on_mouse(self, isDown, key, xcoord, ycoord):
        if self.currentSectionName:    
            self.sections[self.currentSectionName].on_mouse(isDown, key, xcoord, ycoord)

    def on_timer(self, name):
        if self.currentSectionName:    
            self.sections[self.currentSectionName].on_timer(name)

    def addTimer(self, name, milliseconds:float, numRepeats:int=-1, delayMS=0.0):
        if name not in self.timers:
            self.curUserEventId += 1
            timer = GameTimer(self, name, self.curUserEventId, milliseconds, numRepeats, delayMS)
            timer.msAtStart = self.getMS()
            # self.timers.append(timer)
            self.timers[name]  = timer
        else:
            timer = self.timers[name]
            timer.msAtStart = self.getMS()
            timer.milliseconds = milliseconds
            timer.numRepeats = numRepeats
            timer.numLoopsPerformed = 0
            timer.active = True

    def stopTimer(self, name):
        self.timers[name].active = False

    def start(self):
        
       
        self.on_start()
        global gblScene
        gblScene = self.scene
        
        self.virtualKeys.append(VirtualKey(self, 'L', kb.K_LEFT, (2,1)))
        self.virtualKeys.append(VirtualKey(self, 'R', kb.K_RIGHT, (4,1)))
        self.virtualKeys.append(VirtualKey(self, 'U', kb.K_UP, (3,0)))
        self.virtualKeys.append(VirtualKey(self, 'D', kb.K_DOWN, (3,1)))
        self.virtualKeys.append(VirtualKey(self, 'R', kb.K_r, (0,2)))
        self.virtualKeys.append(VirtualKey(self, 'ESC', kb.K_ESCAPE, (0,0)))
        self.virtualKeys.append(VirtualKey(self, 'OK', kb.K_RETURN, (6,2)))    
        
     
        
        run(self.scene)
        
    def quit(self):
        self.scene.view.close()

 
if __name__ == "__main__" :
    print('start')
    app = GameApp()
    
   # app.image.render()
    GameApp().start()
