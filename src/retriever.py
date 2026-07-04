
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from src.storage import load_meta
from pathlib import Path

EMB_MODEL = "all-MiniLM-L6-v2"  # small, fast
MODEL = SentenceTransformer(EMB_MODEL)

INDEX_PATH = Path("data/rag_index.faiss")


# -----------------------------
# Embed text safely
# -----------------------------
def embed(texts):
    if isinstance(texts, str):
        texts = [texts]
    return MODEL.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


# -----------------------------
# Build FAISS index from meta
# -----------------------------
def build_index():
    meta = load_meta()

    # If no examples exist → empty index
    if not meta:
        dim = MODEL.get_sentence_embedding_dimension()
        return faiss.IndexFlatL2(dim)

    # Combine bug + fix for better retrieval context
    docs = []
    for m in meta:
        bug = m.get("bug_snippet", "")
        fix = m.get("fix_snippet", "")
        docs.append(bug + "\n" + fix)

    embeddings = embed(docs)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index


# -----------------------------
# Save & Load index
# -----------------------------
def save_index(index):
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))


def load_index():
    if INDEX_PATH.exists():
        try:
            return faiss.read_index(str(INDEX_PATH))
        except:
            # corrupted or incompatible index → rebuild
            return build_index()
    return build_index()


# -----------------------------
# Query K most similar examples
# -----------------------------
def query_similar(bug_snippet, topk=3):
    meta = load_meta()
    if not meta:
        return []

    index = load_index()

    q = embed([bug_snippet])

    # If index empty
    if index.ntotal == 0:
        return []

    # FAISS query
    try:
        D, I = index.search(q, topk)
    except:
        # rebuild index if dimension mismatch
        index = build_index()
        save_index(index)
        D, I = index.search(q, topk)

    results = []
    for idx in I[0]:
        if idx < len(meta):
            results.append(meta[idx])

    return results
