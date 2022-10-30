#!/usr/bin/python
from asyncio import sleep
import os
from appwrite.exception import AppwriteException
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage

from dotenv import load_dotenv

### Warning ###
import warnings
from flask import jsonify

warnings.filterwarnings('ignore')

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)


client = Client()
client.set_endpoint(os.environ['APPWRITEENDPOINT'])
client.set_project(os.environ['APPWRITEPROJECTID'])
client.set_key(os.environ['APPWRITEAPIKEY'])


database_id = os.environ['RDB_DB']
bucket_preproc_id = os.environ['TABLE_FILE']
dataset_id = os.environ['TABLE_DATASET']
data_model_id = os.environ['TABLE_DATA_MODEL']
model_id = os.environ['TABLE_MODEL']
 
def is_database_available():
    try:
        global database_id
        databases = Databases(client=client)
        response = databases.list()
        list_databases = []
        for database in response['databases']:
            list_databases.append(database['$id'])
        
        if os.environ['RDB_DB'] in list_databases:
            return True
        return False
    except AppwriteException as e:
        print({'code':501, 'message':e.message})
 
def create_appwrite_db():
    try:
        global database_id
        databases = Databases(client)
        response = databases.create(database_id, os.environ['RDB_DB'])
        database_id = response['$id']
    except AppwriteException as e:
        print({'code':501, 'message':e.message})

def create_collection_model():
    try: 
        global database_id
        databases = Databases(client)
        
        response = databases.create_collection(database_id=database_id,
                                               collection_id=model_id,
                                               name=model_id)
        
        # ID Data model
        response = databases.create_string_attribute(
            database_id=database_id,
            collection_id=model_id,
            key='data_model_id',
            size=40,
            required=True,
        )
        # Parameter
        response = databases.create_string_attribute(
            database_id=database_id,
            collection_id=model_id,
            key='model',
            size=20,
            required=True,
        )
        # Value
        response = databases.create_string_attribute(
            database_id=database_id,
            collection_id=model_id,
            key='model_type',
            size=20,
            required=True,
        )
        # Value
        response = databases.create_string_attribute(
            database_id=database_id,
            collection_id=model_id,
            key='pos_tech_id',
            size=40,
            required=True,
        )
        sleep(2)
        # Create Index data model ID
        response = databases.create_index(
            database_id=database_id,
            collection_id=model_id,
            key='data_model_id',
            type="fulltext",
            attributes=['data_model_id']
        )
        # Create index model
        response = databases.create_index(
            database_id=database_id,
            collection_id=model_id,
            key='model',
            type="fulltext",
            attributes=['model']
        )
        # Create index model type
        response = databases.create_index(
            database_id=database_id,
            collection_id=model_id,
            key='model_type',
            type="fulltext",
            attributes=['model_type']
        )
        # Create index 
        response = databases.create_index(
            database_id=database_id,
            collection_id=model_id,
            key='pos_tech_id',
            type="fulltext",
            attributes=['pos_tech_id']
        )
        
        # Create index 
        response = databases.create_index(
            database_id=database_id,
            collection_id=model_id,
            key='full_index',
            type="fulltext",
            attributes=['model','model_type', 'data_model_id', 'pos_tech_id']
        )
    except AppwriteException as e:
        print({'code':501, 'message':e.message})


def is_collection_available(collection_name: str) -> bool:
    try:
        databases = Databases(client)
        collections = databases.list_collections(database_id)
        list_collections = []
        for collection in collections['collections']:
            list_collections.append(collection['$id'])
            
        if collection_name in list_collections:
            return True
        return False
    except AppwriteException as e:
        print({'code':501, 'message':e.message})
    
    
if __name__ == '__main__':
    # Instances
    databases = Databases(client)
    storage = Storage(client)
    
    # Create a temporal directory to store files
    temp_path = os.path.join(os.getcwd(), 'application', 'models')
    
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    
    # Verify if the database exist
    is_db_available = is_database_available()
    if not is_db_available:
        create_appwrite_db()
        
    # Verify is the data cleansing collection exist
    collection_model = is_collection_available(model_id)
    if not collection_model:
        create_collection_model()

        
    