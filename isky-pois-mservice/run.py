# run.py
import os
import logging
from application import create_app
from application.presentation import app
from dotenv import load_dotenv

log=logging.getLogger(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

config_name = os.environ['CONFIGURATION_SETUP']

app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
