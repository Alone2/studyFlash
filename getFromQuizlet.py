#!/bin/python3

import sys
import json
import os
from pathlib import Path
import urllib.request
import study

class main:
    def __init__(self):
        # Tests if arguments there
        if len(sys.argv) < 3:
            print("needs 2 arguments ( [quizlet link] [filename] )")
            return
        
        arguments = sys.argv[1:]
        link = arguments[0]
        path = arguments[1]

        # new file
        main = study.main()
        main.new_file(path)
        # new Card from Quizlet
        myCard = self.cardsFromQuizlet(link, path)
        # save
        myCard.save(path)

        print("Created file from Quizlet. Study: ./study.py study [FILENAME]")
  
        # get between window.Quizlet.setPageData = {  und }
        # need urllib
        # to save card maybe import other script
    
    # returns cards
    def cardsFromQuizlet(self, link, path):
        # get from website
        html = str(urllib.request.urlopen(link).read().decode("utf-8"))
        find1String = "window.Quizlet.setPageData = "
        found1 = html.find(find1String)
        html = html[found1 + len(find1String):]
        found2 = html.find("; QLoad('Quizlet.setPageData');")
        html = html[:found2]

        # to array
        #html = html.replace("\\", "")
        jsonData = json.loads(html)

        # new cards List
        #print(json.dumps(jsonData["termIdToTermsMap"], indent=3))
        cards = study.cardList()
        cards.get(path)
        for key,value in jsonData["termIdToTermsMap"].items():
            #print(key, value)
            c = study.card(value["word"], value["definition"])
            cards.add_new(c)

        return cards


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Save exit comming soon!
        print("\n")
        sys.exit()
