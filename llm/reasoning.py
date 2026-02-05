from transformers import pipeline
from config import LLM_MODEL

llm = pipeline(
    "text2text-generation",
    model=LLM_MODEL
)

def reason(context, question):
    prompt = f"""
You are a senior business analyst.

Context:
{context}

Question:
{question}

Provide structured, data-driven business insights.
"""
    result = llm(prompt, max_length=512)
    return result[0]["generated_text"]
