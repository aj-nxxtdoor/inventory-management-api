import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    with app.test_client() as client:
        yield client
        with app.app_context():
            db.drop_all()


def test_get_items_empty(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_item(client):
    response = client.post('/items', json={
        'name': 'Test Item',
        'barcode': '1234567890',
        'category': 'Test Category',
        'quantity': 10,
        'price': 9.99
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Item'
    assert data['quantity'] == 10


def test_create_item_missing_name(client):
    response = client.post('/items', json={
        'quantity': 5
    })
    assert response.status_code == 400


def test_get_single_item(client):
    create_response = client.post('/items', json={'name': 'Widget', 'quantity': 3})
    item_id = create_response.get_json()['id']

    response = client.get(f'/items/{item_id}')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Widget'


def test_get_item_not_found(client):
    response = client.get('/items/999')
    assert response.status_code == 404


def test_update_item(client):
    create_response = client.post('/items', json={'name': 'Gadget', 'quantity': 1})
    item_id = create_response.get_json()['id']

    response = client.patch(f'/items/{item_id}', json={'quantity': 50})
    assert response.status_code == 200
    assert response.get_json()['quantity'] == 50


def test_update_item_not_found(client):
    response = client.patch('/items/999', json={'quantity': 5})
    assert response.status_code == 404


def test_delete_item(client):
    create_response = client.post('/items', json={'name': 'ToDelete', 'quantity': 1})
    item_id = create_response.get_json()['id']

    response = client.delete(f'/items/{item_id}')
    assert response.status_code == 200

    get_response = client.get(f'/items/{item_id}')
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete('/items/999')
    assert response.status_code == 404


def test_external_barcode_lookup(client):
    response = client.get('/external/barcode/3017620422003')
    assert response.status_code == 200
    data = response.get_json()
    assert 'name' in data


def test_import_item_missing_barcode(client):
    response = client.post('/items/import', json={})
    assert response.status_code == 400