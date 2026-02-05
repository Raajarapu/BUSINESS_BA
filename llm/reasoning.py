from transformers import pipeline

# Use a universally supported model
llm = pipeline(
    "text-generation",
    model="distilgpt2"
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
    output = llm(
        prompt,
        max_length=300,
        do_sample=True,
        temperature=0.7
    )

    return output[0]["generated_text"]
