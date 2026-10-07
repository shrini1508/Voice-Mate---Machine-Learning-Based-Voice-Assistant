from flask import Flask, render_template, request, jsonify
import joblib
import datetime
import urllib.parse

app = Flask(__name__)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        command = data.get("command", "").strip().lower()

        if not command:
            return jsonify({
                "success": False,
                "response": "Please enter a command.",
                "intent": "",
                "action": ""
            })

        vector = vectorizer.transform([command])
        intent = model.predict(vector)[0]

        response = "Sorry, I did not understand your command."
        action = "none"
        url = ""

        if intent == "open_youtube":
            response = "Opening YouTube"
            action = "open_url"
            url = "https://www.youtube.com"

        elif intent == "open_google":
            response = "Opening Google"
            action = "open_url"
            url = "https://www.google.com"

        elif intent == "open_github":
            response = "Opening GitHub"
            action = "open_url"
            url = "https://github.com"

        elif intent == "search_youtube":
            search = command.replace("search", "").replace("youtube", "").strip()

            if search:
                response = f"Searching YouTube for {search}"
                action = "open_url"
                url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(search)

        elif intent == "search_google":
            search = command.replace("search", "").replace("google", "").strip()

            if search:
                response = f"Searching Google for {search}"
                action = "open_url"
                url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(search)

        elif intent == "tell_time":
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The time is {current_time}"

        elif intent == "tell_date":
            today = datetime.datetime.now().strftime("%d %B %Y")
            response = f"Today is {today}"

        elif intent == "weather":
            response = "Opening weather information"
            action = "open_url"
            url = "https://www.google.com/search?q=weather"

        elif intent == "play_music":
            song = command.replace("play", "").replace("music", "").strip()

            if not song:
                song = "trending songs"

            response = f"Playing {song}"
            action = "open_url"
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(song)

        elif intent == "open_calculator":
            response = "Calculator command detected"
            action = "none"

        else:
            response = f"I detected the command: {intent}"

        return jsonify({
            "success": True,
            "response": response,
            "intent": intent,
            "action": action,
            "url": url
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "success": False,
            "response": "Something went wrong.",
            "intent": "",
            "action": ""
        }), 500


@app.route("/health")
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(debug=True)