
from pathlib import Path
import uuid

from detector import run_pylint
from retriever import query_similar, build_index, save_index
from generator import generate_fix
from validator import apply_fix_and_test
from storage import load_meta, save_meta
from dotenv import load_dotenv
load_dotenv()

SAMPLE_FILE = Path("sample_code/buggy.py")
TEST_FILE = Path("sample_code/test_buggy.py")

def read_file(p: Path):
    return p.read_text(encoding="utf-8")

def add_to_rag(bug_snippet, fix_snippet, filename):
    meta = load_meta()
    meta.append({
        "id": str(uuid.uuid4()),
        "bug_snippet": bug_snippet,
        "fix_snippet": fix_snippet,
        "filename": filename
    })
    save_meta(meta)

    # rebuild FAISS index
    index = build_index()
    save_index(index)

def run_pipeline():
    print("=== 1) Running pylint detector ===")
    msgs = run_pylint(str(SAMPLE_FILE))
    print("Pylint messages:", msgs)

    buggy_code = read_file(SAMPLE_FILE)

    print("\n=== 2) Retrieving similar cases from RAG ===")
    sim = query_similar(buggy_code)
    print("Retrieved examples:", sim)

    print("\n=== 3) Generating fix using LLM ===")
    fix_code = generate_fix(buggy_code, sim)
    print("Model returned:\n", fix_code[:500])

    print("\n=== 4) Running unit tests (pytest) ===")
    ok, logs = apply_fix_and_test(SAMPLE_FILE, fix_code, TEST_FILE)
    print("Tests pass:", ok)
    print("Logs:\n", logs)

    if ok:
        print("\n=== 5) Storing this fix into RAG memory ===")
        add_to_rag(buggy_code, fix_code, str(SAMPLE_FILE))
        print("Saved!")
    else:
        print("\nFix failed — please try again or manually review.")

if __name__ == "__main__":
    run_pipeline()
