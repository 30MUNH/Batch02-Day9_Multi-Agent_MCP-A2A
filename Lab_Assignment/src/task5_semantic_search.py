"""
Task 5 — Semantic Search Module.

Tim kiem ngu nghia (dense retrieval) tren ChromaDB vector store.
Su dung cung embedding model (all-MiniLM-L6-v2) voi Task 4.
"""

from .task4_chunking_indexing import get_embedding_model, get_chroma_collection


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tim kiem ngu nghia su dung vector similarity.

    Args:
        query: Cau truy van
        top_k: So luong ket qua toi da

    Returns:
        List of {
            'content': str,      # Noi dung chunk
            'score': float,      # Cosine similarity score
            'metadata': dict     # source, type, chunk_index
        }
        Sorted by score descending.
    """
    # Step 1: Embed query
    model = get_embedding_model()
    query_embedding = model.encode(query).tolist()

    # Step 2: Query ChromaDB
    collection = get_chroma_collection()
    if collection.count() == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    # Step 3: Format results
    # ChromaDB returns cosine distance, convert to similarity: 1 - distance
    output = []
    if results and results["documents"] and results["documents"][0]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            score = 1.0 - dist  # cosine distance -> similarity
            output.append({
                "content": doc,
                "score": round(score, 4),
                "metadata": meta,
            })

    # Sort by score descending
    output.sort(key=lambda x: x["score"], reverse=True)
    return output[:top_k]


if __name__ == "__main__":
    results = semantic_search("hinh phat cho toi tang tru ma tuy", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
