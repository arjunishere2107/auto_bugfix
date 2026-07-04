
import json
from pathlib import Path
from typing import List, Dict

RAG_META = Path("data/rag_meta.json")
RAG_META.parent.mkdir(exist_ok=True)

def load_meta() -> List[Dict]:
    """
    Load the RAG metadata list safely.
    Returns empty list if file is missing or invalid.
    """
    if not RAG_META.exists():
        return []
    try:
        return json.loads(RAG_META.read_text(encoding="utf-8"))
    except Exception:
        return []  # fallback if corrupted JSON

def save_meta(meta: List[Dict]):
    """
    Save metadata as pretty JSON.
    """
    RAG_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
