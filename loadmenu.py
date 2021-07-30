import os, json
from gameapp import GameImage, GameText, GameFont, kb
from menu import Menu, MenuButton


class LoadMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/BGE_LoadBackground.png')
        self.MenuOverlay = GameImage(self, 'images/background/BGE_LoadOverlay.png')
        self.menuTabs = 0
        self.songList = os.listdir('songlibrary')
        topY = 20
        self.TitleFont = GameFont(self, 'fonts/vcr.ttf', 10, isSys = False)
        self.menuTitle = GameText(self, self.TitleFont, text = 'SONG LIST', position = (5, 6), RGB = (255, 255, 255))
        self.menuDetails = GameText(self, self.TitleFont, text = 'DETAILS', position = (188, 6), RGB = (255, 255, 255))
        self.details = []
        self.songName = None

        for myfoldername in self.songList:
            self.Buttons.append(MenuButton(
            name = myfoldername,
            menuTab = 0,
            imgNormal = GameText(self, self.GUIFont, text = f'{myfoldername}', position = (5, topY), RGB = (255, 255, 255)),
            imgSelected = GameText(self, self.GUIFont, text = f'{myfoldername}', position = (5, topY), RGB = (255, 233, 127)),
        ))   
            topY += 8

        self.loadDetails()

    def on_loop(self):
        pass

    def on_render(self):
        super().on_render()
        self.menuTitle.render()
        self.menuDetails.render()
        if self.details:
            for info in range(len(self.details)):
                self.details[info].render()

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.parent.currentSectionName = 'mainmenu'
            
            if key == kb.K_RETURN and self.highlightedOverlay == 0:
                self.parent.sections['level'].loadedSong = self.songList[self.highlighted]
                self.parent.currentSectionName = 'level'
                self.parent.sections['level'].loadFile()
            if key == kb.K_w or key == kb.K_s or key == kb.K_UP or key == kb.K_DOWN:
                self.loadDetails()

    def loadDetails(self):
        self.details.clear()
        self.songName = self.Buttons[self.highlighted].name
        chart = open(f'songlibrary/{self.songName}/{self.songName}.json')
        data = json.load(chart)
        self.JSONbpm = data['song']['bpm']
        self.JSONspeed = round(data['song']['speed'], 2)
        self.JSONsections = len(data['song']['notes'])
        self.details.append(GameText(self, self.GUIFont, text = f'BPM: {self.JSONbpm}', position = (188, 20), RGB = (255, 255, 255)))
        self.details.append(GameText(self, self.GUIFont, text = f'Speed: {self.JSONspeed}', position = (188, 28), RGB = (255, 255, 255)))
        self.details.append(GameText(self, self.GUIFont, text = f'Sections: {self.JSONsections}', position = (188, 36), RGB = (255, 255, 255)))
