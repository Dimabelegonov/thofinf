from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Country(db.Model):
    __tablename__ = "country"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    area = db.Column(db.Float, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    languages = db.relationship("CountryLanguage", backref="country", lazy=True)
    events = db.relationship("CountryEvent", backref="country", lazy=True)
    people = db.relationship("CountryPerson", backref="country", lazy=True)


class Language(db.Model):
    __tablename__ = "language"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    countries = db.relationship("CountryLanguage", backref="language", lazy=True)
    people = db.relationship("PersonLanguage", backref="language", lazy=True)


class CountryLanguage(db.Model):
    __tablename__ = "country_language"
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"), nullable=False)
    percentage = db.Column(db.Float, nullable=False)


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    death_year = db.Column(db.Integer, nullable=True)
    languages = db.relationship("PersonLanguage", backref="person", lazy=True)
    events = db.relationship("PersonEvent", backref="person", lazy=True)
    countries = db.relationship("CountryPerson", backref="person", lazy=True)


class PersonLanguage(db.Model):
    __tablename__ = "person_language"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"), nullable=False)


class EventType(db.Model):
    __tablename__ = "event_type"
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(255), nullable=False)
    events = db.relationship("Event", backref="event_type", lazy=True)


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("event_type.id"), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=True)
    people = db.relationship("PersonEvent", backref="event", lazy=True)
    countries = db.relationship("CountryEvent", backref="event", lazy=True)


class PersonEvent(db.Model):
    __tablename__ = "person_event"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    role = db.Column(db.String(255), nullable=False)


class CountryEvent(db.Model):
    __tablename__ = "country_event"
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)


class CountryPerson(db.Model):
    __tablename__ = "country_person"
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
