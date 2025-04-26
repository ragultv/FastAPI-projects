from passlib.context import CryptContext
import config
from jose import JWTError, jwt  ,ExpiredSignatureError
from datetime  import timedelta,datetime
from fastapi import HTTPException

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta:timedelta |None =None)->str:
    data_copy=data.copy()

    if expires_delta is None:
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire=datetime.utcnow()+expires_delta
    data_copy.update({"exp":expire})

    token=jwt.encode(data_copy,config.SECRET_KEY,algorithm=config.ALGORITHM)
    return token

def verify_access_token(token:str)->dict:
    try:
        payload=jwt.decode(token,config.SECRET_KEY,algorithms=config.ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(staus_code=401,details="Token is invalid ")
    
def create_refresh_token(data:dict,expires_delta:timedelta |None =None)->str:
    data_copy=data.copy()

    if expires_delta is None:
        expires_delta=timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)

    expire=datetime.utcnow()+expires_delta
    data_copy.update({"exp":expire})

    token=jwt.encode(data_copy,config.SECRET_KEY,algorithm=config.ALGORITHM)
    return token

def verify_refresh_token(token:str)->dict:
    try:
        payload=jwt.decode(token,config.SECRET_KEY,algorithms=config.ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")