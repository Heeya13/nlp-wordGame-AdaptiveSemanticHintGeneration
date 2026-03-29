def get_hint_level(similarity):

    if similarity < 0.30:
        return "LOW"

    elif similarity < 0.90:
        return "MEDIUM"

    else:
        return "HIGH"