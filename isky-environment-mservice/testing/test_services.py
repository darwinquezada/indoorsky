import pytest
import os
from flask.testing import FlaskClient
from application import create_app
from application.presentation import app
from dotenv import load_dotenv
from flask import  json


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

config_name = os.environ['CONFIGURATION_SETUP']

app = create_app(config_name)


@pytest.fixture
def client():
    return app.test_client()


def test_insert_environment(client: FlaskClient):
    data = {
            "name": 'TUT4',
            "address": 'Tampere001',
            "num_buildings": 1,
            "is_public": True,
            "is_active": True
            }
    resp = client.post(
        '/api/v1/environment', json=data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'

def test_get_environments(client: FlaskClient):
    resp = client.get(
        '/api/v1/environment')

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    
def test_get_environment_by_id(client: FlaskClient):
    id = '0bf1e58f-bf56-4b08-a226-4e9d741a4df5'
    resp = client.get(
        '/api/v1/environment/' + id)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["id"] == id
    
def test_get_environment_by_name(client: FlaskClient):
    name = "UJI"
    resp = client.get(
        '/api/v1/environment/' + name + '/name')

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200

def test_delete_environment_by_id(client: FlaskClient):
    id = "3bb747a7-c572-495a-8813-bc149ca09a58"
    resp = client.delete(
        '/api/v1/environment/'+ id +'/delete')

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'


def test_update_environment(client: FlaskClient):
    id = "c32638bb-b80f-4b47-ab10-ad899894777d"
    data = {
            "address": "Finland",
            "is_active": True,
            "is_public": True,
            "name": "UJI",
            "num_buildings": 4
            }
    resp = client.put(
        '/api/v1/environment/'+id+'/update', json=data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'