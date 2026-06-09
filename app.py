from jinja2 import Environment
from flask import Flask, render_template, request
from model import predict_result
from database import (create_database, get_top_students, get_pass_fail_count,
                      get_gender_stats, get_subject_difficulty, get_overall_stats)

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)
create_database()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    math = int(request.form["math"])
    reading = int(request.form["reading"])
    writing = int(request.form["writing"])

    result, confidence = predict_result(math, reading, writing)
    label = "Pass ✅" if result == 1 else "Fail ❌"

    return render_template("index.html",
                           prediction=label,
                           confidence=confidence,
                           math=math,
                           reading=reading,
                           writing=writing)

@app.route("/dashboard")
def dashboard():
    top_students = get_top_students().to_dict(orient="records")
    pass_fail = get_pass_fail_count()
    pass_count = next((c for pf, c in pass_fail if pf == 1), 0)
    fail_count = next((c for pf, c in pass_fail if pf == 0), 0)
    pass_rate = round((pass_count / (pass_count + fail_count)) * 100, 1)
    gender_stats = get_gender_stats().to_dict(orient="records")
    subject_diff = get_subject_difficulty()
    overall = get_overall_stats()

    return render_template("dashboard.html",
                           top_students=top_students,
                           pass_count=pass_count,
                           fail_count=fail_count,
                           pass_rate=pass_rate,
                           gender_stats=gender_stats,
                           subject_diff=subject_diff,
                           overall=overall)

if __name__ == "__main__":
    app.run(debug=True)