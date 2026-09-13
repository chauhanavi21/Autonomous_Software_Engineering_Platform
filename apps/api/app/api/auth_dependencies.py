from typing import Annotated
from uuid import UUID
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import DbSession
from app.auth.jwt import decode_access_token
from app.models.user import User
security=HTTPBearer(auto_error=False)
async def get_current_user(session:DbSession,credentials:Annotated[HTTPAuthorizationCredentials|None,Depends(security)])->User:
    if not credentials: raise HTTPException(401,"Authentication required")
    try: payload=decode_access_token(credentials.credentials); user_id=UUID(payload["sub"])
    except (jwt.PyJWTError,ValueError,KeyError): raise HTTPException(401,"Invalid access token")
    user=await session.get(User,user_id)
    if not user or not user.is_active: raise HTTPException(401,"Invalid user")
    return user
CurrentUser=Annotated[User,Depends(get_current_user)]
