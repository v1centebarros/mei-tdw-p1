from typing import List
from pydantic import BaseModel


class User(BaseModel):
    """Schema for user information with roles"""
    username: str
    roles: List[str]
    sub: str


class UserRegistration(BaseModel):
    """Schema for user registration"""
    username: str
    email: str
    password: str
    firstName: str
    lastName: str


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str
