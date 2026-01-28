from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from decimal import Decimal
import sqlparse

from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# =====================================================
# DATABASE CONFIG (READ-ONLY USER RECOMMENDED)
# =====================================================

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "sakila_user",
    "password": "sakila_pass",
    "database": "sakila"
}

# =====================================================
# LOAD FULL SCHEMA FROM information_schema
# =====================================================

def load_full_schema() -> str:
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        ORDER BY table_name, ordinal_position
    """, (MYSQL_CONFIG["database"],))

    schema = {}
    for table, column, dtype in cursor.fetchall():
        schema.setdefault(table, []).append(f"{column} ({dtype})")

    conn.close()

    formatted = []
    for table, columns in schema.items():
        formatted.append(
            f"{table}(\n  " + ",\n  ".join(columns) + "\n)"
        )

    return "\n\n".join(formatted)

# =====================================================
# SYSTEM PROMPTS
# =====================================================

SQL_SYSTEM_PROMPT = """
You are a MySQL Text-to-SQL engine.

ABSOLUTE RULES:
- Output ONLY one valid MySQL SELECT statement
- Use ONLY tables and columns present in the schema
- Use explicit JOINs with ON conditions
- NEVER use SELECT *
- LIMIT results to 20 rows unless aggregation is used
- Do NOT explain anything
- Do NOT use markdown
- If the question cannot be answered using the schema, output exactly:
CANNOT_ANSWER
"""

ANSWER_SYSTEM_PROMPT = """
You are a database assistant.

Rules:
- Answer ONLY using the SQL result
- Do NOT use outside knowledge
- If the result is empty, say:
No data found in the database.
"""

# =====================================================
# LOCAL LLM (ADVANCED MODEL – OLLAMA)
# =====================================================

llm = ChatOllama(
    model="qwen2.5:14b",  # change to deepseek-coder:33b if you have RAM
    temperature=0
)

# =====================================================
# TEXT → SQL
# =====================================================

def text_to_sql(question: str) -> str:
    schema = load_full_schema()

    messages = [
        SystemMessage(content=SQL_SYSTEM_PROMPT),
        HumanMessage(content=f"""
DATABASE SCHEMA:
{schema}

QUESTION:
{question}

SQL:
""")
    ]

    response = llm.invoke(messages)
    return response.content.strip()

# =====================================================
# SQL SAFETY CHECK
# =====================================================

def is_safe_select(sql: str) -> bool:
    try:
        parsed = sqlparse.parse(sql)
        return parsed and parsed[0].get_type() == "SELECT"
    except Exception:
        return False

# =====================================================
# EXECUTE SQL
# =====================================================

def execute_sql(sql: str):
    if not is_safe_select(sql):
        return None

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    # Convert Decimal → float
    cleaned = []
    for row in rows:
        cleaned_row = {}
        for k, v in row.items():
            cleaned_row[k] = float(v) if isinstance(v, Decimal) else v
        cleaned.append(cleaned_row)

    return cleaned

# =====================================================
# SQL RESULT → NATURAL LANGUAGE ANSWER
# =====================================================

def explain_result(question: str, rows):
    if not rows:
        return "No data found in the database."

    messages = [
        SystemMessage(content=ANSWER_SYSTEM_PROMPT),
        HumanMessage(content=f"""
Question:
{question}

SQL Result:
{rows}
""")
    ]

    response = llm.invoke(messages)
    return response.content.strip()

# =====================================================
# LANGGRAPH NODE
# =====================================================

def ollama_node(state: MessagesState):
    question = state["messages"][-1].content

    sql = text_to_sql(question)

    if sql == "CANNOT_ANSWER":
        return {
            "messages": state["messages"] + [
                AIMessage(content="I don’t have information about this in my database.")
            ]
        }

    rows = execute_sql(sql)
    answer = explain_result(question, rows)

    return {
        "messages": state["messages"] + [
            AIMessage(content=answer)
        ]
    }

# =====================================================
# LANGGRAPH FLOW
# =====================================================

graph = StateGraph(MessagesState)
graph.add_node("ollama", ollama_node)
graph.add_edge(START, "ollama")
graph.add_edge("ollama", END)
graph = graph.compile()

# =====================================================
# FASTAPI
# =====================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    result = graph.invoke({
        "messages": [
            {"role": "user", "content": query.question}
        ]
    })
    return {"answer": result["messages"][-1].content}
