# Autogen Research Assistant

A **Virtual Research Assistant** built with Streamlit that retrieves research papers from multiple sources (ArXiv and Google Scholar), summarizes them using an AI-powered agent, and presents concise summaries along with advantages and disadvantages.

## Features

- 🔍 **Multi-Source Research Retrieval**: Fetches papers from ArXiv and Google Scholar.
- 🤖 **Integrated Chatbot Interaction**: Enter your research topic via chat input.
- ✨ **Advanced Summarization**: AI-driven summarization for quick insights.
- 🔄 **Automatic Query Expansion**: Enhances search results by suggesting related topics.
- 📊 **Visual Data Presentation**: Easy-to-read interface with professional styling.

## Setup

1. Install [Python](https://www.python.org/downloads/).
2. Clone the repository to your local machine.
3. Navigate to the project directory:
    ```
    cd F:/Autogen-Research-Agent
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

- `app.py` – Main Streamlit app file.
- `agents.py` – Contains the AI agent logic for summarization and analysis.
- `data_loader.py` – Handles fetching research papers from ArXiv and Google Scholar.
- `README.md` – This file.

## Built With

- [Streamlit](https://streamlit.io/)
- [Scholarly](https://github.com/scholarly-python-package/scholarly)
- [Groq](https://groq.com/) API integration
- Python libraries: `requests`, `xml.etree.ElementTree`, etc.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Thanks to the contributors of the libraries used.
- Built with **Groq** | **Autogen**