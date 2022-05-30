from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import gensim
from src.models import Guess, GuessReult, Hint, TodayInfo
import random


print("Loading model... This might take a while!")
model = gensim.models.KeyedVectors.load_word2vec_format("model/model.bin", binary=True, unicode_errors="replace")
print("Model loaded!")

model.sort_by_descending_frequency()  # Just in case :)


# TODO: Run this on a cronjob at midnight
# Set seed to current day in order to generate same word when running on the same day
random.seed(datetime.now().strftime("%Y-%m-%d"))

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"])

# Fetch info
app.puzzle_number = random.randint(0, 5000)  # Only fetch words from the first 5000 to avoid obscure words
app.current_word = model.index_to_key[app.puzzle_number]
app.top_1000 = model.most_similar(app.current_word, topn=1000)
app.top_1000_words = list(map(lambda x: x[0], app.top_1000))
app.top_1_similarity = app.top_1000[0][1]
app.top_10_similarity = app.top_1000[10 - 1][1]
app.top_1000_similarity = app.top_1000[1000 - 1][1]


async def calculate_guess(guess: Guess) -> GuessReult:
    """
    Takes a given guess and calculates the similarity, correctness and closeness of the guess
    """

    try:
        similarity = model.similarity(guess.word, model.index_to_key[guess.puzzleNumber])
    except KeyError:
        raise HTTPException(status_code=404, detail="Word not found")

    is_correct = similarity > 0.9

    if guess.puzzleNumber != app.puzzle_number:  # If user is still submitting for yesterday's puzzle. Still respond
        top_1000 = model.most_similar(model.index_to_key[guess.puzzleNumber], topn=1000)
        top_1000_words = list(map(lambda x: x[0], top_1000))
    else:
        top_1000_words = app.top_1000_words

    is_close = True if guess.word in top_1000_words else False
    closeness = top_1000_words.index(guess.word) + 1 if is_close else None

    is_close = True if is_correct else is_close  # Set is_close to True if the guess is correct

    return GuessReult(
        word=guess.word, similarity=similarity, isClose=is_close, isCorrect=is_correct, ofThousand=closeness
    )


@app.get("/today", response_model=TodayInfo)
async def today_info() -> TodayInfo:
    """
    Metadata about today's puzzle
    """

    return TodayInfo(
        puzzleNumber=app.puzzle_number,
        similarity=app.top_1_similarity,
        similarityTenth=app.top_10_similarity,
        similarityThousandth=app.top_1000_similarity,
    )


# POST requests below because it's much more convinient to define a type than to use query parameters


@app.post("/guess", response_model=GuessReult)
async def guess(guess: Guess) -> GuessReult:
    """
    Submit a guess and get the result
    """

    return await calculate_guess(guess)


@app.post("/hint", response_model=GuessReult)
async def hint(hint: Hint) -> GuessReult:
    """
    Return a word that is closer to the solution than the current best guess
    """

    closer = model.closer_than(model.index_to_key[hint.puzzleNumber], hint.bestGuess)
    hint_word = random.choice(closer)

    return await calculate_guess(Guess(word=hint_word, puzzleNumber=hint.puzzleNumber))


@app.get("/surrender", response_model=GuessReult)
async def surrender(puzzle: int) -> GuessReult:
    """
    Return the correct word as a guess result
    """

    return GuessReult(word=model.index_to_key[puzzle], similarity=1, isClose=True, isCorrect=True, ofThousand=0)


@app.get("/top1000", response_class=HTMLResponse)
async def top1000(puzzle: int):
    """
    Return the top 1000 closes words and their similarity for a given puzzle
    """

    if puzzle != app.puzzle_number:  # If user is still submitting for yesterday's puzzle. Still respond
        top_1000 = model.most_similar(model.index_to_key[puzzle], topn=1000)
    else:
        top_1000 = app.top_1000_words

    top_1000 = list(
        map(
            lambda x: f"<p>{x} {model.similarity(model.index_to_key[puzzle], x)}</p>",
            top_1000,
        )
    )
    top_1000 = "\n".join(top_1000)

    return f"""
    <html>
        <body>
            {top_1000}
        </body>
    </html>
    """
