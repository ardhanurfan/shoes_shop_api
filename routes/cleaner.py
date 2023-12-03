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
    responseSepatu = requests.post(url, headers=headers, params=params)

    if responseSepatu.status_code == 200:
        shoes_id = responseSepatu.text.split(" ")[2]

        url = shoes_cleaner +'authentications/current_user'
        responseUser = requests.post(url, headers=headers)

        if responseUser.status_code == 200:
            userid = responseUser.json()[0]

            # Consultations
            url = shoes_cleaner +'consultations/consultations'
            params = {
                'shoeid': int(shoes_id),
                'userid': userid,
            }
            requests.post(url, headers=headers, params=params)
            responseConsult = requests.get(url, headers=headers, params=params)

            if responseConsult.status_code == 200:
                return {
                    "code": 200,
                    "messages" : "Get Cleaners Consultation successfully",
                    "data" : responseConsult
                }
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Get consultations on Shoe Wizards Co. failed")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Get user on Shoe Wizards Co. failed")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Add shoes to Shoe Wizards Co. failed")
