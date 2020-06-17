import sys
import time
import json
import os
import random
import curses
import locale
from pathlib import Path
from curses.textpad import rectangle
from studyFlash import graphics

class inputField():
    @classmethod
    def __init__(cls):
        # locale.setlocale(locale.LC_ALL, '')
        # cls.code = locale.getpreferredencoding()
        cls.stdscr = curses.initscr()
        # Do not echo input
        curses.noecho()
        # respond to keys immediately (don't wait for enter)
        curses.cbreak()
        # Capture keys
        cls.stdscr.keypad(True)
        # position stuff
        maxwh = cls.stdscr.getmaxyx()
        cls.maxx = maxwh[1]
        cls.maxy = maxwh[0]

    # @classmethod
    # def validator(cls, keystroke):
        # print(keystroke) 
        # print(str(curses.keyname(keystroke)).encode(cls.code))
        # time.sleep(5)
        # if keystroke == curses.KEY_ENTER or keystroke == 10 or keystroke == 13:
            # return 7
        # cls.box.do_command(keystroke)
        # return keystroke
        # return keystroke
    
    @classmethod
    def setQuestion(cls, title, text="", underline="", justWait = False, noUserInput = False):
        cls.stdscr.erase()
        # draw rectangle
        editwin = curses.newwin(5,cls.maxx-4, cls.maxy-9,2)
        rectangle(cls.stdscr, cls.maxy-10, 1, cls.maxy-4, 1+cls.maxx-4+1)
        # new textbox
        cls.box = graphics.Textbox(editwin)
        # Title, text and underline
        cls.stdscr.addstr(cls.maxy-16, 2, title, curses.A_BOLD) 
        cls.stdscr.addstr(cls.maxy-13, 2, text) 
        cls.stdscr.addstr(cls.maxy-3, 2, underline) 
        # refesh screen
        cls.stdscr.refresh()
        # if just want char
        if justWait:
            char = cls.stdscr.getch()
            return curses.keyname(char).decode("utf-8") 
        # get user input
        if not noUserInput:
            return cls.box.gather()
        return ""
    @classmethod
    def close(cls):
        cls.stdscr.clear()
        cls.stdscr.refresh()
        try:
            os.system("stty sane")
        except:
            pass

class editParent:
    def __init__(self, path):
        # get card
        self.path = path
        self.c = cardList()
        self.c.get(self.path)
        self.ending = ".tempWords"

    def _errorHandling(self, retryfunc):
        a = input("Formattig error, type \"r\" to re-edit file, \"d\" to discard changes, \"s\" to save as temp file ")
        # rewrite stuff
        if a == "r":
            self.originalOutput = self._getUserInput(self.originalOutput)
            retryfunc()
    
            sys.exit()
        # just close
        if a == "d":
            sys.exit()
        # save everything
        if a == "s":
            self._saveFile(input("Filename to save: "), self.originalOutput)
            sys.exit()

        self._errorHandling(retryfunc)
    
    def _getUserInput(self, all_words):
        # open temp file 
        cur_path = self.path + self.ending
        self._saveFile(cur_path, all_words)
        
        # user can chage file
        os.system(self.c.standartTextEdit + " " + cur_path)

        # read temp file after user input
        f = open(cur_path, "r")
        originalOutput = f.read()
        f.close()

        os.remove(cur_path)

        return originalOutput

    @staticmethod
    def _saveFile(path, text):
        f = open(path, "w+")
        f.write(text)
        f.close()

class editTestCorrect(editParent):
    def __init__(self, path):
        super().__init__(path)
        self.ending = ".tempwords.py"
        self.testcase = self.c.correcttest
        # Get user input
        self.originalOutput = self._getUserInput(self.testcase)
        self.c.correcttest = self.originalOutput
        # Save
        self.c.save(self.path)

class editClass(editParent):
    def __init__(self, path, startComments, replaceQuestion, replaceAnswer):
        super().__init__(path)
        self.all_words = startComments
        self.all_words_newline_count = self.all_words.count("\n")

        self.replaceQuestion = replaceQuestion
        self.replaceAnswer = replaceAnswer

        # if no cards -> dummy cards
        if len(self.c) < 1:
            a = card(self.replaceQuestion, self.replaceAnswer)
            self.c.add_new(a)
        
        for i in self.c:
            self.all_words +="\n" + i.text + "\n" + i.solution + "\n"
        self.oldOutput = self.all_words.split("\n")
        
        # Get user input
        self.originalOutput = self._getUserInput(self.all_words)
        # Save input
        self.checkOutput()
    
    def checkOutput(self):
        # User input saved
        output = self.originalOutput.split("\n")
        cl = 0
        isError = False
        remove_from_list = []
        for i in range(self.all_words_newline_count + 1, len(output), 3):
            # If error
            if output[i] == "" or output[i+1] == "":
                isError = True
                break
            # If delete
            if output[i] == "###" or output[i+1] == "###":
                remove_from_list.append(cl)
            # If new words -> append
            if cl+1 > (len(self.oldOutput) - 2)/3:
                new_card = card(output[i], output[i+1])
                self.c.add_new(new_card)
                continue
            
            self.c[cl].text = output[i]
            self.c[cl].solution = output[i+1]
            self.c[cl].toDict()
            cl += 1
        # if error
        if isError:
            self._errorHandling(self.checkOutput)
            return
        # remove from list
        minus = 0
        for i in remove_from_list:
            self.c.remove(i - minus)
            minus += 1
        # save
        self.c.save(self.path)

