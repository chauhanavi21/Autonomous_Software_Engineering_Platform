from fastapi import APIRouter, Cookie, Response, HTTPException
from app.api.auth_dependencies import CurrentUser
from app.api.dependencies import DbSession
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth import AuthService
router=APIRouter(prefix="/auth",tags=["Authentication"])
COOKIE="forgeos_refresh"
@router.post("/register",response_model=UserResponse,status_code=201)
async def register(body:RegisterRequest,session:DbSession): return await AuthService(session).register(str(body.email),body.password,body.display_name)
@router.post("/login",response_model=TokenResponse)
async def login(body:LoginRequest,response:Response,session:DbSession):
    user,access,refresh=await AuthService(session).login(str(body.email),body.password); response.set_cookie(COOKIE,refresh,httponly=True,samesite="lax",secure=False,max_age=7*86400,path="/api/v1/auth"); return TokenResponse(access_token=access,user=user)
@router.post("/refresh",response_model=TokenResponse)
async def refresh(response:Response,session:DbSession,forgeos_refresh:str|None=Cookie(default=None)):
    if not forgeos_refresh: raise HTTPException(401,"Refresh token required")
    user,access,new_refresh=await AuthService(session).rotate_refresh(forgeos_refresh); response.set_cookie(COOKIE,new_refresh,httponly=True,samesite="lax",secure=False,max_age=7*86400,path="/api/v1/auth"); return TokenResponse(access_token=access,user=user)
@router.post("/logout",status_code=204)
async def logout(response:Response,session:DbSession,forgeos_refresh:str|None=Cookie(default=None)):
    if forgeos_refresh: await AuthService(session).logout(forgeos_refresh)
    response.delete_cookie(COOKIE,path="/api/v1/auth")
@router.get("/me",response_model=UserResponse)
async def me(user:CurrentUser): return user
