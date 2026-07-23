import whisper

model = whisper.load_model("base")

def speech_to_text(audio_path: str):
    result = model.transcribe(
        audio_path,
        language="en"
    )

    return result["text"]