import httpx

from app.agents.providers.base import ModelProvider, ModelRequest, ModelResponse


class AnthropicProvider(ModelProvider):
    name = "anthropic"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def generate(self, request: ModelRequest) -> ModelResponse:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": request.model,
                    "system": request.system_prompt,
                    "messages": [{"role": "user", "content": request.user_prompt}],
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                },
            )
            response.raise_for_status()
            data = response.json()
        blocks = data.get("content", [])
        text = "\n".join(block.get("text", "") for block in blocks if block.get("type") == "text")
        usage = data.get("usage", {})
        return ModelResponse(
            content=text,
            input_tokens=int(usage.get("input_tokens", 0)),
            output_tokens=int(usage.get("output_tokens", 0)),
            metadata={"provider": self.name, "response_id": data.get("id")},
        )
