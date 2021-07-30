from gameapp import GameImage

# params to add: milliseconds, isEnemy, sustainLength
class EditorArrow():
    def __init__(self, parent, type):
        self.type = type
        self.parent = parent
        
        # self.milliseconds = milliseconds
        # self.isEnemy = isEnemy
        # self.sustainLength = sustainLength

        self.img = GameImage(self, f'images/funkeditor/Arrow{type}Editor.gif')
        self.img.position.x = 8
        self.img.position.y = 7

    def render(self):
        self.img.render()