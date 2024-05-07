from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.recipe_searcher import RecipeSearcher
import os
# import argparse

app = Flask(__name__)
CORS(app)
text_processor = TextProcessor()
speech_processor = SpeechProcessor()

# Create a RecipeSearcher instance
searcher = RecipeSearcher("./data/inverted_index.json")
@app.before_request
def before_request():
    print("Incoming request:", request.path)

# @app.route('/generate_recipe', methods=['POST'])
def process_text():
    print("Received a request!")

    data = request.get_json()
    print("Data received:", data)
    # text_input = data.get('text', '')
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
        # exclude = text_processor.process_text(exclude_ingredients) if exclude_ingredients else []
        recipes = searcher.display_recipes(include_ingredients, exclude_ingredients)
        # dislikes = []  # You might want to handle dislikes similarly
        return jsonify({
            'status': 'success',
            'data': recipes
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# @app.route('/process_audio', methods=['POST'])
# def process_audio():
#     data = request.get_json()
#     audio_file = data.get('audio_file', '')
#     if audio_file and os.path.exists(audio_file):
#         try:
#             transcript = speech_processor.speech_to_text(audio_file)
#             ingredients = text_processor.process_text(transcript)
#             dislikes = []  # Similarly for dislikes
#             response = {
#                 'status': 'success',
#                 'data': searcher.display_recipes(ingredients, dislikes)
#             }
#         except Exception as e:
#             response = {
#                 'status': 'error',
#                 'message': str(e)
#             }
#     else:
#         response = {
#             'status': 'error',
#             'message': 'Audio file not found or not provided'
#         }
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True)
