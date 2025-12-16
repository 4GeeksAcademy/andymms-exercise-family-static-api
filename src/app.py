"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()
    if body is None:
        return jsonify({'msg': 'Body is empty'}), 400
    if 'first_name' not in body:
        return jsonify({'msg': 'First name is required'}), 400
    if 'age' not in body:
        return jsonify({'msg': 'Age is required'}), 400
    if 'lucky_numbers' not in body:
        return jsonify({'msg': 'Lucky numbers is required'}), 400

    new_member = {
        'first_name': body['first_name'],
        'last_name': jackson_family.last_name,
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers']
    }

    if 'id' in body:
        new_member['id'] = body['id']

    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({'msg': 'Member not found'}), 404

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    member = jackson_family.delete_member(id)
    if member == True:
        return jsonify({'done': True}), 200
    return jsonify({'msg': 'Member not found'}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
