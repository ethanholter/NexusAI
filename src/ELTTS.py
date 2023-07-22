# Eleven Labs Text-To-Speech

import os

import requests
from pydub import AudioSegment
from pydub.playback import play

key = os.getenv("ELEVEN_LABS_API_KEY")

voice_keys = {
    "Wayne":"NqgC6vmdp2h8X7vyJv7E"
}
    
def speakText(text, voice_name="Wayne"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_keys[voice_name]}"

    querystring = {"optimize_streaming_latency":"22"}

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.8,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }
    
    headers = {
        "xi-api-key": "96c85a87b51e579e3966fcf324571d59",
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    if response.status_code == 200:
        audio_content = response.content
        with open("audio_file.mp3", "wb") as file:
            file.write(audio_content)

        audio = AudioSegment.from_mp3("audio_file.mp3")
        play(audio)

        os.remove("audio_file.mp3")
    else:
        print("Error:", response.status_code)
        
if __name__ == "__main__":
    speakText("Hello World - This is some sample text. How much wood would a wood chuck chuck if a wood chuck could chuck wood.")