class studyClass:
    def __init__(self, path):
        self.path = path
        cardL = cardList()
        cardL.get(path)
        self.cardList = cardL
        self.inpField = inputField()
        
        self.isKnownList = []
        for i in self.cardList:
            self.isKnownList.append(self.isKnown(i))
    
    def evilLoop(self):
        # Error when window too small
        try:
            self.inpField.setQuestion("starting...", noUserInput=True)
        except:
            self.inpField.close()
            print("Your terminal-window is probably too small to display the UI of studyflash.\nMake it bigger and retry")
            return
        # Study Loop
        while(True):
            # Shuffle, if requested
            if self.cardList.autoshuffle:
                self.cardList.shuffle()
            knownNumber = 0
            for num in range(len(self.cardList)):
                # Tests if word is known
                if self.isKnownList[num]:
                    knownNumber += 1
                    continue
                # Question input
                i = self.cardList[num]
                inp = self.inpField.setQuestion("Question", text=i.text, underline="Type the answer and click enter to submit\n  Press 'ctrl+c' to exit")

                # Shows user answer in comparison to correct answer
                replyW = "Your answer:     " + inp +  "\n  Correct answer:  " + i.solution
                replyC = "Answer:           " + inp 
                # Tests if input matchs answer
                if i.guess(inp):
                    self.inpField.setQuestion("correct! \n\n  Question:        "+ i.text, text=replyC, underline="(Enter to continue)", justWait=True)
                # If incorrect, asks if typo
                else:
                    correct = self.inpField.setQuestion("incorrect \n\n  Question:        " + i.text, text=replyW, underline="\"c\" -> correct (typo), \"r\" -> replace (correct) \n  \"w\" -> replace with sth new, Enter -> continue", justWait=True)
                    if correct == "c":
                        i.reverseGuess()
                    elif correct == "r":
                        i.solution = inp
                        i.toDict()
                        i.reverseGuess()
                    elif correct == "w":
                        i.solution = self.inpField.setQuestion("correct", "old: " + i.text + " -> " + i.solution, underline="Type the new correct answer")
                        i.toDict()
                    else:
                    # if really incorrect 
                        self.retypeUntilCorrect(i.solution, i.text)
                
                # Test if user knows the word
                if self.isKnown(i):
                    knownNumber += 1
                    self.isKnownList[num] = True
                
                # Saves everything
                self.cardList.save(self.path, False)
            # Checks if user knows every word 
            if knownNumber >= len(self.cardList):
                self.inpField.close()
                print("Congratulations! You mastered every card! \nUsing 'studyflash reset FILENAME' you can reset your statistics and start once again!")
                break
    
    def isKnown(self, card):
        # customizable algorithm
        # myCard.timesCorrect > myCard.timesIncorrect and myCard.timesCorrect > 2:
        req = "ctest = (" + self.cardList.correcttest + ")" 
        ldict = {"card":card}
        try:
            exec(req, globals(), ldict)
        except:
            self.inpField.close()
            print("Your condition for knowing if a card is mastered has an error.")
            print("Change it using: studyflash condition FILENAME")
            sys.exit()
        ctest = ldict['ctest']
        if ctest:
            return True
        return False
    
    def retypeUntilCorrect(self, text, oldtxt):
        inp = self.inpField.setQuestion("incorrect ", text= oldtxt + " -> " + text, underline="Type the correct answer")
        if inp != text: 
            return self.retypeUntilCorrect(text, oldtxt)

    def generateList(self):
        # List are going to be sorted here
        # Idea: save the cards to study with their array id, because we wanna save the whole list later on
        return self.cardList


class card:
    def __init__(self, text, solution, timesCorrect = 0, timesIncorrect = 0, timesPlayed = 0, streak = 0):
        self.dict = {}

        self.text = text
        self.solution = solution
        self.timesCorrect = timesCorrect
        self.timesIncorrect = timesIncorrect
        self.timesPlayed = timesPlayed
        self.streak = streak
        self.streakBefore = streak

        self.toDict()

    def toDict(self):
        self.dict["text"] = self.text
        self.dict["solution"] = self.solution
        self.dict["timesCorrect"] = self.timesCorrect
        self.dict["timesIncorrect"] = self.timesIncorrect
        self.dict["timesPlayed"] = self.timesPlayed
        self.dict["streak"] = self.streak
    
    def guess(self, text):
        self.timesPlayed += 1
        if text == self.solution:
            self.timesCorrect += 1
            self.streakBefore = self.streak
            self.streak += 1
            self.toDict()
            return True
        else:
            self.timesIncorrect += 1
            self.streakBefore = self.streak
            self.streak = 0
            self.toDict()
            return False

    def reverseGuess(self):
        self.timesIncorrect -= 1 
        self.timesCorrect += 1
        self.streak = self.streakBefore + 1
        self.toDict()

    def reverse(self):
        t = self.text 
        s = self.solution
        self.text = s
        self.solution = t
        self.toDict()

