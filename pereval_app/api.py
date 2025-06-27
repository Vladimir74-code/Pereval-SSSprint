from fastapi import FastAPI, HTTPException
from .db_manager import DBManager
import json

app = FastAPI()

# Инициализация класса для работы с БД
db = DBManager()

@app.post("/submitData")
async def submit_data(data: dict):
    # Проверяем, все ли обязательные поля есть
    required_fields = ['title', 'user', 'coords', 'add_time']
    if not all(field in data for field in required_fields):
        raise HTTPException(status_code=400, detail="Отсутствуют обязательные поля")

    # Вызываем метод для добавления данных
    result = db.add_pereval(data)

    # Возвращаем результат
    if result['status'] == 500:
        raise HTTPException(status_code=500, detail=result['message'])
    elif result['status'] == 200:
        return {"status": 200, "message": "Отправлено успешно", "id": result['id']}
    else:
        raise HTTPException(status_code=400, detail="Некорректные данные")

# Пример запуска (для теста)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)