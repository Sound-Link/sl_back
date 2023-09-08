from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import requests

router = APIRouter()

KAKAO_CLIENT_ID = "8d14be00636c3c6f065f37e3ea715cb4"
REDIRECT_URI = "http://127.0.0.1:8000/login/callback"

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
    response_data = response.json()
    print(response_data)  # 로그 추가
    
    if "error" in response_data:
        raise HTTPException(status_code=400, detail=response_data["error_description"])
    
    token = response_data.get("access_token")
    if not token:
        raise HTTPException(status_code=500, detail="Access token was not found in the response.")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    user_info_response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
    user_info = user_info_response.json()

    if "id" not in user_info:
        raise HTTPException(status_code=500, detail="Failed to retrieve user information from Kakao.")

    # 성공적으로 로그인 후 메인 페이지 또는 사용자 대시보드로 리디렉션
    return RedirectResponse(url="/dashboard")

@router.get("/dashboard")
def dashboard():
    return {"message": "Welcome to the dashboard!"}