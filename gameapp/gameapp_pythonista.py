import os
from rect import Rect
from constants import *
from pygamew import pygame

if os.name == 'nt':
    from scenew import run, Scene, SpriteNode
else:
    from scene import *

allImages = []
renderImages = []

class GameImage():
    def __init__(self, fileName = None, position = (0,0)):
        self.image = None
        self.fileName = fileName
        self.position = Rect(position[0], position[1], 0, 0)
        self.load()

    def load(self):
        if self.fileName and not self.image:
            self.image = SpriteNode(self.fileName, (self.position.x, self.position.y))
            allImages.append(self)
            

    def render(self, position = None):
        # self.load()

        if position:
            self.position.x = position[0]
            self.position.y = position[1]


        renderImages.append(self)
        # pygame.display.get_surface().blit(self.image, self.position)

    def scale2x(self):
        self.image = pygame.transform.scale2x(self.image)
        

class GameFont():
    def __init__(self, name, size, isSys = True):
        self.name = name
        self.size = size
        self.font = None
        self.isSys = isSys
        self.load()

    def load(self):
        if not self.font:
            if self.isSys:
                self.font = pygame.font.SysFont(self.name, self.size)
            else:
                self.font = pygame.font.Font(self.name, self.size)


class GameText(GameImage):
    def __init__(self, font, text = '', position = (0,0), RGB = (0,0,0)):
        super().__init__(fileName=None, position=position)
        self.font = font
        self.text = text
        self.color = pygame.Color(RGB[0],RGB[1],RGB[2])

    def renderText(self, text, position = None):
        self.text = str(text)
        self.render(position)

    def render(self, position = None):
        # self.font.load()

        if position != None:
            self.position = position

        if self.text != '':
            self.image = self.font.font.render(self.text, True, self.color)
            pygame.display.get_surface().blit(self.image, self.position)

class MyScene(Scene):
    def update(self):
        for image in renderImages:
            image.image.remove_from_parent()

        renderImages.clear()
        self.gameapp.on_render()
        for image in renderImages:
            self.add_child(image.image)

        self.gameapp.on_loop()


class GameApp():
    def __init__(self, width=640, height=480):
        self.isRunning = True
        self.surface = None
        self.width = width
        self.height = height
        self.isFullScreen = False
        self.fps = 5
        self.keysPressed = []
        self.curUserEventId = USEREVENT 
        self.milliseconds_since_start = 0


        # pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.width, self.height))
        if self.isFullScreen == True:
            pygame.display.toggle_fullscreen()
      
 


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

        s = MyScene()
        s.gameapp = self
        run(s)


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
    app.image = GameImage('test.png', (100,100))
    app.image.render()
    GameApp().start()
