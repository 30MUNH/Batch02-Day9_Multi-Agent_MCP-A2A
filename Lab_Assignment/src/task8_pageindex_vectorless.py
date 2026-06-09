"""
Task 8 — PageIndex Vectorless RAG.

PageIndex cho phep RAG ma khong can vector store — su dung
structural understanding cua document thay vi embedding.

Neu khong co API key, tra ve ket qua rong (fallback gracefully).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def _has_valid_api_key() -> bool:
    """Check if PageIndex API key is configured."""
    return bool(PAGEINDEX_API_KEY) and PAGEINDEX_API_KEY not in ("pi_xxx", "", "xxx")


def upload_documents():
    """Upload toan bo markdown documents len PageIndex."""
    if not _has_valid_api_key():
        print("  [WARN] PAGEINDEX_API_KEY chua duoc cau hinh")
        return

    try:
        from pageindex import PageIndex
        pi = PageIndex(api_key=PAGEINDEX_API_KEY)

        for md_file in STANDARDIZED_DIR.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            pi.upload(
                content=content,
                metadata={"filename": md_file.name, "type": md_file.parent.name}
            )
            print(f"  [OK] Uploaded: {md_file.name}")
    except ImportError:
        print("  [WARN] pageindex chua duoc cai dat: pip install pageindex")
    except Exception as e:
        print(f"  [ERR] Upload that bai: {e}")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval su dung PageIndex.
    Dung lam fallback khi hybrid search khong co ket qua tot.

    Args:
        query: Cau truy van
        top_k: So luong ket qua toi da

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': 'pageindex'
        }
    """
    if not _has_valid_api_key():
        # Fallback: tra ve ket qua tu local search don gian
        return _local_fallback_search(query, top_k)

    try:
        from pageindex import PageIndex
        pi = PageIndex(api_key=PAGEINDEX_API_KEY)
        results = pi.query(query=query, top_k=top_k)

        return [
            {
                "content": r.text if hasattr(r, 'text') else str(r),
                "score": r.score if hasattr(r, 'score') else 0.5,
                "metadata": r.metadata if hasattr(r, 'metadata') else {},
                "source": "pageindex"
            }
            for r in results
        ]
    except Exception as e:
        print(f"  [WARN] PageIndex query that bai: {e}")
        return _local_fallback_search(query, top_k)


def _local_fallback_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Fallback: tim kiem don gian trong cac file markdown khi khong co PageIndex API.
    Su dung keyword matching co ban.
    """
    results = []
    query_terms = query.lower().split()

    if not STANDARDIZED_DIR.exists():
        return results

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        content_lower = content.lower()

        # Simple scoring: count matching query terms
        score = sum(1 for term in query_terms if term in content_lower)
        if score > 0:
            # Return relevant excerpts
            lines = content.split("\n")
            relevant_lines = []
            for line in lines:
                line_lower = line.lower()
                if any(term in line_lower for term in query_terms):
                    relevant_lines.append(line.strip())
                if len(relevant_lines) >= 5:
                    break

            excerpt = "\n".join(relevant_lines) if relevant_lines else content[:500]
            results.append({
                "content": excerpt,
                "score": round(score / len(query_terms), 4),
                "metadata": {"source": md_file.name, "type": md_file.parent.name},
                "source": "pageindex"
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    if not _has_valid_api_key():
        print("[WARN] PAGEINDEX_API_KEY chua duoc cau hinh, su dung local fallback")
    else:
        print("Uploading documents...")
        upload_documents()

    print("\nTest query:")
    results = pageindex_search("hinh phat su dung ma tuy", top_k=3)
    for r in results:
        print(f"[{r['score']:.3f}] [{r['source']}] {r['content'][:100]}...")
