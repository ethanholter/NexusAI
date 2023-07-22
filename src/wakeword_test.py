import os

from pvcheetah import CheetahActivationLimitError, create
from pvrecorder import PvRecorder

from Assistant import Assistant
from ELTTS import speakText

DEBUG_MODE = False

def debugPrint(text):
    if DEBUG_MODE:
        print(text)
        
KEY = os.getenv("PICOVOICE_API_KEY")

cheetah = create(access_key=KEY,
                 endpoint_duration_sec=1)

try:
    print('Cheetah version : %s' % cheetah.version)

    recorder = PvRecorder(frame_length=cheetah.frame_length, device_index=1)
    recorder.start()
    print('Listening... (press Ctrl+C to stop)')

    try:
        while True:
            partial_transcript, is_endpoint = cheetah.process(recorder.read())
            print(partial_transcript, end='', flush=True)
            if is_endpoint:
                print(cheetah.flush())
    finally:
        print()
        recorder.stop()

except KeyboardInterrupt:
    pass
except CheetahActivationLimitError:
    print('AccessKey has reached its processing limit.')
finally:
    cheetah.delete()







# print(f"User: {text}")
# response = assistant.processInput(text)
# print("Jarvis: " + response)
# speakText(response)