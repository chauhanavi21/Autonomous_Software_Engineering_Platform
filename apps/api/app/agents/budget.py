from dataclasses import dataclass


class BudgetExceededError(RuntimeError):
    pass


@dataclass(slots=True)
class ExecutionBudget:
    max_tokens: int = 4000
    max_tool_calls: int = 8
    timeout_seconds: int = 60
    max_cost_usd: float = 0.50

    def ensure_token_budget(self, used_tokens: int) -> None:
        if used_tokens > self.max_tokens:
            raise BudgetExceededError(
                f"Execution used {used_tokens} tokens; budget is {self.max_tokens}"
            )
