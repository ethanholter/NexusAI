import json
import sys

from src.models.Assistant import Assistant
from src.text_to_speech.ELTTS import speakText

DISABLE_TTS = True
if DISABLE_TTS:
    # print("Warning: Text-To-Speech disabled to conserve API calls")
    print("\x1b[1;33m" + "Warning: Text-To-Speech disabled to conserve API calls" + "\x1b[0m")

if __name__ == "__main__":
    assistant = Assistant(verbose=True)
    
    with open(f"{sys.path[0]}/toolkits.json") as file:
        assistant.setFunctions(json.load(file))

    while True:
        try:
            userInput = input("User: ")
            
            if not userInput:
                break
            
            response = assistant.processInput(userInput)
            print("\x1b[1;37m" + "Nexus: " + response + "\x1b[0m")
            
            if not DISABLE_TTS:
                speakText(response)
                
        except KeyboardInterrupt:
            break