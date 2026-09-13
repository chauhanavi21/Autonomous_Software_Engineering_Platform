from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
class UserRepository:
    def __init__(self,session:AsyncSession): self.session=session
    async def by_email(self,email:str)->User|None: return await self.session.scalar(select(User).where(User.email==email.lower()))
    async def by_id(self,user_id): return await self.session.get(User,user_id)
    async def create(self,**data)->User:
        u=User(**data); self.session.add(u); await self.session.flush(); await self.session.refresh(u); return u
