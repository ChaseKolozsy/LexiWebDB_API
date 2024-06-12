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
    media_references = db.Column(db.ARRAY(db.String), nullable=True, comment='Stores filenames for media references')
    object_exploration_link = db.Column(db.String, nullable=True)
    anki_card_ids = db.Column(db.ARRAY(db.Integer), nullable=True)
    familiar = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

class GrammarPoint(db.Model):
    __tablename__ = 'grammar_points'
    gp_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    grammar_point = db.Column(db.String, nullable=False)
    example_phrase = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<GrammarPoint {self.gp_id}: {self.grammar_point}>'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, grammar_point=None, example_phrase=None):
        if grammar_point is not None:
            self.grammar_point = grammar_point
        if example_phrase is not None:
            self.example_phrase = example_phrase
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def query_all():
        return GrammarPoint.query.all()

    @staticmethod
    def query_by_id(gp_id):
        return GrammarPoint.query.filter_by(gp_id=gp_id).first()

# Association tables
object_attributes = db.Table('object_attributes',
    db.Column('object_id', db.Integer, db.ForeignKey('objects.object_id'), primary_key=True),
    db.Column('attribute_id', db.Integer, db.ForeignKey('attributes.attribute_id'), primary_key=True)
)

object_verbs = db.Table('object_verbs',
    db.Column('object_id', db.Integer, db.ForeignKey('objects.object_id'), primary_key=True),
    db.Column('verb_id', db.Integer, db.ForeignKey('verbs.verb_id'), primary_key=True)
)

object_states = db.Table('object_states',
    db.Column('object_id', db.Integer, db.ForeignKey('objects.object_id'), primary_key=True),
    db.Column('state_id', db.Integer, db.ForeignKey('states.state_id'), primary_key=True)
)

object_routines = db.Table('object_routines',
    db.Column('object_id', db.Integer, db.ForeignKey('objects.object_id'), primary_key=True),
    db.Column('routine_id', db.Integer, db.ForeignKey('routines.routine_id'), primary_key=True)
)

class Object(db.Model):
    __tablename__ = 'objects'
    object_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attributes = db.relationship('Attribute', secondary=object_attributes, backref=db.backref('objects', lazy='dynamic'))
    verbs = db.relationship('Verb', secondary=object_verbs, backref=db.backref('objects', lazy='dynamic'))
    states = db.relationship('State', secondary=object_states, backref=db.backref('objects', lazy='dynamic'))
    routines = db.relationship('Routine', secondary=object_routines, backref=db.backref('objects', lazy='dynamic'))

    def __repr__(self):
        return f'<Object {self.object_id}: {self.name}>'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, name=None):
        if name:
            self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_all():
        return Object.query.all()

    @staticmethod
    def query_by_name(name):
        return Object.query.filter_by(name=name).first()

    @staticmethod
    def query_by_id(object_id):
        return Object.query.filter_by(object_id=object_id).first()

class Attribute(db.Model):
    __tablename__ = 'attributes'
    attribute_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Attribute {self.attribute_id}: {self.name}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None):
        if name:
            self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_all():
        return Attribute.query.all()

    @staticmethod
    def query_by_name(name):
        return Attribute.query.filter_by(name=name).first()

    @staticmethod
    def query_by_id(attribute_id):
        return Attribute.query.filter_by(attribute_id=attribute_id).first()

class Verb(db.Model):
    __tablename__ = 'verbs'
    verb_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Verb {self.verb_id}: {self.name}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None):
        if name:
            self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_all():
        return Verb.query.all()

    @staticmethod
    def query_by_name(name):
        return Verb.query.filter_by(name=name).first()

    @staticmethod
    def query_by_id(verb_id):
        return Verb.query.filter_by(verb_id=verb_id).first()

class State(db.Model):
    __tablename__ = 'states'
    state_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<State {self.state_id}: {self.name}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None):
        if name:
            self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_all():
        return State.query.all()

    @staticmethod
    def query_by_name(name):
        return State.query.filter_by(name=name).first()

    @staticmethod
    def query_by_id(state_id):
        return State.query.filter_by(state_id=state_id).first()

class Routine(db.Model):
    __tablename__ = 'routines'
    routine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Routine {self.routine_id}: {self.name}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, description=None):
        if name:
            self.name = name
        if description:
            self.description = description
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_all():
        return Routine.query.all()
     
    @staticmethod
    def query_by_name(name):
        return Routine.query.filter_by(name=name).first()

    @staticmethod
    def query_by_id(routine_id):
        return Routine.query.filter_by(routine_id=routine_id).first()