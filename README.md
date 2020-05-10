
# studyFlash
A python application for learning flashcards inside your terminal (for language learning)

<img src="https://github.com/Alone2/studyFlash/blob/master/images/sample.png" width="400">

## Table of Contents
1. [Installation](#installation)
   1. [With pip](#pip)
   1. [Arch Linux (AUR)](#aur)
1. [Usage](#usage)
   1. [Create Flashcard File](#create)
   2. [Add Cards](#add)
   3. [Import from Quizlet](#import)
   5. [Learn Cards](#learn)
   4. [Edit Cards](#edit)
   4. [Change Default Editor](#editor)
   4. [Shuffle Cards](#shuffle)
   4. [Condition for Card to be Mastered](#mastered)
   6. [Reset Statistics](#reset)
   7. [Replace Solution with Answers](#solution)

## Installation <a name="installation"></a>

### With pip <a name="pip"></a>
Clone the git repo and install the application: 
```
git clone https://github.com/Alone2/studyFlash.git
sudo pip install ./studyFlash
```
When the command above returns an error message you can also try: 

```sudo pip3 install ./studyFlash``` or ```sudo python3 -m pip install ./studyFlash``` 

Uninstall the application:
```
sudo pip uninstall studyFlash
```
### Arch Linux (AUR) <a name="aur"></a>
studyFlash is in the AUR ([link](https://aur.archlinux.org/packages/studyflash/))

Install it [manually](https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages) or with your favorite AUR helper:
```
yay -S studyflash
```


## Usage <a name="usage"></a>

### Create a Flashcard File (.json)  <a name="create"></a>
```
studyflash new FILENAME.json
```

A file is being created. You can add your questions / solutions with ```studyflash add FILENAME.json``` or ```studyflash edit FILENAME.json``` (opens with text editor, default -> vim)


### Add Cards to File  <a name="add"></a>
NOTE: It is recommended to use [edit](#edit) for adding cards, because you currently [cannot fix typos](https://github.com/Alone2/studyFlash/issues/2#issuecomment-626209501) with add.
```
studyflash add FILENAME.json
```

You need to type your questions / solutions


### Import Cards from Quizlet <a name="import"></a>
```
studyflash-quizlet QUIZLET_LINK FILENAME.json
```

Creates a new file with cards from Quizlet. 
When the file already exists, the cards are going to be added to the existing ones.


### Learn Cards <a name="learn"></a>
```
studyflash study FILENAME.json
```

The script now asks you for your flashcards. 
You need to type them correctly.
If you made a typo you can press "c" to count your answer as correct.

You can [configure](#mastered) when a card counts as mastered and will not appear again.

(use ctrl+c to return to terminal)


### Edit your Cards <a name="edit"></a>
```
studyflash edit FILENAME.json
```

Vi opens with all your cards in it. (Vi can be difficult for beginners. Change your editor like [this](#editor))

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

### Change your Default Editor <a name="editor"></a>
Change your editor from vi to something different. 
```
studyflash editor FILENAME.json EDITOR
```
I suggest to use nano, if you're a beginner:
```
studyflash editor FILENAME.json nano
```

### Shuffle your Cards  <a name="shuffle"></a>
You can either shuffle your cards manually  with```studyflash shuffle FILENAME.json``` 
or enable automatic shuffling: 
```
studyflash shuffle-auto FILENAME.json
```

Once enabled, you can disable automatic shuffling like this: ```studyflash shuffle-manual FILENAME.json``` 

### Condition for Card to be Mastered <a name="mastered"></a>
You can configure if when a card will no longer appear and is mastered using:
```
studyflash condition FILENAME.json
```

The following explanation will appear. You can change the last line to your liking to configure when a card counts as mastered:
```
# It is defined here when a card counts as mastered and will 
# not be asked again. 
# (reset statistics to study cards again with: 'studyflash reset FILENAME')

# Syntax: A python boolean is defined
# You can use 'and' and 'or' to combine statements (see example 2)

# Parameters you can use:
# card.timesCorrect: How many times your answer was correct
# card.timesIncorrect: How many times your answer was incorrect
# card.timesPlayed: How many times you answered the question
# card.streak: Your current streak on how many times you're answer was correct.

# Example 1: 
# card.streak > 2
# Explanation: Card needs to be guessed correctly more than 3 times in a row:
# for it to not appear anymore and be marked as mastered

# Example 2 ():
# card.timesCorrect > card.timesIncorrect and card.timesCorrect > 2
# Explanation: You need to have guessed the card correctly more times than you guessed it incorrectly
# and the card has to be answered correctly more than 2 times for it to not appear again.

# Example 3: 
# False
# Explanation: Never sort a card out. Every card will be asked everytime 
# even if you answered the question correctly 100x times. 

# Current configuration: You need to have a streak of more or equal to 2
# and need to have answered the question correctly at least 3 times:
card.timesCorrect > 2 and card.streak >= 2
```

### Reset your Statistics  <a name="reset"></a>
```
studyflash reset FILENAME.json
```

The script resets the number of you knowing the correct/wrong answer, so you can start studying from scratch again.


### Learn Words by Solution <a name="solution"></a>
```
studyflash reverse FILENAME.json
```

Use that command if you want to switch your solutions with your anwsers.

