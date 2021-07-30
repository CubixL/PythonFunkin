import os
from gameapp import GameImage, GameText, GameFont, kb
from menu import Menu


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

        for myfoldername in self.songList:
            self.Buttons.append( { 
                'folderName' : myfoldername,
                'menuTab' : 0,
                'imgNormal' : GameText(self, self.GUIFont, text = f'{myfoldername}', position = (5, topY), RGB = (255, 255, 255)),
                'imgSelected' : GameText(self, self.GUIFont, text = f'{myfoldername}', position = (5, topY), RGB = (255, 233, 127)),
            })
            topY += 8

    def on_render(self):
        super().on_render()
        self.menuTitle.render()
        self.menuDetails.render()

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.parent.currentSectionName = 'mainmenu'
            
            if key == kb.K_RETURN and self.highlightedOverlay == 0:
                self.parent.sections['level'].loadedSong = self.songList[self.highlighted]
                self.parent.currentSectionName = 'level'
                self.parent.sections['level'].loadFile()
                # self.songList[self.highlighted]
                    # pass
                # self.parent.sections['level'].

        # chart = open(f'songlibrary/{songName}/{songName}.json')
        # data = json.load(chart)