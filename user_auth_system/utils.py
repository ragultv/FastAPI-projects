from passlib.context import CryptContext
import config
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    data_copy=data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta  # ✅ Fixing error
    data_copy.update({"exp": expire})

    token = jwt.encode(data_copy, config.SECRET_KEY, algorithm=config.ALGORITHM) 
    return token

