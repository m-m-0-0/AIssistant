from . import SpeechSynthesizer

import azure.cognitiveservices.speech as speechsdk

from concurrent.futures import Future

class AzureSpeechSynthesizer(SpeechSynthesizer):
    def __init__(self, service_name="azure", voice_name="en-US-JessaNeural", subscription_key=None, region=None):
        super().__init__(service_name)

        self.voice_name = voice_name
        
        self.subscription_key = subscription_key
        self.region = region

        self.speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.region)
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

    def speak(self, text: str) -> Future:
        return self.speech_synthesizer.speak_text_async(text, self.speech_config.speech_synthesis_voice_name)
    
    def speak_ssml(self, ssml_text: str) -> Future:
        return self.speech_synthesizer.speak_ssml_async(ssml_text, self.speech_config.speech_synthesis_voice_name)