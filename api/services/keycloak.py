from typing import Dict, List, Optional
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakGetError
from fastapi import HTTPException

from core.config import get_settings
from schemas.auth import UserRegistration

settings = get_settings()


class KeycloakService:
    def __init__(self):
        self.keycloak_admin = KeycloakAdmin(
            server_url=settings.KEYCLOAK_URL,
            realm_name=settings.KEYCLOAK_REALM,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
            verify=True
        )

    def create_user(self, user_data: UserRegistration) -> str:
        """Create a new user in Keycloak"""
        try:
            user_input = {
                "username": user_data.username,
                "email": user_data.email,
                "enabled": True,
                "firstName": user_data.firstName,
                "lastName": user_data.lastName,
                "credentials": [{
                    "type": "password",
                    "value": user_data.password,
                    "temporary": False
                }]
            }

            self.keycloak_admin.create_user(user_input)
            user_id = self.keycloak_admin.get_user_id(user_data.username)

            # Assign default roles
            self._assign_default_roles(user_id)

            return user_id
        except KeycloakGetError as e:
            if "username already exists" in str(e):
                raise HTTPException(status_code=400, detail="Username already exists")
            raise HTTPException(status_code=500, detail=str(e))

    def _assign_default_roles(self, user_id: str):
        """Assign default roles to a user"""
        roles = self.keycloak_admin.get_realm_roles()
        default_roles = ['file:read', 'file:write']

        roles_to_assign = []
        for role in roles:
            if role['name'] in default_roles:
                roles_to_assign.append(role)

        if roles_to_assign:
            self.keycloak_admin.assign_realm_roles(user_id=user_id, roles=roles_to_assign)