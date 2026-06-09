"""
Task 6 — Lexical Search Module (BM25).

Su dung BM25Okapi tu rank-bm25.
BM25 hoat dong the nao:
    - Term Frequency (TF): tu xuat hien nhieu trong document -> diem cao
    - Inverse Document Frequency (IDF): tu hiem -> quan trong hon
    - Document length normalization: document dai khong bi uu tien qua muc
    - k1=1.5 (term saturation), b=0.75 (length normalization)
"""

from pathlib import Path
from rank_bm25 import BM25Okapi

# Global BM25 index and corpus
_bm25 = None
_corpus = None


def _load_corpus() -> list[dict]:
    """Load chunks tu data/standardized/ va chunk chung."""
    from .task4_chunking_indexing import load_documents, chunk_documents
    docs = load_documents()
    if not docs:
        return []
    chunks = chunk_documents(docs)
    return chunks


def _get_bm25():
    """Build hoac tra ve BM25 index (cached)."""
    global _bm25, _corpus
    if _bm25 is not None and _corpus is not None:
        return _bm25, _corpus

    _corpus = _load_corpus()
    if not _corpus:
        return None, []

    # Tokenize corpus - dung split() don gian cho tieng Viet
    tokenized_corpus = [doc["content"].lower().split() for doc in _corpus]
    _bm25 = BM25Okapi(tokenized_corpus)
    return _bm25, _corpus


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tim kiem tu khoa su dung BM25.

    Args:
        query: Cau truy van
        top_k: So luong ket qua toi da

    Returns:
        List of {
            'content': str,
            'score': float,      # BM25 score
            'metadata': dict
        }
        Sorted by score descending.
    """
    bm25, corpus = _get_bm25()
    if bm25 is None or not corpus:
        return []

    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    # Get top_k indices sorted by score descending
    indexed_scores = list(enumerate(scores))
    indexed_scores.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, score in indexed_scores[:top_k]:
        if score > 0:
            results.append({
                "content": corpus[idx]["content"],
                "score": round(float(score), 4),
                "metadata": corpus[idx]["metadata"],
            })

    return results


if __name__ == "__main__":
    results = lexical_search("Dieu 248 tang tru trai phep chat ma tuy", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
