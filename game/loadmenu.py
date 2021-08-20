from game.level import Level
import os, json
from gameapp import GameImage, GameText, GameFont, kb
from game.menu import Menu, MenuButton


class LoadMenu(Menu): # menu for loading songs
    def on_start(self):
        super().on_start()
        self.MenuBackground = GameImage('images/background/menu/BGE_LoadBackground.png')
        self.MenuOverlay = GameImage('images/background/menu/BGE_LoadOverlay.png')
        self.menuTabs = 0
        self.songList = os.listdir('songlibrary')
        self.maxButtons = 14
        topY = 20

        self.menuTitle = GameText(font = self.TitleFont, text = 'SONG LIST', position = (5, 6), color = (255, 255, 255))
        self.menuDetails = GameText(font = self.TitleFont, text = 'DETAILS', position = (188, 6), color = (255, 255, 255))
        self.details = []
        self.songName = None

        with open('saveFile.json') as json_file:
                self.saveFile = json.load(json_file)
        self.highscore = None

        for myfoldername in self.songList:
            if (len(self.Buttons) % self.maxButtons) == 0:
                topY = 20
            else:
                topY += 8            

            if len(myfoldername) > 16:
                displayedname = myfoldername[:16]
            else:
                displayedname = myfoldername
            
            button = MenuButton(
                name = myfoldername,
                menuTab = 0,
                type = 'text',
                position = (5, topY),
                menuText = f'{displayedname}'
        )
            button.menuTab = int(len(self.Buttons) / self.maxButtons)
            self.Buttons.append(button)
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
                self.active = False
                self.gameapp.sections['mainmenu'].active = True
                return False
            
            if key == kb.K_RETURN:
                level = self.gameapp.sections['level']
                level.loadedSong = self.songList[self.highlighted] # type:ignore
                self.active = False
                self.gameapp.sections['level'].active = True
                self.gameapp.sections['level'].loadFile() # type:ignore
                return False
            if key == kb.K_w or key == kb.K_s or key == kb.K_UP or key == kb.K_DOWN:
                self.loadDetails()

    def loadDetails(self):
        self.details.clear()
        self.songName = self.Buttons[self.highlighted].name

        # Assume highscore is zero if it doesn't exist.
        try:
            self.highscore = self.saveFile['highscores'][f'{self.songName}']
        except:
            self.highscore = 0
        
        try: # Details from JSON
            chart = open(f'songlibrary/{self.songName}/{self.songName}.json')
            data = json.load(chart)
            self.JSONbpm = data['song']['bpm']
            self.JSONspeed = round(data['song']['speed'], 2)
            self.JSONsections = len(data['song']['notes'])
            self.details.append(GameText(font = self.GUIFont, text = f'BPM: {self.JSONbpm}', position = (188, 20), color = (255, 255, 255)))
            self.details.append(GameText(font = self.GUIFont, text = f'Speed: {self.JSONspeed}', position = (188, 28), color = (255, 255, 255)))
            self.details.append(GameText(font = self.GUIFont, text = f'Sections: {self.JSONsections}', position = (188, 36), color = (255, 255, 255)))
        except: # If JSON cannot be loaded, show error message
            self.details.append(GameText(font = self.GUIFont, text = f'Failed to load', position = (182, 20), color = (255, 255, 255)))
            self.details.append(GameText(font = self.GUIFont, text = f'JSON file.', position = (190, 28), color = (255, 255, 255)))
        self.details.append(GameText(font = self.GUIFont, text = f'Highscore: ', position = (188, 52), color = (255, 255, 255)))
        self.details.append(GameText(font = self.GUIFont, text = f'{self.highscore}', position = (188, 58), color = (0, 255, 147)))

    # Sub-init function
    def refreshPage(self):
        with open('saveFile.json') as json_file:
                self.saveFile = json.load(json_file)
        self.loadDetails()
        