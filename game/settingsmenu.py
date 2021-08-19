from gameapp import GameImage, GameText, kb
from game.menu import Menu, MenuButton
from game.keybinds import keys
import json
import os.path

class SettingsMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.MenuBackground = GameImage(self, 'images/background/menu/BGE_SettingsBackground.png')
        self.MenuOverlay = GameImage(self, 'images/background/menu/BGE_SettingsOverlay.png')
        self.menuTabs = 0

        with open('saveFile.json') as json_file:
            self.saveFile = json.load(json_file)
        self.currentStage = self.saveFile['settings']['LevelBackground']
        self.leftKeybind = keys[self.saveFile['settings']['LeftKeybind']]
        self.downKeybind = keys[self.saveFile['settings']['DownKeybind']]
        self.upKeybind = keys[self.saveFile['settings']['UpKeybind']]
        self.rightKeybind = keys[self.saveFile['settings']['RightKeybind']]
        self.menuTitle = GameText(self, self.TitleFont, text = 'SETTINGS', position = (10, 6), RGB = (255, 255, 255))

        self.Buttons.append(MenuButton(
            name = 'background',
            menuTab = 0,
            type = 'text',
            position = (10, 20),
            menuText = self.getStageText()
        ))  

        self.Buttons.append(MenuButton(
            name = 'left keybind',
            menuTab = 0,
            type = 'text',
            position = (10, 28),
            menuText = f'Left Keybind: {self.leftKeybind}'
        )) 

        self.Buttons.append(MenuButton(
            name = 'down keybind',
            menuTab = 0,
            type = 'text',
            position = (10, 36),
            menuText = f'Down Keybind: {self.downKeybind}'
        )) 

        self.Buttons.append(MenuButton(
            name = 'up keybind',
            menuTab = 0,
            type = 'text',
            position = (10, 44),
            menuText = f'Up Keybind: {self.upKeybind}'
        )) 

        self.Buttons.append(MenuButton(
            name = 'right keybind',
            menuTab = 0,
            type = 'text',
            position = (10, 52),
            menuText = f'Right Keybind: {self.rightKeybind}'
        )) 
        
        self.Buttons.append(MenuButton(
            name = 'apply',
            menuTab = 0,
            type = 'text',
            position = (10, 60),
            menuText = 'Apply',
            normalColor = (27, 174, 27),
            selectedColor = (50, 255, 50)
        ))  

    def on_loop(self):
        self.testText = GameText(self, self.GUIFont, text = f'{self.currentStage}', position = (0, 0), RGB = (255, 255, 255))

    def on_render(self):
        super().on_render()
        self.menuTitle.render()
        self.testText.render()

    def getStageText(self):
        return f'Level Background: {self.currentStage}'

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.parent.currentSectionName = 'mainmenu'
            
            # Stage background settings
            numStages = 7
            if key == kb.K_a or key == kb.K_LEFT:
                if self.highlighted == 0:
                    if self.currentStage != 1:
                        self.currentStage -= 1
                    else:
                        self.currentStage = numStages
            if key == kb.K_d or key == kb.K_RIGHT:
                if self.highlighted == 0:
                    if self.currentStage != numStages:
                        self.currentStage += 1
                    else:
                        self.currentStage = 1

            StageButton:MenuButton = self.Buttons[0]
            StageButton.menuText = self.getStageText()
            StageButton.update()

            # Enter key
            if key == kb.K_RETURN:
                if 'keybind' in self.Buttons[self.highlighted].name == True:
                    print('success')

                if self.Buttons[self.highlighted].name == 'apply':
                    if not os.path.exists('saveFile.json'):
                        self.saveFile['settings'] = {
                                    'LevelBackground' : 1,
                                    'LeftKeybind' : kb.K_a,
                                    'DownKeybind' : kb.K_s,
                                    'UpKeybind' : kb.K_w,
                                    'RightKeybind' : kb.K_d
                                }
                        self.saveFile['highscores'] = {
                            'Tutorial' : 0
                        }
                    else:
                        with open('saveFile.json') as json_file:
                            self.saveFile = json.load(json_file)
                    self.saveFile['settings'] = {
                        'LevelBackground' : self.currentStage
                    }
                    with open('saveFile.json', 'w') as outfile:
                        json.dump(self.saveFile, outfile, indent = 2)
                    print('Settings saved')