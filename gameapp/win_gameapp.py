
import pygame
import pygame.constants as k
from gameapp import Rect
from typing import List, Dict, Tuple
import time
import math

gblScale = 5.0

# class GameShape(GameImage):
#     def __init__(self, parent, type, left, top, right, bottom)
#         super().__init__(parent)
#         self.type = type

#         def render(self)
#         self.surf = pygame.display.get_surface()

#         if self.type == 'circle':
#             pygame.draw.circle(surf, (255,255,255), (self.position[0], self.position[1]), self.diameter)
#         elif self.type == 'rect'
#         pass
#     #circle, rect
#     pass

class GameImage():
    def __init__(self, parent = None, fileName = None, *, position = (0,0), anchor_point = (0,0), rotation = 0.0, scale = 1.0):
        self.parent = parent
        self.image = None
        self.fileName = fileName
        self.position = Rect(position[0], position[1], 0, 0)
        self.anchor_point = anchor_point
        self.rotation = rotation
        self.scale = scale
        # self.transformation = Transformation()


        if self.fileName and not self.image:
            self.load(self.fileName)
    
    def load(self, fileName):
            self.image = pygame.image.load(fileName)#.convert()
            # pygame.image.set_alpha(128)
            size = self.image.get_size()
            global gblScale
            newsize = (int(size[0] * gblScale), int(size[1] * gblScale))
            self.image = pygame.transform.scale(self.image, newsize)

    def render(self, position = None):
        if position:
            # if type(position) == Rect:
            #     self.position = position.copy()
            # else:
                self.position = Rect(position[0], position[1],0,0)


        global gblScale
        scaledposition = self.position.copy() #Rect(self.position.x, self.position.y)
        scaledposition.x *= gblScale        
        scaledposition.y *= gblScale

        # img = self.image
        img  = pygame.transform.rotozoom(self.image, self.rotation, self.scale) 
        # self.image = img

        pygame.display.get_surface().blit(img, (scaledposition.x-(img.get_size()[0]*self.anchor_point[0]), scaledposition.y-(img.get_size()[1]*self.anchor_point[1])))

    def rotoZoom(self, angle=0, scale=0):
        self.image = pygame.transform.rotozoom(self.image, angle, scale)

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
    def __init__(self, parent = None, name = 'Verdana', size = 20, isSys = True):
        self.parent = parent
        self.name = name
        self.size = size
        self.font = None
        self.isSys = isSys

        global gblScale

        if not self.font:
            if self.isSys:
                self.font = pygame.font.SysFont(self.name, int(self.size * gblScale))
            else:
                self.font = pygame.font.Font(self.name, int(self.size * gblScale))


class GameText(GameImage):
    def __init__(self, parent = None, font = None, text = '', position = (0,0), RGB = (0,0,0)):
        super().__init__(parent, fileName=None, position=position)
        self.font = font
        self.text = text
        self.color = pygame.Color(RGB[0],RGB[1],RGB[2])

    def renderText(self, text, position = None):
        self.text = str(text)
        self.render(position)

    def render(self, position = None):
        if position:
            # if type(position) == Rect:
            #     self.position = position.copy()
            # else:
                self.position = Rect(position[0], position[1],0,0)


        if self.text != '' and self.font:
            self.image = self.font.font.render(self.text, True, self.color)

            global gblScale
            scaledposition = Rect(self.position.x, self.position.y, 0,0)
            scaledposition.x *= gblScale
            scaledposition.y *= gblScale

            pygame.display.get_surface().blit(self.image, (scaledposition.x, scaledposition.y))

class GameAudio():
    def __init__(self, fileName = None, volume = 1):
        self.mySound:pygame.mixer.Sound = None 
        self.played = False
        if fileName:
            self.load(fileName)
            self.set_volume(volume)
    
    def load(self, fileName):
        if self.mySound:
            self.mySound.stop()
            
        self.mySound = pygame.mixer.Sound(fileName + '.ogg')

    def play(self, numRepeat = 0):
        if not self.played:
            self.mySound.play(loops = numRepeat)    
            self.played = True

    def stop(self):
        self.mySound.stop()
        self.played = False

    def set_volume(self, volume = 1):
        self.mySound.set_volume(volume)

class VirtualKey():
    def __init__(self, parent, label, key, colrow):
        self.parent = parent
        self.label = label
        self.key = key
        self.diameter = 20
        self.spacing = 2.5
        self.distance = (self.diameter*2) + (self.spacing * 2)

        if parent and colrow:
            xpos = self.diameter + self.spacing
            ypos  = self.parent.surface.get_height() - (self.distance * 3) + self.diameter + self.spacing
            self.position = Rect(xpos + (colrow[0]*self.distance), ypos + (colrow[1]*self.distance), 0, 0)
            self.text = GameText(self, GameFont(self, 'Calibri', 20), label, (self.position.x-10, self.position.y-10))
        
        

    def render(self):
        surf = pygame.display.get_surface()
        pygame.draw.circle(surf, (255,255,255), (self.position[0], self.position[1]), self.diameter)
        self.text.render()
        
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

        

