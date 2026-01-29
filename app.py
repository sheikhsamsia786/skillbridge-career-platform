from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
import json

app = Flask(__name__)
app.secret_key = "skillbridge_secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="skillbridge"
)
cursor = db.cursor(dictionary=True)


# ---------------- CREATE ROADMAP ----------------
@app.route("/create-roadmap", methods=["GET", "POST"])
def create_roadmap():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        steps = request.form.getlist("steps[]")

        steps_data = [{"text": s, "done": False} for s in steps]

        user_id = 1  # demo user

        cursor.execute(
            "INSERT INTO custom_roadmaps (user_id, title, description, steps_json) VALUES (%s, %s, %s, %s)",
            (user_id, title, description, json.dumps(steps_data))
        )
        db.commit()

        return redirect("/my-roadmaps")

    return render_template("create_roadmap.html")


# ---------------- SHOW ROADMAPS ----------------
@app.route("/my-roadmaps")
def my_roadmaps():
    user_id = 1

    cursor.execute(
        "SELECT * FROM custom_roadmaps WHERE user_id=%s",
        (user_id,)
    )
    roadmaps = cursor.fetchall()

    for r in roadmaps:
        if r["steps_json"]:                      # ✅ IMPORTANT LINE
            r["steps"] = json.loads(r["steps_json"])
        else:
            r["steps"] = []                      # ✅ prevents crash

    return render_template("my_roadmaps.html", roadmaps=roadmaps)


# ---------------- UPDATE PROGRESS (AJAX) ----------------
@app.route("/update-progress", methods=["POST"])
def update_progress():
    data = request.get_json()

    roadmap_id = data["roadmap_id"]
    steps = data["steps"]

    cursor.execute(
        "UPDATE custom_roadmaps SET steps_json=%s WHERE id=%s",
        (json.dumps(steps), roadmap_id)
    )
    db.commit()

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)
