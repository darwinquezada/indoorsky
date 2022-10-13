# run.py
import os
import logging
from application import create_app
from application.presentation.endpoints import app
from dotenv import load_dotenv

log=logging.getLogger(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

config_name = os.environ['CONFIGURATION_SETUP']

app = create_app(config_name)
context = (os.path.join(os.getcwd(),'certs','cert.pem'),
           os.path.join(os.getcwd(),'certs','privkey.pem'))

context = ('/etc/letsencrypt/live/insky.cloud/cert.pem', '/etc/letsencrypt/live/insky.cloud/privkey.pem')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, ssl_context=context, threaded=True, debug=True)