from pydantic import BaseModel


class TodayInfo(BaseModel):
    puzzleNumber: int
    similarity: float
    similarityTenth: float
    similarityThousandth: float


class Guess(BaseModel):
    word: str
    puzzleNumber: int


class GuessReult(BaseModel):
    word: str
    similarity: float
    isClose: bool
    isCorrect: bool
    of_thousand: int | None = None


class Hint(BaseModel):
    puzzleNumber: int
    bestGuess: str
