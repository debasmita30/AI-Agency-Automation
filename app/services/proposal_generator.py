from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)

def generate_proposal(project_type, description):

    prompt = f"""
Write a professional proposal for an AI automation project.

Project Type: {project_type}

Client Request: {description}

Include:
1. brief solution
2. estimated timeline
3. expected outcome
"""

    result = generator(
        prompt,
        max_length=200,
        do_sample=True
    )

    return result[0]["generated_text"]