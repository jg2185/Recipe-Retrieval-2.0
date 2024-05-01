from flask import Flask, request, jsonify
from text_processing import TextProcessor
from speech_processing import SpeechProcessor
import os

app = Flask(__name__)
text_processor = TextProcessor()  
speech_processor = SpeechProcessor() 

@app.route('/process_ingredients', methods=['POST'])
def process_ingredients():
    data = request.get_json()
    input_type = data.get('type', '').lower()
    response = {}

    try:
        if input_type == 'text':
            text_input = data.get('text', '')
            if text_input:
                ingredients = text_processor.process_text(text_input)
                response = {
                    'status': 'success',
                    'data': ingredients
                }
            else:
                response = {'status': 'error', 'message': 'No text input provided'}
        
        elif input_type == 'audio':
            audio_file = data.get('audio_file', '')
            if audio_file and os.path.exists(audio_file):
                transcript = speech_processor.speech_to_text(audio_file)
                ingredients = text_processor.process_text(transcript)
                response = {
                    'status': 'success',
                    'data': ingredients
                }
            else:
                response = {'status': 'error', 'message': 'Audio file not found or not provided'}
        
        else:
            response = {'status': 'error', 'message': 'Invalid input type'}
    
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

