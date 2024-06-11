from flask import Blueprint, jsonify, request
from models import db, Object
from sqlalchemy.exc import IntegrityError

objects = Blueprint('objects', __name__)

@objects.route('/schema')
def get_objects_schema():
    schema = {}
    for column in Object.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@objects.route('/objects', methods=['GET'])
def get_all_objects():
    objects = Object.query_all()

@objects.route('/objects/<int:object_id>', methods=['GET'])
def get_object(object_id):
    obj = Object.query_by_id(object_id)
    if obj:
        return jsonify(obj.to_dict()), 200
    return jsonify({'error': 'Object not found'}), 404

@objects.route('/objects', methods=['POST'])
def create_object():
    data = request.get_json()
    obj = Object(name=data.get('name'))
    try:
        obj.add()
        return jsonify(obj.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error, possibly duplicate entry'}), 400

@objects.route('/objects/<int:object_id>', methods=['PUT'])
def update_object(object_id):
    data = request.get_json()
    obj = Object.query_by_id(object_id)
    if obj:
        obj.update(name=data.get('name'))
        return jsonify(obj.to_dict()), 200
    return jsonify({'error': 'Object not found'}), 404

@objects.route('/objects/<int:object_id>', methods=['DELETE'])
def delete_object(object_id):
    obj = Object.query_by_id(object_id)
    if obj:
        obj.delete()
        return jsonify({'message': 'Object deleted'}), 200
    return jsonify({'error': 'Object not found'}), 404