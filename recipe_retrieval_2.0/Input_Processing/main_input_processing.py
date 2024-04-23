import text_processing
import speech_processing

def main():
    text_input = "Hello, please tell me what ingredients you like and dislike."
    ingredients_text = text_processing.process_text(text_input)
    print("Extracted ingredients from text:", ingredients_text)

    audio_file = 'path_to_your_audio_file.wav'
    transcript = speech_processing.speech_to_text(audio_file)
    print("Transcribed text from audio:", transcript)
    ingredients_audio = text_processing.process_text(transcript)
    print("Extracted ingredients from audio:", ingredients_audio)

if __name__ == "__main__":
    main()
