import json
from nltk.stem import PorterStemmer
from nltk import pos_tag
from nltk import word_tokenize


class FormatJson:
    """
    class to make json files nice and readable for user
    """
    def __init__(self, path):
        self.path = path

    def readable(self, path):
        """
            path is a path to a json file
        """
        f = open(path,)
        file = json.load(f)
        readable_recipes = {}
        key_counter = 0
        for item in file:
            inner_dict = file[item]
            item_dict = {}
            temp_list = []
            item_dict["title"] = inner_dict["title"]
            for word in inner_dict["ingredients"]:
                replaced = word.replace("ADVERTISEMENT", "")
                temp_list.append(replaced)
            item_dict["ingredients"] = temp_list
            item_dict["instructions"] = inner_dict["instructions"]
            readable_recipes[key_counter] = item_dict
            key_counter += 1
        return readable_recipes

class GetIngredients:
    """
    class to get just the ingredients out of a recipe, to search through
    """
    def __init__(self, path):
        self.path = path


    def get_ingredients(self, path, stop_words):
        """
        path is a path to a json file
        stop_words is a list of words we don't want in final ingredients list
        """
        f = open(path, )
        file = json.load(f)
        stemmer = PorterStemmer()

        recipe_list = []
        for item in file:
            recipe_list.append(file[item])
        just_ingredients = []
        for recipe in recipe_list:
            just_ingredients.append(recipe["ingredients"])
        pos_keep = ["NN", "NNS", "JJ"]
        recipe_doc = []  # this will be a list of lists of lists- per recipe: [all ingredients[line of ingredient[content words from ingredient]]]
        for recipe in just_ingredients:  # list of ingredients by recipe
            pure_recipe = []  # this will be the cleaned, total ingredients list or one recipe
            for food in recipe:  # one item in recipe list
                food_tokens = word_tokenize(food)
                food_tokens = pos_tag(food_tokens)
                pure_foods = []  # this will be the cleaned line item of each individual ingredient
                for word, tag in food_tokens:
                    if tag in pos_keep:
                        if word not in stop_words:
                            pure_foods.append(word)
                stem_foods = stemmer.stem(pure_foods)
                string_foods = " ".join(stem_foods)
                string_foods = string_foods.lower()
                pure_recipe.append(string_foods)
            recipe_doc.append(pure_recipe)
        # this is so that we can iterate through this list of just ingredients, but we can still match this recipe with the
        # full readable text- index of ingredients will match index of recipe
        recipe_dict = {}
        for item in recipe_doc:
            recipe_dict[recipe_doc.index(item)] = item

        return recipe_dict




