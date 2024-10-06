from flask import render_template
from app import _sandAnimation as sandAnimation

def index():
    return render_template('index.html')

def start():
    # global sandAnimation
    if sandAnimation:
        sandAnimation.start_stop_click()
        return "SandAnimation started"
    else:
        return "SandAnimation not initialized", 500
    
def angle():
    # global sandAnimation
    if sandAnimation:
        sandAnimation.set_angle()
        return "Angle set"
    else: 
        return "SandAnimation not initialized", 500
    