from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[ModelT]:
    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelT],
    ) -> None:
        self.session = session
        self.model = model

    async def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity