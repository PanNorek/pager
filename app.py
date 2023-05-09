from dotenv import load_dotenv
from flask import Flask, abort, make_response, redirect, render_template, request

load_dotenv()


app = Flask(__name__)


@app.route("/")
def index():
    """Handler for the application's root URL"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
