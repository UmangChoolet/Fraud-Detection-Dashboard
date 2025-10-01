💳 Kafka Fraud Detection System

A real-time fraud detection system built with Apache Kafka, Flask, React, and SQLite.
It simulates payment transactions, stores them in a database, and detects fraudulent activities based on predefined rules.

🚀 Features

-> Add transactions via UI or random generator.

-> Real-time fraud detection with Kafka consumers.

-> Fraud alerts stored and displayed on the dashboard.

Rules include:

-> High-value transactions

-> Rapid multiple transactions

-> Spending spikes

-> Blacklisted users

-> Clean dashboard for transactions and fraud alerts.

🛠 Tech Stack

-> Backend: Flask, Kafka Producer/Consumer (Python)

-> Frontend: React

-> Database: SQLite

-> Messaging: Apache Kafka

⚙️ Setup
1️⃣ Clone the project
git clone https://github.com/<your-username>/kafka_project.git
cd kafka_project

2️⃣ Start Kafka & Zookeeper
zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties

3️⃣ Install backend dependencies
cd backend
pip install -r requirements.txt

4️⃣ Install frontend dependencies
cd frontend
npm install

5️⃣ Run the backend

Open 3 terminals:

# Terminal 1

python app.py

# Terminal 2

python consumers/payment_consumer.py

# Terminal 3

python consumers/fraud_alerts_consumer.py

6️⃣ Run the frontend
cd frontend
npm start

Visit 👉 http://localhost:3000

🗄 Database Schema

-> transactions

-> id (PK)

-> user_id

-> amount

-> status

-> fraud_alerts

-> id (PK)

-> user_id

-> amount

-> alert

📊 Usage

-> Submit transactions from UI.

-> Consumers process & store them in DB.

-> Fraud alerts appear in dashboard when triggered.

🚧 Future Enhancements

-> Docker support

-> Cloud deployment

-> Authentication

-> Advanced ML-based fraud detection
