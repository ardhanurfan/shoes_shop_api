from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import connectDB
from middleware.jwt import check_is_admin, check_is_login
from models.shoes import Shoes

shoes = APIRouter()

@shoes.get('/shoes', tags=["User"])
async def read_data(check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    query = "SELECT * FROM shoes;"
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()

    for i in range (0, len(data)):
        query = "SELECT * FROM varians WHERE shoes_id = %s;"
        cursor.execute(query, (data[i]["id"],))
        data_varians = cursor.fetchall()
        data[i]["varians"] = data_varians 

        query = "SELECT * FROM brands WHERE id = %s;"
        cursor.execute(query, (data[i]["brand_id"],))
        data_varians = cursor.fetchone()
        data[i]["brand"] = data_varians 
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Get All Shoes successfully",
        "data" : data
    }

@shoes.get('/shoes/{id}', tags=["User"])
async def read_data(id: int, check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    select_query = "SELECT * FROM shoes WHERE id = %s;"
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()

    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data shoes id {id} Not Found")

    query = "SELECT * FROM varians WHERE shoes_id = %s;"
    cursor.execute(query, (data["id"],))
    data_varians = cursor.fetchall()
    data["varians"] = data_varians 

    query = "SELECT * FROM brands WHERE id = %s;"
    cursor.execute(query, (data["brand_id"],))
    data_varians = cursor.fetchone()
    data["brand"] = data_varians 
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Get Shoes successfully",
        "data" : data
    }

@shoes.post('/shoes', tags=["Admin"])
async def write_data(shoes: Shoes, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    shoes_json = shoes.model_dump()
    select_query = "SELECT * FROM brands WHERE id = %s;"
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_query, (shoes_json["brand_id"],))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand id {shoes_json['brand_id']} Not Found")

    query = "INSERT INTO shoes(brand_id, name, category, stock, price) VALUES(%s, %s, %s, %s, %s);"
    cursor.execute(query, (shoes_json["brand_id"], shoes_json["name"], shoes_json["category"], shoes_json["stock"], shoes_json["price"],))
    conn.commit()

    select_query = "SELECT * FROM shoes WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_shoes = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Add Shoes successfully",
        "data" : new_shoes
    }
    
@shoes.put('/shoes/{id}', tags=["Admin"])
async def update_data(shoes: Shoes, id:int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    shoes_json = shoes.model_dump()
    select_query = "SELECT * FROM shoes WHERE id = %s;"
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data shoes id {id} Not Found")
    
    query = "UPDATE shoes SET brand_id=%s, name=%s, category=%s, stock=%s, price=%s WHERE shoes.id = %s;"
    cursor.execute(query, (shoes_json["brand_id"], shoes_json["name"], shoes_json["category"], shoes_json["stock"], shoes_json["price"], id,))
    conn.commit()

    select_query = "SELECT * FROM shoes WHERE shoes.id = %s;"
    cursor.execute(select_query, (id,))
    new_shoes = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Update Brand successfully",
        "data" : new_shoes
    }

@shoes.delete('/shoes/{id}', tags=["Admin"])
async def delete_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM shoes WHERE id = %s;"
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data shoes id {id} Not Found")
    
    query = "DELETE FROM shoes WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Delete Shoes successfully",
    }