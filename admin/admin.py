from flask import Blueprint, render_template, request, redirect, url_for, flash, session


adminpanel = Blueprint("adminpanel", __name__, template_folder="templates")


@adminpanel.route("/")
def index():
    return render_template("adminpanel.html")
