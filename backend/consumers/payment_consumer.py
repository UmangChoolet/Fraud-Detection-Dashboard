# consumers/payment_consumer.py
import json
import time
from confluent_kafka import Consumer, Producer
from backend.database.db_handler import insert_transaction, update_transaction_status

# Redpanda Cloud Broker Config
KAFKA_BROKER = "d3gnh3scvm0i0evg9fdg.any.ap-south-1.mpx.prd.cloud.redpanda.com:9092"
SASL_USERNAME = "cGMDf8PA99i0pyJBNQjNSJrxQHEK2A0F"
SASL_PASSWORD = "lXeyTqUHGMZyCz4C0iqh5mYFRhMvFfzu-Yzmr4R_sc3kpTON4VXol_3fwzKTqZxX"

TOPICS = {
    "transactions": "transactions",
    "fraud_alerts": "fraud_alerts"
}

# Track user activity for fraud detection
recent_activity = {}
user_spending = {}
blacklist = {1234, 1500, 1999}


def detect_fraud(transaction):
    user_id = transaction["user_id"]
    amount = transaction["amount"]
    now = time.time()

    # Rule 1: High transaction
    if amount > 5000:
        return True, "High transaction amount"

    # Rule 2: Rapid transactions
    if user_id not in recent_activity:
        recent_activity[user_id] = []
    recent_activity[user_id].append(now)
    if len(recent_activity[user_id]) >= 3 and now - recent_activity[user_id][-3] < 10:
        return True, "Rapid multiple transactions"

    # Rule 3: Spending spike
    avg = user_spending.get(user_id, amount)
    if amount > 10 * avg:
        return True, "Unusual spike in spending"
    user_spending[user_id] = (avg + amount) / 2

    # Rule 4: Blacklist
    if user_id in blacklist:
        return True, "Blacklisted user"

    return False, None


def start_consumer():
    consumer_config = {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "payment-consumer-group",
        "auto.offset.reset": "earliest",
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": SASL_USERNAME,
        "sasl.password": SASL_PASSWORD
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([TOPICS["transactions"]])

    producer_config = {
        "bootstrap.servers": KAFKA_BROKER,
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": SASL_USERNAME,
        "sasl.password": SASL_PASSWORD
    }
    producer = Producer(producer_config)

    print("🚀 Payment Consumer started. Listening for transactions...\n")

    try:
        while True:
            msg = consumer.poll(2.0)  # slightly increased timeout for CPU efficiency
            if msg is None:
                continue
            if msg.error():
                print(f"❌ Consumer error: {msg.error()}")
                continue

            transaction = json.loads(msg.value().decode("utf-8"))
            print(f"✅ Received transaction: {transaction}")

            # Insert into DB as SUCCESS initially
            insert_transaction(transaction["user_id"], transaction["amount"], transaction["status"])

            # Fraud detection
            is_fraud, reason = detect_fraud(transaction)
            if is_fraud:
                # Update DB to FAILED
                update_transaction_status(transaction["user_id"], transaction["amount"], "FAILED")

                alert = {
                    "user_id": transaction["user_id"],
                    "amount": transaction["amount"],
                    "alert": f"🚨 Fraud detected! Reason: {reason}"
                }
                producer.produce(TOPICS["fraud_alerts"], value=json.dumps(alert).encode("utf-8"))
                print(f"⚠️ Fraud alert sent: {alert}")
            else:
                print(f"💰 Transaction processed successfully: {transaction}")

            producer.flush()

    except KeyboardInterrupt:
        print("🛑 Stopping payment consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    start_consumer()
