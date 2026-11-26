from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("portfolio.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not all([name, email, message]):
            flash("Please complete all fields.", "error")
        else:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                    (name, email, message)
                )
            flash("Thank you! Your message has been saved.", "success")
        return redirect(url_for("home") + "#contact")
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
