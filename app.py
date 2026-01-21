from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = "hospital.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/patients")
def patients():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()
    conn.close()
    return render_template("patients.html", patients=patients)

@app.route("/add_patient", methods=["POST"])
def add_patient():
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)", (name, age, gender))
    conn.commit()
    conn.close()
    return redirect(url_for("patients"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
