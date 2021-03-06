#from __future__ import annotations
from gameapp import GameImage, GameAudio, GameFont, GameText, kb, GameSection, GameApp, GameTimer
from game.playerarrow import PlayerArrow
from game.targetarrow import TargetArrow
import json, random, ctypes
import os
from typing import List

# Error message box.
def ErrorBox(title, text, style = 0):
    if os.name == 'nt':
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

class Level(GameSection):
    def on_start(self):

        self.LevelBackground = GameImage()
        self.saveFile = {}
        self.saveFile['highscores'] = {}
        # Background
        fileName = 'saveFile.json'
        if not os.path.exists(fileName):
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
            with open('saveFile.json', 'w') as outfile:
                json.dump(self.saveFile, outfile, indent = 2)
        else:
            with open('saveFile.json') as json_file:
                self.saveFile = json.load(json_file)
        self.hadException = False
        
        self.BackgroundBeat = None
        
        self.IntroReady = GameImage('images/level/ready-pixel.png', position = (76, 40))
        self.IntroSet = GameImage('images/level/set-pixel.png', position = (76, 40))
        self.IntroGo = GameImage('images/level/go-pixel.png', position = (76, 40))
        self.PlayerArrowL = PlayerArrow(self, type = 'Left')
        self.PlayerArrowD = PlayerArrow(self, type = 'Down')
        self.PlayerArrowU = PlayerArrow(self, type = 'Up')
        self.PlayerArrowR = PlayerArrow(self, type = 'Right')
        self.Combo = 0
        self.loadedSong = None
        self.isStarted = False
        self.BPMTimer = GameTimer('', 0, 0, 0)
        
        self.JSONspeed = 1
        self.totalMoveTime = 1500

        self.TargetList:List[TargetArrow] = []
        self.PlayerScore = 0
        self.milliAtStart = self.gameapp.get_MS()

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
        self.GUIFont = GameFont('fonts/vcr.ttf', 6, False)
        self.DebugFont = GameFont('fonts/vcr.ttf', 4, False)
        self.MSText = GameText(font = self.DebugFont)
        self.FPSText = GameText(font = self.DebugFont)
        self.ScoreText = GameText(font = self.GUIFont, color = (255, 255, 255))
        self.ComboText = GameText(font = self.GUIFont, color = (255, 255, 255))

        # Rating
        self.RatingYpos = 10
        self.currentRating = None
        self.RatingSick = GameImage('images/level/sick-pixel.png', position = (100, 10))
        self.RatingGood = GameImage('images/level/good-pixel.png', position = (108, 10))
        self.RatingBad = GameImage('images/level/bad-pixel.png', position = (115, 10))
        self.RatingShit = GameImage('images/level/shit-pixel.png', position = (110, 10))
        self.RatingTimer = GameTimer('', 0, 0, 0)

        # Girlfriend and dancers
        self.GFimgList = []
        self.DemonImgList = []
        self.GFTimer = GameTimer('', 0, 0, 0)
        self.BGBeatTimer = GameTimer('', 0, 0, 0)
        self.curGFframe = 0
        for image in range(9):
            self.GFimgList.append(GameImage(f'images/level/girlfriend/gf_frame{image}.png', position = (60, 6)))

        self.curBGframe = 1

    def getMS(self):
        # return the number of milliseconds since start of level
        return self.gameapp.get_MS() - self.milliAtStart

    def stopAssets(self):
        try:
            self.music_inst.stop()
            self.music_voices.stop()
        except:
            pass
        self.gameapp.stop_timer('BPM')
        self.gameapp.stop_timer('Girlfriend')
        self.gameapp.stop_timer('BackgroundBeat')

    def on_loop(self):
        currentscore = 0
        
        for target in self.TargetList:
            score = target.calcScore()
            ms = self.getMS()
            # Check for targets that need to become active
            # if target.state == 'hidden' and (ms >= target.milliseconds - self.totalMoveTime + 300):
            if target.state == 'hidden' and (ms >= target.milliseconds - self.totalMoveTime):
                target.state = 'active'
                if target.sustainLength != 0:
                                                                # total move dist
                    susHeight = int((130 * target.sustainLength) / self.totalMoveTime)

                    target.img_sustain.resize(width = 7, height = susHeight, in_place = True)
                    # target.img_sustain.rect.top = target.img.rect.center_y
                    # target.img_sustainend.rect.top = target.img_sustain.rect.bottom
                    




            if target.endstate == 'hidden' and (ms >= target.sustainMilli - self.totalMoveTime):
                target.endstate = 'active'
            if target.endstate == 'active' and target.img_sustainend.position.y < 19:
                target.endstate = 'played'
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
        if self.hadException == False and self.isStarted == True:
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
                self.active = False
                self.gameapp.sections['loadmenu'].active = True
                self.gameapp.sections['loadmenu'].refreshPage() # type:ignore
                

    def on_render(self):
        self.LevelBackground.render() 

        # Render more stuff around the girlfriend if certain backgounds are selected (i.e. dancers, lights, cars)
        if self.saveFile['settings']['LevelBackground'] == 4:
            self.DemonImgList[self.curBGframe].render(position = (55, 19))
            self.DemonImgList[self.curBGframe].render(position = (105, 19))
            self.DemonImgList[self.curBGframe].render(position = (155, 19))
            self.DemonImgList[self.curBGframe].render(position = (205, 19))

        self.GFimgList[self.curGFframe].render()

        if self.saveFile['settings']['LevelBackground'] == 4:
            limo = GameImage('images/background/limo/LevelBackground4_limo.gif', position = (-6, 77))
            limo.render()

        # After the visuals, we render the player + target arrows
        self.PlayerArrowL.render()
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        
        for target in self.TargetList: 
            target.render()
        
        # then the overlay text
        self.MSText.render_text(f'Game time: {self.getMS()}') 
        self.FPSText.render_text(f'FPS: {1000.0/self.gameapp.get_lastframe_MS()}', position = (0, 4))
        self.ScoreText.render_text(f'Score: {self.PlayerScore}', position = (98, 124))
        self.ComboText.render_text(f'Combo: {self.Combo}', position = (98, 114))
        
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
            if self.BPMTimer.num_loops_performed == 2:
                self.IntroReady.render()
            if self.BPMTimer.num_loops_performed == 3:
                self.IntroSet.render()
            if self.BPMTimer.num_loops_performed == 4:
                self.IntroGo.render()
        
    def on_key(self, isDown, key, mod): 
        if isDown == True and key == kb.K_ESCAPE:
            self.stopAssets()
            self.active = False
            self.gameapp.sections['mainmenu'].active = True
            return False
        else:
            self.PlayerArrowL.on_key(isDown, key) # Check player arrows to switch sprites
            self.PlayerArrowD.on_key(isDown, key)
            self.PlayerArrowU.on_key(isDown, key)
            self.PlayerArrowR.on_key(isDown, key)

            # Check state of target arrows
            currentscore = 0
            for target in self.TargetList:
                # If target arrow was in score range and correct key was pressed
                score = target.calcScore()
                if score > 0 and isDown and target.state == 'active':
                    if key == target.key or key == target.altkey:
                        target.state = 'played'
                        currentscore += score
                        self.Combo += 1
                        self.music_voices.set_volume(1)

                        if score == 350:
                            self.currentRating = 'Sick'
                        elif score == 200:
                            self.currentRating = 'Good'
                        elif score == 100:
                            self.currentRating = 'Bad'
                        elif score == 50:
                            self.currentRating = 'Shit'
                        self.RatingYpos = 10
                        self.gameapp.add_timer('Rating', 20, num_repeats = 8)
                        self.RatingTimer = self.gameapp.timers['Rating']
                        break
            
            # If score is still 0, the bad key was pressed
            if currentscore == 0 and key in (
                    kb.K_DOWN, 
                    kb.K_UP, 
                    kb.K_LEFT, 
                    kb.K_RIGHT, 
                    self.PlayerArrowL.altkey, 
                    self.PlayerArrowD.altkey, 
                    self.PlayerArrowU.altkey, 
                    self.PlayerArrowR.altkey,
                ) and isDown:

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


    def loadFile(self): # Load the entire song chart (JSON file stuff)
        # When called, reset score, timer and note list to 0 before loading
        if self.loadedSong == None:
            self.loadedSong = 'Tutorial'
        songName = self.loadedSong

        self.PlayerArrowL.altkey = self.saveFile['settings']['LeftKeybind']
        self.PlayerArrowD.altkey = self.saveFile['settings']['DownKeybind']
        self.PlayerArrowU.altkey = self.saveFile['settings']['UpKeybind']
        self.PlayerArrowR.altkey = self.saveFile['settings']['RightKeybind']

        # Refreshing settings
        with open('saveFile.json') as json_file:
            self.saveFile = json.load(json_file)
        savedStage = self.saveFile['settings']['LevelBackground']
        self.LevelBackground = GameImage(f'images/background/LevelBackground{savedStage}.gif')

        if self.saveFile['settings']['LevelBackground'] == 3:
            self.LevelBackground = GameImage('images/background/philly/LevelBackground3_lights1.gif')
        if self.saveFile['settings']['LevelBackground'] == 4:
            for image in range(1, 7):
                self.DemonImgList.append(GameImage(f'images/background/limo/dancer{image}.png', position = (55, 19)))

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
        #try:
        if True:
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
                    # Order of parameters: self/parent, type, milliseconds, isEnemy
                    if self.JSONtype == 0:
                        self.TargetList.append(TargetArrow(self, type='Left', milliseconds=self.HitTime, isEnemy=self.JSONenemy, sustainLength=self.JSONsustain))
                    if self.JSONtype == 1:
                        self.TargetList.append(TargetArrow(self, type='Down', milliseconds=self.HitTime, isEnemy=self.JSONenemy, sustainLength=self.JSONsustain))
                    if self.JSONtype == 2:
                        self.TargetList.append(TargetArrow(self, type='Up', milliseconds=self.HitTime, isEnemy=self.JSONenemy, sustainLength=self.JSONsustain))
                    if self.JSONtype == 3:
                        self.TargetList.append(TargetArrow(self, type='Right', milliseconds=self.HitTime, isEnemy=self.JSONenemy, sustainLength=self.JSONsustain))
                    if self.JSONtype == 4:
                        self.TargetList.append(TargetArrow(self, type='Left', milliseconds=self.HitTime, isEnemy=not self.JSONenemy, sustainLength=self.JSONsustain))
                    if self.JSONtype == 5:
                        self.TargetList.append(TargetArrow(self, type='Down', milliseconds=self.HitTime, isEnemy=not self.JSONenemy, sustainLength=self.JSONsustain))
                    if self.JSONtype == 6:
                        self.TargetList.append(TargetArrow(self, type='Up', milliseconds=self.HitTime, isEnemy=not self.JSONenemy, sustainLength=self.JSONsustain))
                    if self.JSONtype == 7:
                        self.TargetList.append(TargetArrow(self, type='Right', milliseconds=self.HitTime, isEnemy=not self.JSONenemy, sustainLength=self.JSONsustain))

            self.isStarted = False
            self.milliAtStart = self.gameapp.get_MS()
        # except:
        #     ErrorBox('Error',  
        #     f'''
        #     Failure to load JSON file.
        #     Have you tried:
        #         - Checking if the file exists / is properly named (It should be named "{songName}.json")
        #         - Checking if the file has extra data at the end
        #         - Checking if the file is corrupted
        #     '''
        #     )
        #     self.JSONbpm = 120
        #     self.hadException = True

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
            self.gameapp.add_timer('BPM', 60000.0 / self.JSONbpm, delay_MS=350)
            if self.JSONbpm < 200:
                self.gameapp.add_timer('Girlfriend', 120000.0 / self.JSONbpm / 9, delay_MS = 350)
            elif self.JSONbpm >= 200:
                self.gameapp.add_timer('Girlfriend', 240000.0 / self.JSONbpm / 9, delay_MS = 350)
            self.BPMTimer = self.gameapp.timers['BPM']
            self.GFTimer = self.gameapp.timers['Girlfriend']
            if self.saveFile['settings']['LevelBackground'] == 3:
                self.gameapp.add_timer('BackgroundBeat', 240000.0 / self.JSONbpm, delay_MS = 350 + (self.JSONbpm * 2))
            if self.saveFile['settings']['LevelBackground'] == 4:
                self.gameapp.add_timer('BackgroundBeat', 120000.0 / self.JSONbpm / 6, delay_MS = 350)
                self.BGBeatTimer = self.gameapp.timers['BackgroundBeat']
            self.milliAtStart = self.gameapp.get_MS() 
            if self.gameapp.platform == 'win':
                self.milliAtStart += 350

    def on_timer(self, timer:GameTimer):
        if timer.name == 'BPM':
            if self.BPMTimer.num_loops_performed == 1:
                self.sound_introList[0].stop()
                self.sound_introList[0].play()
            if self.BPMTimer.num_loops_performed == 2:
                self.sound_introList[1].stop()
                self.sound_introList[1].play()
            if self.BPMTimer.num_loops_performed == 3:
                self.sound_introList[2].stop()
                self.sound_introList[2].play()
                self.IntroSet.render()
            if self.BPMTimer.num_loops_performed == 4:
                self.sound_introList[3].stop()
                self.sound_introList[3].play()
                self.IntroGo.render()
            if self.BPMTimer.num_loops_performed == 5:
                try:
                    self.music_inst.play()
                    self.music_voices.play()
                except:
                    pass

        if timer.name == 'Rating':
            if self.RatingTimer.num_loops_performed <= 3:
                self.RatingYpos -= 1
            else:
                self.RatingYpos += 1

        if timer.name == 'Girlfriend':
            self.curGFframe = self.GFTimer.num_loops_performed % 9

        if timer.name == 'BackgroundBeat':
            if self.saveFile['settings']['LevelBackground'] == 3:
                self.LevelBackground = GameImage(f'images/background/philly/LevelBackground3_lights{random.randrange(1, 6)}.gif')
            if self.saveFile['settings']['LevelBackground'] == 4:
                self.curBGframe = self.BGBeatTimer.num_loops_performed % 6
