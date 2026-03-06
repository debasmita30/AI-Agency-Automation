from fastapi import APIRouter
from app.models.lead_schema import LeadRequest, LeadResponse
from app.services.ai_analyzer import classify_project
from app.services.proposal_generator import generate_proposal
from app.services.lead_scoring_service import predict_lead_score

router = APIRouter()


@router.post("/lead", response_model=LeadResponse)
def process_lead(data: LeadRequest):

    project_type = classify_project(data.description)

    proposal = generate_proposal(
        project_type,
        data.description
    )

    score = predict_lead_score(
        data.company_size,
        data.budget,
        data.urgency,
        data.ai_interest
    )

    if score > 80:
        priority = "High Value Client"
    elif score > 50:
        priority = "Medium Priority"
    else:
        priority = "Low Priority"

    return {
        "project_type": project_type,
        "lead_score": score,
        "priority": priority,
        "proposal": proposal
    }