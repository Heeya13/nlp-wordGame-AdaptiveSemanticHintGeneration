import random


def get_attribute(word_data, hint_level, selected_domain=None, used_values=None):

    if used_values is None:
        used_values = set()

    # domain handling
    if selected_domain is not None:
        domain_name = selected_domain.replace("_domain", "")
        word_data = word_data[selected_domain]
    else:
        domain_name = None

    # LOW
    if hint_level == "LOW":
        if selected_domain is not None:
            return "domain", domain_name
        else:
            return "category", word_data.get("category")

    # MEDIUM (context)
    elif hint_level == "MEDIUM":
        context_list = word_data.get("context", [])

        # remove used ones
        available = [c for c in context_list if c not in used_values]

        if not available:
            return None, None

        return "context", random.choice(available)

    # HIGH
    elif hint_level == "HIGH":
        return "function", word_data.get("function")

    return None, None