from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Snakebite@123",
        database="flask_app"
    )
    print("Connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")

cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form["message"]
        cursor.execute(
            "INSERT INTO messages (content) VALUES (%s)",
            (message,)
        )
        db.commit()
        return redirect("/")

    cursor.execute("SELECT content FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True,port=8022)
