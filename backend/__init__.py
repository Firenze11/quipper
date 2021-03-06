from flask import Flask
from flask import request
from flask_cors import CORS
import os


def create_app(test_config=None):

    app = Flask(__name__)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY="dev",
        # Todo: add db
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # Todo: load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import routes

    app.register_blueprint(routes.bp)

    return app
