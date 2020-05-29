#!/bin/python3

import sys
import json
import csv
from studyFlash import study

class csv_class:
    def __init__(self, cvsFile, cardsFile):
        self.cvsFile = cvsFile
        self.cardsFile = cardsFile

        # new file
        study.cardList().new(
            self.cardsFile, errormsg="File is already here.\nAppending flashcards to existing ones...")

    # importing
    def import_csv(self):
        k = 0 
        myCard = None
        for i in [";", "\t", ","]:
            try:
                k += 1
                myCard = self.cardsFromFile(self.cvsFile,self.cardsFile,i)
                break
            except Exception:
                pass
        if (k <= 0):
            print("Error opening file...")
            return
        myCard.save(self.cardsFile)
        print("Created studyflash file from a CSV file\n ")
    
    # export csv
    def export_csv(self, delimiter = '\t'):
        cards = study.cardList()
        cards.get(self.cardsFile)
        with open(self.cvsFile, 'w', newline='') as csvfile:
            w = csv.writer(csvfile, delimiter=delimiter)
            for c in cards:
                w.writerow([c.text, c.solution])
        print("Exported cards to CSV file\n ")

    # returns cards
    def cardsFromFile(self, inp, path, delimiter):
        cards = study.cardList()
        cards.get(path)
        i = 0
        with open(inp) as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row in reader:
                i += 1
                if len(row) <= 1 and i > 1:
                    raise Exception()
                elif len(row) <= 1:
                    continue
                c = study.card(row[0], row[1])
                cards.add_new(c)
        return cards
