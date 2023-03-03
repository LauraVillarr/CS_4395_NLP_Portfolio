# CS_4395_NLP_Portfolio
Coursework and Projects from the UT Dallas Human Language Technologies course

## Assignment 0: Overview_of_NLP
A document covering the general idea of NLP

[Overview of NLP document](Overview_of_NLP.pdf)

## Assignment 1: Text Processing
A program that opens a data file with employee info, processes the data to the proper format,
and displays the information

[Link to open python file](Text_Processing.py)

### How to run the program
1. Create a new project (I used Pycharm, but you can use any IDE)
2. In the project, create a new folder called data
3. download [this data file](data.csv) and place it inside the data folder (Note: I did not create the data file, it was provided to me for the assignment)
4. If using Pycharm, edit the configurations of the python file and in the **Parameters** section type **data/data.csv**
5. Run the program

### Reflections
Strengths/Weaknesses:

Personally, I think Python works pretty well for text processing, as there are a lot of built-in functions that allow you
to break up text and manipulate it to what you need. Python also has a lot of libraries that give you a lot of options on
how you want to process your text. However, Python is slower compared to other languages, which may not make it the best
choice if you need to process a lot of text quickly. I personally also like being explicit in what types of data structures I am
using so I won't forget, and Python does not allow that since it has dynamic types

What I Learned/Reviewed:

In this assignment, I learned how to code a simple program using Python, as I had never used Python prior to this assignment. I also reviewed how to do simple regex expressions to recognize specific types of strings. Finally, I learned how to do sysarg in Python as well as what a pickle is
and how to create and read one.

## Assignment 2: Word Guess Game
A program that utilizes the nltk library to preprocess a dataset. Fetches the top 50 most frequently occurring nouns from the dataset and uses them in a guessing game. For the guessing game, the user is given a set of blanks corresponding to one of the nouns and is prompted to guess a letter. The game ends when either the user has negative points for too many incorrect guesses or if they type in a sentinel value.

[Link to open python file](Homework2_lmv180001.py)

### How to run the program
1. Create a new project (I used Pycharm, but you can use any IDE)
2. download [this data file](anat19.txt) and save it in the same folder as the python program (Note: I did not create the data file, it was provided to me for the assignment)
4. If using Pycharm, edit the configurations of the python file and in the **Parameters** section type **anat19.txt**
5. Run the program

## Assignment 3: WordNet
A Python notebook that goes through different functionalities of WordNet, SentiWordNet, and the concept of collocations.

Here is the [link to a PDF of the notebook](WordNet.ipynb-Colaboratory.pdf)

## Assignment 4: N-gram Language Model
This assignment consists of 2 programs. The first program reads in test data in English, French, and Italian, creates unigram and bigram
dictionaries for them, and then pickles those 6 dictionaries to be used in program 2. The second program unpickles the 6 dictionaries,
then reads in our test data (LangId.test) and determines for each sentence the probability that the sentence is in English, French or Italian based off of our language models. Then the program prints out the accuracy of our guesses by comparing our guesses to the actual solutions (the actual solutions are held in a file named LangId.sol)

This assignment also has a narrative, describing what N-grams are, where they are used, and how they are used to create language models.

[Link to open program 1](Homework4_program1_lmv180001.py)

[Link to open program 2](Homework4_program2_lmv180001.py)

Here is the [link to the N-gram narrative](Ngram_Narrative_lmv180001.pdf)

### How to run program 1
1. Create a new project (I used Pycharm, but you can use any IDE) and download program 1
2. Download the following files (these files I did not create, they were provided to me):

[LangId.train.English](LangId.train.English)

[LangId.train.French](LangId.train.French)

[LangId.train.Italian](LangId.train.Italian)

3. Save these downloaded files in the same folder as the python program
4. Run the program (this will take a while to complete as it takes a while to split all 3 files into bigrams and unigrams)

### How to run program 2
1. Create a new project (I used Pycharm, but you can use any IDE) and download program 2
2. Take all 6 of the .pickle files generated from program 1 and place them in the same folder where you are storing program 2
3. Download the following files (these files I did not create, they were provided to me):

[LangId.test](LangId.test)

[LangId.sol](LangId.sol)

4. Save these downloaded files in the same folder as the python program
5. Run the program (running the program will result in a file named MyLangIdSolutions.sol to be created)

## Assignment 5: Parsing Sentences
A pdf document performing the 3 types of parsing (PSG, dependency, and SRL) on an example sentence and analyzing each type of parse

[Link to pdf](Sentence_Parsing_lmv180001.pdf)