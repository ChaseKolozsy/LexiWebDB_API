from flask import Blueprint, jsonify, request
from models import db, Branch
from sqlalchemy.exc import IntegrityError

branches = Blueprint('branches', __name__)

@branches.route('/schema')
def get_branches_schema():
    schema = {}
    for column in Branch.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@branches.route('', methods=['POST'])
def create_branch():
    data = request.json
    root_node = data.get('root_node', None)
    branch_name = data.get('branch_name', None)

    if not root_node:
        return jsonify(error="Root node is required"), 400

    new_branch = Branch(
        root_node=root_node,
        branch_name=branch_name
    )

    try:
        new_branch.add()
        return jsonify(message="Branch created successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Branch already exists"), 400

@branches.route('', methods=['GET'])
def get_all_branches():
    all_branches = Branch.query_all()
    return jsonify(branches=[branch.to_dict() for branch in all_branches])

@branches.route('/<int:branch_id>', methods=['GET'])
def get_branch_by_id(branch_id):
    branch = Branch.query_by_id(branch_id)
    if branch:
        return jsonify(branch.to_dict())
    return jsonify(error="Branch not found"), 404

@branches.route('/<int:branch_id>', methods=['PUT'])
def update_branch(branch_id):
    data = request.json
    existing_branch = Branch.query_by_id(branch_id)
    if existing_branch:
        for key, value in data.items():
            setattr(existing_branch, key, value)
        existing_branch.update()
        return jsonify(message="Branch updated successfully")
    return jsonify(error="Branch not found"), 404

@branches.route('/<int:branch_id>', methods=['DELETE'])
def delete_branch(branch_id):
    existing_branch = Branch.query_by_id(branch_id)
    if existing_branch:
        existing_branch.delete()
        return jsonify(message="Branch deleted successfully")
    return jsonify(error="Branch not found"), 404