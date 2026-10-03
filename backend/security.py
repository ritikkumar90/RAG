from jose import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from database import get_db
from models import User
from sqlalchemy.orm import Session

load_dotenv()
# ALGORITHM = os.getenv("ALGORITHM")
ALGORITHM = "HS256"
SECRET_CODE = "code"
passwordHash = PasswordHash.recommended()


def hash_password(raw_password):
    return passwordHash.hash(raw_password)

def verify_password(raw_password, hashed):
    return passwordHash.verify(raw_password, hashed)

def create_user_token(id:int):
    expire = datetime.now(timezone.utc) +  timedelta(minutes=30)

    payload = {
        "sub":str(id),
        "exp":expire
    }
    token = jwt.encode(
        payload,
        SECRET_CODE,
        algorithm=ALGORITHM
    )
    return token


oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalide credintials",
        headers={"www-Authenticate":"bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_CODE, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id==None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions
    user = db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise credentials_exceptions
    
    return user


