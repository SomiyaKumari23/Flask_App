from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lionattack@123",
    database="flask_app"
)
cursor = db.cursor(dictionary=True) 

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

    cursor.execute("SELECT content FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()
    return render_template("index.html", messages=messages)

@app.route("/delete/<int:msg_id>", methods=["POST"])
def delete(msg_id):
    cursor.execute("DELETE FROM messages WHERE id = %s", (msg_id,))
    db.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8022)
