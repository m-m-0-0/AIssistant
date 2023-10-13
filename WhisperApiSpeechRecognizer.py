from . import SpeechRecognizer

import speech_recognition as sr

class WhisperApiSpeechRecognizer(SpeechRecognizer):
    def __init__(self, service_name="whisper_api", api_key=None):
        super().__init__(service_name)

        self.api_key = api_key
        self.recognizer = sr.Recognizer()

    def recognize_from_file(self, file_path : str) -> str:
        with sr.AudioFile(file_path) as source:
            audio = self.recognizer.record(source)
            return self.recognizer.recognize_whisper_api(audio, key=self.api_key)
    
    def recognize_from_microphone(self) -> str:
        raise NotImplementedError("SpeechRecognizers must implement the recognize_from_microphone method.")