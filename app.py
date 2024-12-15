from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/countries")
def countries():
    countries = Country.query.all()
    return render_template("countries.html", countries=countries)


@app.route("/countries/<int:id>")
def country(id):
    country = Country.query.get_or_404(id)
    # Извлечение языков, событий и людей, связанных с этой страной
    languages = (
        db.session.query(Language, CountryLanguage)
        .filter(
            CountryLanguage.country_id == id,
            CountryLanguage.language_id == Language.id,
        )
        .all()
    )
    events = [ce.event for ce in country.events]
    people = [cp.person for cp in country.people]
    return render_template(
        "country.html",
        country=country,
        languages=languages,
        events=events,
        people=people,
    )


@app.route("/people")
def people():
    people = Person.query.all()
    return render_template("people.html", people=people)


@app.route("/people/<int:id>")
def person(id):
    person = Person.query.get_or_404(id)
    languages = [pl.language for pl in person.languages]
    events = [pe.event for pe in person.events]
    countries = [pc.country for pc in person.countries]
    return render_template(
        "person.html",
        person=person,
        languages=languages,
        events=events,
        countries=countries,
    )


@app.route("/events")
def events():
    events = Event.query.all()
    return render_template("events.html", events=events)


@app.route("/events/<int:id>")
def event(id):
    event = Event.query.get_or_404(id)
    event_type = event.event_type
    people = [pe.person for pe in event.people]
    countries = [ce.country for ce in event.countries]
    return render_template(
        "event.html",
        event=event,
        event_type=event_type,
        people=people,
        countries=countries,
    )


@app.route("/languages")
def languages():
    languages = Language.query.all()
    return render_template("languages.html", languages=languages)


@app.route("/languages/<int:id>")
def language(id):
    language = Language.query.get_or_404(id)
    countries = [cl.country for cl in language.countries]
    people = [pl.person for pl in language.people]
    return render_template(
        "language.html", language=language, countries=countries, people=people
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
