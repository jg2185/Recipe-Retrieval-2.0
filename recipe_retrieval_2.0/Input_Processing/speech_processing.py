from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import torchaudio

def speech_to_text(audio_file):
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
    waveform, sample_rate = torchaudio.load(audio_file)
    input_values = processor(waveform, sampling_rate=sample_rate, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription
