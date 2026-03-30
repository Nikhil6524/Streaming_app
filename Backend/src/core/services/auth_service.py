from handlers.http_clients.google_oauth_client import GoogleOAuthClient
from data.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.google_client = GoogleOAuthClient()

    def google_login(self, token: str):
        user_info = self.google_client.verify_token(token)

        user = self.repo.get_or_create(user_info)

        return user