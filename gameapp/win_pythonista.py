class Path():
    #Create a Path with an oval in the given rectangle.
    def oval(self, x, y, width, height):
        pass


    #Create a Path with a given rectangle.
    def rect(self, x, y, width, height):
        pass

    #Create a Path with a rounded rectangle.
    def rounded_rect(self, x, y, width, height, corner_radius):
        pass

class Scene():
    pass

# class Img():
    # anchor
class SpriteNode():
    def __init__(self, texture, position=(0, 0), z_position=0.0, scale=1.0, x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None, size=None, color='white', blend_mode=0):
        # self.image = Img()
        self.anchor_point = (0,0)
        self.scale = 1.0

    def add_child(self, node):
        pass
            
    def remove_from_parent(self):
        pass
    
class LabelNode():
    def __init__(self, text, position=(0, 0), z_position=0.0, scale=1.0, x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None, size=None, color='white', blend_mode=0):
        pass

    def add_child(self, node):
        pass
            
    def remove_from_parent(self):
        pass

class ShapeNode():
    def __init__(self, path=None, fill_color='white', stroke_color='clear', shadow=None):
        pass

def run(scene, orientation='DEFAULT_ORIENTATION', frame_interval=1, anti_alias=False, show_fps=False, multi_touch=True):
    pass

class sound():
    pass