from sentence_transformers import SentenceTransformer


class BERTEmbeddingEngine:
    def __init__(self):
        print("Loading BERT model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_vector(self, text):
        try:
            return self.model.encode(text)
        except Exception:
            return None