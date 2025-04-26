import database,config,models,schema,utils
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError,jwt

oauth_token = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str =Depends(oauth_token),db:Session=Depends(database.get_db)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        
  
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(models.user).filter(models.user.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")