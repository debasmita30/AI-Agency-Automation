USE_TRANSFORMERS = False
classifier = None

try:
    from transformers import pipeline

    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

    USE_TRANSFORMERS = True

except Exception:
    USE_TRANSFORMERS = False


# ---------------- PROJECT LABELS ----------------

LABELS = [
    "Website Development",
    "AI Automation",
    "Marketing Automation",
    "Data Analytics",
    "Chatbot Development",
    "ML Pipeline",
    "Other"
]


# ---------------- CLASSIFICATION FUNCTION ----------------

def classify_project(description: str) -> str:
    """
    Classify project type from client description.

    Uses transformers model if available.
    Otherwise falls back to rule-based keyword classification.
    """

    if not description:
        return "Other"

    # -------- TRANSFORMERS MODEL --------

    if USE_TRANSFORMERS and classifier is not None:
        try:
            result = classifier(
                description,
                candidate_labels=LABELS
            )

            return result["labels"][0]

        except Exception:
            pass

    # -------- KEYWORD FALLBACK --------

    description_lower = description.lower()

    if any(word in description_lower for word in ["ai", "automation", "ml", "machine learning"]):
        return "AI Automation"

    if any(word in description_lower for word in ["chatbot", "bot", "assistant", "conversation"]):
        return "Chatbot Development"

    if any(word in description_lower for word in ["web", "website", "frontend", "backend"]):
        return "Website Development"

    if any(word in description_lower for word in ["data", "analytics", "dashboard", "visualization"]):
        return "Data Analytics"

    if any(word in description_lower for word in ["marketing", "email automation", "campaign"]):
        return "Marketing Automation"

    if any(word in description_lower for word in ["pipeline", "training", "model deployment"]):
        return "ML Pipeline"

    return "Other"
