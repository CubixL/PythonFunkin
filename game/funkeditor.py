from gameapp import GameImage, GameFont, GameText, kb, GameSection
from game.editorarrow import EditorArrow

class Editor(GameSection):
    def on_start(self):
        self.EditorBackground = GameImage('images/background/menu/EditBackground.gif')
        self.mousePos = (0, 0)
        self.EditorFont = GameFont('fonts/vcr.ttf', 6, False)
        self.MouseText = GameText(font = self.EditorFont)
        self.ArrowList = []
        

    def on_loop(self):
        pass

    def on_render(self):
        self.EditorBackground.render()
        for arrow in self.ArrowList:
            arrow.render()
    
        self.MouseText.render_text(f'{self.mousePos}')

    def on_key(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.active = False
                self.gameapp.sections['mainmenu'].active = True
                return False
            if key == kb.K_r:
                self.ArrowList.clear()

    # def on_mouse(self, isDown, key, xcoord, ycoord):
    #     if isDown:
    #         if key == 1:
    #             self.mousePos = (xcoord, ycoord)
    #             self.ArrowList.append(EditorArrow(self, 'Left'))
