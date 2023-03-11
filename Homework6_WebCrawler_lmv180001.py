# Homework 6
# Laura Villarreal
import math
import pathlib
import pickle

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


# grab 15 urls that are relevant and will provide good information to the corpus
def get_relevant_urls(URL):
    # grab the text from the URL
    page = requests.get(URL)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')

    # make it a set so that duplicate links won't be added
    saved_urls = set()

    # websites that gave me errors when scraping them, or gave me data that was useless, poorly formatted,
    # or repeated, go here
    problem_scrape_list = ['http://helpwithbowling.com/history-origins-of-bowling.php',
                           'https://vault.si.com/vault/1986/04/07'
                           '/heres-a-memory-lane-for-bowling'
                           '-fanatics-who-have-some-spare-time',
                           'https://www.upi.com/Archives/1984/06/02/Bruce-Pluckhahn-says-theres-a-little-bit-of'
                           '-bowling/7180454996800/',
                           'https://vault.si.com/vault/1986/04/07/heres-a-memory-lane-for-bowling-fanatics-who-have-some-spare-time',
                           'https://www.si.com/vault/1986/04/07/643890/heres-a-memory-lane-for-bowling-fanatics-who-have-some-spare-time',
                           'https://www.britannica.com/sports/bowling',
                           'https://www.almanac.com/fact/first-recorded-ten-pin-bowling-match-played-at',
                           'https://www.bowlingball.com/BowlVersity/bowling-ball-evolution',
                           'https://www.britannica.com/topic/International-Bowling-Board',
                           'http://bowlingmedia.wstemp03.com/About-Us/IBMA-History',
                           'http://www.bowlingmuseum.com/Visit/Online-Exhibits',
                           'http://bowlingmedia.wstemp03.com/About-Us/NWBW-History',
                           'https://wp.talktenpin.net/2019/03/17/btba-bowling-pin-who-was-william-ivor-massil/',
                           'http://www.dailyadvance.com/Sports/2018/09/18/The-sport-of-bowling-more-than-10-pins-and-two-rolls.html',
                           'https://www.britannica.com/topic/Young-American-Bowling-Alliance',
                           'https://web.archive.org/web/20180917215354/https://www.bowlingball.com/BowlVersity/bowling-ball-evolution',
                           'http://www.brunswickbowling.com/news/article/brunswick-names-dream-bowl-palace-host-of-brunswick-euro-challenge-through/',
                           'https://www.nytimes.com/2010/01/25/sports/25bowling.html',
                           'https://bowlinghistory.wordpress.com/2009/01/19/jimmy-smith-famous-bowler-bibliography/',
                           'https://web.archive.org/web/20150701214701/http://www.whitehousemuseum.org/floor0/bowling-alley.htm']

    # get only 15 urls
    num_urls = 0

    for link in soup.find_all('a'):
        link_str = str(link.get('href'))

        # immediately skip if the website is a problem website
        if link_str in problem_scrape_list:
            continue

        # grab relevant links
        if ('bowling' in link_str or "Bowling" in link_str) and '.pdf' not in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]

            # skip over any wikipedia article that is not in english
            if "wikipedia" in link_str:
                if re.match(r'.*en\.wikipedia\.org.*', link_str) is None:
                    continue
            # this page is a dead link, skip it
            if re.match(r'.*canbowl.com.*', link_str):
                continue

            # skip this link, as I was having issues with the certificates on this one
            if re.match(r'.*ohiohistorycentral.org.*', link_str):
                continue

            # append it only if its a link with http at the front
            if link_str.startswith('http') and 'google' not in link_str:
                saved_urls.add(link_str)
                # this is used to remove any duplicate urls in the set
                if len(saved_urls) > num_urls:
                    num_urls += 1

            if num_urls == 15:
                break

    return saved_urls


# from each of the urls, grab the data from it
def grab_text(web_urls):
    num_file = 1
    file_list = []
    for website in web_urls:
        req = Request(website)

        data = urlopen(req).read()
        soup = BeautifulSoup(data, 'html.parser')

        # I will grab data only from the p tags as that contains the bulk of the information that I need
        data = soup.find_all('p')
        temp_list = []
        for val in data:
            temp_list.append(val.get_text())

        temp_str = ' '.join(temp_list)

        # write data to a file
        filename = "WebCrawlerData" + str(num_file) + ".txt"
        data_file = open(pathlib.Path.cwd().joinpath(filename), 'w', encoding="utf-8")
        data_file.write(temp_str)
        data_file.close()
        num_file += 1

        # get the name of the file for later use
        file_list.append(filename)

    return file_list


# cleans the data from each file by taking out the tabs and newlines
def clean_text(filenames):
    num_file = 1
    clean_filename_list = []
    for filename in filenames:
        with open(pathlib.Path.cwd().joinpath(filename), 'r', encoding="utf-8") as f:
            # clean up the text by removing newlines and tabs
            data = [a_word.rstrip() for a_word in f]
            data = ' '.join(data)
            sent_tokens = sent_tokenize(data)

        # place the cleaned text in a new file
        clean_filename = "CleanData" + str(num_file) + ".txt"
        clean_filename_list.append(clean_filename)
        data_file = open(pathlib.Path.cwd().joinpath(clean_filename), 'w', encoding="utf-8")
        sent_tokens = ' '.join(sent_tokens)
        data_file.write(sent_tokens)
        data_file.close()
        num_file += 1

    return clean_filename_list


