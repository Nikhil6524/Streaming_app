import requests
from fastapi import HTTPException
from config.settings import settings

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

class GoogleOAuthClient:
    def verify_token(self, token: str):
        response = requests.get(GOOGLE_TOKEN_INFO_URL, params={"id_token": token})

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Google token")

        data = response.json()

        #  IMPORTANT SECURITY CHECK
        if data.get("aud") != settings.google_client_id:
            raise HTTPException(status_code=401, detail="Invalid audience")

        return data