# 1️⃣ edit distance
from torch import dist


def edit_distance(a, b):
    dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]

    for i in range(len(a)+1):
        dp[i][0] = i
    for j in range(len(b)+1):
        dp[0][j] = j

    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],
                    dp[i][j-1],
                    dp[i-1][j-1]
                )
    return dp[-1][-1]


# 2️⃣ closest word
def get_closest_word(word, vocabulary):
    best_word = None
    min_dist = float("inf")

    for v in vocabulary:
        # allow more candidates
        if abs(len(v) - len(word)) > 3:
            continue

        # softer first-letter check
        if word[0] != v[0] and word[:2] != v[:2]:
            continue

        dist = edit_distance(word, v)

        if dist < min_dist:
            min_dist = dist
            best_word = v

    return best_word


# 3️⃣ wrapper
def spell_check_word(word, embedding_engine):

    if not hasattr(embedding_engine, "model"):
        return word

    vec = embedding_engine.get_vector(word)

    if vec is not None:
        return word

    vocab = embedding_engine.model.key_to_index.keys()

    corrected = get_closest_word(word, vocab)

    if corrected:
        return corrected

    return word