import datetime

from flask import Flask, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal_with

app = Flask(__name__, static_url_path='')
api = Api(app)

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
    Barrel(1, '001'),
    Barrel(2, '002')
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
            abort(404)
        return barrel[0]

api.add_resource(BarrelListAPI, '/barrels', endpoint='barrels')
api.add_resource(BarrelAPI, '/barrels/<int:barrel_id>', endpoint='barrel')

if __name__ == "__main__":
    app.run(debug=True)
