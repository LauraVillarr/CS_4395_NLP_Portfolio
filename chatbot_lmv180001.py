# Laura Villarreal
# Chatbot project
import random
import ast

import pandas as pd
import csv
from nltk import word_tokenize, WordNetLemmatizer, pos_tag, ne_chunk, Tree
import string
import contractions
from nltk.corpus import stopwords
from pathlib import Path


def preprocess_name_response(user_response):
    # contractions are not handled properly in NLTK, so expand those first
    expanded_words = []
    named_entity_text = ''
    ner_tuples = []

    for word in user_response.split():
        expanded_words.append(contractions.fix(word))
    expanded_text = ' '.join(expanded_words)

    # tokenize, then pos tag
    tokens = word_tokenize(expanded_text)

    # for some reason, 'I am' sometimes labels names as JJ
    # make it clear its a name by adding the word 'name' after 'I am'
    counter = 0
    while counter < len(tokens):
        if counter+2 <= len(tokens) and 'I' in tokens[counter] and 'am' in tokens[counter+1]:
            tokens.insert(counter + 2, 'name')
        counter += 1

    # pos tag the unique lemmas
    tagged_tokens = pos_tag(tokens)

    # if the user just types their name (one token) in some cases it would be classified as a noun
    # check if it is NN and return if it is
    if len(tagged_tokens) == 1 and tagged_tokens[0][1] == 'NN':
        return tagged_tokens[0][0].capitalize()

    # if the user types a phrase, check for a proper noun
    proper_nouns = [t[0] for t in tagged_tokens if t[1] == 'NNP']

    # I'm only going to return the first proper noun I find
    # this means that I am not going to be accepting full names
    if len(proper_nouns) != 0:
        return proper_nouns[0].capitalize()
    else:
        # returns an empty set
        return proper_nouns


def user_greeting():
    print("Hello! I can help give you some recipe recommendations.")
    user_response = input("First, what is your first name?\n")
    user_name = preprocess_name_response(user_response)
    while len(user_name) == 0:
        # if a name is not found, prompt the user to enter something else
        user_response = input("I'm sorry, I didn't quite get that. What is your first name again?  Make sure to "
                              "capitalize it properly!\n")
        user_name = preprocess_name_response(user_response)

    return user_name


