__author__ = 'amayausky'

from datetime import datetime
from flask import Flask, jsonify, make_response, request
# noinspection PyPackageRequirements
# needs: pip install python-simplexml
from simplexml import dumps


class Barrel(object):
    def __init__(self, barrel_id, serial_number, inspection_date=None):
        self.id = barrel_id
        self.serial_number = serial_number
        self.inspection_date = inspection_date or datetime.utcnow().strftime('%d/%m/%y')

    def to_dict(self):
        return {'SerialNumber': self.serial_number, 'InspectionDate': self.inspection_date}

app = Flask(__name__)
barrels_store = [Barrel(1, '001', '1/1/2001')]


@app.route('/barrels')
def list_barrels():
    page_size = request.args.get('page_size', "100")
    return jsonify(PageSize=page_size, Barrels=['Some Uri 1', 'Some Uri 2'])


@app.route("/barrels/<int:barrel_id>")
def get_barrel(barrel_id):
    barrels = [b for b in barrels_store if b.id == barrel_id]
    if len(barrels) == 0:
        return jsonify(Error='404 No barrel with ID %s exists.' % barrel_id), 404
    if request.headers['Accept'] == 'application/xml':
        resp = make_response(dumps({'response': barrels[0].to_dict()}))
        resp.headers['Content-Type'] = 'application/xml'
        return resp
    return jsonify(barrels[0].to_dict())

if __name__ == "__main__":
    app.run(debug=True)