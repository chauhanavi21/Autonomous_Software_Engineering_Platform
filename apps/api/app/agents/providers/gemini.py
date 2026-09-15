import httpx

from app.agents.providers.base import ModelProvider, ModelRequest, ModelResponse


class GeminiProvider(ModelProvider):
    name = "gemini"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def generate(self, request: ModelRequest) -> ModelResponse:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{request.model}:generateContent?key={self.api_key}"
        prompt = f"{request.system_prompt}\n\nUser request:\n{request.user_prompt}"
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": request.temperature,
                        "maxOutputTokens": request.max_tokens,
                    },
                },
            )
            response.raise_for_status()
            data = response.json()
        candidates = data.get("candidates", [])
        parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        text = "\n".join(part.get("text", "") for part in parts)
        usage = data.get("usageMetadata", {})
        return ModelResponse(
            content=text,
            input_tokens=int(usage.get("promptTokenCount", 0)),
            output_tokens=int(usage.get("candidatesTokenCount", 0)),
            metadata={"provider": self.name},
        )