class GameApp:
    def __init__(self, *, width=640, height=480, displayNumber = 0, scale = 1.0, hasVK = False, fps = 60):
        self.hasVK = hasVK
        self.platform = 'win'
        self.isRunning = True
        self.surface = None
        self.width = width
        self.height = height
        self.isFullScreen = False
        self.fps = fps
        # self.keysPressed = []
        self.pressedKeys = []
        self.curUserEventId = k.USEREVENT 


        self._milliseconds_since_start =  time.time() * 1000
        self._milliseconds_since_last_frame = 0.0

        self.currentSectionName:str = ''
        self.sections: Dict[str, GameSection] = {}
        self.virtualKeys: List[VirtualKey] = []
        # self.timersById: Dict[int, GameTimer] = {}
        self.timers: Dict[str, GameTimer] = {}
        # self.timers: List[GameTimer] = []



        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        vkspace = 0
        if hasVK:
            vk = VirtualKey(None, None, None, None)
            vkspace = vk.distance * 3

        global gblScale
        self.surface = pygame.display.set_mode((int(self.width * gblScale), int(self.height * gblScale + vkspace)), display=displayNumber)
        if self.isFullScreen == True:
            pygame.display.toggle_fullscreen()
      
    def getMS(self):
        return self._milliseconds_since_start

    def getLastFrameMS(self):
        return self._milliseconds_since_last_frame 

    def on_start(self):
        pass

    def on_event(self, eventId):
        pass
    
    def on_loop(self):
        if self.currentSectionName != '':
            self.sections[self.currentSectionName].on_loop()

    def on_render(self):
        if self.currentSectionName != '':
            self.sections[self.currentSectionName].on_render()

    def on_after_render(self):
        if self.currentSectionName != '':
            self.sections[self.currentSectionName].on_after_render()

    def on_key(self, isDown, key, mod):
        if self.currentSectionName != '':
            self.sections[self.currentSectionName].on_key(isDown, key, mod)


    def on_mouse(self, isDown, key, xcoord, ycoord):
        if self.currentSectionName != '':
            self.sections[self.currentSectionName].on_mouse(isDown, key, xcoord, ycoord)

    def on_timer(self, name):
        if self.currentSectionName != '':
            self.sections[self.currentSectionName].on_timer(name)



    def cleanup(self):
        pygame.quit()
 
    def addTimer(self, name, milliseconds:float, numRepeats:int=-1, delayMS=0.0):
        if name not in self.timers:
            self.curUserEventId += 1
            timer = GameTimer(self, name, self.curUserEventId, milliseconds, numRepeats, delayMS)
            timer.msAtStart = self.getMS()
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

        if self.hasVK:
            self.virtualKeys.append(VirtualKey(self, 'L', k.K_LEFT, (5,1)))
            self.virtualKeys.append(VirtualKey(self, 'R', k.K_RIGHT, (7,1)))
            self.virtualKeys.append(VirtualKey(self, 'U', k.K_UP, (6,0)))
            self.virtualKeys.append(VirtualKey(self, 'D', k.K_DOWN, (6,1)))
            self.virtualKeys.append(VirtualKey(self, 'R', k.K_r, (1,2)))
            self.virtualKeys.append(VirtualKey(self, 'ESC', k.K_ESCAPE, (1,0)))
            self.virtualKeys.append(VirtualKey(self, 'OK', k.K_RETURN, (9,2)))


        self.on_start()

        while( self.isRunning ):

            curTime = time.time() * 1000
            self._milliseconds_since_last_frame = curTime - self._milliseconds_since_start
            self._milliseconds_since_start =  curTime

            # self._milliseconds_since_last_frame = self.clock.get_time()
            # self._milliseconds_since_start += self._milliseconds_since_last_frame


            # self.keysPressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

                self.on_event(event.type)

                pos = pygame.mouse.get_pos()
                if event.type == k.KEYDOWN:
                    self.on_key(True, event.key, event.mod)
                    self.pressedKeys.append(event.key)
                if event.type == k.KEYUP:
                    self.on_key(False, event.key, event.mod)
                    self.pressedKeys.remove(event.key)

                if event.type in (k.MOUSEBUTTONDOWN, k.MOUSEBUTTONUP):
                    for vk in self.virtualKeys:
                        vk: VirtualKey 
                        if pos[0] > vk.position.x - vk.diameter and pos[0] < vk.position.x + vk.diameter and \
                           pos[1] > vk.position.y - vk.diameter and pos[1] < vk.position.y + vk.diameter:
                            self.on_key(event.type == k.MOUSEBUTTONDOWN, vk.key, None)
                            if event.type == k.MOUSEBUTTONDOWN:
                                self.pressedKeys.append(vk.key)
                            else:
                                self.pressedKeys.remove(vk.key)

                global gblScale
                if event.type in (k.MOUSEBUTTONDOWN, k.MOUSEBUTTONUP):
                    self.on_mouse(event.type == k.MOUSEBUTTONDOWN, event.button, pos[0] / gblScale, pos[1] / gblScale)


            for timer in self.timers.values():
                if timer.active and self._milliseconds_since_start > timer.getNextRunMS():
                    timer.numLoopsPerformed += 1
                    self.on_timer(timer.name)
                    #check if last loop
                    #if not infinite timer
                    if timer.numRepeats >= 0 and timer.numLoopsPerformed > timer.numRepeats:
                        timer.active = False


                    
            self.on_loop()
            self.on_render()

            #display virtual keys if we have any
            for vk in self.virtualKeys:
                vk.render()

            pygame.display.flip()

            self.on_after_render()

            self.clock.tick(self.fps)
 
    def quit(self):
        self.isRunning = False

    def fill(self, color= (0,0,0)):
        pygame.display.get_surface().fill(color)

if __name__ == "__main__" :
    
    GameApp().start()
