from gensim.models import KeyedVectors


class EmbeddingEngine:

    def __init__(self, model_path):

        print("Loading embeddings...")
        self.model = KeyedVectors.load_word2vec_format(
            model_path,
            binary=False,
            no_header=True
        )
        print("Embeddings ready.")

    def get_vector(self, word):

        try:
            return self.model[word]
        except KeyError:
            return None