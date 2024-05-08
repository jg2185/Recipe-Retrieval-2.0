from text_processing import TextProcessor
from speech_processing import SpeechProcessor

def main():
    text_processor = TextProcessor()
    speech_processor = SpeechProcessor()

    print("Welcome to the Ingredient Processor")
    print("Enter 'text' for text processing or 'audio' for audio processing:")
    input_type = input().lower()

    if input_type == 'text':
        print("Enter your text containing ingredients:")
        text_input = input()
        if text_input:
            result = text_processor.process_ingredients([text_input], [])
            print("Processed Ingredients:", result)
        else:
            print("No text input provided.")

    elif input_type == 'audio':
        print("Enter the path to your audio file:")
        audio_path = input()
        if os.path.exists(audio_path):
            transcript = speech_processor.speech_to_text(audio_path)
            print("Transcription:", transcript)
            result = text_processor.process_ingredients([transcript], [])
            print("Processed Ingredients from Audio:", result)
        else:
            print("Audio file not found or not provided.")

    else:
        print("Invalid input type. Please enter 'text' or 'audio'.")

if __name__ == '__main__':
    main()
