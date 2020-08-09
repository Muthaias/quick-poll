from flask import Flask, jsonify
from flask_session import Session
from uuid import uuid4
import os
import json
from quick_poll.endpoints.poll import poll
from quick_poll.endpoints.user import user


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    db_uri = "sqlite:///%s/%s" % (app.instance_path, "quick-poll.db")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE="redis",
        SESSION_PERMANENT=False,
    )
    Session(app)
    config_path = os.path.join(app.instance_path, "config.json")
    try:
        with open(config_path, 'r') as config:
            print(" * Loading instance config file: %s" % config_path)
            try:
                data = json.loads(config.read())
                app.config.update(data)
            except json.JSONDecodeError:
                print(" * Failed to load config file.")
    except IOError:
        print(" * No config file. Using defaults.")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from quick_poll.models import db
    db.init_app(app)

    app.register_blueprint(poll)
    app.register_blueprint(user)

    app_id = app.config.get("QUICKPOLL_ID", str(uuid4()))

    @app.route('/')
    def api_root():
        return jsonify({
            "message": "Welcome to the QuickPoll API root",
            "id": app_id
        })

    return app
