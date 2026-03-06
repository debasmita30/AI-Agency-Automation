from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

labels = [
    "Website Development",
    "AI Automation",
    "Marketing Automation",
    "Data Analytics",
    "Chatbot Development",
    "Other"
]

def classify_project(description):

    result = classifier(
        description,
        candidate_labels=labels
    )

    return result["labels"][0]