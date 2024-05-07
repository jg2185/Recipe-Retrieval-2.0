
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
# sys.path.insert(0, os.path.abspath('/Users/kuangchuyun/Desktop/GU/ds5400/project/Recipe-Retrieval-2.0/recipe_retrieval_2.0/'))
# sys.path.insert(0, os.path.abspath('../'))
# from Input_Processing.text_processing import TextProcessor
# from Input_Processing.speech_processing import SpeechProcessor
sys.path.insert(0, os.path.abspath('/Users/kuangchuyun/Desktop/GU/ds5400/project/Recipe-Retrieval-2.0/recipe_retrieval_2.0/src/recipe_retrieval_2.0/'))
# sys.path.insert(0, os.path.abspath('../src/recipe_retrieval_2.0/'))
from utils.recipe_searcher import RecipeSearcher
import os

print('3')
app = Flask(__name__)
CORS(app)
# text_processor = TextProcessor()
# speech_processor = SpeechProcessor()

# Create a RecipeSearcher instance
print('2')
searcher = RecipeSearcher("../../data/inverted_index.json")
print('1')
@app.route('/')
def home():
    return render_template('receive.html')


@app.route('/generate_recipe', methods=['POST'])
def process_text():
    print("Received a request!")
    data = request.get_json()
    print("Data received:", data)
    include_ingredients = data.get('include', '')
    exclude_ingredients = data.get('exclude', '')
    print("Ingredients included:", include_ingredients)
    print("Ingredients excluded:", exclude_ingredients)

    if not include_ingredients:
        return jsonify({
            'status': 'error',
            'message': 'No ingredients provided'
        })

    try:
        # include = text_processor.process_text(include_ingredients)
        # exclude = text_processor.process_text(exclude_ingredients)
        # recipes = searcher.display_recipes(include, exclude)
        recipes = searcher.display_recipes(include_ingredients, exclude_ingredients)
        return jsonify({
            'status': 'success',
            'data': recipes
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
