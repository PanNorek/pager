from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import re, os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from admin import adminpanel

load_dotenv()
email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

app = Flask(__name__)
app.register_blueprint(adminpanel, url_prefix='/admin')  # register admin blueprint (


app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)  # FIXME: temporary solution

db = SQLAlchemy(app=app)

app.app_context().push()


class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f'<User {self.name}>'

class Tweets(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(280), nullable=False) 
    
    def __init__(self, comment_id, text):
        self.comment_id = comment_id
        self.text = text
    
    def __repr__(self):
        return f'{self.text}'


@app.route("/")
def index():
    users = Users.query.filter(Users.name != None).all()

    context = {
        'users' : users
    }
    
    return render_template("index.html", **context)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("login.html")
    
    session.permanent = True
    session["user.login"] = request.form.get("email")
    
    found_user = Users.query.filter_by(email=request.form.get("email")).first()
    
    if found_user is None:
        flash("Invalid credentials!", "error")
        return redirect(url_for("login"))
    
    if found_user.password != request.form.get("password"):
        flash("Invalid credentials!", "error")
        return redirect(url_for("login"))
    
    if request.form.get("email") != os.getenv("SEED_LOGIN") or request.form.get("password") != os.getenv("SEED_PASSWORD"):
        flash("It works but only for admin!", "error")
        return redirect(url_for("login"))
        
    
    
    
    flash("Login succesful!", "message")
    # user = request.form["login"]
    return redirect(url_for("user"))
       

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method != "POST":
        return render_template("register.html")
    
    # block of code to register user 
    # TODO: connect to database and add user to database
    
    name = request.form.get("user.name")
    email = request.form.get("user.email")
    password = request.form.get("user.password")
    password2 = request.form.get("user.password_repeat")
    
    found_user = Users.query.filter_by(email=email).first()
    
    # TODO: validate user input
    if found_user is not None:
        flash("Email already registered!", "error")
        return redirect(url_for("register"))
    
    if password!=password2:
        flash("Passwords do not match!", "error")
        return redirect(url_for("register"))
    
    new_user = Users(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    flash("Registration succesful!", "message")
    return redirect(url_for("login"))

@app.route("/user")
def user():
    if "user.login" not in session:
        return redirect(url_for("login"))
    user = session["user.login"]
    return render_template("user.html", user=user)


@app.route("/logout")
def logout():
    session.pop("user.login", None)
    flash("You have been logged out!", "message")
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
