from flask import render_template
from app.flask_init import _sandAnimation as sandAnimation


def index():
    return render_template("index.html")


def start():
    if sandAnimation:
        sandAnimation.start_stop_click()
        return "SandAnimation started"
    else:
        return "SandAnimation not initialized", 500


def angle():
    if sandAnimation:
        sandAnimation.set_angle()
        return "Angle set"
    else:
        return "SandAnimation not initialized", 500
