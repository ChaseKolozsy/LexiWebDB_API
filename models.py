from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Enumerated_Lemmas(db.Model):
    __tablename__ = 'enumerated_lemmas'  # Explicitly set the table name
    enumerated_lemma = db.Column(db.String, primary_key=True, unique=True)
    base_lemma = db.Column(db.String, nullable=False)
    definition = db.Column(db.String, nullable=False)
    part_of_speech = db.Column(db.String, nullable=True)
    frequency = db.Column(db.Integer, nullable=True)
    phrase = db.Column(db.String, nullable=True)
    story_link = db.Column(db.String, nullable=True)
    media_excerpts = db.Column(db.ARRAY(db.String), nullable=True, comment='Stores filenames for media excerpts')
    object_exploration_link = db.Column(db.String, nullable=True)
    anki_card_ids = db.Column(db.ARRAY(db.Integer), nullable=True)
    familiar = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Definition {self.enumerated_lemma} ({self.Part_of_speech}):\nfrequency: {self.frequency}:\ndefinition: {self.definition}>'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def increment_frequency(self):
        if self.frequency is None:
            self.frequency = 0
        self.frequency += 1
        db.session.commit()

    @staticmethod
    def query_all():
        return Enumerated_Lemmas.query.all()

    @staticmethod
    def query_by_lemma(lemma_n):
        return Enumerated_Lemmas.query.filter_by(enumerated_lemma=lemma_n).first()

class Phrases(db.Model):
    __tablename__ = 'phrases'
    phrase = db.Column(db.String, primary_key=True, unique=True)
    lemma_references = db.Column(db.ARRAY(db.String), nullable=True)
    media_references = db.Column(db.ARRAY(db.String), nullable=True, comment='Stores filenames for mediafiles that contain the phrase')
    anki_card_ids = db.Column(db.ARRAY(db.Integer), nullable=True)
    familiar = db.Column(db.Boolean, nullable=False)
    frequency = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Phrase {self.phrase}>'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def increment_frequency(self):
        if self.frequency is None:
            self.frequency = 0
        self.frequency += 1
        db.session.commit()

    @staticmethod
    def query_all():
        return Phrases.query.all()

    @staticmethod
    def query_by_phrase(phrase):
        return Phrases.query.filter_by(phrase=phrase).first()

class Branch(db.Model):
    __tablename__ = 'branches'
    branch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    root_node = db.Column(db.String, nullable=False)
    branch_name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Branch {self.branch_id}: {self.branch_name}>'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def query_all():
        return Branch.query.all()

    @staticmethod
    def query_by_id(branch_id):
        return Branch.query.filter_by(branch_id=branch_id).first()


class BranchNode(db.Model):
    __tablename__ = 'branch_nodes'
    node_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    enumerated_lemma = db.Column(db.String, db.ForeignKey('enumerated_lemmas.enumerated_lemma'), nullable=False)
    parent_node_id = db.Column(db.Integer, db.ForeignKey('branch_nodes.node_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    branch = db.relationship('Branch', backref=db.backref('nodes', lazy=True))
    parent_node = db.relationship('BranchNode', remote_side=[node_id], backref='children')
    lemma = db.relationship('Enumerated_Lemmas', backref=db.backref('nodes', lazy=True))

    def __repr__(self):
        return f'<BranchNode {self.node_id}: {self.lemma.enumerated_lemma}>'
    def __repr__(self):
        return f'<BranchNode {self.node_id}: {self.value}>'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def query_all():
        return BranchNode.query.all()

    @staticmethod
    def query_by_id(node_id):
        return BranchNode.query.filter_by(node_id=node_id).first()