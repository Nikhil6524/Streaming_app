from data.clients.postgres_client import get_db
from data.repositories.user_repo import UserRepository
from core.services.auth_service import AuthService
from fastapi import Depends
from sqlalchemy.orm import Session

def get_auth_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return AuthService(repo)