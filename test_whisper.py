import whisper

print("Loading Whisper model...")

model = whisper.load_model("base")

print("Model loaded!")

result = model.transcribe("answer.wav.m4a")

print("\nTranscription:")
print(result["text"])