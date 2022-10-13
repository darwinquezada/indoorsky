import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import time

from pydoc import describe
from . import positioning_tag, api_positioning
from application.core.decorators.jwt_manager import login_required
from application.presentation.data_injection.injection_container import ApplicationContainer
from flask import jsonify,g,abort
# Environment request body
from application.presentation.req_body.position_body import ListPositionBody

@api_positioning.post('/position', tags=[positioning_tag])
# @login_required
def insert_poi(body: ListPositionBody):
        # insert_environment_use_case = InsertPoiUseCase(poi_repository=ApplicationContainer.poi_repository())
        print(body.json)
        data = {
                "latitude": 39.992846,
                "longitude": -0.068626,
                "altitude": 0,
                "building": 'UJI-IT',
                "floor": '2',
                "environment": 'UJI'
                }
        time.sleep(0.5)
        # return insert_environment_use_case.execute(data)
        return jsonify(data)
