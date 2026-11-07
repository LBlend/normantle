from src.vectors import KeyedVectors

PAIRS = [
    ("kvinne", "kvinner"),
    ("mann", "menn"),
    ("mann", "kvinne"),
    ("hund", "valp"),
    ("riktig", "korrekt"),
]

if __name__ == "__main__":
    print("Loading model...")
    model = KeyedVectors.load("model/model.bin")
    print(f"Loaded {len(model)} words")

    for first, second in PAIRS:
        print(first, second, model.similarity(first, second))
