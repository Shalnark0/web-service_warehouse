from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.user import UserLogin, UserRegister
from services.auth import authenticate_user, register_user
from utils.jwt import generate_tokens, create_access_token
from utils.security import verify_refresh_token
from jose import JWTError
from utils.security import verify_access_token

auth = APIRouter()

@auth.post("/register", response_model=dict)
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        new_user = register_user(user, db)
        return {"message": "User successfully registered!"}
    except HTTPException as e:
        raise e

@auth.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        db_user = authenticate_user(user, db)
        access_token, refresh_token = generate_tokens(db_user)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=1800 
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 3600 
        )

        return {"message": "Login successful"}

    except HTTPException as e:
        raise e
    
@auth.post("/refresh")
def refresh_token(response: Response, refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        user = verify_refresh_token(refresh_token, db)        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token, _ = generate_tokens(user)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800
    )

    return {"message": "Access token refreshed"}

@auth.get("/me")
def auth_me(response: Response, access_token: str = Cookie(None), refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    if access_token:
        user_data = verify_access_token(access_token)
        if user_data:
            return {"message": "Authenticated", "user": user_data}
    
    if refresh_token:
        user_data = verify_refresh_token(refresh_token, db)
        if user_data:
            new_access_token = create_access_token(user_data)
            response.set_cookie(
                key="access_token", 
                value=new_access_token, 
                max_age=1800,
                httponly=True,
                secure=False,
                samesite="lax"
            )
            
            return {"message": "Token refreshed"}
    
    raise HTTPException(status_code=401, detail="Not authenticated")

@auth.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logout successful"}