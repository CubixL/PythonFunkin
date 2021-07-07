import pygame
from pygame import Rect
from pygame.locals import *
from pygame.transform import scale


class GameImage():
    def __init__(self, parent, fileName = None, position = (0,0)):
        self.parent = parent
        self.image = None
        self.fileName = fileName
        self.position = Rect(position[0], position[1], 0, 0)
        self.scale = parent.scale
        self.load()

    def load(self):
        if self.fileName and not self.image:
            self.image = pygame.image.load(self.fileName).convert()
            size = self.image.get_size()
            newsize = (int(size[0] * self.scale), int(size[1] * self.scale))
            self.image = pygame.transform.scale(self.image, newsize)

    def render(self, position = None):
        # self.load()

        if position != None:
            if type(position) == Rect:
                self.position = position.copy()
            else:
                self.position.x = position[0]
                self.position.y = position[1]


        scaledposition = self.position.copy()
        scaledposition.x *= self.scale
        scaledposition.y *= self.scale
        pygame.display.get_surface().blit(self.image, scaledposition)

    def scale2x(self):
        self.image = pygame.transform.scale2x(self.image)
        

class GameFont():
    def __init__(self, parent, name, size, isSys = True):
        self.parent = parent
        self.scale = parent.scale
        self.name = name
        self.size = size
        self.font = None
        self.isSys = isSys
        self.load()

    def load(self):
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
        # self.font.load()

        if position != None:
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

class GameApp:
    def __init__(self, width=640, height=480, displayNumber = 0, scale = 1.0):
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
        self._milliseconds_since_start = 0
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((int(self.width * self.scale), int(self.height * self.scale)), display=displayNumber)
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
                


            self.on_loop()
            self.on_render()

            pygame.display.update()
            self._milliseconds_since_start += self.clock.get_time()
            self.clock.tick(self.fps)
 

if __name__ == "__main__" :
    
    GameApp().start()
