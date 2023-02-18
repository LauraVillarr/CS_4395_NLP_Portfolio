# Homework 2
# Laura Villarreal

import sys
import pathlib
from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords
from random import seed
from random import randint

seed(1234)

'''
Processes the raw text from the dataset to extract tokens that are alphabetic,
not a stop word, and with a length greater than 5. Finds all the nouns from the
set of tokens.

Args: 
    raw_text: the text read from the dataset without any preprocessing done on it
    
Returns:
    the tokens from the raw text, as well as the nouns found in the tokens
    
Example:
    >>>preprocess_text(['Extract raw text from the datafile'])
    >>>['extract', 'datafile'] [('datafile', 'NN')]

'''


def preprocess_text(raw_text):
    # tokenize and lowercase the text
    tokens = word_tokenize(raw_text)
    lowercase_t = [t.lower() for t in tokens]

    # get only alphabetical words with length > 5 that are not stop words
    tokens = [t for t in lowercase_t if t.isalpha()
              and t not in stopwords.words('english')
              and len(t) > 5]

    # lemmatize the tokens and get a set of unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas = list(set(lemmas))

    # pos tag the unique lemmas
    lemma_pos = pos_tag(lemmas)
    print("First 20 pos tags from the unique lemmas: \n", lemma_pos[:20])

    # create a list of lemmas that are nouns
    # in lemma_pos, get the 2nd part of the tuple (the pos) which is at index 1.
    # in the tuple, get the first character (at index 0) and check if it is a noun
    # for the matches, put only the noun itself (t[0]) in the variable nouns and ignore the pos tag
    nouns = [t[0] for t in lemma_pos if t[1][0] == 'N']

    print("number of tokens in dataset:", len(tokens))

    print("number of nouns in dataset:", len(nouns))

    return tokens, nouns


'''
Runs the guessing game, which gives the user a random noun from the top 50 nouns
in the dataset and prompts them to guess letters in order to correctly guess
the word.

Args: 
    noun_options: a list of the top 50 nouns collected from the dataset
    
Returns:
    nothing
    
Example:
    >>>guessing_game(['vessel', 'stretch', ... , 'cardiac'])
    >>>runs guessing game
'''


def guessing_game(noun_options):
    points = 5
    guess = ''
    prev_guesses = list()
    word = noun_options[randint(0, 49)]
    progress = list()
    for i in range(len(word)):
        progress.append('_ ')

    print("\nLet's play a word guessing game!")
    print("".join(progress))

    # get only a single character, not including any beginning or trailing spaces
    print("previous guesses:", prev_guesses)
    guess = input("Guess a letter: ").strip()[0]
    print("Guess is", guess)

    while points > -1 and guess != '!':

        # if the user already guessed that letter
        if guess in prev_guesses:
            print("Already guessed that letter. Score is", points)

        # guessed correctly
        elif guess in word:
            points += 1
            print("Right! Score is", points)
            prev_guesses.append(guess)
            for i in range(len(word)):
                if word[i] == guess:
                    progress[i] = word[i] + " "

            # if the word is complete, get a new word
            if '_ ' not in progress:
                print("You solved it! Score is", points)
                print("\nCurrent score:", points)
                print("\nGuess another word")
                prev_guesses.clear()

                # get a new word and refresh the progress
                word = noun_options[randint(0, 49)]
                progress.clear()
                for i in range(len(word)):
                    progress.append('_ ')

        # incorrect guess
        else:
            points -= 1
            print("Sorry, guess again, score is", points)
            prev_guesses.append(guess)
            if points == -1:
                continue

        # get the next guess
        print("".join(progress))
        print("previous guesses:", prev_guesses)
        guess = input("Guess a letter: ").strip()[0]
        print("Guess is", guess)

    print("Game is over! the word was", word)
    print("Final score:", points)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Data not found. Add a parameter specifying where to find the data.")
        quit()
    else:
        filepath = sys.argv[1]
        with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
            read_data = f.read()
        # tokenize the data
        first_tokens = word_tokenize(read_data)

        # set the tokens to lowercase and only alphabetical
        lowercase_tokens = [t.lower() for t in first_tokens]
        lowercase_tokens = [t for t in lowercase_tokens if t.isalpha()]

        # put the tokens in a set to filter out unique tokens, then get the length of the set to get the number
        # of unique tokens
        num_unique_tokens = len(set(lowercase_tokens))
        lexical_diversity = num_unique_tokens / len(lowercase_tokens)
        print(f'Lexical Diversity of input data: {lexical_diversity:.2f}')

        # preprocess the raw text
        second_tokens, noun_list = preprocess_text(read_data)

        # create a dictionary of nouns and their frequency in the tokens list
        noun_dict = {}

        # count the number of times every noun occurs in the token set
        for n in noun_list:
            noun_dict[n] = second_tokens.count(n)

        # sort the dict based on its values to get it in descending order
        noun_dict = dict(sorted(noun_dict.items(), key=lambda item: item[1], reverse=True))

        # save the first 50 items in this dict into a list of tuples
        noun_tuple = list(noun_dict.items())[:50]
        print("Top 50 words with their counts from the dataset:", noun_tuple)

        game_nouns = [n[0] for n in noun_tuple]

        guessing_game(game_nouns)
