# Homework 4 Program 2
# Laura Villarreal
import pathlib
import pickle
from nltk import word_tokenize, ngrams

if __name__ == '__main__':
    # unpickle the 6 pickles made in program 1
    with open('english_unigram.pickle', 'rb') as handle:
        eng_unigram_dict = pickle.load(handle)

    with open('english_bigram.pickle', 'rb') as handle:
        eng_bigram_dict = pickle.load(handle)

    with open('french_unigram.pickle', 'rb') as handle:
        fre_unigram_dict = pickle.load(handle)

    with open('french_bigram.pickle', 'rb') as handle:
        fre_bigram_dict = pickle.load(handle)

    with open('italian_unigram.pickle', 'rb') as handle:
        ita_unigram_dict = pickle.load(handle)

    with open('italian_bigram.pickle', 'rb') as handle:
        ita_bigram_dict = pickle.load(handle)

    # read in the LangId.test file and split it by newlines to get sentences
    with open(pathlib.Path.cwd().joinpath("LangId.test"), 'r', encoding="utf-8") as f:
        read_data = f.read().splitlines()

    # open a file in preparation to write the results inside of it
    solutions = open(pathlib.Path.cwd().joinpath("MyLangIdSolutions.sol"), 'w', encoding="utf-8")

    num_sentence = 0
    # calculate a probability that a line in the test file is a certain language
    for sentence in read_data:
        num_sentence = num_sentence + 1
        # get the bigrams and unigrams of that line of text
        sentence_unigrams = word_tokenize(sentence)
        sentence_bigrams = list(ngrams(sentence_unigrams, 2))

        # we will be calculating the probability of each language for each sentence
        probability_eng = 1
        probability_fre = 1
        probability_ita = 1

        # vocab size
        v = len(eng_unigram_dict) + len(fre_unigram_dict) + len(ita_unigram_dict)

        # for each bigram in the sentence, calculate its probability
        for bigram in sentence_bigrams:
            # get the count of that bigram in each dictionary
            b_eng = eng_bigram_dict[bigram] if bigram in eng_bigram_dict else 0
            b_fre = fre_bigram_dict[bigram] if bigram in fre_bigram_dict else 0
            b_ita = ita_bigram_dict[bigram] if bigram in ita_bigram_dict else 0

            # get the count of the first word of each bigram (unigram count) in each dictionary
            u_eng = eng_unigram_dict[bigram[0]] if bigram[0] in eng_unigram_dict else 0
            u_fre = fre_unigram_dict[bigram[0]] if bigram[0] in fre_unigram_dict else 0
            u_ita = ita_unigram_dict[bigram[0]] if bigram[0] in ita_unigram_dict else 0

            # calculate the probability for that bigram and multiply it to the bigram probabilities for that sentence
            probability_eng = probability_eng * ((b_eng + 1) / (u_eng + v))
            probability_fre = probability_fre * ((b_fre + 1) / (u_fre + v))
            probability_ita = probability_ita * (b_ita + 1) / (u_ita + v)

        # find the largest of the 3 probabilities, then print it out
        largest_prob = max(probability_eng, probability_fre, probability_ita)
        if largest_prob == probability_eng:
            solutions.write(str(num_sentence) + " English\n")
        elif largest_prob == probability_fre:
            solutions.write(str(num_sentence) + " French\n")
        else:
            solutions.write(str(num_sentence) + " Italian\n")

    # close the write file
    solutions.close()

    # open the actual solution file and my solution file
    with open(pathlib.Path.cwd().joinpath("LangId.sol"), 'r', encoding="utf-8") as f:
        actual_solutions = f.read().splitlines()

    with open(pathlib.Path.cwd().joinpath("MyLangIdSolutions.sol"), 'r', encoding="utf-8") as f:
        my_solutions = f.read().splitlines()

    # for every value, compare them and see if they match
    correct_solutions = 0

    for i in range(len(actual_solutions)):
        if my_solutions[i] == actual_solutions[i]:
            correct_solutions = correct_solutions + 1
        else:
            print("in MyLangIdSolutions.sol: innacurate solution found at sentence line ", i+1)

    # determine the accuracy of my ngram algorithm on the dataset
    accuracy = (correct_solutions / len(actual_solutions)) * 100
    print("\nOverall accuracy of ngram algorithm: ", accuracy, "%")


