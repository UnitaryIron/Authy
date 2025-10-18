from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
import os
import json
from urllib.parse import quote, unquote
from app.utils.auth import create_access_token
from app.utils.database import db

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://logify-cva8.onrender.com/auth/google/callback")

@router.get("/auth/google")
async def google_oauth(redirect_uri: str = None):
    """Redirect to Google OAuth"""
    if not redirect_uri:
        redirect_uri = "https://logify-cva8.onrender.com/auth/success"
    
    state_data = {"redirect_uri": redirect_uri}
    state = quote(json.dumps(state_data))
    
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        "response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        "scope=openid email profile&"
        f"state={state}&"
        "access_type=offline&"
        "prompt=consent"
    )
    return RedirectResponse(google_auth_url)

@router.get("/auth/google/callback")
async def google_callback(code: str, state: str = None):
    """Handle Google OAuth callback"""
    try:
        if state:
            state_data = json.loads(unquote(state))
            redirect_uri = state_data.get("redirect_uri", "https://logify-cva8.onrender.com/auth/success")
        else:
            redirect_uri = "https://logify-cva8.onrender.com/auth/success"
        
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
        
        redirect_url = (
            f"{redirect_uri}"
            f"?token={access_token}"
            f"&user_id={user['id']}"
            f"&email={user['email']}"
            f"&name={quote(user.get('name', ''))}"
            f"&provider=google"
        )
        return RedirectResponse(redirect_url)
        
    except Exception as e:
        error_redirect = f"{redirect_uri}?error=oauth_failed&message={str(e)}"
        return RedirectResponse(error_redirect)

@router.get("/auth/success")
async def oauth_success():
    """Demo page to show OAuth success"""
    return {
        "message": "OAuth login successful!",
        "note": "Developers should set redirect_uri to their own app URL",
        "usage": "Add ?redirect_uri=YOUR_APP_URL to /auth/google"
    }
