from sqlalchemy.orm import Session
from data.models.postgres.user_model import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_google_id(self, google_id: str):
        return self.db.query(User).filter(User.google_id == google_id).first()

    def create_user(self, user_data: dict):
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_or_create(self, user_data: dict):
        user = self.get_by_google_id(user_data["sub"])

        if user:
            return user

        return self.create_user({
            "email": user_data["email"],
            "name": user_data["name"],
            "picture": user_data["picture"],
            "google_id": user_data["sub"],
        })