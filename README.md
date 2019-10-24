
# studyFlash
A python script to learn flashcards inside your terminal (for language learning)

## Table of Contents
1. [Usage](#usage)
1.1. [Create Flashcard File](#create)
1.2. [Add Cards](#add)
1.3. [Import from Quzlet](#import)
1.5. [Study](#learn)
1.4. [Edit Cards](#edit)
1.6. [Reset Statistics](#reset)
1.7. [Replace Solution by Answers](#solutions)

## Usage <a name="usage"></a>

### Create a Flashcard File (.json)  <a name="create"></a>
```
./study.py new FILENAME.json
```

A file is being created. You can add your questions / solutions with ```./study.py add FILENAME.json``` or ```./study.py edit FILENAME.json``` (opens with text editor, default -> vim)


### Add Cards to File  <a name="add"></a>
```
./study.py add FILENAME.json
```

You need to type your questions / solutions


### Import Cards from Quizlet <a name="import"></a>
```
./getFromQuizlet.py QUIZLET_LINK FILENAME.json
```

Creates a new file with cards from Quizlet. 
When the file already exists, the cards are going to be added to the existing ones.


### Study Cards <a name="learn"></a>
```
./study.py study FILENAME.json
```

The script now asks you your flashcards. 
You need to type them correctly.
If made a typo you can press "r" to count your answer as correct.

If the number of you knowing the correct answer is bigger than of you not knowing the answer, the word will not appear any more. 

(use ctrl+c to return to terminal)


### Edit your Cards <a name="edit"></a>
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
### Reset your Statistics  <a name="reset"></a>
```
./study.py reset FILENAME.json
```

The script resets the number of you knowing the correct/wrong answer, so you can start studying from scratch again.


### Learn Words by Solution <a name="solution"></a>
```
./study.py reverse FILENAME.json
```

Use that command if you want to switch your solutions with your anwsers.

