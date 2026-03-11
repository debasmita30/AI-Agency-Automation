from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.routes.lead_routes import router
from app.services.lead_scoring_service import score_lead
from app.services.proposal_generator import generate_proposal
from app.services.transcription_service import transcribe_audio, WHISPER_AVAILABLE

app = FastAPI(
    title="AI Agency Workflow Automation API",
    description="AI-powered lead scoring, proposal generation, and workflow automation",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {"status": "online", "message": "AI Agency Workflow Automation API"}

@app.get("/health")
def health_check():
    return {"status": "online", "service": "AI Agency Backend", "version": "1.0"}

@app.get("/transcription/status")
def transcription_status():
    return {"available": WHISPER_AVAILABLE, "model": "whisper-base"}

@app.post("/transcription/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    result = transcribe_audio(audio_bytes, filename=file.filename)
    if not result["success"]:
        return {"status": "error", "message": result["error"]}
    return {
        "status": "success",
        "transcription": result["text"],
        "language": result["language"]
    }

@app.websocket("/ws/lead")
async def websocket_lead(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        await websocket.send_json({"stage": "received", "message": "Lead data received"})
        score = score_lead(data)
        await websocket.send_json({"stage": "scored", "lead_score": score})
        proposal = generate_proposal(data)
        await websocket.send_json({"stage": "complete", "proposal": proposal, "lead_score": score})
    except Exception as e:
        await websocket.send_json({"stage": "error", "message": str(e)})
    finally:
        await websocket.close()
