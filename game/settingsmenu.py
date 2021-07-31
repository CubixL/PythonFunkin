from gameapp import GameImage, GameText, kb
from game.menu import Menu, MenuButton
import json

class SettingsMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/BGE_SettingsBackground.png')
        self.MenuOverlay = GameImage(self, 'images/background/BGE_SettingsOverlay.png')
        self.menuTabs = 0
        self.currentStage = 1
        self.menuTitle = GameText(self, self.TitleFont, text = 'SETTINGS', position = (10, 6), RGB = (255, 255, 255))

        self.saveFile = {}
        self.saveFile['settings'] = []

        self.Buttons.append(MenuButton(
            name = 'background',
            menuTab = 0,
            imgNormal = GameText(self, self.GUIFont, text = f'Level Background: {self.currentStage}', position = (10, 20), RGB = (255, 255, 255)),
            imgSelected = GameText(self, self.GUIFont, text = f'Level Background: {self.currentStage}', position = (10, 20), RGB = (255, 233, 127)),
        ))  
        self.Buttons.append(MenuButton(
            name = 'apply',
            menuTab = 0,
            imgNormal = GameText(self, self.GUIFont, text = 'Apply', position = (10, 30), RGB = (27, 174, 27)),
            imgSelected = GameText(self, self.GUIFont, text = 'Apply', position = (10, 30), RGB = (50, 255, 50)),
        ))  

    def on_loop(self):
        self.testText = GameText(self, self.GUIFont, text = f'{self.currentStage}', position = (0, 0), RGB = (255, 255, 255))

    def on_render(self):
        super().on_render()
        self.menuTitle.render()
        self.testText.render()

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.parent.currentSectionName = 'mainmenu'
            
            numStages = 6
            if key == kb.K_a or key == kb.K_LEFT:
                if self.currentStage != 1:
                    self.currentStage -= 1
                else:
                    self.currentStage = numStages
            if key == kb.K_d or key == kb.K_RIGHT:
                if self.currentStage != numStages:
                    self.currentStage += 1
                else:
                    self.currentStage = 1

            if key == kb.K_RETURN:
                if self.highlighted == len(self.Buttons) - 1:
                    self.saveFile['settings'].append({
                        'LevelBackground' : f'{self.currentStage}'
                    })
                    with open('saveFile.json', 'w') as outfile:
                        json.dump(self.saveFile, outfile, indent = 2)
                    print('Data saved')