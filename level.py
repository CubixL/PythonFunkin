
from gameapp import *
from playerarrow import PlayerArrow
from targetarrow import TargetArrow
from rating import Rating

import json

class Level():
    def __init__(self, parent):
        self.parent = parent
        self.scale = parent.scale        
        self.LevelBackground = GameImage(self, 'images/background/StageBackground.gif', (0, 0))
        self.PlayerArrowL = PlayerArrow(self, type = 'Left')
        self.PlayerArrowD = PlayerArrow(self, type = 'Down')
        self.PlayerArrowU = PlayerArrow(self, type = 'Up')
        self.PlayerArrowR = PlayerArrow(self, type = 'Right')
        self.Rating = Rating(self)
        self.Combo = 0

        self.TargetList = []
        self.PlayerScore = 0
        self.milliAtStart = self.parent.getMillisecondsSinceStart()
        self.music = GameAudio()

        # font & text
        self.GUIFont = GameFont(self, 'fonts/vcr.ttf', 6, False)
        self.DebugFont = GameFont(self, 'fonts/vcr.ttf', 4, False)
        self.MSText = GameText(self, self.DebugFont)
        self.FPSText = GameText(self, self.DebugFont)
        self.ScoreText = GameText(self, self.GUIFont, RGB = (255, 255, 255))
        self.ComboText = GameText(self, self.GUIFont, RGB = (255, 255, 255))

    def getMilli(self):
        return self.parent.getMillisecondsSinceStart()  - self.milliAtStart

    def on_loop(self):
        currentscore = 0
        
        for target in self.TargetList:
            score = target.calcScore()
            # Check for targets that need to become active
            if target.state == 'hidden' and self.getMilli() >= target.milliseconds:
                target.state = 'active'
            # Check for targets that have passed the input range (If it is the enemy's, it has to seem like it hit the note)
            if target.isEnemy == False:
                if target.state == 'active' and score < 0:
                    target.state = 'played'
                    currentscore += score
                    # reset combo
                    self.Combo = 0
            elif target.isEnemy == True:
                if target.state == 'active' and target.img.position.y < 11:
                    target.state = 'played'
            target.move() # Move targets up

        self.PlayerScore += currentscore


    def on_render(self):
        self.LevelBackground.render()                                           # 1. Background
        self.PlayerArrowL.render()                                              # 2. Player arrows
        self.PlayerArrowD.render()
        self.PlayerArrowU.render()
        self.PlayerArrowR.render()
        for target in self.TargetList:                                          # 3. Target arrows (Note, then sustain line, then sustain end)
            target.render()
           
        self.MSText.renderText(f'Game time: {self.getMilli()}')                 # 4. GUI (Text)
        self.FPSText.renderText(f'FPS: {self.parent.fps}', position = (0, 4))
        self.ScoreText.renderText(f'Score: {self.PlayerScore}', position = (98, 124))
        self.ComboText.renderText(f'{self.Combo}', position = (120, 114))

        self.Rating.render()

    def on_key(self, isDown, key, mod): 
        if isDown == True and key == K_ESCAPE:
            self.music.stop()
            self.parent.section = 'menu'
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
                        # Add 1 to combo
                        self.Combo += 1
            
            # If score is still 0, the bad key was pressed
            if currentscore == 0 and key in (K_DOWN, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d) and isDown:
                currentscore = -10
                # reset combo
                self.Combo = 0
            self.PlayerScore += currentscore

            # R resets the chart
            if isDown == True and key == K_r:
                self.loadFile()

    def on_mouse(self, isDown, key, xcoord, ycoord):
        pass

    def loadFile(self, songName = None): # Load the entire song chart (JSON file stuff)
        # When called, reset score, timer and note list to 0 before loading
        if songName == None:
            songName = 'Tutorial'

        self.PlayerScore = 0
        self.milliAtStart = self.parent.getMillisecondsSinceStart()
        self.TargetList.clear()
        self.Combo = 0


        self.music.load(f'song/{songName}_Inst')

        
        chart = open(str('song') + '//' + f'{songName}.json')
        data = json.load(chart)

        # Song variables
        
        self.JSONbpm = data['song']['bpm']
        self.JSONsections = data['sections']
        #for section in range (0, self.JSONsections):
            #print (data['notes'][section]['sectionNotes'])

        # The big complicated note stuff
        for section in range (0, self.JSONsections): # Find the number of notes in every single section
            self.JSONnotenumber = len(data['notes'][section]['sectionNotes'])
            for note in range (0, self.JSONnotenumber): # For every note in a section, find all it's characteristics
                self.JSONmilliseconds = data['notes'][section]['sectionNotes'][note][0] - self.JSONbpm * 15
                self.JSONtype = data['notes'][section]['sectionNotes'][note][1]
                self.JSONenemy = not data['notes'][section]['mustHitSection']
                self.JSONsustain = data['notes'][section]['sectionNotes'][note][2]
                if self.JSONtype == 0:
                    self.TargetList.append(TargetArrow(self, type = 'Left', milliseconds = self.JSONmilliseconds, isEnemy = self.JSONenemy, sustainLength = self.JSONsustain))
                if self.JSONtype == 1:
                    self.TargetList.append(TargetArrow(self, type = 'Down', milliseconds = self.JSONmilliseconds, isEnemy = self.JSONenemy, sustainLength = self.JSONsustain))
                if self.JSONtype == 2:
                    self.TargetList.append(TargetArrow(self, type = 'Up', milliseconds = self.JSONmilliseconds, isEnemy = self.JSONenemy, sustainLength = self.JSONsustain))
                if self.JSONtype == 3:
                    self.TargetList.append(TargetArrow(self, type = 'Right', milliseconds = self.JSONmilliseconds, isEnemy = self.JSONenemy, sustainLength = self.JSONsustain))

        self.music.play()


        # 1. 'notes': the entire list of all the notes
        # 2. int: section number
        # 3. 'sectionNotes': notes in the section
        # 4. int: number of the note in the section
        # 5. int: desired variable of a specific note
                # 0 is number in milliseconds when it appears
                # 1 is note type (0 - left, 1 - down, 2 - up, 3 - right)
                # 2 is sustain duration (how much time you have to hold it)
