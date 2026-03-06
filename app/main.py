from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.lead_routes import router

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

# Routes
app.include_router(router)


@app.get("/")
def home():
    return {"status": "online", "message": "AI Agency Workflow Automation API"}


@app.get("/health")
def health_check():
    return {"status": "online", "service": "AI Agency Backend", "version": "1.0"}
