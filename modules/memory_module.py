class MemoryModule:

    def __init__(self):
        self.used_hints = set()  # (type, value)
        self.max_similarity = 0

    def update_similarity(self, similarity):
        self.max_similarity = max(self.max_similarity, similarity)

    def is_used(self, attr_type, attr_value):
        return (attr_type, attr_value) in self.used_hints

    def add_hint(self, attr_type, attr_value):
        self.used_hints.add((attr_type, attr_value))

    def get_max_similarity(self):
        return self.max_similarity