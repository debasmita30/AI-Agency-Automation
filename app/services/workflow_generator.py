from transformers import pipeline
from app.rag.knowledge_loader import retrieve_context
from langgraph.graph import StateGraph, END
from typing import TypedDict

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_workflow(description):
    context = retrieve_context(description)
    prompt = f"""
You are an AI automation architect.
Using the knowledge below design a workflow.
Knowledge:
{context}
Client Request:
{description}
Return a structured automation pipeline.
"""
    result = generator(prompt, max_length=150)
    return result[0]["generated_text"]


class LeadState(TypedDict):
    lead_data: dict
    score: float
    priority: str
    proposal: str
    workflow: str
    status: str


def classify_lead(state: LeadState) -> LeadState:
    score = state.get("score", 0)
    if score >= 75:
        state["priority"] = "High"
    elif score >= 50:
        state["priority"] = "Medium"
    else:
        state["priority"] = "Low"
    state["status"] = "classified"
    return state


def score_lead(state: LeadState) -> LeadState:
    lead = state.get("lead_data", {})
    base_score = 50.0
    base_score += min(lead.get("ai_interest_level", 0) * 3, 30)
    base_score += min(lead.get("budget", 0) / 5000, 20)
    if lead.get("urgency") == "high":
        base_score += 10
    state["score"] = round(min(base_score, 100), 2)
    state["status"] = "scored"
    return state


def generate_proposal_node(state: LeadState) -> LeadState:
    description = state.get("lead_data", {}).get("description", "")
    if description:
        state["proposal"] = generate_workflow(description)
    else:
        state["proposal"] = "No description provided for proposal generation."
    state["status"] = "proposal_ready"
    return state


def finalize(state: LeadState) -> LeadState:
    state["workflow"] = (
        f"Lead Priority: {state.get('priority')} | "
        f"Score: {state.get('score')} | "
        f"Status: {state.get('status')}"
    )
    state["status"] = "complete"
    return state


def build_lead_workflow():
    workflow = StateGraph(LeadState)
    workflow.add_node("score", score_lead)
    workflow.add_node("classify", classify_lead)
    workflow.add_node("propose", generate_proposal_node)
    workflow.add_node("finalize", finalize)
    workflow.set_entry_point("score")
    workflow.add_edge("score", "classify")
    workflow.add_edge("classify", "propose")
    workflow.add_edge("propose", "finalize")
    workflow.add_edge("finalize", END)
    return workflow.compile()


lead_graph = build_lead_workflow()
