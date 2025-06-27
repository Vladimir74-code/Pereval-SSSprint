from fastapi import FastAPI, HTTPException
from .db_manager import DBManager
import json

app = FastAPI()

# Инициализация объекта для работы с базой данных
db = DBManager()

# Обработчик POST-запроса для добавления данных о перевале
@app.post("/submitData")
async def submit_data(data: dict):
    # Проверка наличия обязательных полей
    required_fields = ['title', 'user', 'coords', 'add_time']
    if not all(field in data for field in required_fields):
        raise HTTPException(status_code=400, detail="Отсутствуют обязательные поля")

    # Извлечение данных об уровнях сложности
    level_data = data.get('level', {})
    winter = level_data.get('winter', '')
    summer = level_data.get('summer', '')
    autumn = level_data.get('autumn', '')
    spring = level_data.get('spring', '')

    # Обновление данных для вставки
    data_with_levels = data.copy()
    data_with_levels.update({
        'winter': winter,
        'summer': summer,
        'autumn': autumn,
        'spring': spring
    })

    # Вызов метода добавления и обработка результата
    result = db.add_pereval(data_with_levels)

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