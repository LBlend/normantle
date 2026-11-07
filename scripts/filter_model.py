import csv
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path

import numpy as np
from nltk.corpus import stopwords

from src.vectors import KeyedVectors

SOURCE = Path("model/model.txt")
TARGET = Path("model/model.bin")
NOUNS = Path("model/nouns.txt")
ORDBANK = Path("model/ordbank")
STOP_WORDS = set(stopwords.words("norwegian")) | set(stopwords.words("english"))


def read_ordbank(name: str) -> Iterator[list[str]]:
    with (ORDBANK / f"{name}.txt").open(encoding="latin-1", newline="") as file:
        rows = csv.reader(file, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(rows)
        yield from rows


def word_classes() -> dict[str, set[str]]:
    lemmas = {row[1]: row[2] for row in read_ordbank("lemma")}
    paradigms = {row[1]: row[3] for row in read_ordbank("paradigme")}
    classes = defaultdict(set)
    for row in read_ordbank("lemma_paradigme"):
        if row[1] in lemmas and row[2] in paradigms:
            classes[lemmas[row[1]]].add(paradigms[row[2]])
    return classes


def is_noun(classes: set[str]) -> bool:
    return any(c.startswith("subst") and "appell" in c for c in classes)


def is_only_noun(classes: set[str]) -> bool:
    return is_noun(classes) and all(c.startswith("subst") for c in classes)


def keep(word: str, classes: set[str]) -> bool:
    if not (word.isalpha() and word.islower() and len(word) >= 3) or word in STOP_WORDS:
        return False
    if is_noun(classes) or any(c.startswith(("verb", "adj")) for c in classes):
        return True
    return bool(classes) and all(c.startswith("adv") for c in classes)


def main() -> None:
    print(f"Reading word classes from {ORDBANK}...")
    dictionary = word_classes()

    keys = []
    vectors = []
    nouns = []

    print(f"Filtering {SOURCE}...")
    with SOURCE.open(encoding="utf-8", errors="replace") as file:
        next(file)
        for line_number, line in enumerate(file, start=1):
            word, _, values = line.partition(" ")
            classes = dictionary.get(word, set())
            if keep(word, classes):
                keys.append(word)
                vectors.append(np.array(values.split(), dtype=np.float32))
                if is_only_noun(classes):
                    nouns.append(word)

            if line_number % 100_000 == 0:
                print(f"Processed {line_number} vectors, kept {len(keys)}")

    print(f"Saving {len(keys)} vectors to {TARGET} and {len(nouns)} nouns to {NOUNS}...")
    KeyedVectors(keys, np.vstack(vectors)).save(TARGET)
    NOUNS.write_text("\n".join(nouns) + "\n", encoding="utf-8")
    print("Done")


if __name__ == "__main__":
    main()
