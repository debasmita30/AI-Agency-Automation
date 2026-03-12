import os
import tempfile

def get_whisper_status() -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return {"available": True, "mode": "groq_whisper", "model": "whisper-large-v3"}
    return {"available": False, "mode": "unavailable", "message": "GROQ_API_KEY not set"}

def transcribe_audio(file_bytes: bytes, filename: str, content_type: str = "audio/wav") -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"status": "error", "message": "GROQ_API_KEY not set"}
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        suffix = os.path.splitext(filename)[-1] or ".wav"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=f
            )
        os.unlink(tmp_path)
        return {"status": "success", "transcription": result.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
