import mysql.connector

# FreeSQLDatabase credentials
DB_CONFIG = {
    "host": "sql5.freesqldatabase.com",
    "user": "sql5801326",
    "password": "FDpCLkdkHI",
    "database": "sql5801326",
    "port": 3306
}

def get_connection():
    """Establish and return a database connection"""
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    """Create tables if they don't exist (structure matches imported SQL)"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount DECIMAL(10,2),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount DECIMAL(10,2),
            alert VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def insert_transaction(user_id, amount, status):
    """Insert a new transaction"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, status) VALUES (%s, %s, %s)",
        (user_id, amount, status)
    )
    conn.commit()
    cursor.close()
    conn.close()


def insert_fraud_alert(user_id, amount, alert):
    """Insert a new fraud alert"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fraud_alerts (user_id, amount, alert) VALUES (%s, %s, %s)",
        (user_id, amount, alert)
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_transaction_status(user_id, amount, new_status):
    """
    Update the latest transaction with given user_id and amount.
    Uses subquery for FreeSQLDatabase compatibility.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE transactions t
            JOIN (
                SELECT id FROM transactions
                WHERE user_id = %s AND amount = %s
                ORDER BY created_at DESC
                LIMIT 1
            ) sub ON t.id = sub.id
            SET t.status = %s
        """, (user_id, amount, new_status))
        conn.commit()
        print(f"🔄 Transaction updated to {new_status} for user {user_id}, amount {amount}")
    except Exception as e:
        print(f"❌ Error updating transaction: {e}")
    finally:
        cursor.close()
        conn.close()
