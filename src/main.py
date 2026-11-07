import html
import logging
import os
import random
from contextlib import asynccontextmanager
from datetime import datetime
from functools import lru_cache
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.models import MAX_PUZZLE, Guess, GuessResult, Hint, TodayInfo
from src.vectors import KeyedVectors

TIMEZONE = ZoneInfo(os.getenv("TZ", "").lstrip(":") or "Europe/Oslo")
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",")]
TOP_N = 1000

PuzzleQuery = Annotated[int, Query(ge=0, le=MAX_PUZZLE)]

logger = logging.getLogger("uvicorn.error")
model: KeyedVectors


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model
    path = os.getenv("MODEL_PATH", "model/model.bin")
    logger.info("Loading model from %s", path)
    model = KeyedVectors.load(path)
    nearest.cache_clear()
    logger.info("Loaded %d words", len(model))
    nearest(today_puzzle())
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["GET", "POST"])


def today_puzzle() -> int:
    day = datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    return random.Random(day).randint(0, MAX_PUZZLE)


@lru_cache(maxsize=4)
def nearest(puzzle: int) -> tuple[list[tuple[str, float]], dict[str, int]]:
    words = model.most_similar(model.index_to_key[puzzle], topn=TOP_N)
    ranks = {word: rank for rank, (word, _) in enumerate(words, start=1)}
    return words, ranks


def calculate_guess(word: str, puzzle: int) -> GuessResult:
    if word not in model:
        raise HTTPException(status_code=404, detail="Word not found")

    target = model.index_to_key[puzzle]
    is_correct = word == target
    rank = nearest(puzzle)[1].get(word)

    return GuessResult(
        word=word,
        similarity=model.similarity(word, target),
        isClose=is_correct or rank is not None,
        isCorrect=is_correct,
        ofThousand=rank,
    )


@app.get("/today", response_model=TodayInfo)
def today_info() -> TodayInfo:
    """
    Metadata about today's puzzle
    """

    puzzle = today_puzzle()
    words, _ = nearest(puzzle)

    return TodayInfo(
        puzzleNumber=puzzle,
        similarity=words[0][1],
        similarityTenth=words[9][1],
        similarityThousandth=words[-1][1],
    )


@app.post("/guess", response_model=GuessResult)
def guess(guess: Guess) -> GuessResult:
    """
    Submit a guess and get the result
    """

    return calculate_guess(guess.word, guess.puzzleNumber)


@app.post("/hint", response_model=GuessResult)
def hint(hint: Hint) -> GuessResult:
    """
    Return a word that is closer to the solution than the current best guess
    """

    if hint.bestGuess not in model:
        raise HTTPException(status_code=404, detail="Word not found")

    closer = model.closer_than(model.index_to_key[hint.puzzleNumber], hint.bestGuess)
    if not closer:
        raise HTTPException(status_code=400, detail="No closer words available")

    return calculate_guess(random.choice(closer), hint.puzzleNumber)


@app.get("/surrender", response_model=GuessResult)
def surrender(puzzle: PuzzleQuery) -> GuessResult:
    """
    Return the correct word as a guess result
    """

    return GuessResult(word=model.index_to_key[puzzle], similarity=1, isClose=True, isCorrect=True, ofThousand=0)


@app.get("/top1000", response_class=HTMLResponse)
def top1000(puzzle: PuzzleQuery) -> str:
    """
    Return the top 1000 closest words and their similarity for a given puzzle
    """

    rows = "\n".join(f"<p>{html.escape(word)} {similarity}</p>" for word, similarity in nearest(puzzle)[0])

    return f"""
    <html>
        <body>
            {rows}
        </body>
    </html>
    """
