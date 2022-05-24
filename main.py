from datetime import datetime
from fastapi import FastAPI, HTTPException
import gensim
from models import *
import random


print("Loading model... This might take a while!")
model = gensim.models.KeyedVectors.load_word2vec_format("model/model.bin", binary=True, unicode_errors="replace")
print("Model loaded!")


# TODO: Run this on a cronjob at midnight
# Set seed to current day in order to generate same word when running on the same day
random.seed(datetime.now().strftime("%Y-%m-%d"))
# Fetch info
puzzle_number = random.randint(0, 5000)  # Only fetch words from the first 5000 to avoid obscure words
current_word = model.index_to_key[puzzle_number]
top_1000 = model.most_similar(current_word, topn=1000)
top_1000_words = map(lambda x: x[0], top_1000)
top_1_similarity = top_1000[0][1]
top_10_similarity = top_1000[10 - 1][1]
top_1000_similarity = top_1000[1000 - 1][1]


app = FastAPI()


async def calculate_guess(guess: Guess) -> GuessReult:
    """
    Takes a given guess and calculates the similarity, correctness and closeness of the guess
    """

    try:
        similarity = model.similarity(guess.word, model.index_to_key[guess.puzzleNumber])
    except KeyError:
        raise HTTPException(status_code=404, detail="Word not found")

    is_correct = similarity > 0.9

    if guess.puzzleNumber != puzzle_number:  # If user is still submitting for yesterday's puzzle. Still respond
        top_1000 = model.most_similar(model.index_to_key[guess.puzzleNumber], topn=1000)
        top_1000_words = map(lambda x: x[0], top_1000)

    is_close = True if guess.word in top_1000_words else False

    return GuessReult(word=guess.word, similarity=similarity, isClose=is_close, isCorrect=is_correct)


@app.get("/today", response_model=TodayInfo)
async def today_info() -> TodayInfo:
    """
    Metadata about today's puzzle
    """

    return TodayInfo(
        puzzleNumber=puzzle_number,
        similarity=top_1_similarity,
        similarityTenth=top_10_similarity,
        similarityThousandth=top_1000_similarity,
    )


