from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
	r = client.get("/health")
	assert r.status_code == 200
	assert r.json() == {"status": "ok"}

def test_generate_recipe():
	payload = {"prompt": "I have chicken and garlic"}
	r = client.post("/api/v1/generate-recipe", json=payload)
	assert r.status_code == 200
	data = r.json()
	assert "recipes" in data
	assert isinstance(data["recipes"], list)
