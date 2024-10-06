from flask import Flask

_sandAnimation = None


def create_app(sandAnimation):
    global _sandAnimation
    _sandAnimation = sandAnimation
    app = Flask(__name__)
    with app.app_context():
        from app.routes.main import main_bp

        app.register_blueprint(main_bp)

    return app
