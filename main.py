import random
import json
import subprocess

from modules.embedding_engine import EmbeddingEngine
from modules.similarity_engine import cosine_similarity
from modules.hint_strategy import get_hint_level
from modules.domain_selector import DomainSelector
from modules.attribute_selector import get_attribute


def load_word_list(filepath):

    with open(filepath, "r") as file:
        words = [line.strip() for line in file]

    return words


def choose_target_word(word_list):

    return random.choice(word_list)


def main():

    words = load_word_list("Datasets/word_list.txt")

    target_word = choose_target_word(words)

    print("Target word (debug):", target_word)

    embedding_engine = EmbeddingEngine("Model/glove.6B.50d.txt")
    domain_selector = DomainSelector()

    with open("Datasets/word_attributes.json", "r") as f:
        word_attributes = json.load(f)

    word_data = word_attributes[target_word]

    while True:

        raw_guess = input("\nEnter guess: ").strip()

        # call C program
        process = subprocess.run(
            ["modules/preprocess.exe"],
            input=raw_guess,
            text=True,
            capture_output=True
        )

        output = process.stdout.strip()

        # check result
        if output == "INVALID":
            print("Invalid input. Try again.")
            continue

        # extract processed word
        if output.startswith("VALID:"):
            guess = output.split(":")[1]
        else:
            print("Unexpected error.")
            continue

        print("Processed guess:", guess)

        # get vectors
        guess_vec = embedding_engine.get_vector(guess)
        target_vec = embedding_engine.get_vector(target_word)

        similarity = cosine_similarity(guess_vec, target_vec)

        if similarity is None:
            print("Word not in vocabulary.")
            continue

        hint_level = get_hint_level(similarity)

        print("Similarity:", round(similarity, 3))
        print("Hint level:", hint_level)

        # DOMAIN SELECTION (only happens once internally)
        selected_domain = domain_selector.select_domain(
            word_data,
            guess,
            embedding_engine
        )

        attribute_type, attribute_value = get_attribute(
        word_data,
        hint_level,
        selected_domain
        )

        print("Selected domain:", selected_domain)
        print("Selected attribute:", attribute_type)
        print("Attribute value:", attribute_value)


        if guess == target_word:
            print("Correct! You found the word.")
            break


if __name__ == "__main__":
    main()