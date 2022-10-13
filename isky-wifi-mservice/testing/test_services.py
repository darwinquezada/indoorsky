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


def test_add_wifi_fingerprint(client: FlaskClient):
    data = {
            "bssid": "00:00:00:00:00",
            "fingerprint_id": "123-123-123-123-123",
            "rssi": "-12",
            "ssid": "Test"
            }
    resp = client.post(
        '/api/v1/wifi', json=data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'

def test_get_wifi_by_id(client: FlaskClient):
    data = "4737fc6d-ee76-42c0-94a5-f5115b56e9eb"
    resp = client.get(
        '/api/v1/wifi/'+data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["id"] == data
    
def test_get_wifi_by_fingerprint_id(client: FlaskClient):
    data = "01"
    resp = client.get(
        '/api/v1/wifi/fingerprint/'+data)

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200

def test_delete_wifi_by_id(client: FlaskClient):
    data = "ae799299-6e6e-4947-b20f-12526aa0d20a"
    resp = client.delete(
        '/api/v1/wifi/'+data+'/delete')

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'


def test_delete_wifi_by_fingerprint_id(client: FlaskClient):
    data = "03"
    resp = client.delete(
        '/api/v1/wifi/fingerprint/'+data+'/delete')

    data_resp = json.loads(resp.get_data(as_text=True))

    assert resp.status_code == 200
    assert data_resp["message"] == 'Success!'

