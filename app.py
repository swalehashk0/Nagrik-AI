from flask import Flask, jsonify, request
from flask_cors import CORS

from Services.ai_analyzer import analyze_complaint

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Nagrik-AI Backend is running"
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or not data.get("complaint_text"):
        return jsonify({
            "error": "complaint_text is required"
        }), 400

    complaint_text = data["complaint_text"]

    try:
        result = analyze_complaint(complaint_text)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)