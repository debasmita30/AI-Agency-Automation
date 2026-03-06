from pydantic import BaseModel, EmailStr, Field


class LeadRequest(BaseModel):

    name: str = Field(..., min_length=2)
    email: EmailStr
    description: str = Field(..., min_length=10)

    company_size: int = Field(..., ge=1)
    budget: float = Field(..., ge=100)

    urgency: int = Field(..., ge=1, le=3)

    ai_interest: int = Field(..., ge=0, le=1)


class LeadResponse(BaseModel):

    project_type: str
    lead_score: float
    priority: str
    proposal: str