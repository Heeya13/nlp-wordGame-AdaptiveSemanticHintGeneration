import random
from modules.hint_strategy import get_hint_level
from modules.domain_selector import DomainSelector
from modules.attribute_selector import get_attribute


class SentenceGenerator:

    def __init__(self):
        self.domain_selector = DomainSelector()

        # Template Mapping Layer
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
            "color": [
                "This word is usually {} in color."
            ],
            "definition": [
                "This word means {}.",
                "It refers to {}."
            ]
        }

        # Memory for adaptive hints
        self.previous_domains = set()

    def generate_hint(self, word_data, guess, similarity, embedding_engine):

        # 🔹 1. Hint Strategy
        hint_level = get_hint_level(similarity)

        # 🔹 2. Domain Selection (avoid repetition)
        if isinstance(word_data, str):
            selected_domain = None
        else:
            selected_domain = self.domain_selector.select_domain(
                word_data,
                guess,
                embedding_engine
            )


        # 🔹 3. Attribute Selection
        if isinstance(word_data, str):
            attribute_type = "definition"
            attribute_value = word_data
        else:
            attribute_type, attribute_value = get_attribute(
                word_data,
                hint_level,
                selected_domain
            )

        # 🔹 4. Template Mapping
        if attribute_type in self.templates:
            templates = self.templates[attribute_type]
        else:
            return f"This word is related to {attribute_value}.", hint_level

        # 🔹 5. Adaptive Hint Strength
        if hint_level == "LOW":
            template = templates[0]
        elif hint_level == "MEDIUM":
            template = templates[min(1, len(templates)-1)]
        else:  # HIGH
            template = templates[-1]

        sentence = template.format(attribute_value)

        return sentence, hint_level