from flask import Blueprint, jsonify, request
from models import db, GrammarPoint
from sqlalchemy.exc import IntegrityError

grammar_points = Blueprint('grammar_points', __name__)

@grammar_points.route('/schema')
def get_grammar_points_schema():
    schema = {}
    for column in GrammarPoint.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@grammar_points.route('', methods=['GET'])
def get_all_grammar_points():
    grammar_points = GrammarPoint.query_all()
    return jsonify([gp.to_dict() for gp in grammar_points]), 200

@grammar_points.route('/<int:gp_id>', methods=['GET'])
def get_grammar_point(gp_id):
    grammar_point = GrammarPoint.query_by_id(gp_id)
    if grammar_point:
        return jsonify(grammar_point.to_dict()), 200
    return jsonify({'error': 'GrammarPoint not found'}), 404

@grammar_points.route('', methods=['POST'])
def create_grammar_point():
    data = request.get_json()
    grammar_point = GrammarPoint(
        grammar_point=data.get('grammar_point'),
        example_phrase=data.get('example_phrase')
    )
    try:
        grammar_point.add()
        return jsonify(grammar_point.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integrity error, possibly duplicate entry'}), 400

@grammar_points.route('/<int:gp_id>', methods=['PUT'])
def update_grammar_point(gp_id):
    data = request.get_json()
    grammar_point = GrammarPoint.query_by_id(gp_id)
    if grammar_point:
        grammar_point.update(
            grammar_point=data.get('grammar_point'),
            example_phrase=data.get('example_phrase')
        )
        return jsonify(grammar_point.to_dict()), 200
    return jsonify({'error': 'GrammarPoint not found'}), 404

@grammar_points.route('/<int:gp_id>', methods=['DELETE'])
def delete_grammar_point(gp_id):
    grammar_point = GrammarPoint.query_by_id(gp_id)
    if grammar_point:
        grammar_point.delete()
        return jsonify({'message': 'GrammarPoint deleted'}), 200
    return jsonify({'error': 'GrammarPoint not found'}), 404