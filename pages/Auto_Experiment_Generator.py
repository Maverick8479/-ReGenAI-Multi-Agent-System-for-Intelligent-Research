import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents

# Load API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="🧪 Auto Experiment Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧪 Auto Experiment Generator")
st.markdown("""
Select a research paper summary and I’ll generate a Python experiment setup with:
- 📜 Pseudocode
- 🔗 Dataset links
- 🏗️ Model architecture
- 📏 Evaluation metrics
""")

# Initialize agent
if not groq_api_key:
    st.error("GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()

agents = ResearchAgents(groq_api_key)

# Allow user to input or paste a paper summary
summary = st.text_area("📄 Paste the summary of the paper:", height=300)

if st.button("🚀 Generate Experiment Setup"):
    if not summary:
        st.warning("Please paste a paper summary first.")
    else:
        with st.spinner("Thinking like a scientist... 🧠"):
            prompt = f"""
Based on the following research summary, generate a complete experiment plan in Python. Include:
1. Pseudocode of the methodology
2. Dataset links
3. Suggested model architecture
4. Evaluation metrics to use

Summary:
{summary}
"""

            response = agents.summarizer_agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.get("content", "No experiment generated.")
            st.subheader("🧪 Experiment Plan")
            st.markdown(result)
