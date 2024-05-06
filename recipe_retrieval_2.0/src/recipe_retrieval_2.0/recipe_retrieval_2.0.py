
from utils.recipe_searcher import RecipeSearcher
import argparse





if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="recipe retrieval")
    # parser.add_argument("-f", "--file", required=True, help="path to inverted index- json file")
    # args = parser.parse_args()
    #path for the saved inverted index
    searcher = RecipeSearcher("../data/inverted_index.json")
    ingredients = searcher.get_user_input()
    dislikes = searcher.get_user_dislikes()
    searcher.display_recipes(ingredients, dislikes)

####### in src directory

####### activate your environment
####### pip install tensorflow
####### pip install torch torchvision torchaudio
####### pip install tf-keras
####### python recipe_retrieval_2.0/recipe_retrieval_2.0.py