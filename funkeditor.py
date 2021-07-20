from gameapp import GameImage, GameFont, GameText, k, GameSection
from editorarrow import EditorArrow

class Editor(GameSection):
    def __init__(self, parent):
        self.parent = parent
        
        self.EditorBackground = GameImage(self, 'images/background/EditBackground.gif')
        self.mousePos = (0, 0)
        self.EditorFont = GameFont(self, 'fonts/vcr.ttf', 6, False)
        self.MouseText = GameText(self, self.EditorFont)
        self.ArrowList = []
        

    def on_loop(self):
        pass

    def on_render(self):
        self.EditorBackground.render()
        for arrow in self.ArrowList:
            arrow.render()
    
        self.MouseText.renderText(f'{self.mousePos}')

    def on_key(self, isDown, key, mod):
        if isDown:
            if key == k.K_ESCAPE:
                self.parent.currentSectionName = 'mainmenu'
            if key == k.K_r:
                self.ArrowList.clear()

    def on_mouse(self, isDown, key, xcoord, ycoord):
        if isDown:
            if key == 1:
                self.mousePos = (xcoord, ycoord)
                self.ArrowList.append(EditorArrow(self, 'Left'))
