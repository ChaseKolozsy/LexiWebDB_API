from flask import Blueprint, jsonify, request
from models import db, Verb
from sqlalchemy.exc import IntegrityError

verbs = Blueprint('verbs', __name__)

@verbs.route('/schema')
def get_verbs_schema():
    schema = {}
    for column in Verb.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@verbs.route('/verbs', methods=['GET'])
def get_all_verbs():
    verbs = Verb.query_all()

@verbs.route('/verbs/<int:verb_id>', methods=['GET'])
def get_verb(verb_id):
    verb = Verb.query_by_id(verb_id)
    if verb:
        return jsonify(verb.to_dict()), 200
    return jsonify({'error': 'Verb not found'}), 404

@verbs.route('/verbs', methods=['POST'])
def create_verb():
    data = request.get_json()
    verb = Verb(name=data.get('name'))
    try:
        verb.add()
        return jsonify(verb.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error, possibly duplicate entry'}), 400

@verbs.route('/verbs/<int:verb_id>', methods=['PUT'])
def update_verb(verb_id):
    data = request.get_json()
    verb = Verb.query_by_id(verb_id)
    if verb:
        verb.update(name=data.get('name'))
        return jsonify(verb.to_dict()), 200
    return jsonify({'error': 'Verb not found'}), 404

@verbs.route('/verbs/<int:verb_id>', methods=['DELETE'])
def delete_verb(verb_id):
    verb = Verb.query_by_id(verb_id)
    if verb:
        verb.delete()
        return jsonify({'message': 'Verb deleted'}), 200
    return jsonify({'error': 'Verb not found'}), 404