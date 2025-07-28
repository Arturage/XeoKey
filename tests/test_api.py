import json
from app import app


def test_create_and_get_service():
    client = app.test_client()

    # Create service
    response = client.post('/services', json={'name': 'Servicio A', 'description': 'Test'})
    assert response.status_code == 201
    data = response.get_json()
    service_id = data['id']

    # Get list should contain service
    response = client.get('/services')
    assert response.status_code == 200
    assert any(s['id'] == service_id for s in response.get_json())

    # Get single service
    response = client.get(f'/services/{service_id}')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Servicio A'



def test_update_and_delete_service():
    client = app.test_client()

    # Create service
    response = client.post('/services', json={'name': 'Servicio B'})
    assert response.status_code == 201
    data = response.get_json()
    service_id = data['id']

    # Update service
    response = client.put(f'/services/{service_id}', json={'name': 'Servicio B2'})
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Servicio B2'

    # Delete service
    response = client.delete(f'/services/{service_id}')
    assert response.status_code == 204

    # Ensure deletion
    response = client.get(f'/services/{service_id}')
    assert response.status_code == 404
