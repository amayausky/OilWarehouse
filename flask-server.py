__author__ = 'amayausky'

from flask import Flask, jsonify, make_response, request, url_for
# noinspection PyPackageRequirements
# needs: pip install python-simplexml
from simplexml import dumps


class Barrel(object):
    def __init__(self, barrel_id, serial_number, inspection_date):
        self.id = barrel_id
        self.serial_number = serial_number
        self.inspection_date = inspection_date

    def to_dict(self):
        return {'SerialNumber': self.serial_number, 'InspectionDate': self.inspection_date}


app = Flask(__name__)
barrel = Barrel(1, '001', '1/1/2001')


@app.route('/barrels', methods=['POST'])
def create_barrel():
    if not request.json or not request.json['SerialNumber'] or not request.json['InspectionDate']:
        return jsonify(Error='400 Some barrel information is missing.'), 400
    if request.json['SerialNumber'] == barrel.serial_number:
        return jsonify(
            Error='409 A barrel with the serial number %s is already in the warehouse.' % barrel.serial_number), 409
    serial_number = request.json['SerialNumber']
    inspection_date = request.json['InspectionDate']
    new_barrel = Barrel(3, serial_number, inspection_date)
    resp = make_response(jsonify(new_barrel.to_dict()), 201)
    resp.headers['Location'] = url_for('get_barrel', barrel_id=3)
    return resp


@app.route('/barrels')
def list_barrels():
    page_size = request.args.get('page_size', "100")
    return jsonify(PageSize=page_size, Barrels=['Some Uri 1', 'Some Uri 2'])


@app.route("/barrels/<int:barrel_id>")
def get_barrel(barrel_id):
    if barrel.id != barrel_id:
        return jsonify(Error='404 No barrel with ID %s exists.' % barrel_id), 404
    if request.headers['Accept'] == 'application/xml':
        resp = make_response(dumps({'response': barrel.to_dict()}))
        resp.headers['Content-Type'] = 'application/xml'
        return resp
    return jsonify(barrel.to_dict())


@app.route("/barrels/<int:barrel_id>", methods=['PUT'])
def update_barrel(barrel_id):
    if barrel.id != barrel_id:
        return jsonify(Error='404 No barrel with ID %s exists.' % barrel_id), 404
    if not request.json or not request.json['SerialNumber'] and not request.json['InspectionDate']:
        return jsonify(Error='400 Some barrel information is missing.'), 400
    serial_number = request.json['SerialNumber'] if request.json['SerialNumber'] else barrel.serial_number
    inspection_date = request.json['InspectionDate'] if request.json['InspectionDate'] else barrel.inspection_date
    updated_barrel = Barrel(barrel.id, serial_number, inspection_date)
    return make_response(jsonify(updated_barrel.to_dict()))


if __name__ == "__main__":
    app.run(debug=True)