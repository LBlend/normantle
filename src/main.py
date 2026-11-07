import logging
import os
import random
from contextlib import asynccontextmanager
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.models import Guess, GuessResult, Hint, NearbyWord, TodayInfo
from src.puzzle import Schedule, puzzle_number
from src.ratelimit import RateLimiter
from src.vectors import KeyedVectors

TIMEZONE = ZoneInfo(os.getenv("TZ", "").lstrip(":") or "Europe/Oslo")
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",")]
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))
TOP_N = 1000

PuzzleQuery = Annotated[int, Query(ge=0)]

logger = logging.getLogger("uvicorn.error")
model: KeyedVectors
schedule: Schedule


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model, schedule
    path = os.getenv("MODEL_PATH", "model/model.bin")
    logger.info("Loading model from %s", path)
    model = KeyedVectors.load(path)
    nearest.cache_clear()
    logger.info("Loaded %d words", len(model))

    secret = os.getenv("PUZZLE_SECRET", "")
    if not secret:
        logger.warning("PUZZLE_SECRET is not set, so anyone can work out future answers from the source code")
    nouns = Path(path).with_name("nouns.txt").read_text(encoding="utf-8").split()
    schedule = Schedule([noun for noun in nouns if noun in model], secret)

    nearest(target(today_puzzle()))
    yield


app = FastAPI(lifespan=lifespan, dependencies=[Depends(RateLimiter(RATE_LIMIT))])
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["GET", "POST"])


def today_puzzle() -> int:
    return puzzle_number(datetime.now(TIMEZONE).date())


def target(puzzle: int) -> str:
    if puzzle > today_puzzle():
        raise HTTPException(status_code=400, detail="Puzzle not available yet")

    return schedule.word(puzzle)


@lru_cache(maxsize=4)
def nearest(word: str) -> tuple[list[tuple[str, float]], dict[str, int]]:
    words = model.most_similar(word, topn=TOP_N)
    ranks = {word: rank for rank, (word, _) in enumerate(words, start=1)}
    return words, ranks


def correct_guess(answer: str) -> GuessResult:
    return GuessResult(word=answer, similarity=1, isClose=True, isCorrect=True, ofThousand=0)


def calculate_guess(word: str, answer: str) -> GuessResult:
    if word not in model:
        raise HTTPException(status_code=404, detail="Word not found")

    if word == answer:
        return correct_guess(answer)

    rank = nearest(answer)[1].get(word)

    return GuessResult(
        word=word,
        similarity=model.similarity(word, answer),
        isClose=rank is not None,
        isCorrect=False,
        ofThousand=rank,
    )


@app.get("/today", response_model=TodayInfo)
def today_info() -> TodayInfo:
    """
    Metadata about today's puzzle
    """

    puzzle = today_puzzle()
    words, _ = nearest(target(puzzle))

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

    return calculate_guess(guess.word, target(guess.puzzleNumber))


@app.post("/hint", response_model=GuessResult)
def hint(hint: Hint) -> GuessResult:
    """
    Return a word that is closer to the solution than the current best guess
    """

    answer = target(hint.puzzleNumber)
    if hint.bestGuess not in model:
        raise HTTPException(status_code=404, detail="Word not found")

    words, ranks = nearest(answer)
    best_rank = 1 if hint.bestGuess == answer else ranks.get(hint.bestGuess, len(words) + 1)
    closer = words[: best_rank - 1]
    if not closer:
        raise HTTPException(status_code=400, detail="No closer words available")

    word, _ = random.choice(closer)
    return calculate_guess(word, answer)


@app.get("/surrender", response_model=GuessResult)
def surrender(puzzle: PuzzleQuery) -> GuessResult:
    """
    Return the correct word as a guess result
    """

    return correct_guess(target(puzzle))


@app.get("/top1000", response_model=list[NearbyWord])
def top1000(puzzle: PuzzleQuery) -> list[NearbyWord]:
    """
    Return the 1000 closest words and their similarity for a given puzzle, closest first
    """

    return [NearbyWord(word=word, similarity=similarity) for word, similarity in nearest(target(puzzle))[0]]
