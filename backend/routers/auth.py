from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from security import hash_password, verify_password, create_user_token, get_current_user
import os
from fastapi.security import OAuth2PasswordRequestForm

try: 
    from schemas import UserSignup, UserLogin
    from models import User
    from database import get_db
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from schemas import UserSignup, UserLogin
    from models import User
    from database import get_db

router = APIRouter(prefix="/auth")

@router.post("/signup")
def userSignup(userData: UserSignup, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email==userData.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registerd")
    hashed_password = hash_password(userData.password)
    new_user = User(
        name=userData.name,
        email=userData.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message":"User created successfully"
    }

@router.post("/login")
def userLogin(userData: OAuth2PasswordRequestForm= Depends(), db=Depends(get_db)):
    existing_user = db.query(User).filter(User.email==userData.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Email is not found")

    hashed_password = existing_user.password

    if verify_password(userData.password, hashed_password):
        token = create_user_token(existing_user.id)
        return {
            "access_token":token,
            "token_type":"bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="Cridential not matched")

@router.get("/profile")
def profile(user = Depends(get_current_user), db:Session =Depends(get_db)):
    return {
        "user_id":user.id,
        "user_name":user.name,
        "user_email":user.email
    }

