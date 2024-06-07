from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Enumerated_Lemmas(db.Model):
    enumerated_lemma = db.Column(db.String, primary_key=True)
    base_lemma = db.Column(db.String, nullable=False)
    definition = db.Column(db.String, nullable=False)
    Part_of_speech = db.Column(db.String, nullable=True)
    frequency = db.Column(db.Integer, nullable=True)
    Phrase = db.Column(db.String, nullable=True)
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
        return Enumerated_Lemmas.query.all()

    @staticmethod
    def query_by_lemma(lemma_n):
        return Enumerated_Lemmas.query.filter_by(enumerated_lemma=lemma_n).first()