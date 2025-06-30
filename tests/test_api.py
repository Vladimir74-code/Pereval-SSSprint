import pytest
from pereval_app.db_manager import DBManager
from pereval_app.api import app
import asyncio
import httpx

# Тест для DBManager
@pytest.fixture
def db():
    return DBManager()

def test_add_pereval(db):
    data = {
        "beauty_title": "пер. Тест",
        "title": "Тест",
        "other_titles": "",
        "connect": "",
        "add_time": "2025-06-30 07:00:00",
        "user": {"email": "test@mail.ru", "fam": "Тестов", "name": "Тест", "otc": "", "phone": "+799999999"},
        "coords": {"latitude": "45.0", "longitude": "7.0", "height": 1000},
        "images": [{"data": "<test>", "title": "Тестовая"}]
    }
    result = db.add_pereval(data)
    assert result["status"] == 200
    assert "id" in result

# Тест для API
from fastapi.testclient import TestClient

# Тест для API
@pytest.mark.asyncio
async def test_api_endpoints():
    with TestClient(app) as client:
        # Тест POST
        response = client.post("/submitData", json={
            "beauty_title": "пер. API Тест",
            "title": "API Тест",
            "add_time": "2025-06-30 07:00:00",
            "user": {"email": "api@test.ru", "fam": "API", "name": "Тест", "otc": "", "phone": "+788888888"},
            "coords": {"latitude": "46.0", "longitude": "8.0", "height": 1100}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200

        # Тест GET
        id = data["id"]
        response = client.get(f"/submitData/{id}")
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "new"
        assert "images" in result  # Проверяем, что поле есть, даже если пустое

if __name__ == "__main__":
    asyncio.run(test_api_endpoints())