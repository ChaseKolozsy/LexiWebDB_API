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

