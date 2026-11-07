import math
import time
from collections import Counter

from fastapi import HTTPException, Request


class RateLimiter:
    def __init__(self, limit: int, window: float = 60):
        self.limit = limit
        self.window = window
        self.current_window = -1
        self.counts: Counter[str] = Counter()

    async def __call__(self, request: Request) -> None:
        if self.limit <= 0:
            return

        now = time.monotonic()
        window = int(now // self.window)
        if window != self.current_window:
            self.current_window = window
            self.counts.clear()

        client = request.client.host if request.client else "unknown"
        self.counts[client] += 1

        if self.counts[client] > self.limit:
            retry_after = math.ceil(self.window - now % self.window)
            raise HTTPException(status_code=429, detail="Too many requests", headers={"Retry-After": str(retry_after)})
