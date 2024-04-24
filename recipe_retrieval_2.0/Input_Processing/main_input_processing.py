import text_processing
import speech_processing

def main():
    # Ask the user for input type
    input_type = input("Enter 'text' for text input or 'audio' for audio file: 我想吃葡萄和酸奶，我不想吃红薯和玉米").strip().lower()
    
    if input_type == 'text':
        text_input = "Hello, please tell me what ingredients you like and dislike."
        ingredients_text = text_processing.process_text(text_input)
        print("Extracted ingredients from text:", ingredients_text)
    
    elif input_type == 'audio':
        audio_file = 'path_to_your_audio_file.wav'  # Ensure this path is correct
        transcript = speech_processing.speech_to_text(audio_file)
        print("Transcribed text from audio:", transcript)
        ingredients_audio = text_processing.process_text(transcript)
        print("Extracted ingredients from audio:", ingredients_audio)
    
    else:
        print("Invalid input. Please enter 'text' or 'audio'.")

if __name__ == "__main__":
    main()
