"""
Task 10 — Generation Co Citation.

Pipeline:
    1. Retrieve relevant chunks
    2. Reorder de tranh lost in the middle
    3. Format context voi source labels
    4. Build prompt (system + context + query)
    5. Call LLM (OpenAI)
    6. Return answer co citation

Configuration:
    - TOP_K=5: du evidence ma khong qua dai gay lost in the middle
    - TOP_P=0.9: du diverse nhung khong qua random
    - TEMPERATURE=0.3: RAG can factual, it sang tao
"""

import os
from dotenv import load_dotenv

load_dotenv()

from .task9_retrieval_pipeline import retrieve


# =============================================================================
# CONFIGURATION
# =============================================================================

# top_k: So chunks dua vao context
# Chon 5 vi: du evidence ma khong qua dai gay lost in the middle
TOP_K = 5

# top_p (nucleus sampling): Xac suat tich luy cho token generation
# Chon 0.9 vi: du diverse nhung khong qua random, phu hop cho RAG
TOP_P = 0.9

# temperature: Do ngau nhien cua output
# Chon 0.3 vi: RAG can factual, can cau tra loi chinh xac, it sang tao
TEMPERATURE = 0.3


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """Answer the following question comprehensively in Vietnamese.
For every statement of fact or claim, immediately insert a citation in brackets
linking to the specific source (e.g., [Luat Phong chong ma tuy 2021, Dieu 3]
or [VnExpress, 2024]).

If the information is not explicitly stated in the provided context or knowledge
base, state 'Toi khong the xac minh thong tin nay tu nguon hien co' rather than
guessing.

Rules:
- Only use information from the provided context
- Every factual claim MUST have a citation
- If context is insufficient, say so clearly
- Structure your answer with clear paragraphs"""


# =============================================================================
# DOCUMENT REORDERING (tranh lost in the middle)
# =============================================================================

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """
    Sap xep chunks de tranh "lost in the middle" effect.

    LLM nho tot thong tin o DAU va CUOI prompt, quen thong tin o GIUA.
    Strategy: dat chunks quan trong nhat o dau va cuoi, kem quan trong o giua.

    Input order (by score):  [1, 2, 3, 4, 5]
    Output order:            [1, 3, 5, 4, 2]
    (best first, worst in middle, second-best last)
    """
    if len(chunks) <= 2:
        return chunks

    reordered = []
    # Odd indices (0, 2, 4, ...) go first - important at beginning
    for i in range(0, len(chunks), 2):
        reordered.append(chunks[i])
    # Even indices (1, 3, 5, ...) in reverse - second-best at end
    for i in range(len(chunks) - 1 - (len(chunks) % 2 == 0), 0, -2):
        reordered.append(chunks[i])

    return reordered


# =============================================================================
# CONTEXT FORMATTING
# =============================================================================

def format_context(chunks: list[dict]) -> str:
    """
    Format chunks thanh context string cho prompt.
    Moi chunk co label source de LLM co the cite.
    """
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("source", f"Source {i}")
        doc_type = chunk.get("metadata", {}).get("type", "unknown")
        context_parts.append(
            f"[Document {i} | Source: {source} | Type: {doc_type}]\n"
            f"{chunk['content']}\n"
        )
    return "\n---\n".join(context_parts)


# =============================================================================
# GENERATION
# =============================================================================

def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """
    End-to-end RAG generation co citation.

    Args:
        query: Cau hoi cua user

    Returns:
        {
            'answer': str,           # Cau tra loi co citation
            'sources': list[dict],   # Cac chunks da dung
            'retrieval_source': str  # 'hybrid' hoac 'pageindex'
        }
    """
    # Step 1: Retrieve
    chunks = retrieve(query, top_k=top_k)

    if not chunks:
        return {
            "answer": "Toi khong the xac minh thong tin nay tu nguon hien co.",
            "sources": [],
            "retrieval_source": "none",
        }

    # Step 2: Reorder
    reordered = reorder_for_llm(chunks)

    # Step 3: Format context
    context = format_context(reordered)

    # Step 4: Build prompt
    user_message = f"Context:\n{context}\n\n---\n\nQuestion: {query}"

    # Step 5: Call LLM
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key == "sk-xxx":
        # No API key - return a structured answer from context
        return {
            "answer": f"[Auto-generated from context]\n\n{context[:500]}...",
            "sources": chunks,
            "retrieval_source": chunks[0].get("source", "hybrid") if chunks else "none",
        }

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=TEMPERATURE,
        top_p=TOP_P,
    )

    answer = response.choices[0].message.content

    # Step 6: Return
    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": chunks[0].get("source", "hybrid") if chunks else "none",
    }


if __name__ == "__main__":
    test_queries = [
        "Hinh phat cho toi tang tru trai phep chat ma tuy theo phap luat Viet Nam?",
    ]

    for q in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {q}")
        print("=" * 70)
        result = generate_with_citation(q)
        print(f"\nA: {result['answer']}")
        print(f"\n[Sources: {len(result['sources'])} chunks | via {result['retrieval_source']}]")
