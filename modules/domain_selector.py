from modules.similarity_engine import cosine_similarity


class DomainSelector:

    def __init__(self):
        self.selected_domain = None

    def select_domain(self, word_data, guess, embedding_engine):

        # If domain already selected → reuse it
        if self.selected_domain is not None:
            return self.selected_domain

        # find possible domain keys
        domain_keys = [key for key in word_data.keys() if key.endswith("_domain")]

        # if word has no multiple domains
        if len(domain_keys) == 0:
            return None

        guess_vec = embedding_engine.get_vector(guess)

        best_domain = None
        best_score = -1

        for domain_key in domain_keys:

            domain_name = domain_key.replace("_domain", "")
            domain_vec = embedding_engine.get_vector(domain_name)

            if guess_vec is None or domain_vec is None:
                continue

            score = cosine_similarity(guess_vec, domain_vec)

            if score > best_score:
                best_score = score
                best_domain = domain_key

        self.selected_domain = best_domain

        return best_domain