
# studyFlash
A python application for learning flashcards inside your terminal (for language learning)

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
   6. [Reset Statistics](#reset)
   7. [Replace Solution by Answers](#solution)

## Installation <a name="installation"></a>

### With pip <a name="pip"></a>
Clone the git repo and install the application: 
```
git clone https://github.com/Alone2/studyFlash.git
sudo pip install ./studyFlash
```

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

A file is being created. You can add your questions / solutions with ```./study.py add FILENAME.json``` or ```./study.py edit FILENAME.json``` (opens with text editor, default -> vim)


### Add Cards to File  <a name="add"></a>
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

The script now asks you your flashcards. 
You need to type them correctly.
If made a typo you can press "r" to count your answer as correct.

If the number of you knowing the correct answer is bigger than of you not knowing the answer, the word will not appear any more. 

(use ctrl+c to return to terminal)


### Edit your Cards <a name="edit"></a>
```
studyflash edit FILENAME.json
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
studyflash reset FILENAME.json
```

The script resets the number of you knowing the correct/wrong answer, so you can start studying from scratch again.


### Learn Words by Solution <a name="solution"></a>
```
studyflash reverse FILENAME.json
```

Use that command if you want to switch your solutions with your anwsers.

