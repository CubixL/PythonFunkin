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
        for myfoldername in self.songList:
            self.Buttons.append( { 
                'folderName' : myfoldername,
                'menuTab' : 0,
                'imgNormal' : GameText(self, self.GUIFont, text = f'{myfoldername}', position = (5, topY), RGB = (255, 255, 255)),
                'imgSelected' : GameText(self, self.GUIFont, text = f'{myfoldername}', position = (5, topY), RGB = (255, 233, 127)),
            })
            topY += 8

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.parent.currentSectionName = 'mainmenu'
            if key == kb.K_LEFT and self.highlightedOverlay == 0:
                self.MenuOverlay.render((0, 0))
            if key == kb.K_RIGHT and self.highlightedOverlay == 1:
                self.MenuOverlay.render((176, 0))
            
            if key == kb.K_RETURN and self.highlightedOverlay == 0:
                self.parent.sections['level'].loadedSong = self.songList[self.highlighted]
                self.parent.currentSectionName = 'level'
                self.parent.sections['level'].loadFile()
                # self.songList[self.highlighted]
                    # pass
                # self.parent.sections['level'].