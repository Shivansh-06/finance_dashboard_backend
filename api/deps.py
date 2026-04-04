from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db.session import SessionLocal
from core.security import decode_token
from models.user import User

security = HTTPBearer()


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get current user
def get_current_user(
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = decode_token(token)
    user_id = payload.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    
    return user

def require_role(allowed_roles: list):
    def checker(user=Depends(get_current_user)):
        if user.role.name not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return checker