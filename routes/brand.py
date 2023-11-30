from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import cursor, conn
from middleware.jwt import check_is_admin, check_is_login
from models.brand import Brand

brand = APIRouter()

@brand.get('/brand', tags=["User"])
async def read_data(check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    query = "SELECT * FROM brands;"
    cursor.execute(query)
    data = cursor.fetchall()
    return {
        "code": 200,
        "messages" : "Get All Brands successfully",
        "data" : data
    }

@brand.get('/brand/{id}', tags=["User"])
async def read_data(id: int, check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    select_query = "SELECT * FROM brands WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data brand id {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get Brand successfully",
        "data" : data
    }

@brand.post('/brand', tags=["Admin"])
async def write_data(brand: Brand, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    brand_json = brand.model_dump()
    query = "INSERT INTO brands(name) VALUES(%s);"
    cursor.execute(query, (brand_json["name"],))
    conn.commit()

    select_query = "SELECT * FROM brands WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_brand = cursor.fetchone()

    return {
        "code": 200,
        "messages" : "Add Brand successfully",
        "data" : new_brand
    }
    
@brand.put('/brand/{id}', tags=["Admin"])
async def update_data(brand: Brand, id:int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    brand_json = brand.model_dump()
    select_query = "SELECT * FROM brands WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data brand id {id} Not Found")
    
    query = "UPDATE brands SET name = %s WHERE brands.id = %s;"
    cursor.execute(query, (brand_json["name"], id,))
    conn.commit()

    select_query = "SELECT * FROM brands WHERE brands.id = %s;"
    cursor.execute(select_query, (id,))
    new_brand = cursor.fetchone()
    
    return {
        "code": 200,
        "messages" : "Update Brand successfully",
        "data" : new_brand
    }

@brand.delete('/brand/{id}', tags=["Admin"])
async def delete_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM brands WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data brand id {id} Not Found")
    
    query = "DELETE FROM brands WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    return {
        "code": 200,
        "messages" : "Delete Brand successfully",
    }