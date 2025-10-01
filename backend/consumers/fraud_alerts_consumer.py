# consumers/fraud_alerts_consumer.py
import json
from confluent_kafka import Consumer
from backend.database.db_handler import insert_fraud_alert  # <- adjust import path if needed

KAFKA_BROKER = "localhost:9092"
TOPICS = {
    "fraud_alerts": "fraud_alerts"
}

def start_consumer():
    consumer_config = {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "fraud-consumer-group",
        "auto.offset.reset": "earliest"
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([TOPICS["fraud_alerts"]])

    print("🚨 Fraud Alerts Consumer started. Listening for alerts...\n")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"❌ Consumer error: {msg.error()}")
                continue

            # Deserialize fraud alert
            alert = json.loads(msg.value().decode("utf-8"))
            print(f"⚠️ FRAUD ALERT RECEIVED: {alert}")

            # Safely handle alert message (fallback to "reason")
            alert_msg = alert.get("alert") or alert.get("reason") or "Unknown fraud detected"

            # ✅ Insert fraud alert into DB
            insert_fraud_alert(alert["user_id"], alert["amount"], alert_msg)

    except KeyboardInterrupt:
        print("🛑 Stopping fraud consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    start_consumer()
