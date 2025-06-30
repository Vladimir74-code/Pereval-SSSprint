from fastapi import FastAPI, HTTPException
from .db_manager import DBManager

app = FastAPI(title="Pereval API", description="API для управления данными о перевалах", version="1.0.0")
db = DBManager()

@app.post("/submitData", summary="Добавить новую запись о перевале")
async def submit_data(data: dict):
    required_fields = ['title', 'user', 'coords', 'add_time']
    if not all(field in data for field in required_fields):
        raise HTTPException(status_code=400, detail="Отсутствуют обязательные поля")
    result = db.add_pereval(data)
    if result['status'] == 500:
        raise HTTPException(status_code=500, detail=result['message'])
    return {"status": 200, "message": "Отправлено успешно", "id": result['id']}

@app.get("/submitData/{id}", summary="Получить запись по ID")
async def get_pereval(id: int):
    result = db.get_pereval(id)
    if result:
        images = result[15] if result[15] else []
        return {
            "id": result[0], "beauty_title": result[1], "title": result[2], "other_titles": result[3],
            "connect": result[4], "add_time": result[5], "status": result[6],
            "coords": {"latitude": result[7], "longitude": result[8], "height": result[9]},
            "user": {"email": result[10], "fam": result[11], "name": result[12], "otc": result[13], "phone": result[14]},
            "images": [{"data": img.split('|')[0], "title": img.split('|')[1]} for img in images] if images else []
        }
    raise HTTPException(status_code=404, detail="Перевал не найден")

@app.patch("/submitData/{id}", summary="Редактировать запись")
async def update_pereval(id: int, data: dict):
    result = db.update_pereval(id, data)
    if result['state'] == 0:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.get("/submitData/", summary="Получить список записей по email")
async def get_perevals_by_email(user__email: str):
    results = db.get_perevals_by_email(user__email)
    if results:
        return [
            {
                "id": row[0], "beauty_title": row[1], "title": row[2], "other_titles": row[3],
                "connect": row[4], "add_time": row[5], "status": row[6],
                "coords": {"latitude": row[7], "longitude": row[8], "height": row[9]},
                "user": {"email": row[10], "fam": row[11], "name": row[12], "otc": row[13], "phone": row[14]},
                "images": [{"data": img.split('|')[0], "title": img.split('|')[1]} for img in (row[15] if row[15] else [])]
            } for row in results
        ]
    raise HTTPException(status_code=404, detail="Перевалы для данного email не найдены")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)