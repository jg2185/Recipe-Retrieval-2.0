from text_processing import TextProcessor
from speech_processing import SpeechProcessor
import os

class IngredientExtractor:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.speech_processor = SpeechProcessor()

    def process_input(self, input_type):
        try:
            if input_type == 'text':
                text_input = "Hello, please tell me what ingredients you like and dislike."
                ingredients_text = self.text_processor.process_text(text_input)
                print("Extracted ingredients from text:", ingredients_text)
            elif input_type == 'audio':
                audio_file = 'path_to_your_audio_file.wav'
                if not os.path.exists

