import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents

# Page config
st.set_page_config(
    page_title="🚀 Research x Startup Fusion",
    layout="wide"
)

# Load API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your .env file.")
    st.stop()

# Initialize agents
agents = ResearchAgents(groq_api_key)

st.title("🚀 ReGenAI Fusion Agent")
st.subheader("From Research to Startup 🚀")

st.markdown("""
Give me a paper summary or a topic, and I'll turn it into a startup idea with MVP plan, investor pitch, and more.

**Examples**:
- "Using GANs to detect diabetic retinopathy"
- "Transformer models in legal document analysis"
- "A paper summary from ArXiv on protein folding"
""")

user_input = st.text_area("Enter your research topic or paper summary:", height=200)

if st.button("💡 Generate Startup Idea"):
    if not user_input:
        st.warning("Please enter a research topic or summary.")
        st.stop()

    with st.spinner("Synthesizing commercial potential..."):
        startup_idea_prompt = f"""
        Based on this research summary or topic:

        "{user_input}"

        Generate the following:
        1. Real-World Problem it solves
        2. Bold Startup Idea (short description)
        3. MVP Plan (Tech Stack, Tools, Dataset)
        4. One-line Pitch for investors
        5. Ideal VCs or funding sources
        6. Competitive Advantage
        7. Risk and how to mitigate it
        Format it in a clean markdown table or bullet points.
        """

        fusion_response = agents.summarizer_agent.generate_reply([
            {"role": "user", "content": startup_idea_prompt}
        ])

        if isinstance(fusion_response, dict):
            st.markdown(fusion_response.get("content", "⚠️ Failed to generate response."))
        else:
            st.markdown(fusion_response)

# Optional download as pitch deck
    with st.expander("📥 Export as Pitch Document"):
        export_text = fusion_response.get("content", "") if isinstance(fusion_response, dict) else fusion_response
        st.download_button(
            label="📄 Download as .txt",
            data=export_text,
            file_name="Startup_Pitch.txt",
            mime="text/plain"
        )
