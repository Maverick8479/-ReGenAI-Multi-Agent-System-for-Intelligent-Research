import streamlit as st

# ✅ Must be the first Streamlit command after imports
st.set_page_config(
    page_title="Paper Q&A",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Other imports AFTER set_page_config
import os
from dotenv import load_dotenv
from agents import ResearchAgents

# Load API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY is missing.")
    st.stop()

# Initialize agent
agents = ResearchAgents(groq_api_key)

# Get data passed from main app
paper = st.session_state.get("selected_paper", None)

params = st.experimental_get_query_params()
title = params.get("title", [""])[0]
summary = params.get("summary", [""])[0]
advantages_disadvantages = params.get("adv", [""])[0]


# UI Layout
st.title("🧠 Paper Q&A Chat")
st.subheader(title)

with st.expander("📄 Summary"):
    st.write(summary)

with st.expander("📋 Advantages & Disadvantages"):
    st.write(advantages_disadvantages)

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_question = st.chat_input("Ask a question about this paper")
if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    response = agents.ask_question(summary, user_question)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
