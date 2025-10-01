from flask import Blueprint, request, jsonify
from confluent_kafka import Producer
import json
from backend.utils import KAFKA_BROKER, TOPICS

transactions_bp = Blueprint("transactions", __name__)

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

@transactions_bp.route("/add", methods=["POST"])
def add_transaction():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    if not user_id or not amount:
        return jsonify({"error": "Missing user_id or amount"}), 400

    transaction = {
        "user_id": int(user_id),
        "amount": float(amount),
        "status": "PENDING"   # 👈 consumer will update later
    }

    try:
        producer.produce(
            TOPICS["transactions"],
            value=json.dumps(transaction).encode("utf-8")
        )
        producer.flush()
        print(f"📤 Transaction sent: {transaction}")
        return jsonify({"message": "Transaction submitted"}), 201
    except Exception as e:
        print("❌ Error producing transaction:", e)
        return jsonify({"error": str(e)}), 500
