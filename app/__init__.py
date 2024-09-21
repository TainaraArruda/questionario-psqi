from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.controllers import quiz_controller
    from app.controllers import auth_controller
    app.register_blueprint(quiz_controller.bp)
    app.register_blueprint(auth_controller.bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

from app.models.user import User
from app.models.quiz import Quiz