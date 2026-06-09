"""
Task 7 — Reranking Module.

Implement RRF (Reciprocal Rank Fusion) de gop ket qua tu nhieu ranker.

RRF(d) = sum( 1 / (k + rank_r(d)) ) for each ranker r
  - k = 60 (smoothing constant, tu paper Cormack et al. 2009)
  - Uu diem: khong can huan luyen, khong can API key
  - Don gian nhung hieu qua trong viec gop nhieu ranked lists
"""


def rerank_rrf(
    ranked_lists: list[list[dict]], top_k: int = 5, k: int = 60
) -> list[dict]:
    """
    Reciprocal Rank Fusion — gop ket qua tu nhieu ranker.

    RRF(d) = sum( 1 / (k + rank_r(d)) )

    Args:
        ranked_lists: List of ranked result lists (moi list tu 1 ranker)
        top_k: So luong ket qua cuoi cung
        k: Smoothing constant (default=60, tu paper Cormack et al. 2009)

    Returns:
        List of top_k candidates sorted by RRF score descending.
    """
    rrf_scores = {}    # content -> score
    content_map = {}   # content -> full dict

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, 1):
            key = item["content"]
            rrf_scores[key] = rrf_scores.get(key, 0) + 1 / (k + rank)
            # Keep the item with best original score
            if key not in content_map or item.get("score", 0) > content_map[key].get("score", 0):
                content_map[key] = item

    # Sort by RRF score
    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for content, score in sorted_items[:top_k]:
        item = content_map[content].copy()
        item["score"] = round(score, 6)
        results.append(item)

    return results


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    method: str = "rrf",
) -> list[dict]:
    """
    Unified reranking interface.
    Default: su dung RRF de re-score candidates dua tren vi tri ranking.

    Args:
        query: Cau truy van
        candidates: Danh sach candidates tu retrieval
        top_k: So luong ket qua sau rerank
        method: Phuong phap reranking (mac dinh "rrf")

    Returns:
        List of top_k reranked candidates.
    """
    if not candidates:
        return []

    if method == "rrf":
        # Treat the single list as one ranked list for RRF
        # This effectively re-normalizes scores based on rank position
        return rerank_rrf([candidates], top_k=top_k)
    else:
        # Fallback: just sort by existing score and return top_k
        sorted_candidates = sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_candidates[:top_k]


if __name__ == "__main__":
    dummy_candidates = [
        {"content": "Dieu 248: Toi tang tru trai phep chat ma tuy", "score": 0.8, "metadata": {}},
        {"content": "Nghe si X bi bat vi su dung ma tuy", "score": 0.7, "metadata": {}},
        {"content": "Hinh phat tu tu 2-7 nam cho toi tang tru", "score": 0.6, "metadata": {}},
    ]
    results = rerank("hinh phat tang tru ma tuy", dummy_candidates, top_k=2)
    for r in results:
        print(f"[{r['score']:.6f}] {r['content']}")
