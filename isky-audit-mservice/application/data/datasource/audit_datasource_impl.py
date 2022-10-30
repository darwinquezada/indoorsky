import json
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.audit_datasource import IAuditDatasource
from flask import jsonify, g, Response
from application.core.exceptions.status_codes import CreatedResponseCode, InternalServerErrorResponseCode

r = RethinkDB()

class AuditDatasourceImpl(IAuditDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name

    def insert_audit(self, data: json) -> dict:
        """
        Insert logs to the audit dataset
        :param data: information (JSON format)
        :return: 200 or error
        """
        try:
            insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
            return CreatedResponseCode()

        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)

    def get_audit_by_user_id(self, user_id: str) -> dict:
        """
        Get logs by user ID
        :param user_id: User ID (uuid)
        :return: JSON with the user information
        """
        try:
            # Get information from the dataset
            audit = r.db(self.database_name).table(self.table_name).filter({"user_id": user_id}).run(g.rdb_conn)
            # Convert stream to list
            list_audit = list(audit)
            # Close the database connection
            audit.close()

            # Return an empty json
            if audit==None or audit=="null":
                return jsonify({[]})
            
            return Response(json.dumps(list_audit), mimetype='application/json')
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
