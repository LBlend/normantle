from pydantic import BaseModel


class Guess(BaseModel):
    word: str
    puzzleNumber: int


class GuessReult(BaseModel):
    word: str
    similarity: float
    isClose: bool
    isCorrect: bool
    ofThousand: int | None = None


class Hint(BaseModel):
    puzzleNumber: int
    bestGuess: str


class TodayInfo(BaseModel):
    puzzleNumber: int
    similarity: float
    similarityTenth: float
    similarityThousandth: float


class Top1000(BaseModel):
    top1000: list[tuple[str, float]]
