from flask import Blueprint, jsonify, request
from models import db, Enumerated_Lemmas
from sqlalchemy.exc import IntegrityError

enumerated_lemmas = Blueprint('enumerated_lemmas', __name__)

@enumerated_lemmas.route('/schema')
def get_enumerated_lemmas_schema():
    schema = {}
    for column in Enumerated_Lemmas.__table__.columns:
        schema[column.name] = str(column.type)
    return jsonify(schema)

@enumerated_lemmas.route('', methods=['POST'])
def create_enumerated_lemma():
    data = request.json
    enumerated_lemma = data.get('enumerated_lemma', None)
    base_lemma = data.get('base_lemma', None)
    definition = data.get('definition', None)
    part_of_speech = data.get('part_of_speech', None)
    frequency = data.get('frequency', None)
    phrase = data.get('phrase', None)
    story_link = data.get('story_link', None)
    media_references = data.get('media_references', None)
    object_exploration_link = data.get('object_exploration_link', None)
    familiar = data.get('familiar', None)
    anki_card_ids = data.get('anki_card_ids', None)

    if not enumerated_lemma:
        return jsonify(error="Enumerated Lemma is required"), 400

    new_enumerated_lemma = Enumerated_Lemmas(
        enumerated_lemma=enumerated_lemma, 
        base_lemma=base_lemma,  # Ensure base_lemma is included
        definition=definition, 
        part_of_speech=part_of_speech, 
        frequency=frequency, 
        phrase=phrase, 
        story_link=story_link, 
        media_references=media_references, 
        object_exploration_link=object_exploration_link, 
        familiar=familiar,
        anki_card_ids=anki_card_ids
    )

    try:
        new_enumerated_lemma.add()
        return jsonify(message="Enumerated Lemma created successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Enumerated Lemma already exists"), 400
@enumerated_lemmas.route('', methods=['GET'])
def get_all_enumerated_lemmas():
    all_enumerated_lemmas = Enumerated_Lemmas.query_all()
    return jsonify(enumerated_lemmas=[enumerated_lemma.to_dict() for enumerated_lemma in all_enumerated_lemmas])

@enumerated_lemmas.route('/<lemma_name>', methods=['GET'])
def get_enumerated_lemma_by_name(lemma_name):
    enumerated_lemma = Enumerated_Lemmas.query_by_lemma(lemma_name)
    if enumerated_lemma:
        return jsonify(enumerated_lemma.to_dict())
    return jsonify(error="Lemma not found"), 404

@enumerated_lemmas.route('/<enumerated_lemma>', methods=['PUT'])
def update_enumerated_lemma(enumerated_lemma):
    data = request.json
    existing_lemma = Enumerated_Lemmas.query_by_lemma(enumerated_lemma)
    if existing_lemma:
        for key, value in data.items():
            setattr(existing_lemma, key, value)
        existing_lemma.update()
        return jsonify(message="Lemma updated successfully")
    return jsonify(error="Lemma not found"), 404

@enumerated_lemmas.route('/<enumerated_lemma>', methods=['DELETE'])
def delete_enumerated_lemma(enumerated_lemma):
    existing_lemma = Enumerated_Lemmas.query_by_lemma(enumerated_lemma)
    if existing_lemma:
        existing_lemma.delete()
        return jsonify(message="Lemma deleted successfully")
    return jsonify(error="Lemma not found"), 404

@enumerated_lemmas.route('/increment_frequency/<lemma_name>', methods=['POST'])
def increment_frequency(lemma_name):
    enumerated_lemma = Enumerated_Lemmas.query_by_lemma(lemma_name)
    if enumerated_lemma:
        enumerated_lemma.increment_frequency()
        return jsonify(message="Frequency incremented successfully", frequency=enumerated_lemma.frequency)
    return jsonify(error="Lemma not found"), 404