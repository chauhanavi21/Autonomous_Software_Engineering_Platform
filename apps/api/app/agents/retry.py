from dataclasses import dataclass


@dataclass(slots=True)
class RetryPolicy:
    max_attempts: int = 2
    base_delay_seconds: float = 0.5
    max_delay_seconds: float = 4.0

    def delay_for(self, attempt: int) -> float:
        return min(self.base_delay_seconds * (2 ** max(0, attempt - 1)), self.max_delay_seconds)
