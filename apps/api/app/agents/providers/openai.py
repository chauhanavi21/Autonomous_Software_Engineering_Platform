import httpx

from app.agents.providers.base import ModelProvider, ModelRequest, ModelResponse


class OpenAIProvider(ModelProvider):
    name = "openai"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def generate(self, request: ModelRequest) -> ModelResponse:
        payload = {
            "model": request.model,
            "input": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
        text = data.get("output_text", "")
        usage = data.get("usage", {})
        return ModelResponse(
            content=text,
            input_tokens=int(usage.get("input_tokens", 0)),
            output_tokens=int(usage.get("output_tokens", 0)),
            metadata={"provider": self.name, "response_id": data.get("id")},
        )
