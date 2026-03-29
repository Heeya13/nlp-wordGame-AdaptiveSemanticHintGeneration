# NLP Word Game

A fun word-based NLP game that makes the user guess a hidden target word. It uses word embeddings to check similarity and generate sentence level hints to help guide the user towards the hidden word.

---

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/Heeya13/nlp-wordGame.git
cd nlp-wordGame
```

2. **Create a `model/` folder** and add the embeddings:

* `glove.6B.50d.txt` (GloVe 50-dimensional)
* `wiki-news-300d-1M.vec` (FastText pre-trained)

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the Game

Simply run the main script:

```bash
python main.py
```

> Make sure the dataset files in `datasets/` are present and model filenames match exactly.

---

## Notes

* `model/` folder is **not in the repo** due to large file sizes.
* Only the code and datasets are included.
