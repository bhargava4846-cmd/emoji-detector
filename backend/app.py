from flask import Flask, request, jsonify
from flask_cors import CORS
from emoji_chain import detect_emojis

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Emoji Detector API is running!"})


@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Send JSON with a 'text' field"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400

    safe_search = data.get("safe_search", True)

    result = detect_emojis(text=text, safe_search=safe_search)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
