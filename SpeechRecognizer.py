class SpeechRecognizer:
    def __init__(self, service_name="silence"):
        self.service_name = service_name

    def recognize_from_file(self, file_path : str) -> str:
        raise NotImplementedError("SpeechRecognizers must implement the recognize_from_file method.")
    
    def recognize_from_microphone(self) -> str:
        raise NotImplementedError("SpeechRecognizers must implement the recognize_from_microphone method.")