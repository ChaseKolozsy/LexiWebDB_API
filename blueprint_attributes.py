from flask import Blueprint, jsonify, request
from models import db, Attribute
from sqlalchemy.exc import IntegrityError

attributes = Blueprint('attributes', __name__)

@attributes.route('/schema')
def get_attributes_schema():
    schema = {}
    for column in Attribute.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@attributes.route('/attributes', methods=['GET'])
def get_all_attributes():
    attributes = Attribute.query_all()
    return jsonify([attr.to_dict() for attr in attributes]), 200

@attributes.route('/attributes/<int:attribute_id>', methods=['GET'])
def get_attribute(attribute_id):
    attribute = Attribute.query_by_id(attribute_id)
    if attribute:
        return jsonify(attribute.to_dict()), 200
    return jsonify({'error': 'Attribute not found'}), 404

@attributes.route('/attributes', methods=['POST'])
def create_attribute():
    data = request.get_json()
    attribute = Attribute(name=data.get('name'))
    try:
        attribute.add()
        return jsonify(attribute.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error, possibly duplicate entry'}), 400

@attributes.route('/attributes/<int:attribute_id>', methods=['PUT'])
def update_attribute(attribute_id):
    data = request.get_json()
    attribute = Attribute.query_by_id(attribute_id)
    if attribute:
        attribute.update(name=data.get('name'))
        return jsonify(attribute.to_dict()), 200
    return jsonify({'error': 'Attribute not found'}), 404

@attributes.route('/attributes/<int:attribute_id>', methods=['DELETE'])
def delete_attribute(attribute_id):
    attribute = Attribute.query_by_id(attribute_id)
    if attribute:
        attribute.delete()
        return jsonify({'message': 'Attribute deleted'}), 200
    return jsonify({'error': 'Attribute not found'}), 404