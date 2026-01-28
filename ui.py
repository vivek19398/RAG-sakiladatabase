import streamlit as st
import pandas as pd
from app import graph

st.set_page_config(page_title="Sakila Database Chat", layout="wide")
st.title("🎬 Sakila Database Chat (Local LLM)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_input = st.chat_input("Ask a question about the Sakila database...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    result = graph.invoke({
        "messages": st.session_state.messages
    })

    assistant_content = result["messages"][-1].content
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_content}
    )

# Render chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        content = msg["content"]

        # ✅ TABLE OUTPUT
        if isinstance(content, list) and content and isinstance(content[0], dict):
            df = pd.DataFrame(content)
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True)
        else:
            st.write(content)
