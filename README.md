# studyFlash
A python script to learn flashcards inside your terminal (for language learning)

## Usage
### Create a Flashcard File (.json)
```
./study.py new FILENAME.json
```

A file is being created. You can add your questions / solutions with ```./study.py add FILENAME.json``` or ```./study.py edit FILENAME.json``` (opens with text editor, default -> vim)


### Add Cards to File
```
./study.py add FILENAME.json
```

You need to type your questions / solutions


### Learn Words
```
./study.py study FILENAME.json
```

The script now asks you your flashcards. 
You need to type them correctly.
If made a typo you can press "r" to count your answer as correct.

If the number of you knowing the correct answer is bigger than of you not knowing the answer, the word will not appear any more. 

(use ctrl+c to return to terminal)


### Edit your Cards
```
./study.py edit FILENAME.json
```

Vim opens with all your cards in it. 
You can change all the answers/questions of your flashcards. 
Deleting a card by renaming the answer/question to '###' is also possible.
You can also add cards by adding them at **the end** of the document.

Here an example file with 3 cards in it:
```
# When adding cards -> put them after the existing ones!
# Delete a card by replacing the question or solution with '###'
# Put an empty line between cards

A random question 
A random answer

Turtle 
Schildkröte
 
Something 
Something in another language
```
### Reset your Statistics 
```
./study.py reset FILENAME.json
```

The script resets the number of you knowing the correct/wrong answer, so you can start studying from scratch again.


### Learn Words by Solution
```
./study.py reverse FILENAME.json
```

Use that command if you want to switch your solutions with your anwsers.
