import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader
import urllib.parse
from utils.graph_builder import build_keyword_graph, visualize_graph_pyvis



load_dotenv(dotenv_path="C:/Users/manas/OneDrive/Desktop/ReGenAI- AutoGen Research Assistant/.env")

# Move set_page_config() to be the first Streamlit command.
st.set_page_config(
    page_title="Autogen Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Updated Custom CSS: Set professional type text styling
custom_css = """
<style>
    body {
        background-color: #f5f5f5;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #000000; /* Black text */
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        color: #1a1a1a;
    }
    .stMarkdown, .css-1d391kg, .css-18e3th9 {
        color: #000000;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: #ffffff;
        border-radius: 5px;
        border: none;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
</style>
"""
st.markdown("""
<style>
    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(custom_css, unsafe_allow_html=True)

# Streamlit UI Title
st.title("📚 ReGenAI- MultiAgent Sytem for Intelligent Research")

num_results = 5
source_choice = st.sidebar.multiselect("Select Data Sources", options=["ArXiv", "Google Scholar"], default=["ArXiv"])
# Sidebar with features and footer
with st.sidebar:
    st.divider()
    st.markdown("<h3 style='color: #000000;'>Key Features</h3>", unsafe_allow_html=True)
    st.markdown("""
    <ul style='list-style: none; padding: 0; color: #000000; text-align: left;'>
        <li style='margin-bottom: 8px;'>🔍 <strong>Multi-Source Research Retrieval</strong></li>
        <li style='margin-bottom: 8px;'>🤖 <strong>Integrated Chatbot Interaction</strong></li>
        <li style='margin-bottom: 8px;'>✨ <strong>Advanced Summarization</strong></li>
        <li style='margin-bottom: 8px;'>🔄 <strong>Automatic Query Expansion & Refinement</strong></li>
    </ul>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='text-align: center; color:#000000;'><em>Built with Groq | Autogen</em></p>", unsafe_allow_html=True)

# Retrieve the API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Check if API key is set, else stop execution
if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize AI Agents for summarization and analysis
agents = ResearchAgents(groq_api_key)

# Initialize DataLoader for fetching research papers
data_loader = DataLoader(search_agent=agents.summarizer_agent)
col1, col2 = st.columns([2.5, 1.5])  # 3:2 ratio for main + comparison

# Use chat_input instead of text_input for entering the research topic.
query = st.chat_input("Enter a research topic:")
if query:
    st.session_state["active_query"] = query
elif "active_query" in st.session_state:
    query = st.session_state["active_query"]

# Trigger the search automatically if a query is provided.
if query:
    with st.spinner("Fetching research papers..."):  # Show a loading spinner
        
        all_papers = []
        # Fetch from selected sources based on sidebar choices
        if "ArXiv" in source_choice:
            arxiv_papers = data_loader.fetch_arxiv_papers(query, limit=num_results)
            all_papers.extend(arxiv_papers)
        if "Google Scholar" in source_choice:
            google_scholar_papers = data_loader.fetch_google_scholar_papers(query)
            all_papers.extend(google_scholar_papers)

        # If no papers are found, display an error message
        if not all_papers:
            st.error("Failed to fetch papers. Try again!")
        else:
            processed_papers = []

            # Process each paper: generate summary and analyze advantages/disadvantages
            for paper in all_papers:
                summary = agents.summarize_paper(paper['summary'])  # Generate summary
                adv_dis = agents.analyze_advantages_disadvantages(summary)  # Analyze pros/cons
                visualization_suggestion = agents.generate_visualization(summary)
                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "summary": summary,
                    "advantages_disadvantages": adv_dis,
                    "visualization": visualization_suggestion,
                })
            # ✅ Store all papers for comparison section
            st.session_state["all_papers"] = processed_papers

            with col1:
                # Display the processed research papers
                st.subheader("Top Research Papers:")
                for i, paper in enumerate(processed_papers, 1):
                    st.markdown(f"### {i}. {paper['title']}")  # Paper title
                    st.markdown(f"🔗 [Read Paper]({paper['link']})")  # Paper link
                    st.write(f"**Summary:** {paper['summary']}")  # Paper summary
                    st.write(f"{paper['advantages_disadvantages']}")  # Pros/cons analysis
                    with st.expander("📊 Suggested Visualization"):
                        st.markdown(paper["visualization"])

                        # Optional: Try executing matplotlib/seaborn code if included
                        if "import matplotlib" in paper["visualization"] or "plt." in paper["visualization"]:
                            try:
                                exec_globals = {}
                                exec(paper["visualization"], exec_globals)
                                st.pyplot(exec_globals.get('plt', None))
                            except Exception as e:
                                st.warning("⚠️ Couldn't render chart: " + str(e))
                    st.markdown("---")  # Separator between papers
                    # Create a "Chat about this paper" button
                    if st.button(f"💬 Chat about this paper", key=f"chat_button_{i}"):
                        query_params = {
                            "title": paper["title"],
                            "summary": paper["summary"],
                            "adv": paper["advantages_disadvantages"]
                        }
                        encoded = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
                        chat_url = f"/Paper%20Q%26A?{encoded}"
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={chat_url}" />', unsafe_allow_html=True)
                if st.button("🧠 Show Topic Network Graph"):
                    G = build_keyword_graph(processed_papers)
                    visualize_graph_pyvis(G)
                with st.expander("📚 Get Citation Suggestions for Your Thesis"):
                    thesis_topic = st.text_input("Enter your thesis topic:")
                    if st.button("📌 Suggest Citations"):
                        if not thesis_topic.strip():
                            st.warning("Please enter a thesis topic.")
                        else:
                            st.info("Analyzing papers for citation suitability...")
                            citation_suggestions = agents.recommend_citations(thesis_topic, processed_papers)
                            st.markdown("### 📝 Citation Suggestions")
                            st.write(citation_suggestions)
                if st.session_state.get("trigger_redirect"):
                    st.session_state.trigger_redirect = False
                    st.markdown('<meta http-equiv="refresh" content="0; url=/chat_page">', unsafe_allow_html=True)
                with col2:
                    st.header("⚖️ Compare Papers")
                    if "all_papers" in st.session_state:
                        paper_titles = [p["title"] for p in st.session_state["all_papers"]]
                        selected = st.multiselect("Select 2–3 papers", paper_titles)

                        if len(selected) >= 2:
                            to_compare = [p for p in st.session_state["all_papers"] if p["title"] in selected]
                            if st.button("🔍 Compare Now"):
                                comparison_result = agents.compare_papers(to_compare)
                                st.markdown("### 📊 Comparison Result")
                                st.markdown(comparison_result)
                    else:
                        st.info("Search for papers to enable comparison.")
                    st.subheader("🤼‍♂️ Paper Debate Agent")
                    selected_summary = st.text_area("📄 Paste a paper summary for debate:", height=300)
                    if st.button("🔥 Start Debate"):
                        if not selected_summary:
                            st.warning("Please paste a summary first.")
                        else:
                            with st.spinner("Debating like academic pros..."):
                                support_prompt = f"You are a research supporter. Argue in favor of the paper below. Highlight its innovation, methodology, and potential impact.\n\nPaper Summary:\n{selected_summary}"
                                critic_prompt = f"You are a research critic. Point out limitations, assumptions, or flaws in the paper below. Be rigorous but fair.\n\nPaper Summary:\n{selected_summary}"
                                balance_prompt = f"Based on the following debate, provide a balanced evaluation of the paper including strengths and weaknesses.\n\nSupporter: {{support}}\n\nCritic: {{critic}}"

                                supporter = agents.summarizer_agent.generate_reply(messages=[{"role": "user", "content": support_prompt}]).get("content", "")
                                critic = agents.advantages_disadvantages_agent.generate_reply(messages=[{"role": "user", "content": critic_prompt}]).get("content", "")
                                synthesis = agents.summarizer_agent.generate_reply(messages=[{"role": "user", "content": balance_prompt.format(support=supporter, critic=critic)}]).get("content", "")

                                st.markdown("### 🟢 Supporter Agent")
                                st.markdown(supporter)

                                st.markdown("### 🔴 Critic Agent")
                                st.markdown(critic)

                                st.markdown("### ⚖️ Balanced Evaluation")
                                st.markdown(synthesis)

            