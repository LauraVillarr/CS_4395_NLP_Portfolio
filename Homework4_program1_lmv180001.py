# Homework 4 Program 1
# Laura Villarreal
import pathlib
from nltk import word_tokenize
from nltk.util import ngrams
import pickle

'''
reads the content in the file and tokenizes the words. It then splits the words into unigrams
and bigrams, counts the number of occurrences of that unigram or bigram, and places them in their
respective dicts.

Args: 
    filename: the name of the data file that will be read

Returns:
    a dict of unigrams {key=unigram: value=number of occurrences} and
    a dict of bigrams {key=bigram: value=number of occurrences}

Example:
    >>>build_language_model(exampleFilename)
    >>>{'a': 1, 'word': 1, '.': 1}, {('a', 'word'): 1, ('word', '.'): 1}

'''


def build_language_model(filename):
    with open(pathlib.Path.cwd().joinpath(filename), 'r', encoding="utf-8") as f:
        read_data = f.read().splitlines()
    tokens = word_tokenize("".join(read_data))

    tokens = [t.lower() for t in tokens]
    bigrams = list(ngrams(tokens, 2))
    unigrams = list(ngrams(tokens, 1))

    # create dict with key = bigrams, value = count of bigram
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    # create dict with key = unigrams, value = count of unigram
    unigram_dict = {u: unigrams.count(u) for u in set(unigrams)}

    return unigram_dict, bigram_dict


if __name__ == '__main__':
    # Build 3 language models (6 dictionaries) for each of the 3 datasets
    eng_unigram_dict, eng_bigram_dict = build_language_model("LangId.train.English")
    fre_unigram_dict, fre_bigram_dict = build_language_model("LangId.train.French")
    ita_unigram_dict, ita_bigram_dict = build_language_model("LangId.train.Italian")

    # pickle the 6 dictionaries
    with open('english_unigram.pickle', 'wb') as handle:
        pickle.dump(eng_unigram_dict, handle)

    with open('english_bigram.pickle', 'wb') as handle:
        pickle.dump(eng_bigram_dict, handle)

    with open('french_unigram.pickle', 'wb') as handle:
        pickle.dump(fre_unigram_dict, handle)

    with open('french_bigram.pickle', 'wb') as handle:
        pickle.dump(fre_bigram_dict, handle)

    with open('italian_unigram.pickle', 'wb') as handle:
        pickle.dump(ita_unigram_dict, handle)

    with open('italian_bigram.pickle', 'wb') as handle:
        pickle.dump(ita_bigram_dict, handle)
