from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_db, require_role
from models.role import Role
from models.user import User
from schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    return db.query(User).all()

class StatusUpdate(BaseModel):

    is_active: bool


@router.patch("/{user_id}/status", response_model=UserOut)
def update_user_status(

    user_id: int,

    body: StatusUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(require_role(["Admin"]))

):

    target = db.query(User).filter(User.id == user_id).first()

    if not target:

        raise HTTPException(status_code=404, detail="User not found")

    target.is_active = body.is_active

    db.commit()

    db.refresh(target)

    return target



class RoleUpdate(BaseModel):
    role_id: int


@router.patch("/{user_id}/role", response_model=UserOut)
def update_user_role(
    user_id: int,
    body: RoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin"]))

):

    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    role = db.query(Role).filter(Role.id == body.role_id).first()

    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id")

    target.role_id = body.role_id
    db.commit()
    db.refresh(target)

    return target