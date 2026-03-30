from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from data.clients.postgres_client import get_db
from data.models.postgres.user_model import User

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me")
def get_current_user(
    user_id: str = Cookie(None, alias="user_id"),  # 🔥 ADD alias
    db: Session = Depends(get_db)
):
    print("COOKIE VALUE:", user_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name
    }