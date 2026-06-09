"""
Task 4 — Chunking & Indexing vao Vector Store.

Chunking strategy: RecursiveCharacterTextSplitter
  - An toan, pho bien, phu hop cho cac loai document
  - CHUNK_SIZE=500: du nho de tim kiem chinh xac, du lon de giu ngu canh
  - CHUNK_OVERLAP=50: dam bao khong mat thong tin o ranh gioi chunk

Embedding model: sentence-transformers/all-MiniLM-L6-v2
  - Nhe (80MB), nhanh, phu hop cho prototype
  - 384 dimensions
  - Multilingual support co ban

Vector store: ChromaDB
  - Don gian, chay local khong can Docker
  - Phu hop cho prototype va demo
"""

from pathlib import Path

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "data" / "chromadb"

# =============================================================================
# CONFIGURATION
# =============================================================================

# RecursiveCharacterTextSplitter:
#   CHUNK_SIZE=500 vi: van ban phap luat thuong co cac dieu khoan ngan,
#   500 chars du de giu 1-2 dieu trong 1 chunk ma van du nho de retrieval chinh xac.
CHUNK_SIZE = 500

# CHUNK_OVERLAP=50 vi: dam bao cac cau o ranh gioi khong bi cat doi,
# 10% overlap la ty le pho bien.
CHUNK_OVERLAP = 50

CHUNKING_METHOD = "recursive"

# all-MiniLM-L6-v2: nhe, nhanh, multilingual co ban, phu hop prototype
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

VECTOR_STORE = "chromadb"
COLLECTION_NAME = "drug_law_docs"


# =============================================================================
# IMPLEMENTATION
# =============================================================================

def load_documents() -> list[dict]:
    """
    Doc toan bo markdown files tu data/standardized/.

    Returns:
        List of {'content': str, 'metadata': {'source': str, 'type': str}}
    """
    documents = []
    if not STANDARDIZED_DIR.exists():
        return documents

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        if len(content.strip()) < 50:
            continue
        doc_type = "legal" if "legal" in str(md_file) else "news"
        documents.append({
            "content": content,
            "metadata": {"source": md_file.name, "type": doc_type}
        })
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Chunk documents bang RecursiveCharacterTextSplitter.

    Returns:
        List of {'content': str, 'metadata': dict}
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(splits):
            chunks.append({
                "content": chunk_text,
                "metadata": {**doc["metadata"], "chunk_index": i}
            })
    return chunks


def get_embedding_model():
    """Load embedding model (cached)."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Embed toan bo chunks."""
    model = get_embedding_model()
    texts = [c["content"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb.tolist()
    return chunks


def get_chroma_collection():
    """Get or create ChromaDB collection."""
    import chromadb
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def index_to_vectorstore(chunks: list[dict]):
    """Luu chunks vao ChromaDB."""
    collection = get_chroma_collection()

    # Clear existing data
    existing = collection.count()
    if existing > 0:
        collection.delete(ids=[str(i) for i in range(existing)])

    # Batch insert
    batch_size = 100
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        ids = [str(start + i) for i in range(len(batch))]
        documents = [c["content"] for c in batch]
        embeddings = [c["embedding"] for c in batch]
        metadatas = [c["metadata"] for c in batch]

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    print(f"  [OK] Indexed {collection.count()} chunks to ChromaDB")


def run_pipeline():
    """Chay toan bo pipeline: load -> chunk -> embed -> index."""
    print("=" * 50)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: {VECTOR_STORE}")
    print("=" * 50)

    docs = load_documents()
    print(f"\n[OK] Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"[OK] Created {len(chunks)} chunks")

    chunks = embed_chunks(chunks)
    print(f"[OK] Embedded {len(chunks)} chunks")

    index_to_vectorstore(chunks)
    print("[OK] Done!")


if __name__ == "__main__":
    run_pipeline()
