from flask import Blueprint, jsonify, request
from models import db, State
from sqlalchemy.exc import IntegrityError

states = Blueprint('states', __name__)

@states.route('/schema')
def get_states_schema():
    schema = {}
    for column in State.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@states.route('', methods=['GET'])
def get_all_states():
    states = State.query_all()
    return jsonify([state.to_dict() for state in states]), 200

@states.route('/<int:state_id>', methods=['GET'])
def get_state(state_id):
    state = State.query_by_id(state_id)
    if state:
        return jsonify(state.to_dict()), 200
    return jsonify({'error': 'State not found'}), 404

@states.route('/<string:state_name>', methods=['GET'])
def get_state_by_name(state_name):
    state = State.query_by_name(state_name)
    if state:
        return jsonify(state.to_dict()), 200
    return jsonify({'error': 'State not found'}), 404

@states.route('', methods=['POST'])
def create_state():
    data = request.get_json()
    state = State(name=data.get('name'))
    try:
        state.add()
        return jsonify(state.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error, possibly duplicate entry'}), 400

@states.route('/<int:state_id>', methods=['PUT'])
def update_state(state_id):
    data = request.get_json()
    state = State.query_by_id(state_id)
    if state:
        state.update(name=data.get('name'))
        return jsonify(state.to_dict()), 200
    return jsonify({'error': 'State not found'}), 404

@states.route('/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = State.query_by_id(state_id)
    if state:
        state.delete()
        return jsonify({'message': 'State deleted'}), 200
    return jsonify({'error': 'State not found'}), 404