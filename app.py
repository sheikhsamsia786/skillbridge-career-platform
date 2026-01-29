from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "skillbridge_secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skillbridge"
)
cursor = db.cursor(dictionary=True)

@app.route("/create-roadmap", methods=["GET", "POST"])
def create_roadmap():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        steps = request.form.getlist("steps[]")
        steps_str = ",".join(steps)

        user_id = session.get("user_id", 1)  # demo user

        cursor.execute(
            "INSERT INTO custom_roadmaps (user_id, title, description, steps) VALUES (%s, %s, %s, %s)",
            (user_id, title, description, steps_str)
        )
        db.commit()

        return redirect("/dashboard")

    return render_template("create_roadmap.html")


@app.route("/my-roadmaps")
def my_roadmaps():
    user_id = session.get("user_id", 1)

    cursor.execute(
        "SELECT * FROM custom_roadmaps WHERE user_id=%s",
        (user_id,)
    )
    roadmaps = cursor.fetchall()

    return render_template("my_roadmaps.html", roadmaps=roadmaps)
