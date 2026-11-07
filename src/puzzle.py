import hashlib
import hmac
from datetime import date

LAUNCH = date(2022, 5, 31)
SKIP_MOST_COMMON = 150
WORDS = 3000


def puzzle_number(day: date) -> int:
    return (day - LAUNCH).days


class Schedule:
    def __init__(self, keys: list[str], secret: str):
        key = secret.encode()
        candidates = keys[SKIP_MOST_COMMON : SKIP_MOST_COMMON + WORDS]
        self.words = sorted(candidates, key=lambda word: hmac.new(key, word.encode(), hashlib.sha256).digest())

    def word(self, puzzle: int) -> str:
        return self.words[puzzle % len(self.words)]
