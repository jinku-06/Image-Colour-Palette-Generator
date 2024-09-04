from flask import Flask, redirect, render_template, request, flash, url_for
import os
from werkzeug.utils import secure_filename
from colorthief import ColorThief

app = Flask(__name__)
app.secret_key = "SDLKFJSADLKFJ"

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max file size
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, "static/uploads")  # Saving to 'static/uploads'
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpeg", "jpg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("File successfully uploaded")
            return redirect(url_for("home", file_name=filename))

    file_name = request.args.get("file_name", "")
    color_thief = ColorThief(file=f"static/uploads/{file_name}")
    palette = color_thief.get_palette(color_count=6)
    color_palette = [color for color in palette]

    return render_template(
        "index.html", file_name=file_name, color_palette=color_palette
    )


if __name__ == "__main__":
    app.run(debug=True)
