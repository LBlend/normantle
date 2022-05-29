import gensim

if __name__ == "__main__":
    print("Loading model...")
    model = gensim.models.KeyedVectors.load_word2vec_format("model/model.bin", binary=True, unicode_errors="replace")
    print("Model loaded!")

    print(model.similarity("kvinne", "kvinner"))
    print(model.similarity("mann", "menn"))
    print(model.similarity("mann", "kvinne"))
    print(model.similarity("hund", "valp"))
    print(model.similarity("riktig", "korrekt"))
