# from flask import Flask, request, jsonify
# from text_processing import TextProcessor
# from speech_processing import SpeechProcessor
# import os

# app = Flask(__name__)
# text_processor = TextProcessor()  
# speech_processor = SpeechProcessor() 

# @app.route('/process_text', methods=['POST'])
# def process_text():
#     data = request.get_json()
#     text_input = data.get('text', '')
#     if text_input:
#         try:
#             ingredients = text_processor.process_text(text_input)
#             response = {
#                 'status': 'success',
#                 'data': ingredients
#             }
#         except Exception as e:
#             response = {
#                 'status': 'error',
#                 'message': str(e)
#             }
#     else:
#         response = {
#             'status': 'error',
#             'message': 'No text input provided'
#         }
#     return jsonify(response)

# @app.route('/process_audio', methods=['POST'])
# def process_audio():
#     data = request.get_json()
#     audio_file = data.get('audio_file', '')
#     if audio_file and os.path.exists(audio_file):
#         try:
#             transcript = speech_processor.speech_to_text(audio_file)
#             ingredients = text_processor.process_text(transcript)
#             response = {
#                 'status': 'success',
#                 'data': ingredients
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
#     app.run(debug=True, port=5000)

from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer
import spacy
import re
from functools import lru_cache

class TextProcessor:
    def __init__(self):
        """Load the English NLP model"""
        self.nlp = spacy.load("en_core_web_sm")

    @lru_cache(maxsize=100)
    def translate_text(self, text, target_lang='en'):
        """Translates text to English using Helsinki NLP models from detected language."""
        detected_lang = detect(text)
        if detected_lang == target_lang:
            return text
        model_name = f"Helsinki-NLP/opus-mt-{detected_lang}-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text
    

    def process_text(self, text):
        """Processes text by translating it to English, then extracting ingredient preferences."""
        translated_text = self.translate_text(text)
        return translated_text