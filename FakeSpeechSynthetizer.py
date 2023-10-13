from SpeechSynthetizer import SpeechSynthesizer

class FakeSpeechSynthesizer(SpeechSynthesizer):
    def __init__(self, service_name="none"):
        super().__init__(service_name)

    def speak(self, text: str):
        print(text)
    
    def speak_ssml(self, ssml_text: str):
        print(ssml_text)

        