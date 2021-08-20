from gameapp import GameImage, GameText, kb
from game.menu import Menu, MenuButton
from game.keybinds import keys
import json
import os.path

class SettingsMenu(Menu):
    def on_start(self):
        super().on_start()
        self.MenuBackground = GameImage('images/background/menu/BGE_SettingsBackground.png')
        self.MenuOverlay = GameImage('images/background/menu/BGE_SettingsOverlay.png')
        self.menuTabs = 0

        with open('saveFile.json') as json_file:
            self.saveFile = json.load(json_file)
        self.currentStage = self.saveFile['settings']['LevelBackground']
        self.leftKeyDisplay = keys[self.saveFile['settings']['LeftKeybind']]
        self.downKeyDisplay = keys[self.saveFile['settings']['DownKeybind']]
        self.upKeyDisplay = keys[self.saveFile['settings']['UpKeybind']]
        self.rightDisplay = keys[self.saveFile['settings']['RightKeybind']]
        self.leftKeybind = self.saveFile['settings']['LeftKeybind']
        self.downKeybind = self.saveFile['settings']['DownKeybind']
        self.upKeybind = self.saveFile['settings']['UpKeybind']
        self.rightKeybind = self.saveFile['settings']['RightKeybind']
        self.menuTitle = GameText(font = self.TitleFont, text = 'SETTINGS', position = (10, 6), color = (255, 255, 255))
        self.state = 'idle'
        self.stateText = None

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
            menuText = f'Left Keybind: {self.leftKeyDisplay}'
        )) 

        self.Buttons.append(MenuButton(
            name = 'down keybind',
            menuTab = 0,
            type = 'text',
            position = (10, 36),
            menuText = f'Down Keybind: {self.downKeyDisplay}'
        )) 

        self.Buttons.append(MenuButton(
            name = 'up keybind',
            menuTab = 0,
            type = 'text',
            position = (10, 44),
            menuText = f'Up Keybind: {self.upKeyDisplay}'
        )) 

        self.Buttons.append(MenuButton(
            name = 'right keybind',
            menuTab = 0,
            type = 'text',
            position = (10, 52),
            menuText = f'Right Keybind: {self.rightDisplay}'
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
        if self.state == 'input':
            self.stateText = GameText(font = self.GUIFont, text = 'Waiting for input..', position = (60, 8), color = (255, 0, 0))
        if self.state == 'idle':
            self.stateText = None

    def on_render(self):
        super().on_render()
        self.menuTitle.render()
        if self.stateText:
            self.stateText.render()

    def getStageText(self):
        return f'< Level Background: {self.currentStage} >'

    def updateText(self):
        StageButton:MenuButton = self.Buttons[0]
        LeftKeyText:MenuButton = self.Buttons[1]
        DownKeyText:MenuButton = self.Buttons[2]
        UpKeyText:MenuButton = self.Buttons[3]
        RightKeyText:MenuButton = self.Buttons[4]
        StageButton.menuText = self.getStageText()
        LeftKeyText.menuText = f'Left Keybind: {self.leftKeyDisplay}'
        DownKeyText.menuText = f'Down Keybind: {self.downKeyDisplay}'
        UpKeyText.menuText = f'Up Keybind: {self.upKeyDisplay}'
        RightKeyText.menuText = f'Right Keybind: {self.rightDisplay}'
        StageButton.update()
        LeftKeyText.update()
        DownKeyText.update()
        UpKeyText.update()
        RightKeyText.update()

    def doAction(self, isDown, key, mod):
        if isDown:
            if key == kb.K_ESCAPE:
                self.state == 'idle'
                self.currentStage = self.saveFile['settings']['LevelBackground']
                self.leftKeyDisplay = keys[self.saveFile['settings']['LeftKeybind']]
                self.downKeyDisplay = keys[self.saveFile['settings']['DownKeybind']]
                self.upKeyDisplay = keys[self.saveFile['settings']['UpKeybind']]
                self.rightDisplay = keys[self.saveFile['settings']['RightKeybind']]
                self.leftKeybind = self.saveFile['settings']['LeftKeybind']
                self.downKeybind = self.saveFile['settings']['DownKeybind']
                self.upKeybind = self.saveFile['settings']['UpKeybind']
                self.rightKeybind = self.saveFile['settings']['RightKeybind']
                self.highlighted == 1
                self.active = False
                self.gameapp.sections['mainmenu'].active = True
                return False
            
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

            self.updateText()
    
            # Enter key
            if key == kb.K_RETURN:
                if ('keybind' in self.Buttons[self.highlighted].name) and self.state == 'idle':
                    self.state = 'input'

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
                        'LevelBackground' : self.currentStage,
                        'LeftKeybind' : self.leftKeybind,
                        'DownKeybind' : self.downKeybind,
                        'UpKeybind' : self.upKeybind,
                        'RightKeybind' : self.rightKeybind
                    }
                    with open('saveFile.json', 'w') as outfile:
                        json.dump(self.saveFile, outfile, indent = 2)
                    print('Settings saved')

            if self.state == 'input':
                if key == kb.K_DOWN or key == kb.K_UP:
                    self.state = 'idle'
                if key in keys:
                    if self.highlighted == 1:
                        self.leftKeyDisplay = keys[key]
                        self.leftKeybind = key
                    if self.highlighted == 2:
                        self.downKeyDisplay = keys[key]
                        self.downKeybind = key
                    if self.highlighted == 3:
                        self.upKeyDisplay = keys[key]
                        self.upKeybind = key
                    if self.highlighted == 4:
                        self.rightDisplay = keys[key]
                        self.rightKeybind = key
                    self.state = 'idle'
                    self.updateText()