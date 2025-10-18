from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
import os
from app.utils.auth import create_access_token
from app.utils.database import db

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://logify-cva8.onrender.com/auth/google/callback")

@router.get("/auth/google")
async def google_oauth():
    """Redirect to Google OAuth"""
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        "response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        "scope=openid email profile&"
        "access_type=offline&"
        "prompt=consent"
    )
    return RedirectResponse(google_auth_url)

@router.get("/auth/google/callback")
async def google_callback(code: str):
    """Handle Google OAuth callback"""
    try:
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            tokens = token_response.json()
            
            userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            user_response = await client.get(userinfo_url, headers=headers)
            user_info = user_response.json()
        
        email = user_info["email"]
        name = user_info.get("name", "")
        google_id = user_info["sub"]
        
        existing_user = db.get_user_by_email(email)
        if existing_user:
            user = existing_user
        else:
            user = db.create_user(email, hashed_password=None, name=name, google_id=google_id)
        
        access_token = create_access_token(data={"sub": str(user["id"])})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user.get("name"),
                "provider": "google"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")
