import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "S8ULGamechanger",
    "database": "kafka_db"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount FLOAT,
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount FLOAT,
            alert VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_transaction(user_id, amount, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, status) VALUES (%s, %s, %s)",
        (user_id, amount, status)
    )
    conn.commit()
    conn.close()


def insert_fraud_alert(user_id, amount, alert):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fraud_alerts (user_id, amount, alert) VALUES (%s, %s, %s)",
        (user_id, amount, alert)
    )
    conn.commit()
    conn.close()


def update_transaction_status(user_id, amount, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE transactions
            SET status = %s
            WHERE user_id = %s AND amount = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (new_status, user_id, amount))
        conn.commit()
        print(f"🔄 Transaction updated to {new_status} for user {user_id}, amount {amount}")
    except Exception as e:
        print(f"❌ Error updating transaction: {e}")
    finally:
        cursor.close()
        conn.close()
