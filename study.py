#!/bin/python3

import sys
import json
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
            "new" : self.new_cards, 
            "add":self.new_cards, 
            "study": self.study,
            "search": self.search,
            "delete": self.delete,
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
        f.write("{}")
        f.close()
        self.new_cards()
        
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

    def search(self):
        pass

    def reset(self):
        c = cardList()
        c.get(self.path)
        c.reset(self.path)
    
    def delete(self):
        pass
    
    def reverse(self):
        c = cardList()
        c.get(self.path)
        c.reverse(self.path)

class studyClass:
    def __init__(self, path):
        self.path = path
        cardL = cardList()
        cardL.get(path)
        self.cardList = cardL
        
        self.isKnownList = []
        for i in range(len(self.cardList)):
            self.isKnownList.append(False)
        
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
                correct = input("incorrect: " + i.solution + "      (\"r\" to count as correct, \"c\"/\"w\" to replace current, Enter to continue)")
                if correct == "r":
                    i.reverseGuess()
                elif correct == "c":
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

    def add_new(self, cardItem):
        self.append(cardItem)
        self.list.append(cardItem.dict)

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
        for i in data:
            t = i["text"]
            s = i["solution"]
            c = i["timesCorrect"]
            ic = i["timesIncorrect"]
            tp = i["timesPlayed"]

            newCard = card(t, s, c, ic, tp)
            self.add_new(newCard)

    def save(self, path, output = True):
        if output:
            print("\nsaved...")
        # open file, write
        dataJSON = json.dumps(self.list, indent=2)
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