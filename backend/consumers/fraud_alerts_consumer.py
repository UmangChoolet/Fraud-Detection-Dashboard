# consumers/fraud_alerts_consumer.py
import json
from confluent_kafka import Consumer
from backend.database.db_handler import insert_fraud_alert

# Redpanda Cloud Broker Config
KAFKA_BROKER = "d3gnh3scvm0i0evg9fdg.any.ap-south-1.mpx.prd.cloud.redpanda.com:9092"
SASL_USERNAME = "cGMDf8PA99i0pyJBNQjNSJrxQHEK2A0F"
SASL_PASSWORD = "lXeyTqUHGMZyCz4C0iqh5mYFRhMvFfzu-Yzmr4R_sc3kpTON4VXol_3fwzKTqZxX"

TOPICS = {
    "fraud_alerts": "fraud_alerts"
}

def start_consumer():
    consumer_config = {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "fraud-consumer-group",
        "auto.offset.reset": "earliest",
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "SCRAM-SHA-256",
        "sasl.username": SASL_USERNAME,
        "sasl.password": SASL_PASSWORD
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([TOPICS["fraud_alerts"]])

    print("🚨 Fraud Alerts Consumer started. Listening for alerts...\n")

    try:
        while True:
            msg = consumer.poll(2.0)  # slightly increased timeout for CPU efficiency
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

            # Insert fraud alert into DB
            insert_fraud_alert(alert["user_id"], alert["amount"], alert_msg)

    except KeyboardInterrupt:
        print("🛑 Stopping fraud consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    start_consumer()
