import os
import tempfile

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

_model = None

def get_whisper_model():
    global _model
    if _model is None and WHISPER_AVAILABLE:
        _model = whisper.load_model("base")
    return _model

def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> dict:
    if not WHISPER_AVAILABLE:
        return {
            "success": False,
            "text": "",
            "error": "Whisper not installed"
        }
    try:
        model = get_whisper_model()
        with tempfile.NamedTemporaryFile(
            suffix=os.path.splitext(filename)[-1] or ".wav",
            delete=False
        ) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        result = model.transcribe(tmp_path)
        os.unlink(tmp_path)
        return {
            "success": True,
            "text": result["text"].strip(),
            "language": result.get("language", "en"),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "error": str(e)
        }
