from flask import Flask, request, jsonify
import text_processing
import speech_processing

app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text_input():
    data = request.json
    text_input = data.get('text_input', '')
    ingredients_text = text_processing.process_text(text_input)
    print("Extracted ingredients from text:", ingredients_text)
    return jsonify(ingredients_text)

@app.route('/process_audio', methods=['POST'])
def process_audio_input():
    data = request.json
    audio_file = data.get('audio_file', '')
    transcript = speech_processing.speech_to_text(audio_file)
    print("Transcribed text from audio:", transcript)
    ingredients_audio = text_processing.process_text(transcript)
    print("Extracted ingredients from audio:", ingredients_audio)
    return jsonify(ingredients_audio)

if __name__ == "__main__":
    app.run(debug=True)
