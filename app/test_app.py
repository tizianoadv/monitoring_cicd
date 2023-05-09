import json
import pytest
from app import MonitoringApp

@pytest.fixture
def app():
    yield MonitoringApp().app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_flush_db(client):
    response = client.get('/flush')
    assert response.status_code == 200
    assert response.json == {'message': 'DB flush successfully.'}

# def test_post_data(client):
#     data = {
#         'temperature': 20,
#         'humidity': 60,
#         'luminosity': 500,
#         'timestamp': '2022-01-01T00:00:00Z'
#     }
#     response = client.post('/data', json=data)
#     assert response.status_code == 200
#     assert response.json == {'message': 'Data stored successfully.'}

# def test_get_data(client):
#     response = client.get('/data')
#     assert response.status_code == 200
#     assert isinstance(response.data, bytes)
