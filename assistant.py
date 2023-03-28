import speech_recognition as sr
import pvporcupine

import openai
import tiktoken

import azure.cognitiveservices.speech as speechsdk

import pyaudio
import struct
import copy
import os
import re
import urllib.parse
import json

import pyperclip
from playsound import playsound
import win10toast

#utilities to time functions
import time

BOT_NAME = "BlueBerry"
AZURE_VOICE = "en-US-AriaNeural"
KEYWORDS = ["blueberry"]
OPENAI_MODEL = "gpt-3.5-turbo" #only chat models are supported

#api keys
PCP_ACCESS_KEY = os.environ.get('PORCUPINE_KEY')
OPENAI_KEY = os.environ.get('OPENAI_KEY')
AZURE_SPEECH_KEY = os.environ.get('SPEECH_KEY')
AZURE_SPEECH_REGION = os.environ.get('SPEECH_REGION')

rec_start = "./sounds/rec_start.wav"
rec_finish = "./sounds/rec_finish.wav"

#Speech recognition
sr_instance = sr.Recognizer()

#OpenAI
tokenizer = tiktoken.encoding_for_model(OPENAI_MODEL)

#Azure Speech API
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

#Porcupine wake word
porcupine = pvporcupine.create(PCP_ACCESS_KEY, keywords=KEYWORDS)

"""
takes a file path as input and returns a string with placeholders that can be filled in by keyword arguments provided as **kwargs.
"""
def load_prompt(path, **kwargs):
    with open(path, "r") as f:
        prompt = f.read()
    
    return prompt.format(**kwargs)

"""
waits for the hotword to be said and returns when it is detected
"""
def wait_for_hotword(mic_index):
    audio_stream = pyaudio.PyAudio().open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        input_device_index=mic_index,
        frames_per_buffer=int(porcupine.sample_rate / 10)
    )
    
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        index = porcupine.process(pcm)

        if index >= 0:
            break

    audio_stream.close()

"""
records audio until silence is detected and returns the audio if detected, otherwise returns None
"""
def record_till_silence(mic_index, timeout=6):
    with sr.Microphone(device_index=mic_index) as source:
        try:
            audio = sr_instance.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            return None
        
        return audio
    
"""
transcribes audio and returns the transcription if any speech is detected, otherwise returns None
"""
def transcribe_audio(audio):
    try:
        text = sr_instance.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    
    return text

def preprocess_ssml_text(text, voice_name="en-US-AriaNeural", rate="medium"):
    if rate not in ["x-slow", "slow", "medium", "fast", "x-fast"]:
        raise ValueError("Invalid rate value")

    text = f"<speak xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:mstts=\"http://www.w3.org/2001/mstts\" xmlns:emo=\"http://www.w3.org/2009/10/emotionml\" version=\"1.0\" xml:lang=\"en-US\"><voice name=\"{voice_name}\"><prosody rate=\"{rate}\">{text}</prosody></voice></speak>"
    return text

def stream_tts_async(text, use_ssml=False):
    if use_ssml:
        future = speech_synthesizer.start_speaking_ssml_async(text)
    else:
        future = speech_synthesizer.start_speaking_text_async(text)

    return future

def get_chat_completion(prompt, query):
    chatgpt_messages = [{"role": "system", "content": prompt},
                        {"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chatgpt_messages,
        temperature=0.5,
        max_tokens=500)

    response = response['choices'][0]['message']['content']
    return response

def strip_command(text):
    #detect command tag
    command_tag = re.search(r"<command>(.*?)</command>", text)
    if command_tag is None:
        return None, text, None
    
    command = command_tag.group(1)
    return command, (text.replace(command_tag.group(0), "") if command != "copy" else text.replace(command_tag.group(0), command[5:])), command_tag.start()

def display_toast(title, text, icon_path=None, duration=5):
    toaster = win10toast.ToastNotifier()
    toaster.show_toast(title, text, icon_path=icon_path, duration=duration)

if __name__ == '__main__':
    mic_index = pyaudio.PyAudio().get_default_input_device_info()['index']
    print(pyaudio.PyAudio().get_device_info_by_index(mic_index)['name'])


    with open ("./paths_whitelist.json", "r") as f:
        paths = json.load(f)

    prompt = load_prompt("./prompt.txt", apps_names=paths.keys())

    prompt_length = len(tokenizer.encode(prompt))
    print("Prompt length:", prompt_length)

    while True:
        #start waiting for hotword
        wait_for_hotword(mic_index)

        #hotword detected
        playsound(rec_start)
        audio = record_till_silence(mic_index)
        playsound(rec_finish)

        if audio is None:
            continue

        #start timer
        start_time = time.time()

        text = transcribe_audio(audio)

        if text is not None:
            print("Query: " + text if text is not None else "No speech detected")
            print("Query length:", len(tokenizer.encode(text)) + prompt_length)
            response = get_chat_completion(prompt, text)
            print("Response: " + response)

            command, response, position = strip_command(response)
            while command is not None:
                command = command.lstrip().rstrip().lower()
                print("Command detected: " + command)
                if command.startswith("open"):
                    app = command[5:]
                    print("Opening " + app)
                    try:
                        os.system(f'"{paths[app]}"')
                    except:
                        pass
                elif command.startswith("calculate"):
                    answer = eval(command[10:])
                    response = response.replace("answerhere", str(answer))
                elif command.startswith("copy"):
                    copy_text = command[5:]
                    print("Copying text to clipboard: " + copy_text)
                    display_toast("Copied to clipboard", copy_text)
                    pyperclip.copy(copy_text)
                elif command.startswith("navigate"):
                    url = command[9:]
                    print("Navigating to " + url)
                    os.system(f'start {urllib.parse.quote(url, safe=":/?=")}')
                else:
                    print("Command not recognized: " + command)
                    #put it back in the response
                    response = response[:position] + command + response[position:]

                command, response, position = strip_command(response)
            
            ssml_response = preprocess_ssml_text(response)
            speech_synthesizer.stop_speaking_async().get()
            
            future = stream_tts_async(ssml_response, use_ssml=True)
        else:
            print("No command/query detected")

        #stop timer
        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.3f} seconds")