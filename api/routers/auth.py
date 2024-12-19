from keycloak.exceptions import KeycloakError
from fastapi import APIRouter, HTTPException

from core.security import keycloak_openid
from schemas.auth import UserRegistration, TokenResponse, UserLogin
from services.keycloak import KeycloakService

router = APIRouter(tags=['Authentication'])
keycloak_service = KeycloakService()
@router.post("/auth/register", response_model=dict)
async def register_user(user_data: UserRegistration):
    """
    Register a new user in Keycloak
    """
    try:
        user_id = keycloak_service.create_user(user_data)
        return {
            "message": "User registered successfully",
            "user_id": user_id
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth/login", response_model=TokenResponse)
async def login_user(user_credentials: UserLogin):
    """
    Login user and return access token
    """
    try:
        # Get token from Keycloak
        token = keycloak_openid.token(
            username=user_credentials.username,
            password=user_credentials.password
        )

        return TokenResponse(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            expires_in=token["expires_in"],
            refresh_expires_in=token["refresh_expires_in"],
            token_type=token["token_type"]
        )
    except KeycloakError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token
    """
    try:
        token = keycloak_openid.refresh_token(refresh_token)

        return TokenResponse(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            expires_in=token["expires_in"],
            refresh_expires_in=token["refresh_expires_in"],
            token_type=token["token_type"]
        )
    except KeycloakError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth/logout")
async def logout(refresh_token: str):
    """
    Logout user and invalidate refresh token
    """
    try:
        keycloak_openid.logout(refresh_token)
        return {"message": "Successfully logged out"}
    except KeycloakError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))