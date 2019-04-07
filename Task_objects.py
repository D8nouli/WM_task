import pygame
import random
import logging
import datetime
import re

#Set up log file
dateandtime = re.sub(r"\W","_",datetime.datetime.now().isoformat())
logging.basicConfig(level=logging.DEBUG, filename="./" + dateandtime + " log file.txt")

class QuestionAsker:
    letters = 'FGHIJKLMNOPQRSTU'
    
    def __init__(self, fontObj, displayWidth, displayHeight, screen):
        self.fontObj = fontObj
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.screen = screen
        self.tasks = []
        
    def newMessage(self, fontObj, words):
        messageSurface = self.fontObj.render(words, True, (0,0,0))
        messageRect = messageSurface.get_rect()
        messageRect.center = ((self.displayWidth/2),(self.displayHeight/2))
        return TaskMessage(messageSurface, messageRect)
        
    def addTask(self,numberLetters = 4, incorrectProbe = False, alphabetic = False, attentionTime = 200, fixationTime = 3000, instructionTime = 500, letterTime = 3000, delayTime = 6500, probeTime = 1000, answerTime = 5500):
        if alphabetic:
            taskType = "Alphabetic"
        else:
            taskType = "Forward"
            
        attentionMessage = self.newMessage(self.fontObj, "!")
        fixationMessage = self.newMessage(self.fontObj, "+")
        instructionMessage = self.newMessage(self.fontObj, taskType)
        
        #Create the letter set
        letterSet = [] 
        remainingLetters = self.letters
        for i in range(0,numberLetters):
            chosenLetter = random.choice(remainingLetters)
            letterSet.append(chosenLetter)
            remainingLetters = remainingLetters.replace(chosenLetter,"")
        letterSet = "".join(letterSet)
        letterMessage = self.newMessage(self.fontObj, letterSet)
        
        delayMessage = self.newMessage(self.fontObj, "+")
        
        #Create the probe
        if alphabetic:
            orderedLetters = "".join(sorted(letterSet))
            probeIndex = random.randint(0,len(orderedLetters)-1)
            probeText = orderedLetters[probeIndex] + " = " + str(probeIndex + 1)
            if (incorrectProbe):
                wrongLetters = orderedLetters.replace(orderedLetters[probeIndex],"")
                wrongLetter = random.choice(wrongLetters)
                probeText = wrongLetter + " = " + str(probeIndex + 1)
        else:
            probeIndex = random.randint(0,len(letterSet)-1)
            probeText = letterSet[probeIndex] + " = " + str(probeIndex + 1)
            if (incorrectProbe):
                wrongLetters = letterSet.replace(letterSet[probeIndex],"")
                wrongLetter = random.choice(wrongLetters)
                probeText = wrongLetter + " = " + str(probeIndex + 1)
        probeMessage = self.newMessage(self.fontObj, probeText)
        
        answeringMessage = self.newMessage(self.fontObj, "Answer")
        
        self.tasks.append(FullTask(self.screen, numberLetters, incorrectProbe, alphabetic, letterSet, probeText, attentionMessage, attentionTime, fixationMessage, fixationTime, instructionMessage, instructionTime, letterMessage, letterTime, delayMessage, delayTime, probeMessage, probeTime, answeringMessage, answerTime))
        
    def runTasks(self):
        for task in self.tasks:
            task.run()
        
    def beginning(self):
        logging.info(str(datetime.datetime.now()) + " beginning screen started")
        
        self.clearScreen()
        beginnningMessage = self.newMessage(self.fontObj,"Press up or down to begin")
        beginnningMessage.showMessage(self.screen)
        
        #Define a variable to control the beginning loop
        waiting = True         
        #Beginning loop
        while waiting:
            #Event handling, gets all events from the event queue so the program does not become unresponsive
            for event in pygame.event.get():
                #Check for left or right arrow key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        waiting = False
                        
        self.clearScreen()
        
        logging.info(str(datetime.datetime.now()) + " beginning screen ended")
                        
    def finished(self, waitTime = 15000):
        logging.info(str(datetime.datetime.now()) + " finish screen started")

        self.clearScreen()
        finishedMessage = self.newMessage(self.fontObj,"You have finished. Thank you")
        finishedMessage.showMessage(self.screen)
        
    def clearScreen(self):
        self.screen.fill((255,255,255))
        pygame.display.update()

class FullTask:
    def __init__(self, screen, numberLetters, incorrectProbe, alphabetic, letterSet, probeText, attentionMessage, attentionTime, fixationMessage, fixationTime, instructionMessage, instructionTime, letterMessage, letterTime, delayMessage, delayTime, probeMessage, probeTime, answeringMessage, answerTime):
        self.screen = screen
        self.numberLetters = numberLetters
        self.incorrectProbe = incorrectProbe
        self.alphabetic = alphabetic
        self.letterSet = letterSet
        self.probeText = probeText
        self.attentionMessage = attentionMessage
        self.attentionTime = attentionTime
        self.fixationMessage = fixationMessage
        self.fixationTime = fixationTime
        self.instructionMessage = instructionMessage
        self.instructionTime = instructionTime
        self.letterMessage = letterMessage
        self.letterTime = letterTime
        self.delayMessage = delayMessage
        self.delayTime = delayTime
        self.probeMessage = probeMessage
        self.probeTime = probeTime
        self.answeringMessage = answeringMessage
        self.answerTime = answerTime
        
        
    def wait(self, waitTime):
        #Define a variable to control the waiting loop
        waiting = True
        #Get time - for time limit
        waitBegin = pygame.time.get_ticks()
        #Waiting loop
        while waiting:
            waitingTime = pygame.time.get_ticks() - waitBegin 
            if waitingTime > waitTime:
                return
            for event in pygame.event.get(): None 
        
    def clearScreen(self):
        self.screen.fill((255,255,255))
        pygame.display.update()
        
    def run(self):
        #String to describe what type of task this is
        if self.alphabetic:
            taskType = "Alphabetic"
        else:
            taskType = "Forward"
        
        ##Attention
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task attention started")
        self.attentionMessage.showMessage(self.screen)
        self.wait(self.attentionTime)
        self.clearScreen()
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task attention ended")
        
        ##Fixation
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task fixation started")
        self.fixationMessage.showMessage(self.screen)
        self.wait(self.fixationTime)
        self.clearScreen()
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task fixation ended")
        
        ##Instruction
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task instruction started")
        self.instructionMessage.showMessage(self.screen)
        self.wait(self.instructionTime)
        self.clearScreen()
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task instruction ended")
        
        ##Letter set
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task show letter set started")
        self.letterMessage.showMessage(self.screen)
        self.wait(self.letterTime)
        self.clearScreen()
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task show letter set ended")
        
        ##Delay
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task give delay started")
        self.delayMessage.showMessage(self.screen)
        self.wait(self.delayTime)
        self.clearScreen()
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task give delay ended")

        #Get rid of any previous key presses before presenting the probe
        for event in pygame.event.get(): None 

        logging.info(str(datetime.datetime.now()) + " " + taskType + " task show probe started")
        self.probeMessage.showMessage(self.screen)
        self.wait(self.probeTime)
        self.clearScreen()
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task show probe ended")
        
        ##Answering
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task answering started")
        
        #Prompt for an answer
        self.answeringMessage.showMessage(self.screen)
        
        #Define a variable to control the answer loop
        running = True        
        #Variable to record whether an answer has already been given
        answered = False        
        #Get time - for time limit
        answerBegin = pygame.time.get_ticks()
         
        #Answering loop
        while running:
            answeringTime = pygame.time.get_ticks() - answerBegin 
            
            if answeringTime > 5000:
                if not answered:
                    responseTime = answeringTime
                    self.clearScreen()
                running = False
            
            if not answered:
                #Event handling, gets all events from the event queue so that the program does not freeze while waiting
                for event in pygame.event.get():
                    # Check the answer
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if not self.incorrectProbe:
                                logging.info(str(datetime.datetime.now()) + " Letter set was: " + self.letterSet + "    " + "Probe was: " + self.probeText + "    " + "Response was correct (participant said that the probe was a true statement)")
                                answered = True
                                responseTime = answeringTime
                                self.clearScreen()
                            else:
                                logging.info(str(datetime.datetime.now()) + " Letter set was: " + self.letterSet + "    " + "Probe was: " + self.probeText + "    " + "Response was incorrect (participant said that the probe was a true statement)")
                                answered = True
                                responseTime = answeringTime
                                self.clearScreen()
                        if event.key == pygame.K_DOWN:
                            if self.incorrectProbe:
                                logging.info(str(datetime.datetime.now()) + " Letter set was: " + self.letterSet + "    " + "Probe was: " + self.probeText + "    " + "Response was correct (participant said that the probe was a false statement)")
                                answered = True
                                responseTime = answeringTime
                                self.clearScreen()
                            else:
                                logging.info(str(datetime.datetime.now()) + " Letter set was: " + self.letterSet + "    " + "Probe was: " + self.probeText + "    " + "Response was incorrect (participant said that the probe was a false statement)")
                                answered = True
                                responseTime = answeringTime
                                self.clearScreen()
            else:
                #To stop it freezing after an answer has been given
                for event in pygame.event.get(): None 
                
        logging.info("Response time was: " + str(responseTime))
        logging.info(str(datetime.datetime.now()) + " " + taskType + " task answering ended")
        
class TaskMessage:
    def __init__(self, messageSurface, messageRect):
        self.messageSurface = messageSurface
        self.messageRect = messageRect
        
    def showMessage(self, screen):
        screen.blit(self.messageSurface, self.messageRect)
        pygame.display.update()

    

