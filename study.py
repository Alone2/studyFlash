#!/bin/python3

import sys
import json
import os
from pathlib import Path

class main:
    def __init__(self):
        # Tests if arguments there
        if len(sys.argv) < 3:
            print("needs 2 arguments ( [action] [filename] )")
            return
        
        arguments = sys.argv[1:]
        self.path = arguments[1]

        keywords = {
            "new" : self.new_file, 
            "add":self.new_cards, 
            "study": self.study,
            "edit": self.edit,
            "reset": self.reset,
            "reverse": self.reverse
        }
        
        for i,y in keywords.items():
            if self.testIfArgument(i, arguments[0], y):
                break

    def testIfArgument(self, arg, text, func):
        if arg == text:
            func()
            return True

    def new_file(self):
        p = Path(self.path)
        if p.exists():
            print("File is alredy here!")
            return
        f = open(self.path,"w+")
        f.write(json.dumps({"cards":{}, "config":{"standartTextEditor":"vi"}}))
        f.close()
        print("File created, add cards by typing: ./study.py add [FILENAME]  or  ./study edit [FILENAME]")
        
    def new_cards(self):
        # Cards are taken out of file
        cList = cardList()
        cList.get(self.path)

        print("You are in an endless cicle of typing questions / answers. Press ctrl+c to free yourself. Enjoy!\n")
        
        try:
            while True:
                question = input("Question: ")
                solution = input("Solution: ")
            
                ca = card(question, solution)
                cList.add_new(ca)
                print()
        except KeyboardInterrupt:
            cList.save(self.path)

    def study(self):
        studyClass(self.path)

    def reset(self):
        c = cardList()
        c.get(self.path)
        c.reset(self.path)
    
    def edit(self):
        editClass(self.path)

    def reverse(self):
        c = cardList()
        c.get(self.path)
        c.reverse(self.path)

class editClass:
    def __init__(self, path):
        self.path = path

        self.c = cardList()
        self.c.get(self.path)

        self.all_words = "# When adding cards -> put them after the existing ones!\n"
        self.all_words += "# Delete a card by replacing the question or solution with '###'\n"
        self.all_words += "# Put an empty line between two cards\n"

        # if no cards -> dummy cards
        if len(self.c) < 1:
            a = card("Replace me with a real question", "Replace me with a real answer")
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
        for i in range(4, len(output), 3):
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
                correct = input("incorrect: " + i.solution + "      (\"c\" -> correct (typo), \"r\" -> replace (correct), \"w\" replace with sth new, Enter to continue)")
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
            
            # When times the word was correct is bigger than incorrect -> user knows the word
            if i.timesCorrect > i.timesIncorrect:
                self.isKnownList[num] = True
            
            # Saves everything
            self.cardList.save(self.path, False)
        
        # repeats itself
        self.evilLoop()
    
    def isKnown(self, i):
        # very complex algorithm
        if i.timesCorrect > i.timesIncorrect and i.timesCorrect > 2:
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
    def __init__(self, text, solution, timesCorrect = 0, timesIncorrect = 0, timesPlayed = 0):
        self.dict = {}

        self.text = text
        self.solution = solution
        self.timesCorrect = timesCorrect
        self.timesIncorrect = timesIncorrect
        self.timesPlayed = timesPlayed

        self.toDict()

    def toDict(self):
        self.dict["text"] = self.text
        self.dict["solution"] = self.solution
        self.dict["timesCorrect"] = self.timesCorrect
        self.dict["timesIncorrect"] = self.timesIncorrect
        self.dict["timesPlayed"] = self.timesPlayed
    
    def guess(self, text):
        self.timesPlayed += 1
        if text == self.solution:
            self.timesCorrect += 1
            self.toDict()
            return True
        else:
            self.timesIncorrect += 1
            self.toDict()
            return False

    def reverseGuess(self):
        self.timesIncorrect -= 1 
        self.timesCorrect += 1

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

    def get(self, path):
        # open file, read
        try:
            jsonFile = open(path, 'r')
            data = json.loads(jsonFile.read())
            jsonFile.close()
        except FileNotFoundError:
            print("File not found: create new with 'study.py new [FILENAME]'")
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
        
    def save(self, path, output = True):
        if output:
            print("\nsaved...")
        # open file, write
        dataJSON = json.dumps({"cards":self.list, "config":self.config}, indent=2)
        jsonFile = open(path, 'w')
        jsonFile.write(dataJSON)
        jsonFile.close()

    
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Save exit comming soon!
        print("\n")
        sys.exit()