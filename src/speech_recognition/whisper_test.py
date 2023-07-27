import sys

import whisper

model = whisper.load_model("tiny")
result = model.transcribe(f"{sys.path[0]}/Recording.m4a", fp16=False)
print(result["text"])