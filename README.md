🎬 Sakila Database Chat (Local LLM + LangGraph)
A fully local, offline Text-to-SQL chat application built on the Sakila MySQL database using LangGraph, LangChain, FastAPI, Streamlit, and a local Ollama LLM.
The app converts natural-language questions into safe, read-only SQL, executes them on MySQL, and returns human-readable answers — without sending any data to the internet.
✨ Features
🔐 100% local & offline (no APIs, no cloud)
🤖 Local LLM via Ollama (qwen2.5:14b)
🧠 Natural Language → SQL → Answer
🧱 Strong SQL safety (SELECT-only, schema-aware)
🔁 Stateful workflow with LangGraph
🚀 FastAPI backend
💬 Streamlit chat UI + optional HTML UI
📊 Automatic table rendering for query results
🗄️ Live schema loading from MySQL
🏗️ Architecture
User (Browser / Streamlit)
        |
        v
     FastAPI
        |
        v
   LangGraph Flow
        |
        v
+----------------------+
|  Text → SQL (LLM)    |
|  - Uses DB schema    |
|  - Strict rules     |
+----------------------+
        |
        v
   SQL Safety Check
        |
        v
     MySQL (Sakila)
        |
        v
+----------------------+
| SQL → NL Answer     |
|  - Uses only result |
+----------------------+
        |
        v
     Final Response
🧩 Tech Stack
Layer	Technology
LLM Runtime	Ollama
Model	qwen2.5:14b
Orchestration	LangGraph
LLM Framework	LangChain
Backend	FastAPI
Frontend	Streamlit / HTML
Database	MySQL (Sakila)
📁 Project Structure
sakila-chat/
│
├── app.py          # FastAPI backend + LangGraph
├── ui.py           # Streamlit chat UI
├── index.html      # Optional HTML frontend
├── README.md
└── requirements.txt
⚙️ Prerequisites
Python 3.10 or 3.11 (recommended)
MySQL Server
Sakila database loaded
Ollama installed
🧠 Install Ollama & Model
Install Ollama
👉 https://ollama.com/download
Verify installation:
ollama --version
Download the model (one-time)
ollama pull qwen2.5:14b
🐍 Python Setup
Create virtual environment
macOS / Linux
python -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate
Install dependencies
pip install fastapi uvicorn streamlit mysql-connector-python sqlparse
pip install langchain langgraph langchain-ollama
🗄️ Database Setup
Ensure Sakila DB exists and credentials match app.py:
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "sakila_user",
    "password": "sakila_pass",
    "database": "sakila"
}
Grant read-only access:
GRANT SELECT ON sakila.* TO 'sakila_user'@'localhost';
FLUSH PRIVILEGES;
▶️ How to Run (IMPORTANT ORDER)
Terminal 1 — Start Ollama
ollama serve
Terminal 2 — Start FastAPI
uvicorn app:app --reload
API endpoint:
http://127.0.0.1:8000/chat
Terminal 3 — Start Streamlit UI
streamlit run ui.py
Open in browser:
http://localhost:8501
🌐 Optional: HTML UI
Open index.html in your browser.
It calls the FastAPI backend at /chat.
🧪 Example Questions
List 5 films with their rental rate
Top 10 customers by total payment
Which category has the most films?
Actors who appeared in more than 20 films
🔐 SQL Safety Rules
✅ SELECT statements only
❌ No INSERT / UPDATE / DELETE
❌ No SELECT *
✅ Explicit JOINs required
✅ Schema-validated tables & columns
✅ Result limits enforced
If a question cannot be answered:
CANNOT_ANSWER
📴 Offline Guarantee
After pulling the model:
❌ No internet required
❌ No API keys
❌ No cloud services
✅ All data stays local
🚀 Future Enhancements
Schema caching for performance
SQL execution timeouts
Docker & docker-compose
Authentication & multi-user support
Query visualization
Result-only mode (skip explanation LLM)
📜 License
MIT (or your preferred license)
