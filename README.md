# 🚀 Autonomous Bug Fixing Agent

> **AI-Powered Python Bug Detection, Repair & Validation System**

An intelligent bug-fixing assistant that automatically detects bugs in Python code, retrieves similar fixes using Retrieval-Augmented Generation (RAG), generates context-aware patches using a Large Language Model (Groq LLM), and validates the repaired code before presenting the final output.

---

## ✨ Features

- 🔍 Automatic Python bug detection using **Pylint**
- 🧠 AI-powered bug repair using **Groq LLM**
- 📚 Retrieval-Augmented Generation (RAG) with **FAISS**
- ✅ Automatic validation using **Pytest**
- 🎨 Modern Streamlit-based user interface
- 📄 Supports uploading Python (`.py`) files
- ⚡ End-to-end automated bug fixing pipeline

---

# 🏗️ System Architecture

```
            User Uploads Python File
                     │
                     ▼
          Streamlit Web Interface
                     │
                     ▼
            Pylint Static Analysis
                     │
                     ▼
        FAISS RAG Similar Bug Retrieval
                     │
                     ▼
          Groq LLM Patch Generation
                     │
                     ▼
           Automatic Validation
                     │
                     ▼
        Display Fixed Python Code
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend Development |
| Streamlit | Frontend UI |
| Flask | API Server |
| Pylint | Static Code Analysis |
| Pytest | Validation & Testing |
| FAISS | Vector Database / RAG |
| Sentence Transformers | Embeddings |
| Groq API | LLM-based Patch Generation |
| python-dotenv | Environment Variable Management |

---

# 📂 Project Structure

```
auto_bugfix/
│
├── app.py                    # Streamlit Frontend
│
├── backend/
│   └── server.py             # Flask Backend API
│
├── frontend/                 # UI Components
│
├── src/
│   ├── detector.py
│   ├── generator.py
│   ├── retriever.py
│   ├── validator.py
│   ├── storage.py
│   └── main.py
│
├── data/
│
├── requirements.txt
│
├── .env.example
│
└── README.md
```

---

# 🚀 Getting Started

## Step 1 — Clone the Repository

```bash
git clone https://github.com/arjunishere2107/auto_bugfix.git
cd auto_bugfix
```

---

## Step 2 — Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Configure Environment Variables

Create a file named:

```
.env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

> ⚠️ **Important**
>
> - Never commit your `.env` file.
> - Keep your API key private.
> - The `.env` file is already ignored via `.gitignore`.

---

# ▶️ Running the Project

## ✅ Current Version (Streamlit UI)

Start the Flask backend:

```bash
python backend/server.py
```

Open another terminal and launch the Streamlit application:

```bash
streamlit run app.py
```

Open your browser and navigate to:

```
http://localhost:8501
```

Upload a Python file and let the AI detect, repair, and validate bugs automatically.

---

## 📌 Legacy CLI Version (Before March 2026)

If you are using an older version of the project:

```bash
python src/main.py
```

---

# 🧪 Running Tests

```bash
pytest
```

---

# 🔄 Workflow

```
Upload Python File
        │
        ▼
Static Analysis (Pylint)
        │
        ▼
Retrieve Similar Fixes (FAISS RAG)
        │
        ▼
Generate AI Patch (Groq LLM)
        │
        ▼
Validate Fix (Pytest)
        │
        ▼
Return Fixed Code
```

---

# 🔐 Security

- API keys are securely stored using environment variables.
- `.env` is excluded from Git tracking.
- No credentials are hardcoded in the source code.
- GitHub Secret Scanning compatible.

---

# 🌍 Sustainable Development Goals (SDGs)

This project contributes to:

- 🎯 SDG 4 — Quality Education
- 🎯 SDG 8 — Decent Work and Economic Growth
- 🎯 SDG 9 — Industry, Innovation and Infrastructure

---

# 💡 Future Enhancements

- 🤖 Multi-language support (Java, C++, JavaScript)
- 🐳 Docker deployment
- ☁️ Cloud deployment
- 🔄 CI/CD integration
- 📊 Bug analytics dashboard
- 🧠 Fine-tuned bug-fixing model
- 👥 Team collaboration features

---

# 👨‍💻 Author

## Arjun Bhardwaj

**B.Tech Computer Science & Engineering (AI)**

- Python Developer
- AI/LLM Enthusiast
- Backend Developer
- Machine Learning Enthusiast

GitHub: **https://github.com/arjunishere2107**

---

# ⭐ Support

If you found this project helpful, consider giving it a **⭐ Star** on GitHub!

It motivates future improvements and helps others discover the project.

---

## 📜 License

This project is intended for educational and research purposes.