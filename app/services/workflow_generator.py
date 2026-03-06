from transformers import pipeline
from app.rag.knowledge_loader import retrieve_context

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