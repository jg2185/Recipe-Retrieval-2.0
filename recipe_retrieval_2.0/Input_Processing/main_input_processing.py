from text_processing import TextProcessor
from speech_processing import SpeechProcessor

class IngredientExtractor:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.speech_processor = SpeechProcessor()

    def process_input(self, input_type):
        if input_type == 'text':
            text_input = "Hello, please tell me what ingredients you like and dislike."
            ingredients_text = self.text_processor.process_text(text_input)
            print("Extracted ingredients from text:", ingredients_text)

        elif input_type == 'audio':
            audio_file = 'path_to_your_audio_file.wav'  # Ensure this path is correct
            transcript = self.speech_processor.speech_to_text(audio_file)
            print("Transcribed text from audio:", transcript)
            ingredients_audio = self.text_processor.process_text(transcript)
            print("Extracted ingredients from audio:", ingredients_audio)

        else:
            print("Invalid input. Please enter 'text' or 'audio'.")

def main():
    ingredient_extractor = IngredientExtractor()
    # Ask the user for input type
    input_type = input("Enter 'text' for text input or 'audio' for audio file: ").strip().lower()
    ingredient_extractor.process_input(input_type)

if __name__ == "__main__":
    main()
