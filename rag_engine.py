import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-miniLM-L6-v2")
        self.texts = []
        self.index = None
        
    def load_data(self, folder="data"):
        dataset = []
        for i in os.listdir(folder):
            with open(os.path.join(folder, i), "r", encoding="utf-8") as f:
                dataset.extend(json.load(f))
        return dataset
    
    def prepare_corpus(self):
        raw_data = self.load_data()
        corpus = []
        for item in raw_data:
            corpus.append(json.dumps(item))
        return corpus 
    
    def build_index(self):
        self.texts = self.prepare_corpus()
        embeddings = self.model.encode(self.texts)
        dim = embeddings.shape[1]  
        
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))
        
    def retrieve(self, query, k=3):
        q_emb = self.model.encode([query])
        distances, indices = self.index.search(q_emb, k)
        return [self.texts[i] for i in indices[0]]