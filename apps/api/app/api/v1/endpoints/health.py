import asyncio
import time

from fastapi import APIRouter, Response, status
from redis.asyncio import Redis
from sqlalchemy import text

from app.core.config import settings
from app.db.session import AsyncSessionFactory
from app.schemas.health import ComponentHealth, LiveHealthResponse, ReadyHealthResponse

router = APIRouter(prefix="/health", tags=["System"])


async def check_database() -> ComponentHealth:
    started = time.perf_counter()
    try:
        async with AsyncSessionFactory() as session:
            await session.execute(text("SELECT 1"))
        return ComponentHealth(
            status="healthy", latency_ms=round((time.perf_counter() - started) * 1000, 2)
        )
    except Exception:
        return ComponentHealth(status="unhealthy")


async def check_redis() -> ComponentHealth:
    started = time.perf_counter()
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    try:
        await redis.ping()
        return ComponentHealth(
            status="healthy", latency_ms=round((time.perf_counter() - started) * 1000, 2)
        )
    except Exception:
        return ComponentHealth(status="unhealthy")
    finally:
        await redis.aclose()


@router.get("/live", response_model=LiveHealthResponse)
async def liveness() -> LiveHealthResponse:
    return LiveHealthResponse(status="alive", service="forgeos-api")


@router.get("/ready", response_model=ReadyHealthResponse)
async def readiness(response: Response) -> ReadyHealthResponse:
    database, redis = await asyncio.gather(check_database(), check_redis())
    healthy = database.status == "healthy" and redis.status == "healthy"
    if not healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadyHealthResponse(
        status="healthy" if healthy else "degraded",
        service="forgeos-api",
        database=database,
        redis=redis,
    )
