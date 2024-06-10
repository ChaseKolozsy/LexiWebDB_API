from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect, text

from dotenv import load_dotenv
from models import db, Enumerated_Lemmas, Phrases, Branch, BranchNode
from blueprint_Enumerated_Lemmas import enumerated_lemmas
from blueprint_Phrases import phrases
from blueprint_branches import branches
from blueprint_branch_nodes import branch_nodes

import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(enumerated_lemmas, url_prefix='/enumerated_lemmas')
app.register_blueprint(phrases, url_prefix='/phrases')
app.register_blueprint(branches, url_prefix='/branches')
app.register_blueprint(branch_nodes, url_prefix='/branch_nodes')

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

@app.route('/drop_columns', methods=['POST'])
def drop_columns_not_in_opt_in_list():
    data = request.get_json()
    table_name = data.get('table_name', '')
    opt_in_fields = data.get('opt_in_fields', [])

    try:
        inspector = inspect(db.engine)
        columns = inspector.get_columns(table_name)
        primary_keys = set(inspector.get_pk_constraint(table_name)['constrained_columns'])
        foreign_keys = {fk['constrained_columns'][0] for fk in inspector.get_foreign_keys(table_name)}

        columns_to_drop = [
            col['name'] for col in columns 
            if col['name'] not in opt_in_fields and col['name'] not in primary_keys and col['name'] not in foreign_keys
        ]
        
        with db.engine.connect() as conn:
            for column in columns_to_drop:
                conn.execute(text(f'ALTER TABLE {table_name} DROP COLUMN {column}'))
    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(columns_to_drop), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)