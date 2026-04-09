import base64
import io
from typing import Optional
from ..models.schemas import TranscribeRequest, TranscribeResponse


class SpeechToTextService:
    def __init__(self):
        self.model = None
        self.model_loaded = False
    
    async def load_model(self):
        if not self.model_loaded:
            try:
                import torch
                from transformers import WhisperProcessor, WhisperForConditionalGeneration
                
                processor = WhisperProcessor.from_pretrained("openai/whisper-base")
                model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
                
                self.model = {"processor": processor, "model": model}
                self.model_loaded = True
                print("Whisper model loaded successfully")
            except Exception as e:
                print(f"Failed to load Whisper model: {e}")
                self.model_loaded = False
    
    async def transcribe(self, request: TranscribeRequest) -> TranscribeResponse:
        if not self.model_loaded:
            await self.load_model()
        
        if self.model is None:
            return TranscribeResponse(
                text="Speech-to-text service is currently unavailable. Please type your answer.",
                confidence=0.0
            )
        
        try:
            audio_data = base64.b64decode(request.audio_data)
            audio_array = self._process_audio(audio_data)
            
            if audio_array is None:
                return TranscribeResponse(
                    text="Could not process audio data.",
                    confidence=0.0
                )
            
            import torch
            processor = self.model["processor"]
            model = self.model["model"]
            
            input_features = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
            
            forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
            
            predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            
            return TranscribeResponse(
                text=transcription,
                language="en",
                confidence=0.85
            )
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return TranscribeResponse(
                text="Error processing audio. Please type your answer.",
                confidence=0.0
            )
    
    def _process_audio(self, audio_data: bytes) -> Optional[list]:
        try:
            import numpy as np
            import wave
            
            with wave.open(io.BytesIO(audio_data), 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                frames = wav_file.readframes(wav_file.getnframes())
                audio_array = np.frombuffer(frames, dtype=np.int16)
                
                if sample_rate != 16000:
                    audio_array = self._resample(audio_array, sample_rate, 16000)
                
                audio_float = audio_array.astype(np.float32) / 32768.0
                
                return audio_float.tolist()
                
        except Exception as e:
            print(f"Audio processing error: {e}")
            return None
    
    def _resample(self, audio: list, orig_sr: int, target_sr: int) -> list:
        import numpy as np
        ratio = target_sr / orig_sr
        new_length = int(len(audio) * ratio)
        indices = np.linspace(0, len(audio) - 1, new_length)
        return np.interp(indices, np.arange(len(audio)), audio).astype(np.int16)


speech_to_text = SpeechToTextService()
