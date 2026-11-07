from os import PathLike
from typing import Self

import numpy as np


class KeyedVectors:
    def __init__(self, keys: list[str], vectors: np.ndarray):
        if len(keys) != len(vectors):
            raise ValueError("Number of keys does not match number of vectors")

        self.index_to_key = keys
        self.key_to_index = {key: index for index, key in enumerate(keys)}
        self.vectors = np.asarray(vectors, dtype=np.float32)
        self.norms = np.linalg.norm(self.vectors, axis=1)
        self.norms[self.norms == 0] = 1

    def __contains__(self, key: str) -> bool:
        return key in self.key_to_index

    def __len__(self) -> int:
        return len(self.index_to_key)

    @classmethod
    def load(cls, path: str | PathLike[str]) -> Self:
        with open(path, "rb") as file:
            count, size = map(int, file.readline().split())
            data = file.read()

        vector_bytes = size * np.dtype(np.float32).itemsize
        keys = []
        vectors = np.empty((count, size), dtype=np.float32)
        position = 0

        for index in range(count):
            separator = data.index(b" ", position)
            keys.append(data[position:separator].lstrip(b"\n").decode("utf-8", errors="replace"))
            position = separator + 1
            vectors[index] = np.frombuffer(data, dtype=np.float32, count=size, offset=position)
            position += vector_bytes

        return cls(keys, vectors)

    def save(self, path: str | PathLike[str]) -> None:
        with open(path, "wb") as file:
            file.write(f"{len(self)} {self.vectors.shape[1]}\n".encode())
            for key, vector in zip(self.index_to_key, self.vectors, strict=True):
                file.write(key.encode() + b" " + vector.tobytes())

    def _similarities(self, index: int) -> np.ndarray:
        return (self.vectors @ self.vectors[index]) / (self.norms * self.norms[index])

    def similarity(self, key1: str, key2: str) -> float:
        index1, index2 = self.key_to_index[key1], self.key_to_index[key2]
        return float((self.vectors[index1] @ self.vectors[index2]) / (self.norms[index1] * self.norms[index2]))

    def most_similar(self, key: str, topn: int = 10) -> list[tuple[str, float]]:
        index = self.key_to_index[key]
        topn = min(topn, len(self) - 1)
        if topn <= 0:
            return []

        similarities = self._similarities(index)
        similarities[index] = -np.inf
        best = np.argpartition(-similarities, topn - 1)[:topn]
        best = best[np.argsort(-similarities[best], kind="stable")]

        return [(self.index_to_key[i], float(similarities[i])) for i in best]
