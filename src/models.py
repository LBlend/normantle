from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

MAX_PUZZLE = 3000

PuzzleNumber = Annotated[int, Field(ge=0, le=MAX_PUZZLE)]
Word = Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, min_length=1, max_length=64)]


class Guess(BaseModel):
    word: Word
    puzzleNumber: PuzzleNumber


class GuessResult(BaseModel):
    word: str
    similarity: float
    isClose: bool
    isCorrect: bool
    ofThousand: int | None = None


class Hint(BaseModel):
    puzzleNumber: PuzzleNumber
    bestGuess: Word


class TodayInfo(BaseModel):
    puzzleNumber: int
    similarity: float
    similarityTenth: float
    similarityThousandth: float
