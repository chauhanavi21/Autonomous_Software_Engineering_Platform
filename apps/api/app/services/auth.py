from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.jwt import create_access_token, create_refresh_token, hash_token
from app.auth.password import hash_password, verify_password
from app.models.refresh_token import RefreshToken
from app.repositories.user import UserRepository

class AuthService:
    def __init__(self,session:AsyncSession): self.session=session; self.users=UserRepository(session)
    async def register(self,email:str,password:str,display_name:str):
        if await self.users.by_email(email): raise HTTPException(409,"Email is already registered")
        user=await self.users.create(email=email.lower(),password_hash=hash_password(password),display_name=display_name)
        await self.session.commit(); return user
    async def login(self,email:str,password:str):
        user=await self.users.by_email(email)
        if not user or not verify_password(password,user.password_hash): raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid credentials")
        if not user.is_active: raise HTTPException(403,"Account is disabled")
        access=create_access_token(str(user.id)); raw,h,jti,exp=create_refresh_token(str(user.id))
        self.session.add(RefreshToken(user_id=user.id,token_hash=h,jti=jti,expires_at=exp)); await self.session.commit()
        return user,access,raw
    async def rotate_refresh(self,raw:str):
        row=await self.session.scalar(select(RefreshToken).where(RefreshToken.token_hash==hash_token(raw)))
        if not row or row.revoked_at or row.expires_at<=datetime.now(timezone.utc): raise HTTPException(401,"Invalid refresh token")
        row.revoked_at=datetime.now(timezone.utc); user=await self.users.by_id(row.user_id)
        new_raw,h,jti,exp=create_refresh_token(str(user.id)); self.session.add(RefreshToken(user_id=user.id,token_hash=h,jti=jti,expires_at=exp)); await self.session.commit()
        return user,create_access_token(str(user.id)),new_raw
    async def logout(self,raw:str):
        row=await self.session.scalar(select(RefreshToken).where(RefreshToken.token_hash==hash_token(raw)))
        if row and not row.revoked_at: row.revoked_at=datetime.now(timezone.utc); await self.session.commit()
