import pygame
from pygame import Rect
from pygame.locals import *
import typing


class GameImage():
    def __init__(self, parent, fileName = None, position = (0,0)):
        self.parent = parent
        self.image = None
        self.fileName = fileName
        self.position = Rect(position[0], position[1], 0, 0)
        self.scale = parent.scale

        if self.fileName and not self.image:
            self.image = pygame.image.load(self.fileName)#.convert()
            # pygame.image.set_alpha(128)
            size = self.image.get_size()
            newsize = (int(size[0] * self.scale), int(size[1] * self.scale))
            self.image = pygame.transform.scale(self.image, newsize)

    def render(self, position = None):
        if position:
            if type(position) == Rect:
                self.position = position.copy()
            else:
                self.position.x = position[0]
                self.position.y = position[1]


        scaledposition = self.position.copy()
        scaledposition.x *= self.scale
        scaledposition.y *= self.scale
        pygame.display.get_surface().blit(self.image, scaledposition)

        

class GameFont():
    def __init__(self, parent, name = 'Verdana', size = 20, isSys = True):
        self.parent = parent
        self.scale = parent.scale
        self.name = name
        self.size = size
        self.font = None
        self.isSys = isSys

        if not self.font:
            if self.isSys:
                self.font = pygame.font.SysFont(self.name, int(self.size * self.scale))
            else:
                self.font = pygame.font.Font(self.name, int(self.size * self.scale))


class GameText(GameImage):
    def __init__(self, parent, font, text = '', position = (0,0), RGB = (0,0,0)):
        super().__init__(parent, fileName=None, position=position)
        self.font = font
        self.text = text
        self.scale = parent.scale
        self.color = pygame.Color(RGB[0],RGB[1],RGB[2])

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


        if self.text != '':
            self.image = self.font.font.render(self.text, True, self.color)

            scaledposition = self.position.copy()
            scaledposition.x *= self.scale
            scaledposition.y *= self.scale

            pygame.display.get_surface().blit(self.image, scaledposition)

class GameAudio():
    def __init__(self):
        self.mySound = None 
    
    def load(self, fileName):
        if self.mySound:
            self.mySound.stop()
            
        self.mySound = pygame.mixer.Sound(fileName)

    def play(self, numRepeat = 0):
        self.mySound.play(loops = numRepeat)     
    def stop(self):
        self.mySound.stop()
    def set_volume(self, volume = 1):
        self.mySound.set_volume(volume)


class VirtualKey():
    def __init__(self, parent, label, key, colrow):
        self.parent = parent
        self.scale = 1
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
        
        
class GameApp:
    def __init__(self, width=640, height=480, displayNumber = 0, scale = 1.0, hasVK = False):
        self.hasVK = hasVK
        self.platform = 'win'
        self.scale = scale
        self.isRunning = True
        self.surface = None
        self.width = width
        self.height = height
        self.isFullScreen = False
        self.fps = 5
        self.keysPressed = []
        self.curUserEventId = USEREVENT 
        self.clock = None
        self._milliseconds_since_start = 0.0

        self.virtualKeys = []


        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        vkspace = 0
        if hasVK:
            vk = VirtualKey(None, None, None, None)
            vkspace = vk.distance * 3

        self.surface = pygame.display.set_mode((int(self.width * self.scale), int(self.height * self.scale + vkspace)), display=displayNumber)
        if self.isFullScreen == True:
            pygame.display.toggle_fullscreen()
      
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


    def cleanup(self):
        pygame.quit()
 
    def addTimer(self, mili, runOnce = False):
        self.curUserEventId += 1
        pygame.time.set_timer(self.curUserEventId, mili, runOnce)
        return self.curUserEventId
    
    def start(self):

        if self.hasVK:
            self.virtualKeys.append(VirtualKey(self, 'L', K_LEFT, (5,1)))
            self.virtualKeys.append(VirtualKey(self, 'R', K_RIGHT, (7,1)))
            self.virtualKeys.append(VirtualKey(self, 'U', K_UP, (6,0)))
            self.virtualKeys.append(VirtualKey(self, 'D', K_DOWN, (6,1)))
            self.virtualKeys.append(VirtualKey(self, 'R', K_r, (1,2)))
            self.virtualKeys.append(VirtualKey(self, 'ESC', K_ESCAPE, (1,0)))
            self.virtualKeys.append(VirtualKey(self, 'OK', K_RETURN, (9,2)))


        self.on_start()

        while( self.isRunning ):
            self.keysPressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

                self.on_event(event.type)

                if event.type == KEYDOWN:
                    self.on_key(True, event.key, event.mod)
                if event.type == KEYUP:
                    self.on_key(False, event.key, event.mod)
                if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    for vk in self.virtualKeys:
                        vk: VirtualKey 
                        if pos[0] > vk.position.x - vk.diameter and pos[0] < vk.position.x + vk.diameter and \
                           pos[1] > vk.position.y - vk.diameter and pos[1] < vk.position.y + vk.diameter:
                            self.on_key(event.type == MOUSEBUTTONDOWN, vk.key, None)

            self.on_loop()
            self.on_render()

            #display virtual keys if we have any
            for vk in self.virtualKeys:
                vk.render()

            pygame.display.update()
            self._milliseconds_since_start += self.clock.get_time()
            self.clock.tick(self.fps)
 
    def quit(self):
        self.isRunning = False

if __name__ == "__main__" :
    
    GameApp().start()
