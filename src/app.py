from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

load_dotenv()


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Handler for the application's root URL"""
    # if request.method == "POST":
    #     flash("Form submitted successfully")
    #     redirect(url_for("/"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
