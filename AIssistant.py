import os, json, time, sys, urllib.parse

import pvporcupine
import speech_recognition as sr
import openai
import azure.cognitiveservices.speech as speechsdk

import pyaudio
import pyperclip
import tiktoken
import win10toast
from playsound import playsound

from Plugin import Plugin
from SpeechSynthetizer import SpeechSynthesizer
from FakeSpeechSynthetizer import FakeSpeechSynthesizer
import utils


class AIssistant:
    def __init__(self, 
                name : str = "AIssistant",
                voice_name : str ="en-US-AriaNeural",
                model : str ="gpt-3.5-turbo", 
                wake_words : "list[str]" = ["blueberry"], 
                plugins : "list[Plugin]" = [],
                speech_synthesizer : SpeechSynthesizer = FakeSpeechSynthesizer(),

                ):
        
        self.name = name
        self.voice_name = voiceName
        self.model = model
        self.wake_words = wakeWords

        self.PCP_ACCESS_KEY = os.environ.get('PORCUPINE_KEY')
        self.OPENAI_KEY = os.environ.get('OPENAI_KEY')

        #Azure Speech API
        speechConfig = speechsdk.SpeechConfig(subscription=self.AZURE_SPEECH_KEY, region=self.AZURE_SPEECH_REGION)
        self.speechSynthesizer = speechsdk.SpeechSynthesizer(speech_config=speechConfig, audio_config=audioConfig)

        #Porcupine wake word
        self.porcupine = pvporcupine.create(self.PCP_ACCESS_KEY, keywords=self.wake_words)

        #Speech recognition
        self.speechRecognizer = sr.Recognizer()

        #OpenAI
        self.tokenizer = tiktoken.encoding_for_model(self.model)

        self.prompt = self.loadPrompt("./prompt.txt")

        self.plugins = {}


    def load_prompt(self, path, **kwargs):
        with open(path, "r") as f:
            prompt = f.read()

        #add plugins to prompt
        plugins_prompt = ""
        for i,plugin in enumerate(self.plugins):
            #n. command: description
            plugins_prompt += f"{i}. {plugin.command}: {plugin.description}"

        return prompt.format(plugins=plugins_prompt, **kwargs)
    

    def add_plugin(self, plugin: Plugin):
        self.plugins[plugin.command] = plugin

        self.prompt = self.loadPrompt("./prompt.txt")


    def remove_plugin(self, command):
        del self.plugins[command]

        self.prompt = self.loadPrompt("./prompt.txt")


    def _elaborate_commands(self, response):
        """dict is dict[tag, content, start, end]"""
        tags : "dict[str, str, int, int]" = utils.extract_tags(response)
        for tag, params in tags.items():
            if tag != "command":
                continue

            command, args = params["content"].split(" ", 1)

            if command not in self.plugins:
                continue

            response = self.plugins[command].execute(args)

            if self.plugins[command].remove_args_from_input:
                """
                remove the command tag and command name but not the arguments
                example: <command>command_name arg1 arg2</command> -> arg1 arg2
                """
                response = response[:params["start"]] + args + response[params["end"]:]
            else:
                response = response[:params["start"]] + response[params["end"]:]

