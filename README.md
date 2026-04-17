# 🚀 Auto BugFix — AI Powered Python Code Fixer

An AI-powered autonomous agent that identifies, analyzes, and repairs Python code using a Retrieval-Augmented Generation (RAG) pipeline.

-----

### 📌 Project Architecture

The system operates in a closed-loop sequence to ensure that only code which passes rigorous testing is integrated into the final output.

1.  **Detect:** Static analysis via **Pylint** to identify syntax errors and PEP8 violations.
2.  **Retrieve:** **FAISS** vector search (using `all-MiniLM-L6-v2` embeddings) to find similar historical bug-fix pairs.
3.  **Generate:** Fix synthesis via **Groq (Llama 3.1 8B)** using RAG-enriched contextual prompts.
4.  **Validate:** **Pytest** execution inside a sandboxed `TemporaryDirectory` to ensure the fix is safe and functional.
5.  **Learn:** Successful fixes are indexed back into the FAISS database and `rag_meta.json` for future retrieval.

-----

### 🛠 Tech Stack

  * **Language:** Python 3.10+
  * **AI Engine:** Groq API (Llama 3.1 8B Instant)
  * **Vector Database:** FAISS (Facebook AI Similarity Search)
  * **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
  * **Static Analysis:** Pylint
  * **Testing Framework:** Pytest
  * **Environment Management:** python-dotenv

-----

### 🧑‍💻 How To Run This Project

Follow these steps carefully to set up the environment on your device.

#### ✅ Step 1 — Clone the Repository

```bash
git clone https://github.com/arjunishere2107/auto_bugfix.git
cd auto_bugfix
```

#### ✅ Step 2 — Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### ✅ Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

#### ✅ Step 4 — Setup Environment Variables

Create a file in the root directory named `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

**⚠ Important:**

  * Do NOT add quotes around the key.
  * Do NOT push `.env` to GitHub (this project is pre-configured with a `.gitignore`).

#### ✅ Step 5 — Run the Project

**Core Pipeline (CLI):**

```bash
python src/main.py
```

**Using after 28 March 2026 (Web UI):**

```bash
streamlit run "user_interface Example 2.py"
```

*Workflow: User uploads file → Streamlit UI → AI pipeline runs → Verified fixed code is displayed.*

#### ✅ Step 6 — Run Tests (Optional)

```bash
pytest
```

-----

### 📂 Project Structure

```text
auto_bugfix/
│
├── src/
│   ├── main.py        # Orchestration layer for the pipeline
│   ├── detector.py    # Static analysis wrapping Pylint
│   ├── generator.py   # LLM interface and code sanitization
│   ├── retriever.py   # FAISS index and embedding management
│   ├── validator.py   # Sandboxed pytest execution logic
│   └── storage.py     # Persistent metadata management (JSON)
│
├── sample_code/       # Directory for target code and test suites
├── data/              # Persistent FAISS index and bug-fix logs
├── requirements.txt   # Project dependencies
├── .gitignore         # Excluded files (venv, .env, __pycache__)
└── README.md          # Project documentation
```

-----

### 🔐 Security & Technical Notes

  * **API Security:** Keys are managed strictly via environment variables.
  * **Sandboxing:** The `validator.py` logic utilizes `tempfile.TemporaryDirectory()`. This ensures that when the agent tests a generated fix, it does so in an isolated environment, preventing unauthorized modifications to your local source files until the fix is proven successful.
  * **Incremental Learning:** The system implements a "Self-Correction" loop. Every time a fix passes `pytest`, it is automatically added to the FAISS index, allowing the agent to become more accurate over time.

-----

### 💡 Future Improvements

  * **Web UI:** Fully integrated Streamlit/Flask interfaces.
  * **Containerization:** Dockerize the project for consistent deployment.
  * **CI/CD:** Integrate a pipeline for automated repository maintenance.
  * **Retrieval Tuning:** Further optimize FAISS search parameters for complex codebases.

-----

### 🔥 Extra Professional Touch (Recommended)

Also create a file called `.env.example` in the root directory to help other contributors.

-----

### 👨‍💻 Author

**Arjun Bhardwaj**
*B.Tech CSE (AI)*

```env
GROQ_API_KEY=your_api_key_here
```
