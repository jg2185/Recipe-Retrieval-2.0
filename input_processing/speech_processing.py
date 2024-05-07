from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio

class SpeechProcessor:
    def __init__(self):
        """Initializes the processor and model for the Wav2Vec 2.0 model."""
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53")

    def preprocess_audio(self, audio_file):
        """Preprocess the audio file to the correct sample rate and format."""
        waveform, sample_rate = torchaudio.load(audio_file)
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
        return waveform, 16000

    def speech_to_text(self, audio_file):
        """Converts speech from an audio file to text using the Wav2Vec 2.0 model."""
        waveform, sample_rate = self.preprocess_audio(audio_file)
        input_values = self.processor(waveform, sampling_rate=sample_rate, return_tensors="pt").input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        return transcription

# Example usage
# processor = SpeechProcessor()
# wants_audio = 'path_to_wants_audio.wav'  # Replace with the path to your audio file for wanted ingredients
# dont_wants_audio = 'path_to_dont_wants_audio.wav'  # Replace with the path to your audio file for unwanted ingredients

# wants_transcription = processor.speech_to_text(wants_audio)
# dont_wants_transcription = processor.speech_to_text(dont_wants_audio)

# print("Transcribed Wants:", wants_transcription)
# print("Transcribed Don't Wants:", dont_wants_transcription)