# the user model will have 3 columns: name, tags_used, and recipe_history
# name is the name of the user
# tags_used is a dict of all the tags the user used and their frequency
# recipe_history holds every recipe that the user has searched up
def handle_user_model(name):
    write_data = [name, {}, []]
    # open the user model, create it if it doesn't exist
    path = Path("./user_model.csv")
    if path.is_file() is False:
        # if file doesn't exist, write the name in the file
        with open('user_model.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "tags_used", "recipe_history"])
            writer.writerow(write_data)
    else:
        # file does exist, check if the name is in there already
        with open("user_model.csv", "r") as f:
            reader = csv.reader(f, delimiter=",")
            # skip header
            next(reader)
            for user_vals in reader:
                if name in user_vals[0]:
                    print("Welcome again " + name + "!")
                    return user_vals, False

            # user not found, write them in the file
            with open('user_model.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(write_data)
                print("Hello " + name + "!")

    return write_data, True


def preprocess_recipe_input(recipe_response):
    # list of some common words that are for certain not important for me to keep
    non_important_words = ['please', 'give', 'recipe', 'want', 'need', 'have', 'keep', 'make', 'would', 'something',
                           'prefer', 'take', 'contain', 'contains', 'could', 'recommend', 'made', 'good', 'provide', 'around', 'get']
    # tokenize the data
    tokens = word_tokenize(recipe_response)

    lowercase_t = [t.lower() for t in tokens]
    # remove stop words, pos tag it, and lemmatize it to get it closer to the tags in the data
    tokens = [t for t in lowercase_t if t not in stopwords.words('english')
              and t not in string.punctuation]

    wnl = WordNetLemmatizer()

    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemma_clean = [t for t in lemmas if t not in non_important_words]

    # my knowledge base (with few exceptions) has time tags in minutes, so I need to convert any digit input
    # to minutes
    counter = 0
    num_vals = []
    while counter < len(lemma_clean):
        # if there is a number, look at next tag and see if it says hour. If it does, convert to minutes
        if lemma_clean[counter].isdigit():
            if counter + 1 < len(lemma_clean):
                if lemma_clean[counter + 1] == 'hour' or lemma_clean[counter + 1] == 'hr':
                    # convert string to digit, multiply, then convert back to string
                    lemma_clean[counter] = str(int(lemma_clean[counter]) * 60)
                    lemma_clean[counter + 1] = 'minute'
        elif lemma_clean[counter] == 'hour' or lemma_clean[counter] == 'hr':
            # if this matches, I will assume the user said something like "an hour" instead
            # of a digit followed by the word hour
            if not lemma_clean[counter - 1].isdigit():
                lemma_clean[counter] = '60'
        counter += 1

    for lemma in lemma_clean:
        if lemma.isdigit():
            num_vals.append(int(lemma))
    # assume all number values are in minutes
    if len(num_vals) > 1:
        total_mins = sum(num_vals)
        # clean tags of any minute values
        counter = 0
        while counter < len(lemma_clean):
            if lemma_clean[counter].isdigit() or 'minute' in lemma_clean[counter]:
                lemma_clean.remove(lemma_clean[counter])
            else:
                counter += 1
        # append total minute value to the end of the lemma list
        lemma_clean.append(str(total_mins))
        lemma_clean.append('minute')

    return lemma_clean


# returns a list of tuples consisting of (recipeId, recipeScore)
def get_recipe_scores(preprocessed_input):
    # holds the points that each recipe receives based on the tags
    recipe_points = []

    # lemmatizer will be used to lemmatize words in the recipe title
    wnl = WordNetLemmatizer()

    # open the knowledge base
    with open("recipes_knowledge_base.csv", 'r', encoding='unicode_escape') as file:
        next(file)
        cur_recipe = 0
        csvreader = csv.reader(file)
        for recipe in csvreader:
            cur_recipe_points = 0
            # print("reading recipe", cur_recipe + 1)
            # print(recipe[1])
            # change string representation of list into a list
            tags = recipe[7].strip('][').strip().replace('\'', "").split(', ')

            # get recipe name and place each word in a list
            recipe_name = recipe[1].split()
            # remove stopwords and lowercase recipe name for better comparison to tags
            recipe_name = [part.lower() for part in recipe_name if part not in stopwords.words('english')]
            lemmas = [wnl.lemmatize(recipe_part) for recipe_part in recipe_name]
            for input_token in preprocessed_input:
                # if at least part of the title is found, give it 2 points
                for recipe_name_part in lemmas:
                    if input_token == recipe_name_part:
                        # print("point on title " + input_token)
                        # print("tag was: " + tag)
                        cur_recipe_points += 2
                # look at all the tags
                for tag in tags:
                    # If user input is in a tag, give it 1 point
                    if input_token in tag:
                        # print("point on user input " + input_token)
                        # print("tag was: " + tag)
                        cur_recipe_points += 1
                    # if the tag is a digit, then, based how I did the tags, it's a time in minutes
                    elif tag.isdigit() and input_token.isdigit():
                        # if the user's desired time is within 5 minutes of the recipe time, give the point
                        if abs(int(input_token) - int(tag)) <= 5:
                            # print("point on user input " + input_token)
                            # print("tag was: " + tag)
                            cur_recipe_points += 1

            cur_recipe += 1
            # appends a tuple of the recipe id and the points it received
            recipe_points.append((recipe[0], cur_recipe_points))
        return recipe_points


# this function returns the id of the recipe that will be shown to the user
# returns -1 if no recipe was found
def write_tags_to_user_model(preprocessed_input, user_name):
    # read the tag history from the user
    with open("user_model.csv", 'r', encoding='unicode_escape') as file:
        next(file)
        csvreader = csv.reader(file)
        for row in csvreader:
            if row[0] == user_name:
                prev_tags = ast.literal_eval(row[1])
                break

    # write new tags, or update old ones to reflect the new input
    for tag in preprocessed_input:
        if tag in prev_tags:
            prev_tags[tag] += 1
        else:
            prev_tags[tag] = 1

    # add the updated dict to the model using pandas
    df = pd.read_csv("user_model.csv", index_col="name")
    df.at[user_name, 'tags_used'] = prev_tags
    df = df.reset_index()
    df.to_csv("user_model.csv", index=False)


def get_recipe(recipe_input, user_name):
    preprocessed_input = preprocess_recipe_input(recipe_input)

    while len(preprocessed_input) == 0:
        new_input = input("Sorry I didn't get that. Please be descriptive when asking what you want. Could you tell "
                          "me again?\n")
        preprocessed_input = preprocess_recipe_input(new_input)

    # receive a list of tuples consisting of (recipeId, recipeScore)
    recipe_scores = get_recipe_scores(preprocessed_input)

    # sort recipe scores so that ones with the most points are at the front
    recipe_scores.sort(key=lambda a: a[1], reverse=True)

    # if the first recipe's score is zero, then there were no matches
    if recipe_scores[0][1] == 0:
        print("no matches found")
        return -1

    # if you get this far, you know that the tags were able to get some results so write them to the user model
    write_tags_to_user_model(preprocessed_input, user_name)

    # grab the id and score of the recipe with the max points
    max_recipes = [(recipe_scores[0][0], recipe_scores[0][1])]

    # check the next recipes in the list. If they have the same score as the first recipe, add to the list
    counter = 1
    while counter < len(recipe_scores) and recipe_scores[counter][1] == max_recipes[0][1]:
        max_recipes.append((recipe_scores[counter][0], recipe_scores[counter][1]))
        counter += 1

    # if there is only one recipe in the list, return the id of that one. Otherwise, pick a random recipe of the max
    # scores to show
    if len(max_recipes) == 1:
        print("one recipe found")
        return max_recipes[0][0]
    else:
        print("multiple recipes found!")
        return random.choice(max_recipes)[0]


def write_recipe_id_to_user_model(recipe_id_num, user_name):
    # read the tag history from the user
    with open("user_model.csv", 'r', encoding='unicode_escape') as file:
        next(file)
        csvreader = csv.reader(file)
        for row in csvreader:
            if row[0] == user_name:
                recipe_history = ast.literal_eval(row[2])
                break

    # update history list to have only the 5 most recent ids, only if its a valid id
    if recipe_id_num not in recipe_history and recipe_id_num != -1:
        if len(recipe_history) < 5:
            recipe_history.append(recipe_id_num)
        else:
            recipe_history.pop(0)
            recipe_history.append(recipe_id_num)

    # add the updated dict to the model using pandas
    df = pd.read_csv("user_model.csv", index_col="name")
    df.at[user_name, 'recipe_history'] = recipe_history
    df = df.reset_index()
    df.to_csv("user_model.csv", index=False)


def print_recipe(recipe_id):
    with open("recipes_knowledge_base.csv", 'r', encoding='unicode_escape') as file:
        next(file)
        csvreader = csv.reader(file)
        recipes = list(csvreader)
        index = int(recipe_id) - 1

        print(recipes[index][1] + '\n')
        print("Prep time: " + recipes[index][2])
        print("Cook time: " + recipes[index][3])
        print("Servings: " + recipes[index][4])
        ingredients = recipes[index][5].strip('][').strip().replace('\'', "").split('\n')
        directions = recipes[index][6].strip('][').strip().replace('\'', "").split('\n')
        print("Ingredients:")
        for ingredient in ingredients:
            print(ingredient.lstrip(' , '))
        print("Directions:")
        for direction in directions:
            print(direction.lstrip(' , '))


# gets the 3 most popular tags from the user, gets a score based on those tags, and returns a recipe id
# as long as the recipe id does not show up in the user's recipe history
def get_recommended_recipe(user_name):
    with open("user_model.csv", 'r', encoding='unicode_escape') as file:
        next(file)
        csvreader = csv.reader(file)
        for row in csvreader:
            if row[0] == user_name:
                prev_tags = ast.literal_eval(row[1])
                recipe_history = ast.literal_eval(row[2])
                break
        # sort the tags by value
        sorted_tags = sorted(prev_tags.items(), key=lambda x: x[1], reverse=True)
        tag_dict = dict(sorted_tags)

        # get top 3 user tags
        top_tags = list(tag_dict.keys())[:3]
        print("your top 3 search queries are: " + str(top_tags) + "\n")

        # get scores of recipes based on the 3 tags
        recipe_scores = get_recipe_scores(top_tags)
        recipe_scores.sort(key=lambda a: a[1], reverse=True)

        # if the top 3 tags give no matches, then tell the user as such and don't recommend anything
        if recipe_scores[0][1] == 0:
            print("I can't seem to find a different recipe based on your search terms. Try looking up some "
                  "different recipes!")
            return -1

        # pick a recipe that is not in the search history
        for recipe_data in recipe_scores:
            if recipe_data[0] not in recipe_history:
                recipe_id_val = recipe_data[0]
                recipe_score = recipe_data[1]
                break
        # if a recipe is picked but it is not at all relevant to the top 3 tags, then don't recommend anything
        if recipe_score == 0:
            print("I couldn't find a new recipe that you haven't seen yet. Keep searching!")
            return -1
    return recipe_id_val


if __name__ == '__main__':
    # get the name of the user
    name = user_greeting()

    # handle user_model properly based on the name
    user_data, is_new_user = handle_user_model(name)

    # if its a returning user, show them recommendations based on their tags and search history
    if not is_new_user:
        print("Here is a recipe you may like based on what you have looked at before:")
        recipe_id = get_recommended_recipe(name)
        if recipe_id != -1:
            print_recipe(recipe_id)

    recipe_input = input("What kind of recipe are you looking for?\n")
    recipe_id = get_recipe(recipe_input, name)

    if recipe_id == -1:
        print("Sorry, I was not able to find a recipe that has what you want.\nHere is a random recipe you may "
              "like!")
        rand_id = random.randint(1, 50)
        # add recipe to user_model
        write_recipe_id_to_user_model(rand_id, name)
        print_recipe(rand_id)
    else:
        print("Here is a recipe that you may like based on what you wanted!\n")
        write_recipe_id_to_user_model(recipe_id, name)
        print_recipe(recipe_id)
