from flask import Blueprint, jsonify, request
from models import db, Phrases

phrases = Blueprint('phrases', __name__)

@phrases.route('', methods=['POST'])
def create_phrase():
    data = request.json
    phrase = data.get('phrase', None)
    lemma_references = data.get('lemma_references', None)
    media_references = data.get('media_references', None)
    anki_card_ids = data.get('anki_card_ids', None)
    familiar = data.get('familiar', None)
    frequency = data.get('frequency', None)

    if not phrase:
        return jsonify(error="Phrase is required"), 400

    new_phrase = Phrases(
        phrase=phrase,
        lemma_references=lemma_references,
        media_references=media_references,
        anki_card_ids=anki_card_ids,
        familiar=familiar,
        frequency=frequency
    )
    new_phrase.add()
    return jsonify(message="Phrase created successfully")

@phrases.route('', methods=['GET'])
def get_all_phrases():
    all_phrases = Phrases.query_all()
    return jsonify(phrases=[phrase.to_dict() for phrase in all_phrases])

@phrases.route('/<phrase>', methods=['GET'])
def get_phrase_by_name(phrase):
    found_phrase = Phrases.query_by_phrase(phrase)
    if found_phrase:
        return jsonify(found_phrase.to_dict())
    return jsonify(error="Phrase not found"), 404

@phrases.route('/<phrase>', methods=['PUT'])
def update_phrase(phrase):
    data = request.json
    existing_phrase = Phrases.query_by_phrase(phrase)
    if existing_phrase:
        for key, value in data.items():
            setattr(existing_phrase, key, value)
        existing_phrase.update()
        return jsonify(message="Phrase updated successfully")
    return jsonify(error="Phrase not found"), 404

@phrases.route('/<phrase>', methods=['DELETE'])
def delete_phrase(phrase):
    existing_phrase = Phrases.query_by_phrase(phrase)
    if existing_phrase:
        existing_phrase.delete()
        return jsonify(message="Phrase deleted successfully")
    return jsonify(error="Phrase not found"), 404

@phrases.route('/increment_frequency/<phrase>', methods=['POST'])
def increment_phrase_frequency(phrase):
    found_phrase = Phrases.query_by_phrase(phrase)
    if found_phrase:
        found_phrase.increment_frequency()
        return jsonify(message="Frequency incremented successfully", frequency=found_phrase.frequency)
    return jsonify(error="Phrase not found"), 404