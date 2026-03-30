from fastapi import APIRouter, Depends, Response
from schemas.auth_schema import GoogleAuthRequest
from core.services.auth_service import AuthService
from api.rest.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/google")
def google_login(
    request: GoogleAuthRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    #  Step 1: verify + get user
    user = service.google_login(request.token)

    #  Step 2: set session cookie
    response.set_cookie(
    key="user_id",
    value=str(user.id),
    httponly=True,
    samesite="lax",
    secure=False 
    )
    #  Step 3: return user
    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }