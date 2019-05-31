# studyFlash
A python script to learn flashcards inside your terminal (for language learning)

## Usage
### Create a Flashcard File (.json)
```
./study.py new FILENAME.json
```

A file is being created. You can add your questions / solutions


### Add cards to file
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


### Reset your Statistics 
```
./study.py reset FILENAME.json
```

The script resets the number of you knowing the correct/wrong answer, so you can start studying from scratch again.


### Study by Solution
```
./study.py reverse FILENAME.json
```

If you want that the solution is showed and you need to type the question, you can just reverse your file.


### Edit Flashcards
You can simply edit your cards by opening your flashcard json file.
