from fastapi import APIRouter, HTTPException
from db.connection import cursor, conn
from models.shoes import Shoes

shoes = APIRouter()

@shoes.get('/shoes')
async def read_data():
    query = "SELECT * FROM shoes;"
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

    return {
        "code": 200,
        "messages" : "Get All Shoes successfully",
        "data" : data
    }

@shoes.get('/shoes/{id}')
async def read_data(id: int):
    select_query = "SELECT * FROM shoes WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail=f"Data shoes id {id} Not Found")

    query = "SELECT * FROM varians WHERE shoes_id = %s;"
    cursor.execute(query, (data["id"],))
    data_varians = cursor.fetchall()
    data["varians"] = data_varians 

    query = "SELECT * FROM brands WHERE id = %s;"
    cursor.execute(query, (data["brand_id"],))
    data_varians = cursor.fetchone()
    data["brand"] = data_varians 
    
    return {
        "code": 200,
        "messages" : "Get Shoes successfully",
        "data" : data
    }

@shoes.post('/shoes')
async def write_data(shoes: Shoes):
    shoes_json = shoes.model_dump()
    select_query = "SELECT * FROM brands WHERE id = %s;"
    cursor.execute(select_query, (shoes_json["brand_id"],))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail=f"Brand id {shoes_json['brand_id']} Not Found")

    query = "INSERT INTO shoes(brand_id, name, category, stock) VALUES(%s, %s, %s, %s);"
    cursor.execute(query, (shoes_json["brand_id"], shoes_json["name"], shoes_json["category"], shoes_json["stock"],))
    conn.commit()

    select_query = "SELECT * FROM shoes WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_shoes = cursor.fetchone()

    return {
        "code": 200,
        "messages" : "Add Shoes successfully",
        "data" : new_shoes
    }
    
@shoes.put('/shoes/{id}')
async def update_data(shoes: Shoes, id:int):
    shoes_json = shoes.model_dump()
    select_query = "SELECT * FROM shoes WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail=f"Data shoes id {id} Not Found")
    
    query = "UPDATE shoes SET brand_id=%s, name=%s, category=%s, stock=%s WHERE shoes.id = %s;"
    cursor.execute(query, (shoes_json["brand_id"], shoes_json["name"], shoes_json["category"], shoes_json["stock"], id,))
    conn.commit()

    select_query = "SELECT * FROM shoes WHERE shoes.id = %s;"
    cursor.execute(select_query, (id,))
    new_shoes = cursor.fetchone()
    
    return {
        "code": 200,
        "messages" : "Update Brand successfully",
        "data" : new_shoes
    }

@shoes.delete('/shoes/{id}')
async def delete_data(id: int):
    select_query = "SELECT * FROM shoes WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail=f"Data shoes id {id} Not Found")
    
    query = "DELETE FROM shoes WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    return {
        "code": 200,
        "messages" : "Delete Shoes successfully",
    }