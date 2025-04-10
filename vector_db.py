# Updated imports for LangChain 0.2.2+
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import pickle
import os
from config import Config

class VectorDB:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL
        )
        self.db = None
        self.db_path = "data/news_articles.db"
        
    def create_db(self, documents):
        self.db = FAISS.from_texts(documents, self.embedding_model)
        self._save_db()
        
    def _save_db(self):
        with open(self.db_path, "wb") as f:
            pickle.dump(self.db, f)
            
    def load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "rb") as f:
                self.db = pickle.load(f)
        return self.db
        
    def search(self, query, k=3):
        if not self.db:
            self.load_db()
        if self.db:
            docs = self.db.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        return []