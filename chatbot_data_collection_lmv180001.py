# Laura Villarreal
import math
import pathlib
import pickle

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# for csv file creation
import csv


# grab 15 urls that are relevant and will provide good information to the corpus
def get_relevant_urls(URL):
    # grab the text from the URL
    page = requests.get(URL)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')

    # make it a set so that duplicate links won't be added
    saved_urls = set()

    # websites that gave data that was too problematic goes here
    problem_scrape_list = []

    # get only 50 urls
    num_urls = 0

    for link in soup.find_all('a'):
        link_str = str(link.get('href'))

        # immediately skip if the website is a problem website
        if link_str in problem_scrape_list:
            continue

        # grab relevant links
        # if (re.match(r'.*allrecipes.com/recipe/.*', link_str)) and '.pdf' not in link_str:
        # I don't want any external links here
        if (re.match(r'.*based.cooking/', link_str)) and '.pdf' not in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]

            # append it only if its a link with http at the front
            if link_str.startswith('http') and 'google' not in link_str:
                saved_urls.add(link_str)
                # check if you reached the acceptable number of urls
                if len(saved_urls) > num_urls:
                    num_urls += 1

            if num_urls == 50:
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

        # I will grab data only from the header and article tags as that contains the bulk of the information that I
        # need
        data = soup.find_all(['header', 'article'])
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


def place_in_csv(filenames):
    num_file = 1
    # open the csv file
    with open("recipes.csv", 'w', encoding="utf-8") as file:
        csvwriter = csv.writer(file)

        # create the categories in the csv file
        categories = ['Id', 'Name', 'Prep Time', 'Cook Time', 'Servings', 'Ingredients', 'Directions', 'Tags']
        csvwriter.writerow(categories)

        # go through each file from the webcrawler
        for filename in filenames:
            with open(pathlib.Path.cwd().joinpath(filename), 'r', encoding="utf-8") as f:
                print("Scraping file", num_file)
                data = f.readlines()
                # initialize data values
                prep_time = "None"
                cook_time = "None"
                servings = "None"
                ingredients = []
                directions = []

                name = data[1]

                i = 2
                # go through the rest of the file to get the content
                while i < len(data):
                    if "Prep time" in data[i]:
                        prep_time = data[i]
                    elif "Cook time" in data[i]:
                        cook_time = data[i]
                    elif "Servings" in data[i]:
                        servings = data[i]
                    elif "Ingredients" in data[i]:
                        i += 2
                        while 'Directions' not in data[i]:
                            ingredients.append(data[i])
                            i += 1
                    if "Directions" in data[i]:
                        i += 2

                        # ignoring the start of the contributor(s) section. If that section doesn't exist,
                        # then I am ignoring the tags located at the last 2 lines of the file
                        while 'Contributor(s)' not in data[i] and i != len(data) - 2:
                            # print("in directions")
                            directions.append(data[i])
                            i += 1
                    i += 1
                # write data from the recipe to the file
                print("writing to file")
                write_data = [num_file, name, prep_time, cook_time, servings, ingredients, directions, 'TODO']
                csvwriter.writerow(write_data)
                num_file += 1


if __name__ == '__main__':
    url = "https://based.cooking/"
    knowledge_base = {}

    # get 50 relevant urls from the starting link
    # relevant_urls = get_relevant_urls(url)
    # print(relevant_urls)

    # grab the text from each of the pages
    # filename_list = grab_text(relevant_urls)

    # place the text in a csv file
    # Note: running this will undo all the manual changes I made to the recipe file
    # do not run unless you need to refresh it
    # place_in_csv(filename_list)

