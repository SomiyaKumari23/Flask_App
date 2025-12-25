from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

messages = []  # temporary storage

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            messages.append(message)
        return redirect(url_for("index"))

    return render_template("index.html", messages=messages)

@app.route("/delete/<int:msg_id>", methods=["POST"])
def delete(msg_id):
    if 0 <= msg_id < len(messages):
        messages.pop(msg_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8022)
