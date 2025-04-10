import os
from autogen import AssistantAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchAgents:
    def __init__(self, api_key):
        self.groq_api_key = api_key
        self.llm_config = {'config_list': [{'model': 'llama-3.3-70b-versatile', 'api_key': self.groq_api_key, 'api_type': "groq"}]}

        # Summarizer Agent - Summarizes research papers
        self.summarizer_agent = AssistantAgent(
            name="summarizer_agent",
            system_message="Summarize the retrieved research papers and present concise summaries to the user, JUST GIVE THE RELEVANT SUMMARIES OF THE RESEARCH PAPER AND NOT YOUR THOUGHT PROCESS.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Advantages and Disadvantages Agent - Analyzes pros and cons
        self.advantages_disadvantages_agent = AssistantAgent(
            name="advantages_disadvantages_agent",
            system_message="Analyze the summaries of the research papers and provide a list of advantages and disadvantages for each paper in a pointwise format. JUST GIVE THE ADVANTAGES AND DISADVANTAGES, NOT YOUR THOUGHT PROCESS",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        self.visualization_agent = AssistantAgent(
            name="visualization_agent",
            system_message="Based on this research paper's content, describe a visualization (like a chart, graph, or keyword map) that would help users understand the key ideas. Output a Python matplotlib/seaborn code snippet or a clear description of the visualization. Avoid assumptions and hallucinations.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False  # We'll execute the code in Streamlit
        )
        
    def summarize_paper(self, paper_summary):
        """Generates a summary of the research paper."""
        summary_response = self.summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": f"Summarize this paper: {paper_summary}"}]
        )
        return summary_response.get("content", "Summarization failed!") if isinstance(summary_response, dict) else str(summary_response)

    def analyze_advantages_disadvantages(self, summary):
        """Generates advantages and disadvantages of the research paper."""
        adv_dis_response = self.advantages_disadvantages_agent.generate_reply(
            messages=[{"role": "user", "content": f"Provide advantages and disadvantages for this paper: {summary}"}]
        )
        return adv_dis_response.get("content", "Advantages and disadvantages analysis failed!")
    
    def generate_visualization(self, paper_summary):
        """Ask the agent to propose a visualization based on the summary."""
        vis_response = self.visualization_agent.generate_reply(
            messages=[{"role": "user", "content": f"What kind of visualization can represent this paper: {paper_summary}"}]
        )
        return vis_response.get("content", "No visualization suggestion found.")
    
    def ask_question(self, paper_summary, question):
        """
        Uses the summarizer_agent to answer questions based on the paper summary.
        """
        response = self.summarizer_agent.generate_reply(
            messages=[
                {"role": "user", "content": f"Based on this paper:\n\n{paper_summary}\n\nAnswer this question:\n{question}"}
            ]
        )
        return response.get("content", "No answer generated.")
    # Add this inside ResearchAgents class
    def recommend_citations(self, thesis_topic, papers):
        summaries = "\n\n".join([f"Title: {p['title']}\nSummary: {p['summary']}" for p in papers])
        prompt = (
            f"I'm writing a thesis on: '{thesis_topic}'.\n"
            f"Here are some research papers:\n\n{summaries}\n\n"
            "Please recommend which papers are best suited as citations for this thesis topic, "
            "based on their relevance, clarity of methodology, and impact. "
            "For each recommended paper, explain in 2-3 lines why it's useful to cite."
        )

        response = self.summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": prompt}]
        )
        return response.get("content", "Citation recommendation failed.")
    def compare_papers(self, selected_papers):
        summaries = "\n\n".join([
            f"Title: {p['title']}\nSummary: {p['summary']}\nAdvantages and Disadvantages: {p['advantages_disadvantages']}"
            for p in selected_papers
        ])
        prompt = (
            f"Compare the following papers side-by-side.\n\n{summaries}\n\n"
            "Return a markdown-formatted table comparing:\n"
            "- Methodology\n- Dataset Used\n- Accuracy (if any)\n- Pros & Cons\n"
            "Then provide a short paragraph summarizing which paper is better and why."
        )

        response = self.advantages_disadvantages_agent.generate_reply(
            messages=[{"role": "user", "content": prompt}]
        )
        return response.get("content", "Comparison failed.")
