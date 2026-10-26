from flask import Flask, request, redirect, render_template_string
import mysql.connector
import os

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "appdb"),
        connection_timeout=5
    )


@app.route("/", methods=["GET", "POST"])
def home():
    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

        if request.method == "POST":
            message = request.form.get("message", "").strip()

            if message:
                cursor.execute(
                    "INSERT INTO notes (message) VALUES (%s)",
                    (message,)
                )
                db.commit()

            return redirect("/")

        cursor.execute(
            "SELECT id, message, created_at FROM notes ORDER BY id DESC"
        )
        notes = cursor.fetchall()

        return render_template_string("""
            <!doctype html>
            <html lang="id">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Tugas Individu Komputasi Awan</title>
            </head>
            <body>
                <h1>Tugas Individu Komputasi Awan</h1>
                <p>Aplikasi: Flask</p>
                <p>Database: MySQL</p>
                <p>Status database: Terhubung </p>

                <h2>Tambah Catatan</h2>
                <form method="post">
                    <input name="message" maxlength="255"
                           placeholder="Tulis catatan pengujian"
                           required>
                    <button type="submit">Simpan</button>
                </form>

                <h2>Data Tersimpan</h2>
                {% if notes %}
                    <ul>
                    {% for note in notes %}
                        <li>{{ note[1] }} — {{ note[2] }}</li>
                    {% endfor %}
                    </ul>
                {% else %}
                    <p>Belum ada catatan. Silakan tambahkan data uji.</p>
                {% endif %}
            </body>
            </html>
        """, notes=notes)

    except Exception:
        return (
            "<h1>Database belum siap atau terjadi kesalahan.</h1>",
            503
        )

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
