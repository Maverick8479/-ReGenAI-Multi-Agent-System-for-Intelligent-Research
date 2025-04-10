#🧠 ReGenAI: MultiAgent System for Intelligent Research

A cutting-edge Virtual Research Companion built with Streamlit + Groq + Autogen, designed to simulate real research workflows using AI agents.
ReGenAI is more than just a summarizer — it's your personal PhD advisor, startup incubator, grant writer, and academic strategist all rolled into one.

## Features

🔍 Multi-Source Paper Retrieval	Fetches papers from ArXiv and Google Scholar based on your query
🤖 Agent-based Summarization	Summarizes each paper and outlines advantages and disadvantages
💬 Interactive Q&A	Chat with papers in a dedicated thread
🧠 ReGenAI Lab Mode	Multi-agent brainstorm session: innovator, professor, and fund manager simulate idea refinement
📈 Paper Visualization Agent	Suggests data visualizations (even runs matplotlib code)
📊 Topic Graph Visualizer	Builds knowledge graph of keywords using PyVis/NetworkX
⚖️ Paper Comparison Agent	Side-by-side comparison of 2–3 papers by methodology, accuracy, pros/cons
🤼 Debate Agent	Simulated academic debate between supporter and critic agents
💡 Startup Fusion Agent	Converts papers into bold startup ideas with MVP plan and investor pitch
🧪 Auto Experiment Generator	Suggests experiments from a paper: datasets, architecture, pseudocode
📚 Research Mentor Mode	Suggests reading order, foundational papers, and learning path
🎭 Historical Advisor Roleplay	Get feedback in the tone of Alan Turing, Fei-Fei Li, and others

## Setup

1. Install [Python](https://www.python.org/downloads/).
2. Clone the repository to your local machine.
3. Navigate to the project directory:
    ```
    cd ReGenAI
    ```
4. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Running the App

Start the Streamlit app by running:
```
streamlit run app.py
```

## Configuration

- The app uses environment variables. Create a `.env` file in the project root and add:
    ```
    GROQ_API_KEY=your-api-key-here
    ```

## File Structure

app.py                  # Main dashboard for summarization, comparison, and debate
chat_page.py            # Individual paper Q&A interface
agents.py               # Multi-agent Autogen setup (summarizer, critic, innovator, etc.)
data_loader.py          # Handles ArXiv / Google Scholar fetching
/pages/
    ReGenAI Lab Mode.py             # Brainstorm session for your topic
    Auto Experiment Generator.py    # Generate experiment plan from summary
    Startup Fusion.py               # Turn papers into startup MVPs
    Debate Agent.py (optional)      # Also embedded in app.py
graph_builder.py         # Keyword extraction and topic graph builder

## Built With

-Streamlit
-Autogen
-Groq API
-scholarly for Google Scholar access
-Python Libraries: requests, dotenv, xml.etree.ElementTree, networkx, pyvis, etc.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Thanks to the contributors of the libraries used.
- Built with **Groq** | **Autogen**
