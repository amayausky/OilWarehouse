import datetime

from flask import Flask, make_response, jsonify
from flask.ext.restful import Api, Resource, reqparse, fields, marshal_with
# noinspection PyPackageRequirements
# needs: pip install python-simplexml
from simplexml import dumps

app = Flask(__name__, static_url_path='')
api = Api(app)


class NotFoundException(Exception):
    status_code = 404

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        return {'Error': '%s %s' % (self.status_code, self.message)}


@api.representation('application/xml')
def xml(data, code, headers=None):
    response = make_response(dumps({'response': data}), code)
    response.headers.extend(headers or {})
    return response


@app.errorhandler(NotFoundException)
def handle_not_found_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

barrel_fields = {
    'SerialNumber': fields.String(attribute="serial_number"),
    'InspectionDate': fields.DateTime(attribute="inspection_date")
}


class Barrel(object):
    def __init__(self, barrel_id, serial_number):
        self.barrel_id = barrel_id
        self.serial_number = serial_number
        self.inspection_date = datetime.datetime.now()


barrels = [
    Barrel(1, '001')
]


class BarrelListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('SerialNumber', required=True, type=str, dest='serial_number')
        super(BarrelListAPI, self).__init__()

    @marshal_with(barrel_fields)
    def post(self):
        args = self.reqparse.parse_args()
        new_id = barrels[-1].barrel_id + 1
        new_barrel = Barrel(new_id, args['serial_number'])
        barrels.append(new_barrel)
        return new_barrel, 201


class BarrelAPI(Resource):
    @marshal_with(barrel_fields)
    def get(self, barrel_id):
        barrel = [b for b in barrels if b.barrel_id == barrel_id]
        if len(barrel) == 0:
            raise NotFoundException('No barrel with ID %s exists' % barrel_id)
        return barrel[0]

api.add_resource(BarrelListAPI, '/barrels', endpoint='barrels')
api.add_resource(BarrelAPI, '/barrels/<int:barrel_id>', endpoint='barrel')

if __name__ == "__main__":
    app.run(debug=True)
