from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)


def generate_response(question, retrieved):
    """
    Generate a grounded response using ONLY retrieved reviews.

    Parameters
    ----------
    question : str
        User question

    retrieved : dict
        Output from retrieve()

    Returns
    -------
    dict
        {
            "answer": str,
            "sources": list[str]
        }
    """

    contexts = []
    sources = []

    docs = retrieved["documents"][0]
    metas = retrieved["metadatas"][0]

    for doc, meta in zip(docs, metas):

        source_file = meta["source"]

        contexts.append(
            f"Professor: {meta['professor']}\n"
            f"Source File: {source_file}\n"
            f"Review Text: {doc}"
        )

        sources.append(source_file)

    context_text = "\n\n".join(contexts)

    prompt = f"""
You are a retrieval-augmented assistant answering questions about
ASU Computer Science professors.

IMPORTANT RULES:

1. Use ONLY information found in the retrieved reviews.
2. Do NOT use outside knowledge.
3. Do NOT invent facts that are not supported by the retrieved reviews.
4. You MAY summarize, compare, and synthesize information across multiple retrieved reviews.
5. Any conclusion must be reasonably supported by the retrieved reviews.
6. When appropriate, mention the source filename that supports the information.
7. If the retrieved reviews do not provide enough evidence to answer the question, respond exactly:

"I could not find enough information in the retrieved reviews."

8. When answering comparison questions, compare only the professors and evidence found in the retrieved reviews.
9. Do not claim certainty when the evidence is limited. Prefer phrases such as:
   - "Based on the retrieved reviews..."
   - "According to the retrieved reviews..."
   - "The retrieved reviews suggest..."
   - "Among the retrieved reviews..."

10. Keep answers concise and focused on the question.
11. Do not mention information that does not appear in the retrieved reviews.

Retrieved Reviews:

{context_text}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded RAG assistant. "
                    "Use only the retrieved reviews as evidence. "
                    "You may summarize and compare information across the reviews, "
                    "but do not use outside knowledge."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        top_p=0.1
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sorted(set(sources))
    }