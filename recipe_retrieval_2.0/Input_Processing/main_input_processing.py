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
                if not os.path.exists(audio_file):
                    raise FileNotFoundError("Audio file not found.")
                transcript = self.speech_processor.speech_to_text(audio_file)
                print("Transcribed text from audio:", transcript)
                ingredients_audio = self.text_processor.process_text(transcript)
                print("Extracted ingredients from audio:", ingredients_audio)
            else:
                print("Invalid input. Please enter 'text' or 'audio'.")
        except Exception as e:
            print(f"Error processing input: {e}")

def main():
    ingredient_extractor = IngredientExtractor()
    input_type = input("Enter 'text' for text input or 'audio' for audio file: ").strip().lower()
    ingredient_extractor.process_input(input_type)

if __name__ == "__main__":
    main()
