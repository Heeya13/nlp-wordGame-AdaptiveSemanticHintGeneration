from gensim.models import KeyedVectors

class FastTextEmbeddingEngine:
    def __init__(self, model_path):
        print("Loading FastText embeddings...")
        self.model = KeyedVectors.load_word2vec_format(
            model_path,
            binary=False
        )
        print("FastText embeddings ready.")

    def get_vector(self, word):
        try:
            return self.model[word]
        except KeyError:
            return None
