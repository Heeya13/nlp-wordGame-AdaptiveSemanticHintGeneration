import random
import json
import subprocess

from modules.similarity_engine import cosine_similarity
from modules.sentence_generator import SentenceGenerator
from modules.percentage_module import similarity_to_percentage
from modules.spell_check import spell_check_word

sentence_generator = SentenceGenerator()

def load_word_list(filepath):
    with open(filepath, "r") as file:
        words = [line.strip() for line in file]
    return words


def choose_target_word(word_list):
    return random.choice(word_list)


def main():

    #  SELECT MODEL
    print("Select embedding method:")
    print("1. GloVe")
    print("2. BERT")
    print("3. FastText")

    choice = input("Enter choice (1, 2 or 3): ").strip()

    #  LOAD CORRESPONDING ENGINE
    if choice == "1":
        from modules.embedding_engine import EmbeddingEngine
        embedding_engine = EmbeddingEngine("Model/glove.6B.50d.txt")

    elif choice == "2":
        from modules.bert_embedding_engine import BERTEmbeddingEngine
        embedding_engine = BERTEmbeddingEngine()

    elif choice == "3":
        from modules.fasttext_embedding_engine import FastTextEmbeddingEngine
        embedding_engine = FastTextEmbeddingEngine("Model/wiki-news-300d-1M.vec")

    else:
        print("Invalid choice. Defaulting to BERT.")
        from modules.bert_embedding_engine import BERTEmbeddingEngine
        embedding_engine = BERTEmbeddingEngine()

    #  LOAD DATA
    words = load_word_list("Datasets/word_list.txt")
    target_word = choose_target_word(words)

    print("Target word (debug):", target_word)

    with open("Datasets/word_attributes.json", "r") as f:
        word_attributes = json.load(f)

    word_data = word_attributes[target_word]

    #  GAME LOOP
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

        # spell check only for GloVe
        if choice == "1":
            corrected = spell_check_word(guess, embedding_engine)

            if corrected and corrected != guess:
                print(f"I hope you meant: {corrected}")
                guess = corrected
            elif corrected is None:
                print("No confident correction found.")
                continue

        # get vectors
        guess_vec = embedding_engine.get_vector(guess)
        target_vec = embedding_engine.get_vector(target_word)

        similarity = cosine_similarity(guess_vec, target_vec)

        if similarity is None:
            print("Word not in vocabulary.")
            continue

        # update memory
        sentence_generator.memory.update_similarity(similarity)

        # 👉 ADD THIS
        current_percentage = similarity_to_percentage(similarity)

        max_percentage = similarity_to_percentage(
            sentence_generator.memory.get_max_similarity()
        )

        # generate hint
        sentence, hint_level = sentence_generator.generate_hint(
            word_data,
            guess,
            similarity,
            embedding_engine
        )

        print("Similarity:", round(similarity, 3))
        print("Hint level:", hint_level)
        print("Hint:", sentence)

        # 👉 NOW this works
        print("Closeness:", current_percentage, "%")
        print("Best so far:", max_percentage, "%")
        
        if guess == target_word:
            print("Correct! You found the word.")
            break


if __name__ == "__main__":
    main()