from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_history_endpoint_is_alive():
    response = client.get("/api/v1/prices/all")

    assert response.status_code == 200


def test_history_data_format():
    response = client.get("/api/v1/prices/all")
    data = response.json()['message']

    assert isinstance(data, list)

    if len(data) > 0:
        first_item = data[0]
        assert "price" in first_item
        assert "sma_10" in first_item
        assert "created_at" in first_item