from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio

class SpeechProcessor:
    def __init__(self):
        """Initializes the processor and model for the Wav2Vec 2.0 model."""
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53")

    def speech_to_text(self, audio_file):
        """Converts speech from an audio file to text using the Wav2Vec 2.0 model."""
        waveform, sample_rate = torchaudio.load(audio_file)
        input_values = self.processor(waveform, sampling_rate=sample_rate, return_tensors="pt").input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        return transcription
