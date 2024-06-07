from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv
from models import db, Enumerated_Lemmas
from blueprint_Enumerated_Lemmas import enumerated_lemmas

import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(enumerated_lemmas, url_prefix='/enumerated_lemmas')

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/init_db')
def init_db():
    try:
        with app.app_context():
            db.create_all()
        return "Database initialized successfully!"
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

@app.route('/reset_db', methods=['POST'])
def reset_db():
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
        return "Database reset and reinitialized successfully!"
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)