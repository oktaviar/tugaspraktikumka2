
from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST", "db"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "appuser"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "appdb"),
            connection_timeout=5
        )

        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        db.close()

        return f"""
        <h1>Tugas Individu Komputasi Awan</h1>
        <p>Aplikasi: Flask</p>
        <p>Database: MySQL</p>
        <p>Status database: Terhubung </p>
        <p>Hasil pengujian database: {result}</p>
        """
    except Exception:
        return """
        <h1>Tugas Individu Komputasi Awan</h1>
        <p>Status database: Belum terhubung </p>
        """, 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
