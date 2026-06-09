"""
Task 9 — Retrieval Pipeline Hoan Chinh.

Ket hop semantic search + lexical search + reranking + PageIndex fallback
thanh mot pipeline thong nhat.

Logic:
    1. Chay semantic_search + lexical_search
    2. Merge ket qua (RRF)
    3. Rerank
    4. Neu top result score < threshold -> fallback sang PageIndex
    5. Return top_k results
"""

from .task5_semantic_search import semantic_search
from .task6_lexical_search import lexical_search
from .task7_reranking import rerank, rerank_rrf
from .task8_pageindex_vectorless import pageindex_search


# =============================================================================
# CONFIGURATION
# =============================================================================

SCORE_THRESHOLD = 0.3
DEFAULT_TOP_K = 5


def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
    use_reranking: bool = True,
) -> list[dict]:
    """
    Retrieval pipeline hoan chinh voi fallback logic.

    Pipeline:
        Query
          |-> Semantic Search -> results_dense
          |-> Lexical Search  -> results_sparse
          |
          |-> Merge (RRF) -> merged_results
          |-> Rerank -> reranked_results
          |
          |-> If best_score < threshold:
                |-> PageIndex Vectorless -> fallback_results

    Args:
        query: Cau truy van
        top_k: So luong ket qua cuoi cung
        score_threshold: Nguong diem toi thieu cho hybrid results
        use_reranking: Co ap dung reranking hay khong

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': str  # 'hybrid' hoac 'pageindex'
        }
    """
    # Step 1: Chay semantic + lexical search
    try:
        dense_results = semantic_search(query, top_k=top_k * 2)
    except Exception:
        dense_results = []

    try:
        sparse_results = lexical_search(query, top_k=top_k * 2)
    except Exception:
        sparse_results = []

    # Step 2: Merge bang RRF
    if dense_results or sparse_results:
        ranked_lists = []
        if dense_results:
            ranked_lists.append(dense_results)
        if sparse_results:
            ranked_lists.append(sparse_results)

        merged = rerank_rrf(ranked_lists, top_k=top_k * 2)
        for item in merged:
            item["source"] = "hybrid"
    else:
        merged = []

    # Step 3: Rerank
    if use_reranking and merged:
        final_results = rerank(query, merged, top_k=top_k)
    else:
        final_results = merged[:top_k]

    # Step 4: Check threshold -> fallback PageIndex
    best_score = final_results[0]["score"] if final_results else 0
    if not final_results or best_score < score_threshold:
        try:
            fallback = pageindex_search(query, top_k=top_k)
            if fallback:
                return fallback[:top_k]
        except Exception:
            pass

    return final_results[:top_k]


if __name__ == "__main__":
    test_queries = [
        "Hinh phat cho toi tang tru trai phep chat ma tuy",
        "Nghe si nao bi bat vi su dung ma tuy",
        "Luat phong chong ma tuy 2021 quy dinh gi ve cai nghien",
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print("-" * 60)
        results = retrieve(q, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['score']:.4f}] [{r['source']}] {r['content'][:80]}...")
