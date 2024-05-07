import json
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from transformers import pipeline

# Load the model
generator = pipeline('text-generation', model='pratultandon/recipe-nlg-gpt2-train11_15')


class RecipeSearcher:
    def __init__(self, index_filename):
        self.index = self.load_index(index_filename)
        self.recipes = self.load_recipes()
        self.stemmer = PorterStemmer()

    def load_index(self, filename):
        # load the inverted index
        with open(filename, 'r') as file:
            return json.load(file)

    def load_recipes(self):
        # load original recipes data
        with open("../data/readable_recipes.txt", 'r') as file:
            return json.load(file)

    def get_user_input(self):
        # let the user input ingredients and return a cleaned list of stemmed,lower case ingredients
        # can handle user input with common and white space such as following examples
        #1 tablespoon extra-virgin olive oil
        #1 tablespoon extra-virgin olive oil,
        #1 tablespoon extra-virgin olive oil ,
        user_input = input("Enter ingredients separated by commas (e.g., salt, butter): ")
        ingredients = [ingredient.strip().lower() for ingredient in user_input.split(',') if ingredient.strip()]
        stemmed_ingredients = [self.stemmer.stem(ingredient) for ingredient in ingredients]
        return stemmed_ingredients


    def get_user_dislikes(self):
        # ask the user for ingredients they are allergic to or don't like to eat
        user_input = input("Enter any ingredients you are allergic to or dislike, separated by commas (e.g., nuts, gluten): ")
        # if the user does not have allergy or dislike, enter NONE, NA,N/A,none,na,n/a to skip
        if user_input.lower() in ['none', 'na', 'n/a', '']:
            return []
        dislikes = [dislike.strip().lower() for dislike in user_input.split(',') if dislike.strip()]
        stemmed_dislikes = [self.stemmer.stem(dislike) for dislike in dislikes]
        return stemmed_dislikes
    
    # some ingredients contain exact duplication, remove them as a quality control step before give user output
    def remove_duplicates(self, items):
        seen = set()
        cleaned_items = []
        for item in items:
            if item not in seen:
                seen.add(item)
                cleaned_items.append(item)
        return cleaned_items

    def generate_recipe(self, prompt):
        generator = pipeline('text-generation', model='pratultandon/recipe-nlg-gpt2-train11_15')
        generated_recipes = generator(prompt, max_length=400, truncation=True)  
        # could adjust max_length if needed, I'll leave it as 400
        return generated_recipes[0]['generated_text']

    
    ########### use a Python approach to detect and remove these duplications 
    # We'll divide the text into paragraphs or sections and then remove any duplicate sections. 
    # This process involves splitting the text based on paragraph breaks, identifying duplicates
    # then reconstructing the text without the duplicates.
    def remove_duplicate_paragraphs(self,text):
        paragraphs = text.strip().split('\n')
        seen = set()
        cleaned_paragraphs = []
        for paragraph in paragraphs:
            if paragraph not in seen:
                seen.add(paragraph)
                cleaned_paragraphs.append(paragraph)
        return '\n'.join(cleaned_paragraphs)
    
    #meant to remove duplicates from generated recipe
    def remove_duplicates_generation(self,text):
        lines = text.split("\n")  # split the text into lines or paragraphs
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:  # check if the line has already been encountered
                #if not encountered, append and show in output
                unique_lines.append(line)
                seen.add(line)
        return "\n".join(unique_lines) 

    def display_recipes(self, ingredients, dislikes):
        # show recipes that contain the given ingredients but none of the dislikes, limited to the top 3 matches
        recipe_matches = {}
        for ingredient in ingredients:
            if ingredient in self.index:
                for recipe_id in self.index[ingredient]:
                    if not dislikes or not any(dislike in self.recipes[recipe_id]['ingredients'] for dislike in dislikes):
                        if recipe_id in recipe_matches:
                            recipe_matches[recipe_id] += 1
                        else:
                            recipe_matches[recipe_id] = 1

        # sort recipes by the number of matching ingredients (descending) and limit to top 3
        sorted_recipe_ids = sorted(recipe_matches, key=recipe_matches.get, reverse=True)[:3]

        recipes_data = []
        if not sorted_recipe_ids:
            print("No recipes found with the given ingredients that avoid your dislikes. Generating some suggestions for you:")
            # generate a recipe prompt based on user ingredients
            prompt = f"Recipe with ingredients: {', '.join(ingredients)}:"
            generated_recipe = self.generate_recipe(prompt)
            #some duplications with generated recipe
            #clean_recipe = self.remove_duplicates_generation(generated_recipe)  
            # print(generated_recipe)
            return [generated_recipe]
        else:
            for recipe_id in sorted_recipe_ids:
                recipe = self.recipes[recipe_id]
                # print(f"\nRecipe: {recipe['title']}")
                # print("Ingredients:")
                clean_ingredients = self.remove_duplicates(recipe['ingredients'])  
                # print("\n".join(clean_ingredients))
                # print("Instructions:")
                clean_instructions = self.remove_duplicate_paragraphs(recipe['instructions'])  
                # print(clean_instructions) 
                recipes_data.append({
                'title': recipe['title'],
                'ingredients': clean_ingredients,
                'instructions': clean_instructions
            })
        return recipes_data



