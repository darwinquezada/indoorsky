# config.py
import os
from dotenv import load_dotenv

# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = ":9B~PG6a)Y]&?!k=8tAVS*^atgb7D9$ZV4[8(y8Zj"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    
class TestingConfig(Config):
    ENV = "testing"
    DEBUG = True
   
class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
   
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}