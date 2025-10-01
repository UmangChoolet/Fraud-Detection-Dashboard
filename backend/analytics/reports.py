import mysql.connector

# DB connection settings
DB_CONFIG = {
    "host": "localhost",
    "user": "root",         # change if you use another username
    "password": "S8ULGamechanger",  # replace with your MySQL password
    "database": "kafka_db"
}

def fetch_data(query):
    """Helper function to run SQL query and return results."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def generate_report():
    print("📊 Generating Analytics Report...\n")

    # Total transactions
    total_txn = fetch_data("SELECT COUNT(*) FROM transactions;")[0][0]
    print(f"📦 Total Transactions: {total_txn}")

    # Total fraud alerts
    total_alerts = fetch_data("SELECT COUNT(*) FROM fraud_alerts;")[0][0]
    print(f"🚨 Fraud Alerts: {total_alerts}")

    # Fraud percentage
    fraud_pct = (total_alerts / total_txn * 100) if total_txn > 0 else 0
    print(f"⚠️ Fraud Rate: {fraud_pct:.2f}%")

    # Average transaction amount
    avg_amount = fetch_data("SELECT AVG(amount) FROM transactions;")[0][0] or 0
    print(f"💰 Avg Transaction Amount: ${avg_amount:.2f}")

    # Top user by spending
    top_user = fetch_data("""
        SELECT user_id, SUM(amount) as total_spent
        FROM transactions
        GROUP BY user_id
        ORDER BY total_spent DESC
        LIMIT 1;
    """)
    if top_user:
        print(f"👑 Top User (Spending): User {top_user[0][0]} → ${top_user[0][1]:.2f}")

    # Most flagged user (fraud alerts)
    top_fraud_user = fetch_data("""
        SELECT user_id, COUNT(*) as alerts
        FROM fraud_alerts
        GROUP BY user_id
        ORDER BY alerts DESC
        LIMIT 1;
    """)
    if top_fraud_user:
        print(f"🚨 Most Flagged User: User {top_fraud_user[0][0]} ({top_fraud_user[0][1]} fraud alerts)")

    print("\n✅ Report generation complete!")

if __name__ == "__main__":
    generate_report()
