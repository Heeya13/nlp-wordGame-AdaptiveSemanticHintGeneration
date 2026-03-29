import random


def get_attribute(word_data, hint_level, selected_domain=None):

    # If the word has multiple domains, switch to the selected one
    if selected_domain is not None:
        domain_name = selected_domain.replace("_domain", "")
        word_data = word_data[selected_domain]
    else:
        domain_name = None

    # LOW hint
    if hint_level == "LOW":

        if selected_domain is not None:
            attribute_type = "domain"
            attribute_value = domain_name
        else:
            attribute_type = "category"
            attribute_value = word_data.get("category")

    # MEDIUM hint
    elif hint_level == "MEDIUM":

        attribute_type = "context"

        context_list = word_data.get("context", [])

        if len(context_list) > 0:
            attribute_value = random.choice(context_list)
        else:
            attribute_value = None

    # HIGH hint
    elif hint_level == "HIGH":

        attribute_type = "function"
        attribute_value = word_data.get("function")


    else:
        return None, None

    return attribute_type, attribute_value