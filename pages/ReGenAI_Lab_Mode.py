import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="🧠✨ ReGenAI Lab Mode",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠✨ ReGenAI Lab Mode")
st.markdown("""
"Turn your research queries into ideas, teams, timelines, and even fundable projects."
""")

if not groq_api_key:
    st.error("GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()

agents = ResearchAgents(groq_api_key)

# --- User Input ---
topic = st.text_input("🎯 What research idea are you exploring?")
advisor = st.selectbox("🎭 Pick a Research Advisor for Roleplay:", ["Alan Turing", "Fei-Fei Li", "Yann LeCun", "Geoffrey Hinton", "No Advisor"])

# --- Multi-Agent Brainstorm ---
if st.button("🤖 Generate Full Lab Analysis") and topic:
    with st.spinner("Generating your research lab output..."):
        # Innovator Agent
        innovator_prompt = f"You are an innovative researcher. Suggest bold, unique applications for the research topic: '{topic}'"
        innovator_response = agents.summarizer_agent.generate_reply(messages=[{"role": "user", "content": innovator_prompt}])

        # Professor Agent
        professor_prompt = f"As a research professor, outline key constraints, assumptions, and ethical concerns with the topic: '{topic}'"
        professor_response = agents.advantages_disadvantages_agent.generate_reply(messages=[{"role": "user", "content": professor_prompt}])

        # Fund Manager Agent
        fund_prompt = f"You're a research fund evaluator. Evaluate the feasibility and funding potential of a project based on the topic: '{topic}'"
        fund_response = agents.advantages_disadvantages_agent.generate_reply(messages=[{"role": "user", "content": fund_prompt}])

        # Grant Pitch
        pitch_prompt = f"Write a 1-page research grant pitch for: '{topic}' including Problem, Novelty, ROI, and Proposed Plan."
        pitch_response = agents.summarizer_agent.generate_reply(messages=[{"role": "user", "content": pitch_prompt}])

        # Research Chain Planner
        chain_prompt = f"For the topic '{topic}', create a research roadmap: list key papers, suggest experiments, a paper outline, and a 3-month timeline."
        chain_response = agents.summarizer_agent.generate_reply(messages=[{"role": "user", "content": chain_prompt}])

        # Advisor Roleplay
        if advisor != "No Advisor":
            roleplay_prompt = f"Respond like {advisor} advising a student on the topic: '{topic}'. Include insights in their voice."
            advisor_response = agents.summarizer_agent.generate_reply(messages=[{"role": "user", "content": roleplay_prompt}])
        else:
            advisor_response = {"content": "No advisor selected."}

        # Display results
        st.subheader("👩‍🔬 Innovator Agent Suggestions")
        st.markdown(innovator_response.get("content", "-"))

        st.subheader("🧑‍🏫 Professor Constraints & Ethics")
        st.markdown(professor_response.get("content", "-"))

        st.subheader("💼 Fund Manager Feasibility")
        st.markdown(fund_response.get("content", "-"))

        st.subheader("📄 1-Page Grant Pitch")
        st.markdown(pitch_response.get("content", "-"))

        st.subheader("🧩 Research Chain Planner")
        st.markdown(chain_response.get("content", "-"))

        st.subheader(f"🎭 Advisor: {advisor}")
        st.markdown(advisor_response.get("content", "-"))
