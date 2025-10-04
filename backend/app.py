from flask import Flask, jsonify, request
from flask_cors import CORS
from database.db_handler import get_connection
from producers.payment_producer import producer, delivery_report, TOPIC
import json

app = Flask(__name__)
CORS(app, origins=["https://umangchoolet.github.io"], supports_credentials=True, methods=["GET","POST"])


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Fraud Detection API",
        "endpoints": [
            "/transactions/summary",
            "/frauds/alerts",
            "/users/top",
            "/frauds/recent",
            "/transactions/distribution",
            "/transactions/add (POST)"
        ]
    })


@app.route("/transactions/summary", methods=["GET"])
def transactions_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(amount) FROM transactions")
    avg_amount = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM fraud_alerts")
    fraud_transactions = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    fraud_rate = round(float(fraud_transactions) / float(total_transactions), 3) if total_transactions > 0 else 0.0

    return jsonify({
        "total_transactions": int(total_transactions),
        "fraud_transactions": int(fraud_transactions),
        "avg_amount": round(float(avg_amount), 2),
        "fraud_rate": fraud_rate
    })


@app.route("/frauds/alerts", methods=["GET"])
def frauds_alerts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE(created_at) AS date, COUNT(*) AS alerts
        FROM fraud_alerts
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at) ASC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{"date": str(row["date"]), "alerts": int(row["alerts"])} for row in data])


@app.route("/users/top", methods=["GET"])
def top_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT user_id, SUM(amount) AS total_spent, COUNT(*) as tx_count
        FROM transactions
        GROUP BY user_id
        ORDER BY total_spent DESC
        LIMIT 10
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([
        {"user_id": int(r["user_id"]), "total_spent": float(r["total_spent"]), "tx_count": int(r["tx_count"])}
        for r in data
    ])


@app.route("/frauds/recent", methods=["GET"])
def recent_frauds():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT user_id, amount, alert, created_at
        FROM fraud_alerts
        ORDER BY created_at DESC
        LIMIT 20
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{
        "user_id": int(r["user_id"]),
        "amount": float(r["amount"]),
        "alert": r["alert"],
        "created_at": str(r["created_at"])
    } for r in data])


@app.route("/transactions/distribution", methods=["GET"])
def transaction_distribution():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM transactions
        GROUP BY status
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{"status": r["status"], "count": int(r["count"])} for r in data])


# 🚀 Clean single endpoint for new transactions
@app.route("/transactions/add", methods=["POST"])
def add_transaction():
    try:
        data = request.json
        user_id = data.get("user_id")
        amount = float(data.get("amount"))

        if not user_id or not amount:
            return jsonify({"error": "Missing user_id or amount"}), 400

        # Build transaction (default as SUCCESS)
        transaction = {
            "user_id": int(user_id),
            "amount": float(amount),
            "status": "SUCCESS"
        }

        # ✅ Send to Kafka using payment_producer's producer
        producer.produce(TOPIC, json.dumps(transaction).encode("utf-8"), callback=delivery_report)
        producer.flush()

        print(f"📤 Transaction sent from Flask: {transaction}")

        return jsonify({
            "message": "Transaction submitted",
            "user_id": user_id,
            "amount": amount
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
