from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv
from models import Lemmas, Enumerated_Lemmas
from blueprint_Lemmas import lemmas
from blueprint_Enumerated_Lemmas import enumerated_lemmas

import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(lemmas, url_prefix='/lemmas')
app.register_blueprint(enumerated_lemmas, url_prefix='/enumerated_lemmas')

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/init_db')
def init_db():
    try:
        db.create_all()
        return "Database initialized successfully!"
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

@app.route('/reset_db', methods=['POST'])
def reset_db():
    try:
        db.drop_all()
        db.create_all()
        return "Database reset and reinitialized successfully!"
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

# Load environment variablesPOSTGRES_USER')}:{os.getenv('POSTGRES_P{os.getenv('POSTGRES_DB}"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

