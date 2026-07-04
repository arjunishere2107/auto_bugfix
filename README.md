🚀 Autonomous Bug Fixing Agent

An AI-powered autonomous debugging system that:

🔍 Detects Python bugs using Static Analysis (AST + Pylint)
📚 Retrieves similar bug fixes using FAISS (RAG)
🤖 Generates intelligent patches using Groq LLM
✅ Validates generated fixes automatically
🎨 Provides an interactive Streamlit-based web interface
📌 Project Architecture
                  User Uploads Python File
                           │
                           ▼
                  Streamlit Web Interface
                           │
                           ▼
                     Flask Backend API
                           │
                           ▼
              Static Analysis (AST + Pylint)
                           │
                           ▼
          Retrieval-Augmented Generation (FAISS)
                           │
                           ▼
                  Groq LLM Patch Generator
                           │
                           ▼
               Validation & Syntax Checking
                           │
                           ▼
          Fixed Code + Bug Report + Download
🛠 Tech Stack
Frontend
Streamlit
HTML
CSS
JavaScript
Backend
Flask
Python
AI Components
Groq LLM
FAISS
Sentence Transformers
Retrieval-Augmented Generation (RAG)
Analysis & Validation
Python AST
Pylint
Pytest
🧑‍💻 How To Run This Project

Follow these steps carefully.

✅ Step 1 — Clone the Repository
git clone https://github.com/arjunishere2107/auto_bugfix.git
cd auto_bugfix
✅ Step 2 — Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Linux / macOS
python3 -m venv venv
source venv/bin/activate
✅ Step 3 — Install Dependencies
pip install -r requirements.txt
✅ Step 4 — Configure Environment Variables

Create a file named:

.env

Add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here

Important

Never hardcode your API key.
Do not add quotation marks.
Do not upload your .env file to GitHub.
.env is already included in .gitignore.
✅ Step 5 — Start the Backend Server
python backend/server.py

The Flask API will start on:

http://127.0.0.1:5000

Keep this terminal running.

✅ Step 6 — Launch the Streamlit Frontend

Open another terminal.

Activate the virtual environment again.

Run:

streamlit run app.py

The application will automatically open in your browser.

📂 Project Structure
auto_bugfix/
│
├── app.py
├── backend/
│   └── server.py
│
├── frontend/
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
│   ├── rag_index.faiss
│   └── rag_meta.json
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
🔄 Application Workflow
User uploads Python file
            │
            ▼
Streamlit Interface
            │
            ▼
Flask Backend
            │
            ▼
Static Code Analysis
            │
            ▼
Bug Detection
            │
            ▼
RAG retrieves similar fixes
            │
            ▼
Groq LLM generates patch
            │
            ▼
Validation
            │
            ▼
Fixed Code + Report + Download
🔐 Security Notes
API keys are stored securely using environment variables.
.env is excluded through .gitignore.
No secrets are hardcoded into the project.
GitHub Push Protection is supported.
📄 .env.example

Create a file named:

.env.example

Contents:

GROQ_API_KEY=your_groq_api_key_here
🚀 Run Commands
Terminal 1
python backend/server.py
Terminal 2
streamlit run app.py
💡 Future Improvements
Multi-language support
VS Code Extension
Docker Deployment
GitHub Pull Request Integration
CI/CD Pipeline
Advanced Bug Classification
Automated Unit Test Generation
Self-learning RAG Knowledge Base