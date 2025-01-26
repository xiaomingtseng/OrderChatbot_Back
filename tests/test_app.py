import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import pytest
import json

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == 'Index Page'

def test_view_cart(client):
    response = client.get('/cart')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_add_to_cart(client):
    item = {'name': 'apple', 'quantity': 3}
    response = client.post('/cart', json=item)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data == item