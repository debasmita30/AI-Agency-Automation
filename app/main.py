from fastapi import FastAPI
from app.routes.lead_routes import router

app = FastAPI(
    title="AI Agency Workflow Automation API",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "AI Agency Workflow Automation API"}