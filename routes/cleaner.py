import json
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
import requests
from middleware.jwt import get_current_user
from api.url import shoes_cleaner

cleaner = APIRouter()

@cleaner.post('/cleaner', tags=["Cleaner"])
async def consultation_cleaner(current_user: Annotated[dict, Depends(get_current_user)], shoetype: str = Form(...), shoesize: str = Form(...), shoecolor: str = Form(...), shoebrand: str = Form(...), initialcondition: str = Form(...)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = current_user['data']['cleaning_token']
    url = shoes_cleaner +'shoes/shoes'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    params = {
        'shoetype': shoetype,
        'shoesize': shoesize,
        'shoecolor': shoecolor,
        'shoebrand': shoebrand,
        'initialcondition': initialcondition,
    }
    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:
        shoes_id = response.text.split(" ")[2]
        return {
            "code": 200,
            "messages" : "Get Cleaners Consultation successfully",
            "data" : shoes_id
        }
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Add shoes to Shoe Wizards Co. failed")