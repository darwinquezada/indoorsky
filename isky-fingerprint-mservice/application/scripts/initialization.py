#!/usr/bin/python
import os
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import abort, jsonify, Response

r = RethinkDB()

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

HOST = os.environ['RDB_HOST']
PORT = os.environ['RDB_PORT']
USER = os.environ['RDB_USER']
PASSWORD = os.environ['RDB_PASSWORD']
DATABASE = os.environ['RDB_DB']
TABLE = os.environ['RDB_TABLE']

r = RethinkDB()

def verify_db(db_conn) -> dict:
    try:
        list_databases = r.db_list().run(db_conn)

        if not DATABASE in list_databases:
            r.db_create(DATABASE).run(db_conn)
            r.db(DATABASE).table_create(TABLE).run(db_conn)
            pass

    except RqlRuntimeError as e:
        print(e.message)
        abort(Response(jsonify({'code':503, 'message': e.message})))

def verify_table(db_conn) -> dict:
    try:
        list_tables = r.db(DATABASE).table_list().run(db_conn)

        if not TABLE in list_tables:
            r.db(DATABASE).table_create(TABLE).run(db_conn)

        list_indexes = r.db(DATABASE).table(TABLE).index_list().run(db_conn)

        if not list_indexes :
            r.db(DATABASE).table(TABLE).index_create("poi_id").run(db_conn)
            r.db(DATABASE).table(TABLE).index_wait("poi_id").run(db_conn)
            pass

    except RqlRuntimeError as e:
        abort(Response(jsonify({'code':503, 'message': e.message})))

def conn():
    try:
        connection = r.connect(host=HOST, port=PORT,
                                user=USER, password=PASSWORD)
        return connection
    except RqlDriverError as e:
        abort(Response(jsonify({'code':503, 'message': e.message})))

if __name__ == '__main__':

    "Create database and/or tables in RethinkDB, if it is required"

    connection = conn()
    # Verify if the database exist.
    verify_db(connection)
    # Verify if the table exist.
    verify_table(connection)
    # Close database connection
    connection.close()
