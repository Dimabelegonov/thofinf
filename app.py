from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from module import (
    db,
    Country,
    CountryEvent,
    CountryLanguage,
    CountryPerson,
    Person,
    PersonEvent,
    PersonLanguage,
    Language,
    Event,
    EventType,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


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
