from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from dotenv import load_dotenv
from time import sleep

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Retry logic for MySQL connection
db = None
for i in range(10):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Connected to MySQL!")
        break
    except mysql.connector.Error as err:
        print(f"MySQL connection failed, retrying... ({i+1}/10)")
        sleep(3)

if db is None:
    raise Exception("Could not connect to MySQL after multiple attempts.")

cursor = db.cursor(dictionary=True)

# Ensure the 'messages' table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL
)
""")
db.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            cursor.execute(
                "INSERT INTO messages (content) VALUES (%s)",
                (message,)
            )
            db.commit()
        return redirect(url_for("index"))

    cursor.execute("SELECT id, content FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()
    return render_template("index.html", messages=messages)

@app.route("/delete/<int:msg_id>", methods=["POST"])
def delete(msg_id):
    cursor.execute("DELETE FROM messages WHERE id = %s", (msg_id,))
    db.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
