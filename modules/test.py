from embedding_engine import EmbeddingEngine

engine = EmbeddingEngine("../model/glove.6B.50d.txt")

vector = engine.get_vector("apple")

print(vector[:10])