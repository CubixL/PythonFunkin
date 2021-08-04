#from __future__ import annotations
from gameapp import GameImage, GameAudio, GameFont, GameText, kb, GameSection, GameApp
from game.playerarrow import PlayerArrow
from game.targetarrow import TargetArrow
import json, random, ctypes
import os.path

# Error message box.
def ErrorBox(title, text, style = 0):
    if os.name == 'nt':
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

class Level(GameSection):
    def __init__(self, parent):
        self.parent: GameApp = parent

        self.LevelBackground = None
        self.saveFile = {}
        self.saveFile['highscores'] = {}
        # Background
        fileName = 'saveFile.json'
        if not os.path.exists(fileName):
            self.saveFile['settings'] = {
                        'LevelBackground' : 1
                    }
            self.saveFile['highscores'] = {
                'Tutorial' : 0
            }
            with open('saveFile.json', 'w') as outfile:
                json.dump(self.saveFile, outfile, indent = 2)
        else:
            with open('saveFile.json') as json_file:
                self.saveFile = json.load(json_file)
        self.hadException = False
        
        self.BackgroundBeat = None
        
        self.IntroReady = GameImage(self, 'images/level/ready-pixel.png', position = (76, 40))
        self.IntroSet = GameImage(self, 'images/level/set-pixel.png', position = (76, 40))
        self.IntroGo = GameImage(self, 'images/level/go-pixel.png', position = (76, 40))
        self.PlayerArrowL = PlayerArrow(self, type = 'Left')
        self.PlayerArrowD = PlayerArrow(self, type = 'Down')
        self.PlayerArrowU = PlayerArrow(self, type = 'Up')
        self.PlayerArrowR = PlayerArrow(self, type = 'Right')
        self.Combo = 0
        self.loadedSong = None
        self.isStarted = False
        self.BPMTimer = None 
        
        self.JSONspeed = 1
        self.totalMoveTime = 1500

        self.TargetList = []
        self.PlayerScore = 0
        self.milliAtStart = self.parent.getMS()

        # Audio / sounds
        self.music_inst = GameAudio()
        self.music_voices = GameAudio()
        self.sound_missList = [
            GameAudio('sounds/missnote1', 0.3), 
            GameAudio('sounds/missnote2', 0.3), 
            GameAudio('sounds/missnote3', 0.3)
        ]
        self.sound_introList = [
            GameAudio('sounds/intro3', 0.4),
            GameAudio('sounds/intro2', 0.4),
            GameAudio('sounds/intro1', 0.4),
            GameAudio('sounds/introGo', 0.4)
        ]
        self.sound_tempo = GameAudio('sounds/tempo', 1)

        # font & text
        self.GUIFont = GameFont(self, 'fonts/vcr.ttf', 6, False)
        self.DebugFont = GameFont(self, 'fonts/vcr.ttf', 4, False)
        self.MSText = GameText(self, self.DebugFont)
        self.FPSText = GameText(self, self.DebugFont)
        self.ScoreText = GameText(self, self.GUIFont, RGB = (255, 255, 255))
        self.ComboText = GameText(self, self.GUIFont, RGB = (255, 255, 255))

        # Rating
        self.RatingYpos = 10
        self.currentRating = None
        self.RatingSick = GameImage(self, 'images/level/sick-pixel.png', position = (100, 10))
        self.RatingGood = GameImage(self, 'images/level/good-pixel.png', position = (108, 10))
        self.RatingBad = GameImage(self, 'images/level/bad-pixel.png', position = (115, 10))
        self.RatingShit = GameImage(self, 'images/level/shit-pixel.png', position = (110, 10))
        self.RatingTimer = None

        # Girlfriend and dancers
        self.GFimgList = []
        self.DemonImgList = []
        self.GFTimer = None
        self.BGBeatTimer = None
        self.curGFframe = 0
        for image in range(9):
            self.GFimgList.append(GameImage(self, f'images/level/girlfriend/gf_frame{image}.png', position = (60, 6)))

        self.curBGframe = 1


    def getMS(self):
        # return the number of milliseconds since start of level
        return self.parent.getMS() - self.milliAtStart

    def stopAssets(self):
        try:
            self.music_inst.stop()
            self.music_voices.stop()
        except:
            pass
        self.parent.stopTimer('BPM')
        self.parent.stopTimer('Girlfriend')
        self.parent.stopTimer('BackgroundBeat')

    def on_loop(self):
        currentscore = 0
        
        for target in self.TargetList:
            score = target.calcScore()
            ms = self.getMS()
            # Check for targets that need to become active
            # if target.state == 'hidden' and (ms >= target.milliseconds - self.totalMoveTime + 300):
            if target.state == 'hidden' and (ms >= target.milliseconds - self.totalMoveTime):
                target.state = 'active'
            # Check for targets that have passed the input range (If it is the enemy's, it has to seem like it hit the note)
            if target.isEnemy == False:
                if target.state == 'active' and score < 0:
                    target.state = 'played'
                    currentscore += score
                    # reset combo
                    self.Combo = 0
                    self.music_voices.set_volume(0)
            elif target.isEnemy == True:
                if target.state == 'active' and target.img.position.y < 10:
                    target.state = 'played'
                    self.music_voices.set_volume(1)
            target.move() # Move targets up
        self.PlayerScore += currentscore

        # If song has ended
        if self.hadException == False:
            if not self.music_inst.get_busy() and self.TargetList[0].state == 'played':
                if f'{self.loadedSong}' in self.saveFile == True: # If song already has a highscore AND current score is higher, overwrite
                    if self.PlayerScore > self.saveFile['highscores'][f'{self.loadedSong}']:
                        self.saveFile['highscores'].update({f'{self.loadedSong}' : self.PlayerScore})
                        with open('saveFile.json', 'w') as outfile:
                            json.dump(self.saveFile, outfile, indent = 2)
                            print(f'Highscore saved: {self.PlayerScore} points for {self.loadedSong}')
                else: # If song doesn't have a highscore yet, add one
                    self.saveFile['highscores'].update({f'{self.loadedSong}' : self.PlayerScore})
                    with open('saveFile.json', 'w') as outfile:
                        json.dump(self.saveFile, outfile, indent = 2)
                        print(f'Highscore saved: {self.PlayerScore} points for {self.loadedSong}')
                # If song already has a highscore but current score is lower, do nothing
                
                self.stopAssets()
                self.parent.currentSectionName = 'loadmenu'
                self.parent.sections['loadmenu'].refreshPage()

    def on_render(self):
        self.LevelBackground.render() 

        # Render more stuff around the girlfriend if certain backgounds are selected (i.e. dancers, lights, cars)
        if self.saveFile['settings']['LevelBackground'] == 3:
            if self.BackgroundBeat:
                self.BackgroundBeat.render()
            ground = GameImage(self, 'images/background/philly/LevelBackground3_ground.gif')
            ground.render()

        if self.saveFile['settings']['LevelBackground'] == 4:
            self.DemonImgList[self.curBGframe].render(position = (55, 19))
            self.DemonImgList[self.curBGframe].render(position = (105, 19))
            self.DemonImgList[self.curBGframe].render(position = (155, 19))
            self.DemonImgList[self.curBGframe].render(position = (205, 19))

        self.GFimgList[self.curGFframe].render()

        if self.saveFile['settings']['LevelBackground'] == 4:
            limo = GameImage(self, 'images/background/limo/LevelBackground4_limo.gif', position = (-6, 77))
            limo.render()

        # After the visuals, we render the player + target arrows
        self.PlayerArrowL.render()
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        
        for target in self.TargetList: 
            target.render()
        
        # then the overlay text
        self.MSText.renderText(f'Game time: {self.getMS()}') 
        self.FPSText.renderText(f'FPS: {1000.0/self.parent.getLastFrameMS()}', position = (0, 4))
        self.ScoreText.renderText(f'Score: {self.PlayerScore}', position = (98, 124))
        self.ComboText.renderText(f'Combo: {self.Combo}', position = (98, 114))
        
        # Rating text: SICK, good, etc.
        if self.RatingTimer and self.currentRating:
            if self.RatingTimer.active == True:
                if self.currentRating == 'Sick':
                    self.RatingSick.render((100, self.RatingYpos))
                if self.currentRating == 'Good':
                    self.RatingGood.render((103, self.RatingYpos))
                if self.currentRating == 'Bad':
                    self.RatingBad.render((106, self.RatingYpos))
                if self.currentRating == 'Shit':
                    self.RatingShit.render((102, self.RatingYpos))

        # 3-2-1 GO that appears at the start of the song.
        if self.BPMTimer: 
            if self.BPMTimer.numLoopsPerformed == 2:
                self.IntroReady.render()
            if self.BPMTimer.numLoopsPerformed == 3:
                self.IntroSet.render()
            if self.BPMTimer.numLoopsPerformed == 4:
                self.IntroGo.render()
        
    def on_key(self, isDown, key, mod): 
        if isDown == True and key == kb.K_ESCAPE:
            self.stopAssets()
            self.parent.currentSectionName = 'mainmenu'
        else:
            self.PlayerArrowL.on_key(isDown, key) # Check player arrows to switch sprites
            self.PlayerArrowD.on_key(isDown, key)
            self.PlayerArrowU.on_key(isDown, key)
            self.PlayerArrowR.on_key(isDown, key)

            # Check state of target arrows
            currentscore = 0
            for target in self.TargetList:
                # If target arrow was in score range and correct key was pressed
                if target.calcScore() > 0 and isDown and target.state == 'active':
                    if key == target.key or key == target.altkey:
                        target.state = 'played'
                        currentscore += target.calcScore()
                        self.Combo += 1
                        self.music_voices.set_volume(1)

                        if target.calcScore() == 350:
                            self.currentRating = 'Sick'
                        if target.calcScore() == 200:
                            self.currentRating = 'Good'
                        if target.calcScore() == 100:
                            self.currentRating = 'Bad'
                        if target.calcScore() == 50:
                            self.currentRating = 'Shit'
                        self.RatingYpos = 10
                        self.parent.addTimer('Rating', 20, numRepeats = 8)
                        self.RatingTimer = self.parent.timers['Rating']
            
            # If score is still 0, the bad key was pressed
            if currentscore == 0 and key in (kb.K_DOWN, kb.K_UP, kb.K_LEFT, kb.K_RIGHT, kb.K_w, kb.K_a, kb.K_s, kb.K_d) and isDown:
                currentscore = -10
                # reset combo
                self.Combo = 0
                # miss sound
                self.sound_missList[0].stop()
                self.sound_missList[1].stop()
                self.sound_missList[2].stop()
                soundNumber = random.randrange(len(self.sound_missList))
                self.sound_missList[soundNumber].play()
                self.music_voices.set_volume(0)
            self.PlayerScore += currentscore

            # R resets the chart
            if isDown == True and key == kb.K_r:
                self.stopAssets()
                self.loadFile()

    def on_mouse(self, isDown, key, xcoord, ycoord):
        pass

    def loadFile(self): # Load the entire song chart (JSON file stuff)
        # When called, reset score, timer and note list to 0 before loading
        if self.loadedSong == None:
            self.loadedSong = 'Tutorial'
        songName = self.loadedSong

        # Refreshing settings
        with open('saveFile.json') as json_file:
            self.saveFile = json.load(json_file)
        savedStage = self.saveFile['settings']['LevelBackground']
        self.LevelBackground = GameImage(self, f'images/background/LevelBackground{savedStage}.gif')

        if self.saveFile['settings']['LevelBackground'] == 4:
            for image in range(1, 7):
                self.DemonImgList.append(GameImage(self, f'images/background/limo/dancer{image}.png', position = (55, 19)))

        self.PlayerScore = 0
        # self.milliAtStart = self.parent.getMS()
        self.TargetList.clear()
        self.Combo = 0

        # Loading music
        self.hadException = False
        try:
            self.music_inst.load(f'songlibrary/{songName}/{songName}_Inst')
            self.music_voices.load(f'songlibrary/{songName}/{songName}_Voices')
        except:
            ErrorBox('Error',  
            f'''
            Failure to load OGG / CAF files.
            Have you tried:
                - Checking if the file(s) exists
                (They should be labeled "{songName}_Inst.ogg" or "{songName}_Vocals.ogg")
                - Checking if a file is corrupted
            '''
            )
            self.hadException = True

        # Loading JSON
        try:
            chart = open(f'songlibrary/{songName}/{songName}.json')
            data = json.load(chart)

            # Song variables
            self.JSONsections = len(data['song']['notes'])
            self.JSONspeed = data['song']['speed']
            self.totalMoveTime = 1500 / self.JSONspeed
            self.JSONbpm = data['song']['bpm']

            # for section in range (0, self.JSONsections):
            #     print (data['notes'][section]['sectionNotes'])

            # The big complicated note stuff
            for section in range (0, self.JSONsections): # Find the number of notes in every single section
                self.JSONnotenumber = len(data['song']['notes'][section]['sectionNotes'])
                for note in range (0, self.JSONnotenumber): # For every note in a section, find all it's characteristics
                    self.JSONmilliseconds = data['song']['notes'][section]['sectionNotes'][note][0] # - self.totalMoveTime
                    self.JSONtype = data['song']['notes'][section]['sectionNotes'][note][1]
                    self.JSONenemy = not data['song']['notes'][section]['mustHitSection']
                    self.JSONsustain = data['song']['notes'][section]['sectionNotes'][note][2]
                    self.HitTime = self.JSONmilliseconds + ((60000.0 / self.JSONbpm) * 5)
                    # Order of parameters: self, type, sustype, milliseconds, isEnemy
                    if self.JSONtype == 0:
                        self.TargetList.append(TargetArrow(self, 'Left', 'arrow', self.HitTime, self.JSONenemy, self.JSONsustain))
                    if self.JSONtype == 1:
                        self.TargetList.append(TargetArrow(self, 'Down', 'arrow', self.HitTime, self.JSONenemy, self.JSONsustain))
                    if self.JSONtype == 2:
                        self.TargetList.append(TargetArrow(self, 'Up', 'arrow', self.HitTime, self.JSONenemy, self.JSONsustain))
                    if self.JSONtype == 3:
                        self.TargetList.append(TargetArrow(self, 'Right', 'arrow', self.HitTime, self.JSONenemy, self.JSONsustain))
                    if self.JSONtype == 4:
                        self.TargetList.append(TargetArrow(self, 'Left', 'arrow', self.HitTime, not self.JSONenemy, self.JSONsustain))
                    if self.JSONtype == 5:
                        self.TargetList.append(TargetArrow(self, 'Down', 'arrow', self.HitTime, not self.JSONenemy, self.JSONsustain))
                    if self.JSONtype == 6:
                        self.TargetList.append(TargetArrow(self, 'Up', 'arrow', self.HitTime, not self.JSONenemy, self.JSONsustain))
                    if self.JSONtype == 7:
                        self.TargetList.append(TargetArrow(self, 'Right', 'arrow', self.HitTime, not self.JSONenemy, self.JSONsustain))

            self.isStarted = False
            self.milliAtStart = self.parent.getMS()
        except:
            ErrorBox('Error',  
            f'''
            Failure to load JSON file.
            Have you tried:
                - Checking if the file exists / is properly named (It should be named "{songName}.json")
                - Checking if the file has extra data at the end
                - Checking if the file is corrupted
            '''
            )
            self.JSONbpm = 120
            self.hadException = True

        # 1. 'song': The main folder, contains everything
        # 2. 'notes': the entire list of all the notes
        # 3. int: section number
        # 4. 'sectionNotes': notes in the section
        # 5. int: number of the note in the section
        # 6. int: desired variable of a specific note
                # 0 is number in milliseconds when it appears

                # 1 is note type (0 - left, 1 - down, 2 - up, 3 - right)time.sleep
                # 2 is sustain duration (how much time you have to hold it)

    def on_after_render(self):
        if not self.isStarted:
            # print(f'ms at on_after_render: {self.parent.getMS()}    {self.getMS()}')
            self.isStarted = True
            self.parent.addTimer('BPM', 60000.0 / self.JSONbpm, delayMS=350)
            if self.JSONbpm < 200:
                self.parent.addTimer('Girlfriend', 120000.0 / self.JSONbpm / 9, delayMS = 350)
            elif self.JSONbpm >= 200:
                self.parent.addTimer('Girlfriend', 240000.0 / self.JSONbpm / 9, delayMS = 350)
            self.BPMTimer = self.parent.timers['BPM']
            self.GFTimer = self.parent.timers['Girlfriend']
            if self.saveFile['settings']['LevelBackground'] == 3:
                self.parent.addTimer('BackgroundBeat', 240000.0 / self.JSONbpm, delayMS = 350 + (self.JSONbpm * 2))
            if self.saveFile['settings']['LevelBackground'] == 4:
                self.parent.addTimer('BackgroundBeat', 120000.0 / self.JSONbpm / 6, delayMS = 350)
                self.BGBeatTimer = self.parent.timers['BackgroundBeat']
            self.milliAtStart = self.parent.getMS() 
            if self.parent.platform == 'win':
                self.milliAtStart += 350

    def on_timer(self, name):
        if name == 'BPM':
            if self.BPMTimer.numLoopsPerformed == 1:
                self.sound_introList[0].stop()
                self.sound_introList[0].play()
            if self.BPMTimer.numLoopsPerformed == 2:
                self.sound_introList[1].stop()
                self.sound_introList[1].play()
            if self.BPMTimer.numLoopsPerformed == 3:
                self.sound_introList[2].stop()
                self.sound_introList[2].play()
                self.IntroSet.render()
            if self.BPMTimer.numLoopsPerformed == 4:
                self.sound_introList[3].stop()
                self.sound_introList[3].play()
                self.IntroGo.render()
            if self.BPMTimer.numLoopsPerformed == 5:
                try:
                    self.music_inst.play()
                    self.music_voices.play()
                except:
                    pass

        if name == 'Rating':
            if self.RatingTimer.numLoopsPerformed <= 3:
                self.RatingYpos -= 1
            else:
                self.RatingYpos += 1

        if name == 'Girlfriend':
            self.curGFframe = self.GFTimer.numLoopsPerformed % 9

        if name == 'BackgroundBeat':
            if self.saveFile['settings']['LevelBackground'] == 3:
                self.BackgroundBeat = GameImage(self, f'images/background/philly/LevelBackground3_lights{random.randrange(1, 6)}.gif')
            if self.saveFile['settings']['LevelBackground'] == 4:
                self.curBGframe = self.BGBeatTimer.numLoopsPerformed % 6
