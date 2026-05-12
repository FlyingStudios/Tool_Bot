from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "test"

# =========================
# STATES
# =========================
STATE_MENU = "menu"
STATE_STUNDENLOHN = "stundenlohn"
STATE_STUNDEN = "stunden"


# =========================
# HELPER
# =========================
def antwort(text):
    return jsonify({"answer": text})


# =========================
# ROUTES
# =========================
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

    # =========================
    # NAME SPEICHERN
    # =========================
    if "name" not in session:

        session["name"] = message
        session["state"] = STATE_MENU

        return antwort(
            f"Hallo {session['name']}!\n\n"
            "Welches Programm möchtest du starten?\n\n"
            "- gehaltsrechner"
        )

    state = session.get("state", STATE_MENU)

    # =========================
    # MENÜ
    # =========================
    if state == STATE_MENU:

        if message == "gehaltsrechner":

            session["state"] = STATE_STUNDENLOHN

            return antwort("Bitte gib deinen Stundenlohn ein.")

        return antwort(
            "Programm nicht gefunden.\n\n"
            "- gehaltsrechner"
        )

    # =========================
    # STUNDENLOHN
    # =========================
    if state == STATE_STUNDENLOHN:

        try:
            stundenlohn = float(message.replace(",", "."))

            if stundenlohn <= 0:
                return antwort("Bitte gib eine Zahl größer als 0 ein.")

            session["stundenlohn"] = stundenlohn
            session["state"] = STATE_STUNDEN

            return antwort("Wie viele Stunden arbeitest du pro Woche?")

        except ValueError:
            return antwort("Bitte gib eine gültige Zahl ein.")

    # =========================
    # STUNDEN PRO WOCHE
    # =========================
    if state == STATE_STUNDEN:

        try:
            stunden_pro_woche = float(message.replace(",", "."))

            if stunden_pro_woche <= 0:
                return antwort("Bitte gib eine Zahl größer als 0 ein.")

            stundenlohn = session["stundenlohn"]

            monatsgehalt = stundenlohn * stunden_pro_woche * 4
            jahresgehalt = stundenlohn * stunden_pro_woche * 52
            sekundenlohn = stundenlohn / 3600

            session["state"] = STATE_MENU

            return antwort(
                f"Monatsgehalt: {monatsgehalt:.2f} €\n"
                f"Jahresgehalt: {jahresgehalt:.2f} €\n"
                f"Sekundenlohn: {sekundenlohn:.4f} €\n\n"
                "Zurück im Menü:\n- gehaltsrechner"
            )

        except ValueError:
            return antwort("Bitte gib eine gültige Zahl ein.")

    return antwort("Fehler im System.")


if __name__ == "__main__":
    app.run(debug=True)