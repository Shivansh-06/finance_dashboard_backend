from sqlalchemy.orm import Session
from models.role import Role
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status


def register_user(db: Session, email: str, password: str, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id")

    hashed = hash_password(password)

    user = User(
        email=email,
        password=hashed,
        role_id=role_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    if not user.is_active:
        return None
    
    return user

def login_user(user: User):
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}