class cardList(list):
    def __init__(self):
        self.list = []
        self.config = {}
        self.autoshuffle = False

    def add_new(self, cardItem):
        self.append(cardItem)
        self.list.append(cardItem.dict)

    def remove(self, index):
        del self[index]
        del self.list[index]

    def get(self, path, error="File not found!"):
        # open file, read
        try:
            jsonFile = open(path, 'r')
            data = json.loads(jsonFile.read())
            jsonFile.close()
        except FileNotFoundError:
            print(error)
            sys.exit()
        
        # create new cards with data
        for i in data["cards"]:
            t = i["text"]
            s = i["solution"]
            c = i["timesCorrect"]
            ic = i["timesIncorrect"]
            tp = i["timesPlayed"]
            try:
                st = i["streak"]
            except:
                st = 0

            newCard = card(t, s, c, ic, tp, st)
            self.add_new(newCard)
        
        self.__change_config(data["config"])

    def __change_config(self, config):
        self.config = config
        self.standartTextEdit = config["standartTextEditor"]
        try:
            self.autoshuffle = config["shuffle"]
            self.correcttest = config["correcttest"]
        except:
            self.autoshuffle = False
            self.correcttest = "# It is defined here when a card counts as mastered and will \n"
            self.correcttest += "# not be asked again. \n"
            self.correcttest += "# (reset statistics to study cards again with: 'studyflash reset FILENAME')\n"
            self.correcttest += "\n# Syntax: A python boolean is defined\n"
            self.correcttest += "# You can use 'and' and 'or' to combine statements (see example 2)\n"
            self.correcttest += "\n# Parameters you can use:\n"
            self.correcttest += "# card.timesCorrect: How many times your answer was correct\n"
            self.correcttest += "# card.timesIncorrect: How many times your answer was incorrect\n"
            self.correcttest += "# card.timesPlayed: How many times you answered the question\n"
            self.correcttest += "# card.streak: Your current streak on how many times you're answer was correct.\n"
            self.correcttest += "\n# Example 1: \n"
            self.correcttest += "# card.streak > 2\n"
            self.correcttest += "# Explanation: Card needs to be guessed correctly more than 3 times in a row:\n"
            self.correcttest += "# for it to not appear anymore and be marked as mastered\n"
            self.correcttest += "\n# Example 2 ():\n"
            self.correcttest += "# card.timesCorrect > card.timesIncorrect and card.timesCorrect > 2\n"
            self.correcttest += "# Explanation: You need to have guessed the card correctly more times than you guessed it incorrectly\n"
            self.correcttest += "# and the card has to be answered correctly more than 2 times for it to not appear again.\n"
            self.correcttest += "\n# Example 3: \n"
            self.correcttest += "# False\n"
            self.correcttest += "# Explanation: Never sort a card out. Every card will be asked everytime \n"
            self.correcttest += "# even if you answered the question correctly 100x times. \n"
            self.correcttest += "\n# Current configuration: You need to have a streak of more or equal to 2\n"
            self.correcttest += "# and need to have answered the question correctly at least 3 times:\n"
            self.correcttest += "card.timesCorrect > 2 and card.streak >= 2"
        self.__set_config()
    
    def __set_config(self):
        self.config = {"standartTextEditor":self.standartTextEdit, "shuffle":self.autoshuffle, "correcttest":self.correcttest}

    def toDict(self):
        self.config["standartTextEditor"] = self.standartTextEdit
        
    def save(self, path, output = True, outputTxt = "saved..."):
        self.__set_config()
        if output:
            print("\n" + outputTxt)
        # open file, write
        dataJSON = json.dumps({"cards":self.list, "config":self.config}, indent=2)
        jsonFile = open(path, 'w')
        jsonFile.write(dataJSON)
        jsonFile.close()

    def new(self, path, success = "", errormsg = "File is alredy here!", editor = "vi"):
        if path:
            self.path = path
        p = Path(self.path)
        if p.exists():
            print(errormsg)
            return
        f = open(self.path,"w+")
        f.write(json.dumps({"cards":{}, "config":{"standartTextEditor":editor,"shuffle":False}}))
        f.close()
        print(success)
    
    def reverse(self, path):
        for i in self:
            i.reverse()
        self.save(path)

    def shuffle(self):
        for i in range(len(self)):
            r = random.randint(0, len(self)-1)  
            self[i], self[r] = self[r], self[i]

    def shuffleEverything(self, path):
        for i in range(len(self)):
            r = random.randint(0, len(self)-1)  
            self[i], self[r] = self[r], self[i]
            self.list[i], self.list[r] = self.list[r], self.list[i]
        self.save(path)
    
    def reset(self, path):
        for i in self:
            i.timesCorrect = 0
            i.timesIncorrect = 0
            i.timesPlayed = 0
            i.toDict()
        self.save(path)
