from flask import Blueprint, jsonify, request
from models import db, Routine
from sqlalchemy.exc import IntegrityError

routines = Blueprint('routines', __name__)

@routines.route('/schema')
def get_routines_schema():
    schema = {}
    for column in Routine.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@routines.route('', methods=['GET'])
def get_all_routines():
    routines = Routine.query_all()
    return jsonify([routine.to_dict() for routine in routines]), 200

@routines.route('/<int:routine_id>', methods=['GET'])
def get_routine(routine_id):
    routine = Routine.query_by_id(routine_id)
    if routine:
        return jsonify(routine.to_dict()), 200
    return jsonify({'error': 'Routine not found'}), 404

@routines.route('/<string:routine_name>', methods=['GET'])
def get_routine_by_name(routine_name):
    routine = Routine.query_by_name(routine_name)
    if routine:
        return jsonify(routine.to_dict()), 200
    return jsonify({'error': 'Routine not found'}), 404

@routines.route('', methods=['POST'])
def create_routine():
    data = request.get_json()
    routine = Routine(
        name=data.get('name'),
        description=data.get('description')
    )
    try:
        routine.add()
        return jsonify(routine.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error, possibly duplicate entry'}), 400

@routines.route('/<int:routine_id>', methods=['PUT'])
def update_routine(routine_id):
    data = request.get_json()
    routine = Routine.query_by_id(routine_id)
    if routine:
        routine.update(
            name=data.get('name'),
            description=data.get('description')
        )
        return jsonify(routine.to_dict()), 200
    return jsonify({'error': 'Routine not found'}), 404

@routines.route('/<int:routine_id>', methods=['DELETE'])
def delete_routine(routine_id):
    routine = Routine.query_by_id(routine_id)
    if routine:
        routine.delete()
        return jsonify({'message': 'Routine deleted'}), 200
    return jsonify({'error': 'Routine not found'}), 404