# gets the term frequency of all the data files and normalizing the data
def get_tf_dict(clean_filename):
    with open(pathlib.Path.cwd().joinpath(clean_filename), 'r', encoding="utf-8") as f:
        # do some preprocessing on the data
        read_data = f.read()

        tokens = word_tokenize(read_data)

        tokens = [t.lower() for t in tokens]
        tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

        # add to tf dictionary to account for words in this file
        token_set = set(tokens)
        tf_dict = {t: tokens.count(t) for t in token_set}

        # normalize tf by number of tokens
        for t in tf_dict.keys():
            tf_dict[t] = tf_dict[t] / len(tokens)

    return tf_dict


# gets the idf_dict of the data files
def get_idf_dict(vocab, vocab_by_file, num_docs):
    idf_dict = {}
    # for every term, count the number of times in happens in the files and determine its idf score
    for term in vocab:
        temp = ['x' for voc in vocab_by_file if term in voc]
        idf_dict[term] = math.log((1 + num_docs) / (1 + len(temp)))
    return idf_dict


# multiplies the value of tf with the value of idf for every key in the dictionaries to
# get a tf_idf dict
def create_tfidf(tf_dict, idf_dict):
    tf_idf = {}
    for t in tf_dict.keys():
        tf_idf[t] = tf_dict[t] * idf_dict[t]

    return tf_idf


# does preprocessing on the data and extracts the top 40 terms based on tf-idf
def grab_top_terms(clean_filenames):
    tf_dictlist = [dict() for x in range(len(clean_filenames))]
    tf_idf = {}

    # calculate tf dictionary for all files
    for num in range(len(clean_filenames)):
        tf_dictlist[num] = get_tf_dict(clean_filenames[num])

    # create a vocab consisting of all tf dictionaries
    vocab = set(tf_dictlist[0].keys())
    for num in range(1, len(clean_filenames)):
        vocab = vocab.union(set(tf_dictlist[num].keys()))

    # create a list of vocabs by file
    vocab_by_file = []
    for num in range(len(clean_filenames)):
        vocab_by_file.append(tf_dictlist[num].keys())

    # create idf dictionary for all files
    idf_dict = get_idf_dict(vocab, vocab_by_file, len(clean_filenames))

    # create tf-idf dictionaries for every file
    tf_idf_dictlist = [dict() for x in range(len(clean_filenames))]

    for num in range(len(clean_filenames)):
        tf_idf_dictlist[num] = create_tfidf(tf_dictlist[num], idf_dict)

    # combine all dicts together
    for tf_idf_dict in tf_idf_dictlist:
        # get each key from the dict
        for dict_key in tf_idf_dict:
            # change the tf_idf only if the key currently doesn't exist in the dict, or you found a larger value
            # associated to that key
            if dict_key not in tf_idf or (dict_key in tf_idf and tf_idf[dict_key] < tf_idf_dict[dict_key]):
                tf_idf[dict_key] = tf_idf_dict[dict_key]

    tf_idf = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)

    return tf_idf[:40]


if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Bowling"
    knowledge_base = {}

    # get 15 relevant urls from the starting link
    relevant_urls = get_relevant_urls(url)
    print(relevant_urls)

    # grab the text from each of the pages
    filename_list = grab_text(relevant_urls)

    # clean up the text and place them in new files
    clean_files = clean_text(filename_list)

    # grab the top 40 terms from the files
    top_terms = grab_top_terms(clean_files)

    print("top 40 terms:", top_terms)

    # terms related to the relevant ones are placed in parentheses
    most_relevant_terms = ["target", "alley", "ball", "pins", "shoe", "egypt", "branham",
                           "pluckhahn", "truman", "bwaa"]
    print("\n10 most relevant terms:", most_relevant_terms)

    # so that there can be multiple values in each key
    for relevant_term in most_relevant_terms:
        # set() so that a sentence won't be included multiple times for a term
        knowledge_base.setdefault(relevant_term, set())

    # build a knowledge base by going through each file
    for filename in clean_files:
        with open(pathlib.Path.cwd().joinpath(filename), 'r', encoding="utf-8") as f:
            read_data = f.read()
            sentences = sent_tokenize(read_data)
            for relevant_term in most_relevant_terms:
                for sent in sentences:
                    # we need to word_tokenize so that a search won't falsely return true if
                    # the relevant word is part of a different word (ex. relevant word alley matched with valley)
                    words = word_tokenize(sent)
                    # if a relevant word is found in the sentence, append its sentence to the values in a dictionary
                    # some terms are proper nouns, so check if the capitalized relevant term is in the sentence as well
                    for word in words:
                        if relevant_term == word or relevant_term.capitalize() == word or relevant_term.upper() == word:
                            knowledge_base[relevant_term].add(sent)

    print("knowledge_base:")
    for key in knowledge_base:
        [print(key + ":", sentence) for sentence in knowledge_base[key]]

    with open('knowledge_base_bowling.pickle', 'wb') as handle:
        pickle.dump(knowledge_base, handle)
