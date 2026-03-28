from __future__ import annotations

from typing import List


class State:
    def __init__(self, query: str, memory: List[str] | None = None, output: str = "", steps: int = 0) -> None:
        self.query = query
        self.memory = list(memory) if memory is not None else []
        self.output = output
        self.steps = steps

    def copy(self) -> "State":
        return State(
            query=self.query,
            memory=list(self.memory),
            output=self.output,
            steps=self.steps,
        )

    def update_step(self, increment: int = 1) -> None:
        self.steps += increment
