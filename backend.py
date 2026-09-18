from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from database import get_db_connection
from Services.ai_analyzer import analyze_complaint

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


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

    try:
        ai_result = analyze_complaint(complaint_text)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (
            citizen_name,
            citizen_email,
            complaint_text,
            category,
            priority,
            department,
            summary,
            confidence,
            urgency_reason,
            location,
            suggested_action
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        citizen_name,
        citizen_email,
        complaint_text,
        ai_result["category"],
        ai_result["priority"],
        ai_result["department"],
        ai_result["summary"],
        ai_result["confidence"],
        ai_result["urgency_reason"],
        ai_result["location"],
        ai_result["suggested_action"]
    ))

    complaint_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Complaint submitted successfully",
        "complaint_id": complaint_id,
        "category": ai_result["category"],
        "priority": ai_result["priority"],
        "department": ai_result["department"],
        "summary": ai_result["summary"],
        "confidence": ai_result["confidence"],
        "urgency_reason": ai_result["urgency_reason"],
        "location": ai_result["location"],
        "suggested_action": ai_result["suggested_action"],
        "status": "Pending"
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
    
@app.route("/complaints/<int:complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE id = ?
    """, (complaint_id,))

    complaint = cursor.fetchone()

    conn.close()

    if complaint is None:
        return jsonify({
            "error": "Complaint not found"
        }), 404

    return jsonify(dict(complaint))

@app.route("/complaints/<int:complaint_id>/status", methods=["PUT"])
def update_status(complaint_id):
    data = request.get_json()

    if not data or not data.get("status"):
        return jsonify({
            "error": "status is required"
        }), 400

    status = data.get("status")

    allowed_statuses = {
        "Pending",
        "Assigned",
        "In Progress",
        "Resolved"
    }

    if status not in allowed_statuses:
        return jsonify({
            "error": "Invalid status"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, complaint_id))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({
            "error": "Complaint not found"
        }), 404

    cursor.execute("""
        INSERT INTO complaint_updates (
            complaint_id,
            status,
            note
        )
        VALUES (?, ?, ?)
    """, (
        complaint_id,
        status,
        "Status updated by officer"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Complaint status updated successfully",
        "complaint_id": complaint_id,
        "status": status
    })


@app.route("/complaints/<int:complaint_id>/history", methods=["GET"])
def get_complaint_history(complaint_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, complaint_id, status, note, updated_at
        FROM complaint_updates
        WHERE complaint_id = ?
        ORDER BY updated_at ASC
    """, (complaint_id,))

    updates = cursor.fetchall()

    conn.close()

    return jsonify([
        dict(update)
        for update in updates
    ])
@app.route("/escalations", methods=["GET"])
def get_escalations():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE priority = 'Urgent'
        AND status != 'Resolved'
        ORDER BY created_at ASC
    """)

    complaints = cursor.fetchall()

    conn.close()

    return jsonify([
        dict(complaint)
        for complaint in complaints
    ])
@app.route("/analytics", methods=["GET"])
def get_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM complaints")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM complaints
        GROUP BY status
    """)
    status_data = {
        row["status"]: row["count"]
        for row in cursor.fetchall()
    }

    cursor.execute("""
        SELECT category, COUNT(*) AS count
        FROM complaints
        GROUP BY category
    """)
    category_data = {
        row["category"]: row["count"]
        for row in cursor.fetchall()
    }

    conn.close()

    return jsonify({
        "total_complaints": total,
        "status_counts": status_data,
        "category_counts": category_data
    })
if __name__ == "__main__":
    app.run(debug=True)