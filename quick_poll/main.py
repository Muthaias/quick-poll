from flask import Flask, jsonify
from uuid import uuid4
import os
import json
from quick_poll.endpoints.poll import poll

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    db_uri = "sqlite:///%s/%s" % (app.instance_path, "quick-poll.db")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )
    config_path = os.path.join(app.instance_path, "config.json")
    try:
        if os.path.exists(config_path):
            print(" * Loading instance config file: %s" % config_path)
            with open(config_path, 'r') as config:
                data = json.loads(config.read())
                app.config.update(data)
        else:
            print(" * No config file. Using defaults.")
    except:
        print(" * Failed to load config file.")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from quick_poll.models import db
    db.init_app(app)

    app.register_blueprint(poll)

    app_id = app.config.get("QUICKPOLL_ID", str(uuid4()))
    @app.route('/')
    def api_root():
        return jsonify({
            "message": "Welcome to the QuickPoll API root",
            "id": app_id
        })

    return app