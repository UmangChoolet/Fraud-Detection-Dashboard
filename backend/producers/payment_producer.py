# producers/payment_producer.py
from confluent_kafka import Producer
import json

TOPIC = "transactions"

conf = {
    "bootstrap.servers": "d3gnh3scvm0i0evg9fdg.any.ap-south-1.mpx.prd.cloud.redpanda.com:9092",
    "sasl.mechanisms": "SCRAM-SHA-256",
    "security.protocol": "SASL_SSL",
    "sasl.username": "cGMDf8PA99i0pyJBNQjNSJrxQHEK2A0F",
    "sasl.password": "lXeyTqUHGMZyCz4C0iqh5mYFRhMvFfzu-Yzmr4R_sc3kpTON4VXol_3fwzKTqZxX"
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

def send_transaction(user_id, amount, status="PENDING"):
    transaction = {
        "user_id": user_id,
        "amount": float(amount),
        "status": status
    }
    producer.produce(
        TOPIC,
        key=str(user_id),
        value=json.dumps(transaction),
        callback=delivery_report
    )
    producer.flush()
    print(f"📤 Transaction sent: {transaction}")

# ⚠️ No infinite loop here!
if __name__ == "__main__":
    print("Run this only if you want CLI-based testing.")
