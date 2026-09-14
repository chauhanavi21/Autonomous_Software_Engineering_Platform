from datetime import datetime, timedelta, timezone
from uuid import uuid4
import hashlib, secrets
import jwt
from app.core.config import settings

def create_access_token(user_id:str)->str:
    now=datetime.now(timezone.utc)
    payload={"sub":user_id,"type":"access","jti":str(uuid4()),"iat":now,"exp":now+timedelta(minutes=settings.access_token_minutes)}
    return jwt.encode(payload,settings.jwt_secret,algorithm=settings.jwt_algorithm)

def create_refresh_token(user_id:str)->tuple[str,str,str,datetime]:
    jti=str(uuid4()); raw=secrets.token_urlsafe(48); exp=datetime.now(timezone.utc)+timedelta(days=settings.refresh_token_days)
    return raw, hash_token(raw), jti, exp

def hash_token(raw:str)->str: return hashlib.sha256(raw.encode()).hexdigest()
def decode_access_token(token:str)->dict:
    payload=jwt.decode(token,settings.jwt_secret,algorithms=[settings.jwt_algorithm])
    if payload.get("type")!="access": raise jwt.InvalidTokenError("wrong token type")
    return payload
