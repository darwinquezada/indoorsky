#!/usr/bin/python
from importlib.resources import path
import os
import json
from time import sleep
import uuid
from appwrite.exception import AppwriteException
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.input_file import InputFile
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile

from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dotenv import load_dotenv

### Warning ###
import warnings
from flask import jsonify

warnings.filterwarnings("ignore")

dotenv_path = os.path.join(os.getcwd(), ".env")

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

client = Client()
client.set_endpoint(os.environ["APPWRITEENDPOINT"])
client.set_project(os.environ["APPWRITEPROJECTID"])
client.set_key(os.environ["APPWRITEAPIKEY"])


database_id = os.environ["RDB_DB"]
config_preproc_id = os.environ["TABLE_PREPROCESSING"]
bucket_preproc_id = os.environ["TABLE_FILE"]
dataset_id = os.environ["TABLE_DATASET"]


def connection():
    # Database connection RethinkDB
    try:
        conn = r.connect(host=os.environ['RDB_HOST'], port=os.environ['RDB_PORT'],
                        user=os.environ['RDB_USER'],
                        password=os.environ['RDB_PASSWORD'])
        return conn
    except RqlRuntimeError as e:
        return jsonify({"code": "0", "message": e.message})

def verify_rethinkdb():
    try:
        conn = connection()
        list_databases = r.db_list().run(conn)

        if not database_id in list_databases:
            r.db_create(database_id).run(conn)
            pass
    except RqlRuntimeError as e:
        return jsonify({"code": "0", "message": e.message})

def is_database_available():
    try:
        global database_id
        databases_conn = Databases(client=client)
        response = databases_conn.list()
        list_databases = []
        for database in response["databases"]:
            list_databases.append(database["$id"])

        if os.environ["RDB_DB"] in list_databases:
            return True
        return False
    except AppwriteException as e:
        print({"code":501, "message":e.message})

def create_appwrite_db():
    try:
        global database_id
        databases_conn = Databases(client)
        response = databases_conn.create(database_id, os.environ["RDB_DB"])
        database_id = response["$id"]
    except AppwriteException as e:
        print({"code":501, "message":e.message})


def create_collection_data_preprocesing():
    try:
        global database_id, config_preproc_id
        databases_conn = Databases(client)

        response = databases_conn.create_collection(database_id=database_id,
                                               collection_id=config_preproc_id,
                                               name=config_preproc_id)

        # ID
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=config_preproc_id,
            key="id_preprocessing",
            size=40,
            required=True,
        )
        # Parameter
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=config_preproc_id,
            key="parameter",
            size=40,
            required=True,
        )
        # Value
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=config_preproc_id,
            key="value",
            size=40,
            required=False,
        )
        # Type
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=config_preproc_id,
            key="type",
            size=40,
            required=False,
        )
        # Create indexes
        sleep(2)
        response = databases_conn.create_index(
            database_id=database_id,
            collection_id=config_preproc_id,
            key="id_preprocessing",
            type="fulltext",
            attributes=["id_preprocessing"]
        )

        response = databases_conn.create_index(
            database_id=database_id,
            collection_id=config_preproc_id,
            key="value",
            type="fulltext",
            attributes=["value"]
        )
        response = databases_conn.create_index(
            database_id=database_id,
            collection_id=config_preproc_id,
            key="parameter",
            type="fulltext",
            attributes=["parameter"]
        )
    except AppwriteException as e:
        print({"code": "0", "message": e.response})

def create_collection_dataset():
    try:
        global database_id, dataset_id
        databases_conn = Databases(client)

        response = databases_conn.create_collection(database_id=database_id,
                                               collection_id=dataset_id,
                                               name=dataset_id)

        # Name
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=dataset_id,
            key="name",
            size=40,
            required=True,
        )
        # technique
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=dataset_id,
            key="technique",
            size=40,
            required=True,
        )
        # Type
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=dataset_id,
            key="type",
            size=40,
            required=False,
        )
        # Process_ID
        response = databases_conn.create_string_attribute(
            database_id=database_id,
            collection_id=dataset_id,
            key="process_id",
            size=40,
            required=False,
        )
        # Index
        sleep(2)
        response = databases_conn.create_index(
            database_id=database_id,
            collection_id=dataset_id,
            key="name",
            type="fulltext",
            attributes=["name"]
        )
        response = databases_conn.create_index(
            database_id=database_id,
            collection_id=dataset_id,
            key="process_id",
            type="fulltext",
            attributes=["process_id"]
        )
    except AppwriteException as e:
        print({"code": "0", "message": e.response})

def is_collection_available(collection_name: str):
    try:
        global database_id
        databases_conn = Databases(client)
        collections = databases_conn.list_collections(database_id)
        list_collections = []
        for collection in collections["collections"]:
            list_collections.append(collection["$id"])

        if collection_name in list_collections:
            return True
        return False
    except AppwriteException as e:
        print({"code": "0", "message": e.message})


def is_bucket_available():
    try:
        global bucket_preproc_id
        storage = Storage(client)
        buckets = storage.list_buckets()

        list_buckets = []

        for bucket in buckets["buckets"]:
            list_buckets.append(bucket["$id"])

        if bucket_preproc_id in list_buckets:
            return True
        return False

    except AppwriteException as e:
        print({"code": "0", "message": e.message})

def create_bucket():
    try:
        global bucket_preproc_id
        storage = Storage(client)
        result = storage.create_bucket(bucket_preproc_id, bucket_preproc_id, maximum_file_size=30000000)
    except AppwriteException as e:
        print({"code": "0", "message": e.message})


if __name__ == "__main__":
    # Instances
    # databases = Databases(client)
    # storage = Storage(client)

    # Create a temporal directory to store files
    temp_path = os.path.join(os.getcwd(), "application", "temp")

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    # Verify RethinkDB dataset
    verify_rethinkdb()

    # Verify if the database exist
    is_db_available = is_database_available()
    if not is_db_available:
        create_appwrite_db()

    # Verify if the collection exist
    collection_available = is_collection_available(config_preproc_id)
    if not collection_available:
        create_collection_data_preprocesing()

    # Verify is the dataset exist
    collection_dataset = is_collection_available(dataset_id)
    if not collection_dataset:
        create_collection_dataset()

    # Verify if the bucket exist
    bucket_available = is_bucket_available()
    if not bucket_available:
        create_bucket()
