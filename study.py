import sys
import json
from pathlib import Path

class main:
    def __init__(self):
        # Tests if arguments there
        if len(sys.argv) < 3:
            print("needs 2 arguments ( [action] [storage filename] )")
            return
        
        arguments = sys.argv[1:]
        self.path = arguments[1]

        if arguments[0] == "new":
            self.new_file()
            return
        if arguments[0] == "add":
            self.new_cards()
            return
        if arguments[0] == "remove":
            pass

        if arguments[0] == "search":
            pass

        if arguments[0] == "study":
            studyClass(self.path)
            return
        if arguments[0] == "config":
            pass

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


class studyClass:
    def __init__(self, path):
        self.path = path
        cardL = cardList()
        cardL.get(path)
        self.cardList = cardL
        self.evilLoop()
    
    def evilLoop(self):
        l = self.generateList()
        for i in l:
            inp = input("\nQuestion: " + i.text + " -> ")
            if i.guess(inp):
                input("correct!      (Enter to continue)")
                continue
            correct = input("incorrect: " + i.solution + "      (\"r\" to count as correct, Enter to continue)")
            if correct == "r":
                i.reverseGuess()
                continue
            self.retypeUntilCorrect(i.solution)
        self.evilLoop()
    
    def retypeUntilCorrect(self, text):
        inp = input("Type " + text + " -> ")
        if inp != text: 
            return self.retypeUntilCorrect(text)

    def generateList(self):
        # List are going to be sorted here
        return self.cardList


class card:
    def __init__(self, text, solution, timesCorrect = 0, timesIncorrect = 0, timesPlayed = 0):
        self.dict = {}

        self.text = text
        self.dict["text"] = text

        self.solution = solution
        self.dict["solution"] = solution

        self.timesCorrect = timesCorrect
        self.dict["timesCorrect"] = timesCorrect

        self.timesIncorrect = timesIncorrect
        self.dict["timesIncorrect"] = timesIncorrect

        self.timesPlayed = timesPlayed
        self.dict["timesPlayed"] = timesPlayed
    
    def guess(self, text):
        self.timesPlayed += 1
        if text == self.solution:
            self.timesCorrect += 1
            return True
        else:
            self.timesIncorrect += 1
            return False

    def reverseGuess(self):
        self.timesIncorrect -= 1 
        self.timesCorrect += 1

    def reverse(self):
        t = self.text 
        s = self.solution
        self.text = s
        self.solution = t

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

    def save(self, path):
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Save exit comming soon!
        sys.exit()