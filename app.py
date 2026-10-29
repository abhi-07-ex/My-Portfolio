from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Abhi07@@',
    'database': 'abhi'
}

@app.route('/submit', methods=['POST'])
def save_contact():
    data = request.get_json(silent=True) or request.form
    name = data.get('txName') or data.get('name')
    email = data.get('txEmail') or data.get('email')
    message = data.get('txMessage') or data.get('message')

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO contact_submissions (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Saved to database"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Database sync bridge active on http://127.0.0.1:5000")
    app.run(port=5000)