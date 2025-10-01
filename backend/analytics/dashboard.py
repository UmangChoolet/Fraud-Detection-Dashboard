import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_CONFIG = {
    "host": "localhost",
    "user": "root",          
    "password": "S8ULGamechanger",  
    "database": "kafka_db"   
}

def fetch_data(query):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def generate_dashboard():
    print("📊 Generating Fraud Analytics Dashboard...\n")

    # --- Fetch data ---
    transactions = fetch_data("SELECT * FROM transactions;")
    fraud_alerts = fetch_data("SELECT * FROM fraud_alerts;")

    # --- Plot 1: Transactions over time ---
    plt.figure(figsize=(10,5))
    sns.countplot(data=transactions, x="status")
    plt.title("Transaction Status Distribution")
    plt.show()

    # --- Plot 2: Fraud Alerts per User ---
    plt.figure(figsize=(10,5))
    sns.countplot(data=fraud_alerts, x="user_id")
    plt.title("Fraud Alerts per User")
    plt.xticks(rotation=45)
    plt.show()

    # --- Plot 3: Transaction Amounts Distribution ---
    plt.figure(figsize=(10,5))
    sns.histplot(transactions["amount"], bins=20, kde=True)
    plt.title("Transaction Amount Distribution")
    plt.show()

    # --- Plot 4: Fraud vs Non-Fraud Counts ---
    plt.figure(figsize=(6,6))
    labels = ["Fraud Alerts", "Legit Transactions"]
    sizes = [len(fraud_alerts), len(transactions) - len(fraud_alerts)]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Fraud vs Legit Transactions")
    plt.show()

    print("✅ Dashboard Generated Successfully!")

if __name__ == "__main__":
    generate_dashboard()
