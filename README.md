# 🎬 Sakila Database Chat (Local LLM + LangGraph)

A **fully local, offline Text-to-SQL chat application** built on the **Sakila MySQL database** using **LangGraph**, **LangChain**, **FastAPI**, **Streamlit**, and a **local Ollama LLM**.

The app converts natural-language questions into **safe, read-only SQL**, executes them on MySQL, and returns **human-readable answers** — without sending any data to the internet.

---

## ✨ Features

- 🔐 100% local & offline (no APIs, no cloud)
- 🤖 Local LLM via Ollama (`qwen2.5:14b`)
- 🧠 Natural Language → SQL → Answer
- 🧱 Strong SQL safety (SELECT-only, schema-aware)
- 🔁 Stateful workflow with LangGraph
- 🚀 FastAPI backend
- 💬 Streamlit chat UI + optional HTML UI
- 📊 Automatic table rendering for query results
- 🗄️ Live schema loading from MySQL

---

## 🏗️ Architecture

User (Browser / Streamlit)  
→ FastAPI  
→ LangGraph Flow  
→ Text → SQL (LLM)  
→ SQL Safety Check  
→ MySQL (Sakila)  
→ SQL → Natural Language Answer  
→ Final Response

---

## 🧩 Tech Stack

- **LLM Runtime:** Ollama  
- **Model:** qwen2.5:14b  
- **Orchestration:** LangGraph  
- **Framework:** LangChain  
- **Backend:** FastAPI  
- **Frontend:** Streamlit / HTML  
- **Database:** MySQL (Sakila)

---

## 📁 Project Structure

sakila-chat/  
├── app.py  
├── ui.py  
├── index.html  
├── README.md  
└── requirements.txt  

---

## ⚙️ Prerequisites

- Python 3.10 or 3.11  
- MySQL Server  
- Sakila database  
- Ollama installed  

---

## 🧠 Install Ollama & Model

Download Ollama: https://ollama.com/download

Verify:
ollama --version

Pull model (one time):
ollama pull qwen2.5:14b

---

## 🐍 Python Setup

Create venv:
python -m venv venv

Activate:
macOS/Linux: source venv/bin/activate  
Windows: venv\Scripts\activate  

Install dependencies:
pip install fastapi uvicorn streamlit mysql-connector-python sqlparse  
pip install langchain langgraph langchain-ollama

---

## 🗄️ Database Setup

Ensure credentials in app.py:

MYSQL_CONFIG = {
  host: localhost,
  user: sakila_user,
  password: sakila_pass,
  database: sakila
}

Grant read-only access:
GRANT SELECT ON sakila.* TO 'sakila_user'@'localhost';
FLUSH PRIVILEGES;

---

## ▶️ How to Run (IMPORTANT ORDER)

Terminal 1:
ollama serve

Terminal 2:
uvicorn app:app --reload

Terminal 3:
streamlit run ui.py

Open browser:
http://localhost:8501

---

## 🧪 Example Questions

- List 5 films with their rental rate
- Top 10 customers by total payment
- Which category has the most films?
- Actors who appeared in more than 20 films

---

## 🔐 SQL Safety Rules

- SELECT only
- No INSERT / UPDATE / DELETE
- No SELECT *
- Explicit JOINs required
- Schema-validated tables and columns

---

## 📴 Offline Guarantee

- No internet required after model download
- No API keys
- No cloud services
- All data stays local

---

## 📜 License

MIT
