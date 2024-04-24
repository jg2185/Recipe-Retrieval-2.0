import json

####### there used to be error within the ingredients.txt file due to 2 extra {}
####### used web validation to validate the json text structure
####### error detected and error fixed (deleted the extra {})
class InvertedIndex:
    def __init__(self):
        self.index = {}

    def add(self, recipe_index, ingredients):
        for ingredient in ingredients:
            if ingredient:
                if ingredient not in self.index:
                    self.index[ingredient] = []
                self.index[ingredient].append(recipe_index)

    def get_recipes(self, ingredient):
        return self.index.get(ingredient, [])

    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.index, file, indent=4)

    def save_to_txt(self, file_path):
        with open(file_path, 'w') as file:
            for ingredient, recipes in self.index.items():
                file.write(f"{ingredient}: {recipes}\n")

    def __str__(self):
        return str(self.index)

# read data from ingredients.txt
def read_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# read data from ingredients.txt
recipes_data = read_data("ingredients.txt")

# create an instance of InvertedIndex
index = InvertedIndex()

# populate the index
for recipe_id, ingredients in recipes_data.items():
    index.add(recipe_id, ingredients)

# save the index 2 files
index.save_to_json("inverted_index.json")
index.save_to_txt("inverted_index.txt")


