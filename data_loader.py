import requests
import xml.etree.ElementTree as ET
from scholarly import scholarly

class DataLoader:
    def __init__(self, search_agent=None):
        self.search_agent = search_agent
        print("DataLoader Init")
    def fetch_arxiv_papers(self, query, limit=None):  # Updated signature
        """
            Fetches top 5 research papers from ArXiv based on the user query.
            If <5 papers are found, expands the search using related topics.
            
            Returns:
                list: A list of dictionaries containing paper details (title, summary, link).
        """
        
        def search_arxiv(query):
            """Helper function to query ArXiv API."""
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
            response = requests.get(url)
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                return [
                    {
                        "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                        "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                        "link": entry.find("{http://www.w3.org/2005/Atom}id").text
                    }
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")
                ]
            return []

        papers = search_arxiv(query)

        if len(papers) < 5 and self.search_agent:  # If fewer than 5 papers, expand search
            related_topics_response = self.search_agent.generate_reply(
                messages=[{"role": "user", "content": f"Suggest 3 related research topics for '{query}'"}]
            )
            related_topics = related_topics_response.get("content", "").split("\n")

            for topic in related_topics:
                topic = topic.strip()
                if topic and len(papers) < 5:
                    new_papers = search_arxiv(topic)
                    papers.extend(new_papers)
                    papers = papers[:5]  # Ensure max 5 papers

        if limit is not None:
            papers = papers[:limit]
            
        return papers

    def fetch_google_scholar_papers(self, query):
        """
            Fetches top 5 research papers from Google Scholar.
            Returns:
                list: A list of dictionaries containing paper details (title, summary, link)
        """
        papers = []
        search_results = scholarly.search_pubs(query)

        for i, paper in enumerate(search_results):
            if i >= 5:
                break
            papers.append({
                "title": paper["bib"]["title"],
                "summary": paper["bib"].get("abstract", "No summary available"),
                "link": paper.get("pub_url", "No link available")
            })
        return papers
