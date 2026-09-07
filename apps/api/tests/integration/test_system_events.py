import os

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Set RUN_INTEGRATION_TESTS=1 with PostgreSQL available to run integration tests.",
)


@pytest.mark.asyncio
async def test_create_and_list_system_event() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        created = await client.post(
            "/api/v1/system-events",
            json={"event_type": "phase1.test", "message": "integration test event"},
        )
        assert created.status_code == 201

        listed = await client.get("/api/v1/system-events")
        assert listed.status_code == 200
        assert any(item["event_type"] == "phase1.test" for item in listed.json())
