from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import cursor, conn
from middleware.jwt import check_is_admin, check_is_login
from models.varian import Varian

varian = APIRouter()

@varian.get('/varian')
async def read_data(check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    query = "SELECT * FROM varians;"
    cursor.execute(query)
    data = cursor.fetchall()
    return {
        "code": 200,
        "messages" : "Get All Varians successfully",
        "data" : data
    }

@varian.get('/varian/{id}')
async def read_data(id: int, check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    select_query = "SELECT * FROM varians WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data varian id {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get Varian successfully",
        "data" : data
    }

@varian.post('/varian')
async def write_data(varian: Varian, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    varian_json = varian.model_dump()
    select_query = "SELECT * FROM shoes WHERE id = %s;"
    cursor.execute(select_query, (varian_json["shoes_id"],))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shoes id {varian_json['shoes_id']} Not Found")
    
    query = "INSERT INTO varians(shoes_id, virtual_url, color) VALUES(%s, %s, %s);"
    cursor.execute(query, (varian_json["shoes_id"], varian_json['virtual_url'], varian_json['color'],))
    conn.commit()

    select_query = "SELECT * FROM varians WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_varian = cursor.fetchone()

    return {
        "code": 200,
        "messages" : "Add Varian successfully",
        "data" : new_varian
    }
    
@varian.put('/varian/{id}')
async def update_data(varian: Varian, id:int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    varian_json = varian.model_dump()
    select_query = "SELECT * FROM varians WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data varian id {id} Not Found")
    
    query = "UPDATE varians SET shoes_id=%s, virtual_url=%s, color=%s WHERE varians.id = %s;"
    cursor.execute(query, (varian_json["shoes_id"], varian_json['virtual_url'], varian_json['color'], id,))
    conn.commit()

    select_query = "SELECT * FROM varians WHERE varians.id = %s;"
    cursor.execute(select_query, (id,))
    new_varian = cursor.fetchone()
    
    return {
        "code": 200,
        "messages" : "Update Varian successfully",
        "data" : new_varian
    }

@varian.delete('/varian/{id}')
async def delete_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM varians WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail=f"Data varian id {id} Not Found")
    
    query = "DELETE FROM varians WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    return {
        "code": 200,
        "messages" : "Delete Varian successfully",
    }