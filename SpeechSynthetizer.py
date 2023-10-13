class SpeechSynthesizer:
    def __init__(self, service_name="silence"):
        self.service_name = service_name

    def speak(self, text):
        raise NotImplementedError("SpeechSynthesizers must implement the speak method.")

    def speak_ssml(self, ssml_text):
        raise NotImplementedError("SpeechSynthesizers must implement the speak_ssml method.")