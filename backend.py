from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_db_connection

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "Nagrik-AI Backend is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/complaints", methods=["POST"])
def create_complaint():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    citizen_name = data.get("citizen_name")
    citizen_email = data.get("citizen_email")
    complaint_text = data.get("complaint_text")

    if not citizen_name or not complaint_text:
        return jsonify({
            "error": "citizen_name and complaint_text are required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (
            citizen_name,
            citizen_email,
            complaint_text
        )
        VALUES (?, ?, ?)
    """, (
        citizen_name,
        citizen_email,
        complaint_text
    ))

    complaint_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Complaint submitted successfully",
        "complaint_id": complaint_id
    }), 201
    
@app.route("/complaints", methods=["GET"])
def get_complaints():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        ORDER BY created_at DESC
    """)

    complaints = cursor.fetchall()

    conn.close()

    return jsonify([
        dict(complaint)
        for complaint in complaints
    ])

if __name__ == "__main__":
    app.run(debug=True)