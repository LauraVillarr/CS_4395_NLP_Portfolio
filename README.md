[Skills](skills.md)

# CS_4395_NLP_Portfolio
Coursework and Projects from the UT Dallas Human Language Technologies course

## Summary
I have learned a lot about NLP during my experience doing these projects. I definitely think that this will be useful to me in my future career.
I learned the basics of parsing and analyzing text to get the important information, the basics of scraping the web for data, and the planning
involved in creating an interactive program like a chatbot. As someone who is very interested in web and mobile development, I find the chatbot
aspect quite useful as a chatbot can enhance the functionality of a website. I also found it interesting learning about training models and
deep learning, as those were concepts that I had heard about before but never fully understood until I had done it myself. I will be keeping up with new and interesting use cases for artificial intelligence from companies, as its interesting to see the sheer amount of situations where AI can be used to enhance a situation, as well as pay attention to what should be done to use it ethically. If you like the work you see below or on my github, feel free to contact me with any opportunities using the contact information found on my resume in the [Skills](skills.md) page. Thank you!

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

## Assignment 6: Web Crawler
This assignment creates a web crawler and grabs 15 relevant links given a starting link. In this example, I decided to use bowling for
my topic. Using the scraped data, the most relevant words are determined and are used to help create a knowledge base that can be used
for a chatbot.

This assignment also has a document, describing my process in creating the knowledge base as well as an example conversation that
could be made using this corpus of information.

[Link to open web crawler python code](Homework6_WebCrawler_lmv180001.py)

[Link to open web crawler document](CS4395_Web_Crawler_Project.pdf)

### How to run program
1. Create a new project (I used Pycharm, but you can use any IDE) and download the python code.
2. place the web crawler code in the project and run it. The program will produce 2 sets of 15 files that contain scraped data and cleaned data.
The program will also produce a pickle file that contains the knowledge base produced from the data

## Summary on Selected ACL Paper
I selected the paper "MISC: A Mixed Strategy-Aware Model integrating COMET for Emotional Support Conversation" from the 2022 
"Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)" and summarized it.

[Link to paper](https://aclanthology.org/2022.acl-long.25/)

[Link to my summary pdf](Summary_on_Selected_ACL_Paper_lmv180001.pdf)

## Text Classification 1
For this assignment, I picked the "IMDB dataset" from Kaggle, took the first 5000 elements from the dataset, and ran the dataset on 3 types of models: Naive Bayes, Logistic Regression, and Neural Networks.

[Link to Kaggle Dataset](https://www.kaggle.com/datasets/yasserh/imdb-movie-ratings-sentiment-analysis)

[Link to classification pdf](Text_Classification_1_lmv180001.ipynb-Colaboratory.pdf)

## Chatbot Project
This chatbot collects the first name of the user and, given user input on what they want, picks a recipe that most closely matches what they wanted. On subsequent startups, the chatbot will remember the user based on their first name and will recommend a recipe to them based on their previous searches and will not recommend recipes that the user has seen recently.

The knowledge base that I created is also provided. It contains 50 recipes scraped from the website based.cooking, with tags manually inputted by me.

For completeness sake, the code for the web crawler is provided and is similar in some ways to the previous web crawler, but it writes the data to a csv file. YOU WILL NOT NEED TO RUN THIS WEBCRAWLER IN ORDER TO RUN MY CHATBOT. The csv file outputted by the web crawler will not have the tags that I inputted, and the data will not be clean as I had done some manual cleaning to it. To run the chatbot, please use the provided file recipes_knowledge_base.csv

A report about my chatbot is provided, going more in detail about how I made my chatbot and details about the knowledge base.

[Link to chatbot code](chatbot_lmv180001.py)

[Link to knowledge base used by chatbot](recipes_knowledge_base.csv)

[Link to report about chatbot](Chatbot_Report_lmv180001.pdf)

Do not use the provided web crawler to generate the knowledge base for the chatbot, as the raw generated file won't have everything it needs.

[Link to web crawler](chatbot_data_collection_lmv180001.py)

### How to run the program
1. Create a new project (I used Pycharm, but you can use any IDE) and download the chatbot python file.
2. Place the chatbot file into the newly created project
3. Download the recipes_knowledge_base.csv file and place it in the same area where you placed the python file.
4. Download all the packages in the import section
5. Run the program. Note that after the program is run, user_model.csv is generated. That file contains information that the user provides to the chatbot.
6. If you want to test the user_model, run the program again under the same name. The chatbot will recommend a recipe based on what is in the user model.

## Text Classification 2
For this assignment, I picked the "Text Emotion Recognition" dataset from Kaggle, took the first 110,000 elements from the dataset, and ran the dataset on a dense sequential model, 2 different architectures (RNN and GRU) and with a custom embedding and the GloVe embedding to see whether it could determine whether a piece of text was negative or positive.

[Link to Kaggle Dataset](https://www.kaggle.com/datasets/shreejitcheela/text-emotion-recognition?select=test.csv)

[Link to the source I used to get the GloVe embedding](https://www.kaggle.com/datasets/rtatman/glove-global-vectors-for-word-representation)

[Link to classification pdf](Text_Classification_2_lmv180001.ipynb%20-%20Colaboratory.pdf)
