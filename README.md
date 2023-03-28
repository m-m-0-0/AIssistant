# AIssistant
A voice assistant for your computer, powered by Porcupine, Whisper, ChatGPT and Azure TTS.

## Setup
You need to have a few environmental variables set up before being able to run AIssistant.

`PCP_ACCESS_KEY`: PicoVoice access key, used for Porcupine for wake word detection (https://console.picovoice.ai/)  
`OPENAI_KEY`: OpenAI api key, used for Whisper voice transcription and ChatGPT (https://platform.openai.com/)  
`AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`: Used for Azure neural TTS (https://azure.microsoft.com/)  

After that follow these steps:
1. Create a new venv: `python -m venv env`
2. Activate the venv: `.\env\scripts\activate`
3. Install the prerequisites: `pip install -r requirements.txt`
4. Start the assistant: `python assistant.py`

## Running the assistant
To run the assistant, just run the following commands:

1. Activate the venv: `.\env\scripts\activate`
2. Start the assistant: `python assistant.py`

## Misc
For any criticism about my code, kindly refer to my GitHub bio.
