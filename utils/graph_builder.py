import networkx as nx
from pyvis.network import Network
from rake_nltk import Rake
import tempfile
import streamlit as st

def extract_keywords(text, max_keywords=5):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()[:max_keywords]
    return keywords

def build_keyword_graph(papers, max_keywords_per_paper=5):
    G = nx.Graph()

    for paper in papers:
        text = paper["summary"]
        keywords = extract_keywords(text, max_keywords=max_keywords_per_paper)
        for kw in keywords:
            G.add_node(kw)
        for i in range(len(keywords)):
            for j in range(i + 1, len(keywords)):
                G.add_edge(keywords[i], keywords[j])

    return G

def visualize_graph_pyvis(G, heading="🧠 Topic Network Graph"):
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    net.from_nx(G)

    # Save as HTML and display in Streamlit
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        st.markdown(f"### {heading}")
        st.components.v1.html(open(tmp_file.name, 'r', encoding='utf-8').read(), height=550)
