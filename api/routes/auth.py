from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserLogin
from services.auth_service import register_user, authenticate_user, login_user
from api.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, data.email, data.password, data.role_id)
    return {"message": "User created", "user_id": user.id}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return login_user(user)