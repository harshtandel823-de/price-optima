from flask import Flask, request, jsonify
from db import create_table, get_db_connection

app = Flask(__name__)
create_table()

@app.route("/")
def home():
    return {"message": "Transaction API is running"}

@app.route("/transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()

    if not data or "amount" not in data or "type" not in data:
        return {"error": "Invalid input"}, 400

    amount = data["amount"]
    tx_type = data["type"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (amount, type, timestamp) VALUES (?, ?, datetime('now'))",
        (amount, tx_type)
    )

    conn.commit()
    conn.close()

    return {"message": "Transaction added successfully"}, 201

@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])



@app.route("/analytics", methods=["GET"])
def analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total transactions
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]

    # Total debit amount
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'debit'"
    )
    total_debit = cursor.fetchone()[0]

    # Total credit amount
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'credit'"
    )
    total_credit = cursor.fetchone()[0]

    # Count by type
    cursor.execute(
        "SELECT type, COUNT(*) as count FROM transactions GROUP BY type"
    )
    type_counts = cursor.fetchall()

    conn.close()

    breakdown = {}
    for row in type_counts:
        breakdown[row["type"]] = row["count"]

    return jsonify({
        "total_transactions": total_transactions,
        "total_debit_amount": total_debit,
        "total_credit_amount": total_credit,
        "transactions_by_type": breakdown
    })

if __name__ == "__main__":
    app.run(debug=True)
