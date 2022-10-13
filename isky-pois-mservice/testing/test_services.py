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


def test_insert_poi(client: FlaskClient):
    data = {
            "altitude": 12.0,
            "description": "Test POI 005",
            "floor_id": "aa:aa:aa:aa:aa",
            "image": "",
            "is_active": True,
            "is_public": True,
            "latitude": 23.0,
            "longitude": 34.0,
            "name": "Test POI 005",
            "pos_x": 1.0,
            "pos_y": 1.2,
            "pos_z": 1.3
            }
    resp = client.post(
        '/api/v1/poi', json=data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'

def test_get_poi_by_id(client: FlaskClient):
    data = "075b9927-bdf4-449b-ade7-18d5f5fa70d8"
    resp = client.get(
        '/api/v1/poi/'+data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["id"] == data
    
def test_get_poi_by_name(client: FlaskClient):
    data = "Test POI"
    resp = client.get(
        '/api/v1/poi/'+data+'/name')

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200

def test_delete_poi_by_id(client: FlaskClient):
    data = "2d2a443d-9197-4100-a12a-77150ee6788f"
    resp = client.delete(
        '/api/v1/poi/'+data+'/delete')

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'


def test_update_poi(client: FlaskClient):
    id = "9b152700-09d3-4b23-9d0b-20662a472fc6"
    data = {
            "altitude": 12.0,
            "description": "Test POI 010",
            "floor_id": "aa:aa:aa:aa:aa",
            "image": "",
            "is_active": True,
            "is_public": True,
            "latitude": 23.0,
            "longitude": 34.0,
            "name": "Test POI010",
            "pos_x": 1.0,
            "pos_y": 1.2,
            "pos_z": 1.3
            }
    resp = client.put(
        '/api/v1/poi/'+ id +'/update', json=data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'

