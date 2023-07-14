import sys
import threading

import pyttsx3 as tts
import speech_recognition

recognizer = speech_recognition.Recognizer()
speaker = tts.init()
speaker.setProperty("rate", 150)



while True:
    with speech_recognition.Microphone() as mic:
        try:
            recognizer.adjust_for_ambient_noise(mic, duration=0.6)
            audio = recognizer.listen(mic, timeout=1)
            
            text = recognizer.recognize_google(audio).lower()
            
            if "jarvis" in text:
                print(text)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("error")
        