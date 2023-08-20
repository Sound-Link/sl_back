from fastapi import APIRouter, Depends, HTTPException
import requests

router = APIRouter()

KAKAO_CLIENT_ID = "YOUR_KAKAO_CLIENT_ID"
REDIRECT_URI = "http://your_domain.com/login/callback"

@router.get("/login")
def login():
    kakao_login_url = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return {"login_url": kakao_login_url}

@router.get("/login/callback")
def login_callback(code: str):
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    response = requests.post(token_url, data=data)
    token = response.json().get("access_token")
    
    # With the token, you can request user info or other data as per your needs
    headers = {
        "Authorization": f"Bearer {token}"
    }
    user_info_response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
    user_info = user_info_response.json()
    
    # Process the user info as you see fit
    return user_info
