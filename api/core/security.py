from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from keycloak import KeycloakOpenID

from core.config import get_settings
from schemas.auth import User

settings = get_settings()

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
)

oauth2_scheme = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)
) -> User:
    """Decode and verify JWT token to get current user"""
    try:
        token = credentials.credentials
        token_info = keycloak_openid.decode_token(token)

        return User(
            username=token_info.get("preferred_username", ""),
            roles=token_info.get("realm_access", {}).get("roles", []),
            sub=token_info.get("sub", "")
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(required_roles: list[str]):
    """Decorator to check if user has required roles"""

    async def role_checker(user: User = Security(get_current_user)):
        for role in required_roles:
            if role not in user.roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role {role} is required"
                )
        return user

    return role_checker