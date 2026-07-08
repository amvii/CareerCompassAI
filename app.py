from flask import Flask, render_template, request
from ml.recommender import get_recommendations
from ml.resume_parser import extract_text_from_resume
from ml.skill_extractor import extract_skills
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/skills")
def skills():
    return render_template("skills.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    user_skills = request.form["skills"]

    recommendations = get_recommendations(user_skills)

    return render_template(
        "results.html",
        user_skills=user_skills,
        recommendations=recommendations
    )


@app.route("/upload", methods=["POST"])
def upload():

    resume = request.files["resume"]

    if resume:

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume.filename
        )

        resume.save(file_path)

        resume_text = extract_text_from_resume(file_path)

        extracted_skills = extract_skills(resume_text)

        recommendations = get_recommendations(
            ",".join(extracted_skills)
        )

        return render_template(
            "results.html",
            user_skills=", ".join(extracted_skills),
            recommendations=recommendations
        )

    return "No file uploaded."


if __name__ == "__main__":
    app.run(debug=True, port=5001)