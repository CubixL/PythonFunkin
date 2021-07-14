#import typing
# from gameapp import Rect

        

class PGSurface():
    def __init__(self):
        pass

    def convert(self):
        return self

    def blit(self, image, position):
        print('blitting')
        



class PGImageW():
    def load(self, filename) -> PGSurface: 
        return PGSurface()

class PGTransformW():
    def __init__(self):
        pass

    def scale2x(self, image) -> PGSurface:
        return PGSurface()

class PGClock():
    def tick(self, fps):
        pass

    def get_time(self) -> int:
        return 0
    

class PGTimeW():
    def __init__(self):
        pass

    def Clock(self) -> PGClock:
        return PGClock()

    def set_timer(self, UserEventId, mili, runOnce):
        pass


        

class PGDisplayW():
    def __init__(self):
        pass

    def set_mode(self, width_height) -> PGSurface:
        return PGSurface()
    
    def toggle_fullscreen(self):
        pass

    def update(self):
        pass
    
    def get_surface(self) -> PGSurface:
        return PGSurface()

class PGFont():
    def __init__(self):
        pass

    def render(self, text, antialias, color, background=None):
        pass
    
class PGFontW():
    def __init__(self):
        pass

    def SysFont(self, name, size) -> PGFont:
        return PGFont()

    def Font(self, name, size) -> PGFont:
        return PGFont()

class PGKeyW():
    def __init__(self):
        pass

    def get_pressed(self):
        keys = []
        return keys

class PGEvent():
    def __init__(self):
        self.type = 0
        self.key = 0
        self.mod = {}

        pass

class PGEventW():
    def __init__(self):
        pass

    def get(self):
        events = []
        return events

class PGColor():
    def __init__(self, R, G, B):
        pass

class PyGame():
    def __init__(self):
        self.image = PGImageW()
        self.transform = PGTransformW()
        self.time = PGTimeW()
        self.display = PGDisplayW()
        self.font = PGFontW()
        self.key = PGKeyW()
        self.event = PGEventW()
        

    def init(self):
        pass

    def Color(self, R, G, B):
        return PGColor(R, G, B)


pygame = PyGame()
