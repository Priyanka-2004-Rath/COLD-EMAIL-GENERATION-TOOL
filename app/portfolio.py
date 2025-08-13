# portfolio.py
import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="app/resources/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Use in-memory Chroma client for Streamlit Cloud
        self.chroma_client = chromadb.Client(chromadb.Settings(
            persist_directory=None,  # disables file persistence
            anonymized_telemetry=False
        ))

        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
