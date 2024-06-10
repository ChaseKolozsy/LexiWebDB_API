from flask import Blueprint, jsonify, request
from models import db, BranchNode
from sqlalchemy.exc import IntegrityError

branch_nodes = Blueprint('branch_nodes', __name__)

@branch_nodes.route('/schema')
def get_branch_nodes_schema():
    schema = {}
    for column in BranchNode.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@branch_nodes.route('', methods=['POST'])
def create_branch_node():
    data = request.json
    branch_id = data.get('branch_id', None)
    enumerated_lemma = data.get('enumerated_lemma', None)
    parent_node_id = data.get('parent_node_id', None)

    if not branch_id or not enumerated_lemma:
        return jsonify(error="Branch ID and Enumerated Lemma are required"), 400

    new_branch_node = BranchNode(
        branch_id=branch_id,
        enumerated_lemma=enumerated_lemma,
        parent_node_id=parent_node_id
    )

    try:
        new_branch_node.add()
        return jsonify(message="Branch Node created successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Branch Node already exists"), 400

@branch_nodes.route('', methods=['GET'])
def get_all_branch_nodes():
    all_branch_nodes = BranchNode.query_all()
    return jsonify(branch_nodes=[branch_node.to_dict() for branch_node in all_branch_nodes])

@branch_nodes.route('/<int:node_id>', methods=['GET'])
def get_branch_node_by_id(node_id):
    branch_node = BranchNode.query_by_id(node_id)
    if branch_node:
        return jsonify(branch_node.to_dict())
    return jsonify(error="Branch Node not found"), 404


@branch_nodes.route('/<int:node_id>', methods=['DELETE'])
def delete_branch_node(node_id):
    existing_branch_node = BranchNode.query_by_id(node_id)
    if existing_branch_node:
        existing_branch_node.delete()
        return jsonify(message="Branch Node deleted successfully")
    return jsonify(error="Branch Node not found"), 404