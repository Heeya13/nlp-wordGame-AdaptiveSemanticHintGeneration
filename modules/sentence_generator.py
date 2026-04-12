from modules.hint_strategy import get_hint_level
from modules.domain_selector import DomainSelector
from modules.attribute_selector import get_attribute
from modules.memory_module import MemoryModule
import random

class SentenceGenerator:

    def __init__(self):
        self.domain_selector = DomainSelector()
        self.memory = MemoryModule()

        self.templates = {
            "category": [
                "This word belongs to the category of {}.",
                "It is a type of {}.",
                "This is classified under {}."
            ],
            "context": [
                "This word is commonly associated with {}.",
                "You would often find this in {}.",
                "It is related to {}."
            ],
            "function": [
                "This word is used to {}.",
                "Its main purpose is to {}.",
                "It helps to {}."
            ],
            "domain": [
                "This word is related to {}.",
                "It is commonly used in {}."
            ],
            "definition": [
                "This word means {}.",
                "It refers to {}."
            ]
        }

    def generate_hint(self, word_data, guess, similarity, embedding_engine):

        # 🔹 get level from max similarity
        hint_level = get_hint_level(self.memory.max_similarity)

        # 🔹 domain selection
        if isinstance(word_data, str):
            selected_domain = None
        else:
            selected_domain = self.domain_selector.select_domain(
                word_data,
                guess,
                embedding_engine
            )

        # 🔹 try levels (no downgrade)
        levels = ["LOW", "MEDIUM", "HIGH"]
        start_index = levels.index(hint_level)

        for lvl in levels[start_index:]:

            # get attribute
            attr_type, attr_value = get_attribute(
                word_data,
                lvl,
                selected_domain,
                used_values={v for (_, v) in self.memory.used_hints}
            )

            if attr_type is None or attr_value is None:
                continue

            # check repetition
            if self.memory.is_used(attr_type, attr_value):
                continue

            # store in memory
            self.memory.add_hint(attr_type, attr_value)

            # template
            templates = self.templates.get(attr_type, ["This word is related to {}."])

            if lvl == "LOW":
                template = random.choice(templates[:2])
            elif lvl == "MEDIUM":
                template = random.choice(templates)
            else:
                template = random.choice(templates[-2:])

            return template.format(attr_value), lvl

        # 🔴 nothing left
        return "No more hints available.", hint_level