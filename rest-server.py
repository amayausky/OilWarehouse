import datetime
from flask import Flask, url_for, jsonify, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__, static_url_path='')
api = Api(app)

barrels = [
    {
        'id': 1,
        'SerialNumber': '001',
        'InspectionDate': '10:36AM on July 23, 2010'
    },
    {
        'id': 2,
        'SerialNumber': '002',
        'InspectionDate': '10:36AM on July 23, 2010'
    }
]

barrel_fields = {
    'SerialNumber': fields.String,
    'InspectionDate': fields.String
}


class BarrelAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('SerialNumber', type=str, location='json')
        super(BarrelAPI, self).__init__()

    def _get_current_date(self):
        return datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")


    def post(self):
        args - self.reqparse.parse_args()
        barrel = {
            'id': barrels[-1]['id'] + 1,
            'SerialNumber': args['SerialNumber'],
            'InspectionDate': self._get_current_date()
        }
        barrels.append(barrel)
        return {'barrel': marshal(barrel, barrel_fields)}, 201

    def get(self, id):
        print 'getting...'
        barrel = filter(lambda b: b['id'] == id, barrels)
        print str(barrel)
        if not barrel:
            abort(404)
        return {'barrel': marshal(barrel, barrel_fields)}

api.add_resource(BarrelAPI, '/barrels/<int:id>', endpoint='barrel')


if __name__ == "__main__":
    app.run(debug=True)
