from pathlib import Path

import numpy as np
from nltk.corpus import stopwords

from src.vectors import KeyedVectors

SOURCE = Path("model/model.txt")
TARGET = Path("model/model.bin")
STOP_WORDS = set(stopwords.words("norwegian")) | set(stopwords.words("english"))


def keep(word: str) -> bool:
    return word.isalpha() and len(word) >= 3 and not word[0].isupper() and word not in STOP_WORDS


def main() -> None:
    keys = []
    vectors = []

    print(f"Filtering {SOURCE}...")
    with SOURCE.open(encoding="utf-8", errors="replace") as file:
        next(file)
        for line_number, line in enumerate(file, start=1):
            word, _, values = line.partition(" ")
            if keep(word):
                keys.append(word)
                vectors.append(np.array(values.split(), dtype=np.float32))

            if line_number % 100_000 == 0:
                print(f"Processed {line_number} vectors, kept {len(keys)}")

    print(f"Saving {len(keys)} vectors to {TARGET}...")
    KeyedVectors(keys, np.vstack(vectors)).save(TARGET)
    print("Done")


if __name__ == "__main__":
    main()
