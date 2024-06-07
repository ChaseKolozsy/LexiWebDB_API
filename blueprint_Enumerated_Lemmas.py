from flask import Blueprint, jsonify, request
from models import db, Enumerated_Lemmas

enumerated_lemmas = Blueprint('enumerated_lemmas', __name__)

@enumerated_lemmas.route('/schema')
def get_enumerated_lemmas_schema():
    schema = {}
    for column in Enumerated_Lemmas.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

