import numpy as np

def cosine_similarity(vec1, vec2):

    if vec1 is None or vec2 is None:
        return None

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    similarity = dot_product / (norm1 * norm2)

    return similarity