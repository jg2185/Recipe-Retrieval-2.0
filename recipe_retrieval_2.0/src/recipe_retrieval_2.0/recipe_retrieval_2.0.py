from flask import Flask, request, jsonify
from text_processing import TextProcessor
from speech_processing import SpeechProcessor
from utils.recipe_searcher import RecipeSearcher
import os
import argparse
import logging

#logging part
def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        handlers=[
                            logging.FileHandler("./logs.txt"),
                            logging.StreamHandler()
                        ])
    logging.info("Logging setup complete - outputting to both console and logs.txt")
    
import gdown
import os

os.makedirs(os.path.dirname('../data/readable_recipes.txt'), exist_ok=True)

# download the data from google drive
gdown.download('https://drive.google.com/file/d/1RIxIp1oN-s37NZ4a45-teL4gvUnAxtkp/view?usp=sharing', '../data/readable_recipes.txt', quiet=False)


with open('../data/readable_recipes.txt', 'r') as file:
    content = file.read()


app = Flask(__name__)
text_processor = TextProcessor()
speech_processor = SpeechProcessor()

# Create a RecipeSearcher instance
searcher = RecipeSearcher("./data/inverted_index.json")

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text_input = data.get('text', '')
    if text_input:
        try:
            ingredients = text_processor.process_text(text_input)
            dislikes = []  # You might want to handle dislikes similarly
            response = {
                'status': 'success',
                'data': searcher.display_recipes(ingredients, dislikes)
            }
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
    else:
        response = {
            'status': 'error',
            'message': 'No text input provided'
        }
    return jsonify(response)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    data = request.get_json()
    audio_file = data.get('audio_file', '')
    if audio_file and os.path.exists(audio_file):
        try:
            transcript = speech_processor.speech_to_text(audio_file)
            ingredients = text_processor.process_text(transcript)
            dislikes = []  # Similarly for dislikes
            response = {
                'status': 'success',
                'data': searcher.display_recipes(ingredients, dislikes)
            }
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
    else:
        response = {
            'status': 'error',
            'message': 'Audio file not found or not provided'
        }
    return jsonify(response)

#delete it after use

os.remove('../data/readable_recipes.txt')
print(f"File {'../data/readable_recipes.txt'} has been deleted.")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
