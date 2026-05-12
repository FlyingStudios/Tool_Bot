import os
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev-key")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

STATE_MENU = "menu"
STATE_STUNDENLOHN = "stundenlohn"
STATE_STUNDEN = "stunden"


def antwort(text, delay=0):
    return jsonify({
        "answer": text,
        "delay": delay
    })


@app.route("/")
def home():
    return render_template("index.html", name=session.get("name"))


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data or "message" not in data:
        return antwort("Ungültige Anfrage.")

    message = data["message"].strip().lower()

    if not message:
        return antwort("Bitte gib eine Nachricht ein.")

    # NAME
    if not session.get("name"):
        session["name"] = message
        session["state"] = STATE_MENU
        return antwort(
            f"Hallo {session['name']}!\n\n"
            "Welches Programm möchtest du starten?\n\n"
            "- gehaltsrechner"
        )

    state = session.get("state", STATE_MENU)

    # MENU
    if state == STATE_MENU:

        if message == "gehaltsrechner":
            session["state"] = STATE_STUNDENLOHN
            return antwort("Bitte gib deinen Stundenlohn ein.")

        return antwort("Programm nicht gefunden.\n- gehaltsrechner")

    # STUNDENLOHN
    if state == STATE_STUNDENLOHN:

        try:
            stundenlohn = float(message.replace(",", "."))

            if stundenlohn <= 0:
                return antwort("Bitte Zahl > 0 eingeben.")

            session["stundenlohn"] = stundenlohn
            session["state"] = STATE_STUNDEN

            return antwort("Wie viele Stunden pro Woche?", 1000)

        except ValueError:
            return antwort("Ungültige Zahl.")

    # STUNDEN
    if state == STATE_STUNDEN:

        try:
            stunden = float(message.replace(",", "."))

            if stunden <= 0:
                return antwort("Bitte Zahl > 0 eingeben.")

            lohn = session["stundenlohn"]

            monat = lohn * stunden * 4
            jahr = lohn * stunden * 52
            sekunde = lohn / 3600

            session["state"] = STATE_MENU

            return antwort(
                f"Monatsgehalt: {monat:.2f} €\n"
                f"Jahresgehalt: {jahr:.2f} €\n"
                f"Sekundenlohn: {sekunde:.4f} €\n\n"
                "Zurück im Menü:\n- gehaltsrechner",
                2000
            )

        except ValueError:
            return antwort("Ungültige Zahl.")

    return antwort("Fehler.")