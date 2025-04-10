import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="🎓 Research Mentor Mode",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧑‍🎓 Research Mentor Mode")
st.markdown("""
Ask me what you're working on and I will guide you with a suggested reading plan. 📚
""")

# Query input
query = st.text_input("🧠 What are you researching?")

# Initialize agents
if not groq_api_key:
    st.error("GROQ_API_KEY not found. Check your .env file.")
    st.stop()

agents = ResearchAgents(groq_api_key)
data_loader = DataLoader(search_agent=agents.summarizer_agent)

# Run mentor plan generation
if query:
    with st.spinner("🧭 Finding the right papers for you..."):
        papers = data_loader.fetch_arxiv_papers(query, limit=5)

        if not papers:
            st.error("No papers found. Try a different topic.")
        else:
            st.success("✅ Reading Plan Ready!")

            # Generate summaries to determine survey/intro papers
            summaries = [agents.summarize_paper(paper["summary"]) for paper in papers]

            # Let LLM suggest an order and reasoning
            input_message = """
Based on these summaries, suggest a reading plan. Start with the most general or survey papers, then move to advanced or specific ones. Provide reasoning for each step:

"""
            for i, summary in enumerate(summaries):
                input_message += f"Paper {i+1}: {summary}\n"

            mentor_plan = agents.summarizer_agent.generate_reply(
                messages=[{"role": "user", "content": input_message}]
            )

            # Display mentor output
            st.subheader("📘 Suggested Reading Plan")
            st.markdown(mentor_plan.get("content", "No plan generated."))

            # Show original papers and summaries
            st.divider()
            for i, paper in enumerate(papers):
                st.markdown(f"### {i+1}. {paper['title']}")
                st.markdown(f"🔗 [Read Paper]({paper['link']})")
                with st.expander("📄 Summary"):
                    st.write(summaries[i])
                st.markdown("---")