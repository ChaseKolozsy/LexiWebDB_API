from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lemmas(db.Model):
    lemma = db.Column(db.String, primary_key=True)
    enumerated_lemmas = db.Column(db.ARRAY(db.String), unique=True, nullable=False)
    frequency = db.Column(db.Integer, unique=True, nullable=True)
        # Define a relationship to the Definitions table based on lemma names
    lemma_list = relationship("Enumerated_Lemmas", primaryjoin="Lemmas.enumerated_lemmas.any(Enumerated_Lemmas.enumerated_lemma.like(Lemmas.enumerated_lemmas + '%'))", viewonly=True)

    def __repr__(self):
        lemmas_str = '\n'.join(self.enumerated_lemmas)
        return f'<Lemma {self.lemma}:\nfrequency: {self.frequency}\nlemmas: {lemmas_str}>'

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_all():
        return Lemmas.query.all()

    @staticmethod
    def query_by_lemma(lemma):
        return Lemmas.query.filter_by(lemma=lemma).first()

class Enumerated_Lemmas(db.Model):
    enumerated_lemma = db.Column(db.String, primary_key=True)
    definition = db.Column(db.String, nullable=False)
    Part_of_speech = db.Column(db.String, nullable=True)
    frequency = db.Column(db.Integer, nullable=True)
    Phrase = db.Column(db.String, nullable=True)
    Lemma_link = db.Column(db.String, nullable=False)
    Story_link = db.Column(db.String, nullable=True)
    Media_Excerpts = db.Column(db.ARRAY(db.String), nullable=True, comment='Stores filenames for media excerpts')
    Object_Exploration_link = db.Column(db.String, nullable=True)
    Familiar = db.Column(db.Boolean, nullable=False)

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

    @staticmethod
    def query_all():
        return Lemmas.query.all()

    @staticmethod
    def query_by_lemma(lemma_n):
        return Lemmas.query.filter_by(lemma=lemma_n).first()