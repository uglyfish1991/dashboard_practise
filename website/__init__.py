from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# this function is called when app.py runs, and is returned. Lets you do some config bits here

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    from .views import my_view

    app.register_blueprint(my_view)

    from .models import Salesfigures

    with app.app_context():
        db.create_all()

    return app