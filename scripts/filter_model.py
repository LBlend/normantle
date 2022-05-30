import gensim
import multiprocessing
from nltk.corpus import stopwords


stop_words_norwegian = set(stopwords.words("norwegian"))
stop_words_english = set(stopwords.words("english"))


def clean_section(file_content, range_number):
    print("Range", range_number, "started")

    new_model_output = ""
    for i, line in enumerate(file_content):
        if i % 10_000 == 0:  # Print progress every 10 000th vector
            print(range_number, i)

        word = line.split(" ")[0]
        if (
            word[0].isupper()
            or not word.isalpha()
            or len(word) < 3
            or word in stop_words_norwegian
            or word in stop_words_english
        ):
            continue
        else:
            new_model_output += line

    print("Range", range_number, "finished")

    return new_model_output


if __name__ == "__main__":
    print("Opening model file...")
    with open("model/model.txt", "r", encoding="utf-8") as old_model:
        print("Reading file contents...")
        file_content = old_model.readlines()
        print("Done\n")

    # 50K vectors per process totaling to 81 processes for the model consisting of a little over 4 million vectors
    file_ranges = [(file_content[(i - 1) * 50_000:i * 50_000], i) for i in range(2, 81)]
    file_ranges.append((file_content[1:50_000], 1))

    with multiprocessing.Pool() as pool:
        data = pool.starmap(clean_section, file_ranges)

    print("Concatenating new vectors...")
    final_output = ""
    for text in data:
        final_output += text
    print("Done\n")

    print("Calculating new number of vectors...")
    vectors = len(final_output.split("\n")) - 1
    print("Done\n")

    final_output = f"{vectors} 100\n{final_output}"

    with open("model/new_model.txt", "w", encoding="utf-8", newline="\n") as new_model:
        print("Writing to file...")
        new_model.write(final_output)
        print("Done\n")

    print("Loading newly created model...")
    model = gensim.models.KeyedVectors.load_word2vec_format(
        "model/new_model.txt", binary=False, unicode_errors="replace"
    )
    print("Done\n")

    print("Sorting model...")
    model.sort_by_descending_frequency()  # Model should already be sorted, but just in case
    print("Done\n")

    print("Saving model to binary format...")
    model.save_word2vec_format("model/model.bin", binary=True)
    print("Done\n")
