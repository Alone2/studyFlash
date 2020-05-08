import sys
import json
import os
from pathlib import Path

class editClass:
    def __init__(self, path, startComments, replaceQuestion, replaceAnswer):
        self.path = path

        self.c = cardList()
        self.c.get(self.path)

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
        self.originalOutput = self.__getUserInput(self.all_words)
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
            self.__errorHandling()
            return
        # remove from list
        minus = 0
        for i in remove_from_list:
            self.c.remove(i - minus)
            minus += 1
        # save
        self.c.save(self.path)
    
    def __errorHandling(self):
        a = input("Formattig error, type \"r\" to re-edit file, \"d\" to discard changes, \"s\" to save as temp file ")
        # rewrite stuff
        if a == "r":
            self.originalOutput = self.__getUserInput(self.originalOutput)
            self.checkOutput()
    
            sys.exit()
        # just close
        if a == "d":
            sys.exit()
        # save everything
        if a == "s":
            self.__saveFile(input("Filename to save: "), self.originalOutput)
            sys.exit()

        self.__errorHandling()
    
    def __getUserInput(self, all_words):
        # open temp file 
        cur_path = self.path + ".tempWords"
        self.__saveFile(cur_path, all_words)
        
        # user can chage file
        os.system(self.c.standartTextEdit + " " + cur_path)

        # read temp file after user input
        f = open(cur_path, "r")
        originalOutput = f.read()
        f.close()

        os.remove(cur_path)

        return originalOutput

    @staticmethod
    def __saveFile(path, text):
        f = open(path, "w+")
        f.write(text)
        f.close()

class studyClass:
    def __init__(self, path):
        self.path = path
        cardL = cardList()
        cardL.get(path)
        self.cardList = cardL
        
        self.isKnownList = []
        for i in self.cardList:
            self.isKnownList.append(self.isKnown(i))
        
        self.evilLoop()
    
    def evilLoop(self):
        self.cardList
        for num in range(len(self.cardList)):
            # Tests if word is known
            if self.isKnownList[num]:
                continue
            # Question input
            i = self.cardList[num]
            inp = input("\nQuestion: " + i.text + " -> ")

            # Tests if input matchs answer
            if i.guess(inp):
                input("correct!      (Enter to continue)")
            # If incorrect, asks if typo
            else:
                correct = input("incorrect: " + i.solution + "      (\"c\" -> correct (typo), \"r\" -> replace (correct), \"w\" -> replace with sth new, Enter -> continue)")
                if correct == "c":
                    i.reverseGuess()
                elif correct == "r":
                    i.solution = inp
                    i.toDict()
                    i.reverseGuess()
                elif correct == "w":
                    i.solution = input("correct: ")
                    i.toDict()
                else:
                # if really incorrect 
                    self.retypeUntilCorrect(i.solution)
            
            # Test if user knows the word
            if self.isKnown(i):
                self.isKnownList[num] = True
            
            # Saves everything
            self.cardList.save(self.path, False)
        
        # repeats itself
        self.evilLoop()
    
    def isKnown(self, myCard):
        # "algorithm" (later on: customizable)
        # When times the word was anwered correctly is bigger than incorrectly -> user knows the word
        # Usable stuff: timesPlayed, timesCorrect, timesIncorrect
        # (TODO:) Maybe add: streak 
        if myCard.timesCorrect > myCard.timesIncorrect and myCard.timesCorrect > 2:
            return True
        return False
    
    def retypeUntilCorrect(self, text):
        inp = input("Type: " + text + " -> ")
        if inp != text: 
            return self.retypeUntilCorrect(text)

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
            self.streak = 0
            self.toDict()
            return False

    def reverseGuess(self):
        self.timesIncorrect -= 1 
        self.timesCorrect += 1
        self.streak = self.streakBefore

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

            newCard = card(t, s, c, ic, tp)
            self.add_new(newCard)
        
        self.__change_config(data["config"])

    def __change_config(self, config):
        self.config = config
        self.standartTextEdit = config["standartTextEditor"]

    def toDict(self):
        self.config["standartTextEditor"] = self.standartTextEdit
        
    def save(self, path, output = True, outputTxt = "saved..."):
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
        f.write(json.dumps({"cards":{}, "config":{"standartTextEditor":editor}}))
        f.close()
        print(success)
    
    def reverse(self, path):
        for i in self:
            i.reverse()
        self.save(path)

    def reset(self, path):
        for i in self:
            i.timesCorrect = 0
            i.timesIncorrect = 0
            i.timesPlayed = 0
            i.toDict()
        self.save(path)