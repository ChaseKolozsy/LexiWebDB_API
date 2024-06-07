from flask import Blueprint, jsonify, request
from models import db, Lemmas

lemmas = Blueprint('lemmas', __name__)

@lemmas.route('/schema')
def get_lemmas_schema():
    schema = {}
    for column in Lemmas.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

