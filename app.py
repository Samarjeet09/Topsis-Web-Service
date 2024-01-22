from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Mail, Message
import sys
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config.from_pyfile("secrets")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")


app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"csv", "xlsx"}
mail = Mail(app)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def topsis(df: pd.DataFrame, wts: str, impact: str) -> pd.DataFrame:
    wts = np.array(list(map(float, wts.split(","))))
    impact = np.array(impact.split(","))
    mat = np.array(df.iloc[:, 1:])
    rows, cols = mat.shape
    # mat / rootOfSumOfSquare * weight
    for i in range(cols):
        temp = 0
        for j in range(rows):
            temp += mat[j][i] ** 2
        temp = temp**0.5
        wts[i] /= temp

    weightedNormalized = mat * wts

    idealBestWorst = []  # (best,worst)

    for i in range(cols):
        maxi = weightedNormalized[:, i].max()
        mini = weightedNormalized[:, i].min()
        idealBestWorst.append((maxi, mini) if impact[i] == "1" else (mini, maxi))
    topsisScore = []
    for i in range(rows):
        temp_p, temp_n = 0, 0
        for j in range(cols):
            temp_p += (weightedNormalized[i][j] - idealBestWorst[j][0]) ** 2
            temp_n += (weightedNormalized[i][j] - idealBestWorst[j][1]) ** 2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        topsisScore.append(temp_n / (temp_p + temp_n))

    df["score"] = np.array(topsisScore).T
    df["rank"] = df["score"].rank(method="max", ascending=False)
    df["rank"] = df.astype({"rank": int})["rank"]
    return df


def send_email(result_df, to_email):
    msg = Message(
        "TOPSIS Result", sender="moyemoyemoye3@gmail.com", recipients=[to_email]
    )
    msg.body = "TOPSIS Result attached."

    with app.app_context():
        # Convert DataFrame to CSV format in-memory
        csv_data = result_df.to_csv(index=False)
        msg.attach("result.csv", "text/csv", csv_data)

        mail.send(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_file = None
        if "Input_File" in request.files:
            input_file = request.files["Input_File"]
            if input_file.filename == "":
                flash("No selected file", "error")
                return redirect(request.url)

            # Check if the "uploads" directory exists, create it if not
            if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                os.makedirs(app.config["UPLOAD_FOLDER"])

            if input_file and allowed_file(input_file.filename):
                filename = secure_filename(input_file.filename)
                input_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                input_file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            else:
                flash("Invalid file format. Allowed formats: csv, xlsx", "error")
                return redirect(request.url)

        weights = request.form["Weights"]
        impacts = request.form["Impacts"]

        ext = os.path.splitext(input_file_path)[-1]
        if ext in {".csv", ".xlsx"}:
            # read file
            try:
                if ext == ".csv":
                    input_file = pd.read_csv(input_file_path)
                elif ext == ".xlsx":
                    input_file = pd.read_excel(input_file_path)
                res = topsis(input_file, weights, impacts)
                to_email = request.form["Email"]
                try:
                    send_email(res, to_email)
                    flash("Email sent successfully!", "success")
                    print("q")
                    return render_template("result.html", table=res.to_html())

                except Exception as e:
                    flash(f"Error sending email: {e}", "error")

            except:
                flash("Error")
                jsonify({"status": "error", "message": "Error"})

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
