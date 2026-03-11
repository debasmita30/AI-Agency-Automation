import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_whisper_status() -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return {"available": True, "mode": "openai_api", "model": "whisper-1"}
    return {"available": False, "mode": "unavailable", "message": "OPENAI_API_KEY not set"}

def transcribe_audio(file_bytes: bytes, filename: str, content_type: str) -> dict:
    try:
        import tempfile, os
        suffix = os.path.splitext(filename)[-1] or ".wav"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(model="whisper-1", file=f)
        os.unlink(tmp_path)
        return {"status": "success", "transcription": result.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
