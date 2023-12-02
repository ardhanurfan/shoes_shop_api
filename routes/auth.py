from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
import requests
from middleware.jwt import create_access_token, get_current_user
from passlib.context import CryptContext
from db.connection import connectDB
from api.url import shoes_cleaner

from models.token import Token
from models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

auth = APIRouter()

# Token endpoint
@auth.post("/login", response_model=Token, tags=["Authentication"])
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    query = ("SELECT * FROM users WHERE username = %s")
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and pwd_context.verify(password, result["password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"message": "Login successfully", "access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Integrasi Get Token
def authenticationCleaner(username, password):
    url = shoes_cleaner +'authentications/login'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': username,
        'password': password,
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = response.json()
        access_token = result.get('access_token')
        return access_token
    else:
        return{'Error:', response.status_code, response.text}

# Registration endpoint
@auth.post("/register", tags=["Authentication"])
async def register(fullname: str = Form(...), username: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(default="user")):
    # Check sudah ada belum
    query = ("SELECT * FROM users WHERE username = %s")
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    if result:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Username already exist")
    
    query = ("SELECT * FROM users WHERE email = %s")
    cursor.execute(query, (email,))
    result = cursor.fetchall()
    if result:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email already exist")
    hashed_password = pwd_context.hash(password)

    # Register Consultant

    # Register Shoes Cleaner
    urlCleaner = shoes_cleaner +'users/users'
    headersCleaner = {
        'accept': 'application/json'
    }
    paramsCleaner = {
        'firstname': fullname,
        'lastname': fullname,
        'phonenumber': '0000000',
        'address': 'Ini buat ardhan',
        'email': email,
        'password': password,
        'username': username,
        'role': 'Admin'
    }
    responseCleaner = requests.post(urlCleaner, headers=headersCleaner, params=paramsCleaner)

    if responseCleaner.status_code == 200:
        query = "INSERT INTO users (fullname, username, email, password, role, cleaning_token) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (fullname, username, email, hashed_password, role, authenticationCleaner(username, password),))
        conn.commit()
        cursor.close()
        conn.close()
        return {
                "code": 200,
                "messages" : "Register successfully",
                "data" : {
                    "fullname" : fullname,
                    "username" : username,
                    "email" : email,
                }
        }
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Register to Shoe Wizards Co. failed")

# Protected endpoint
@auth.get("/users/me", tags=["Authentication"])
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
