from flask import Blueprint, request, abort, jsonify
from auth import auth
from uuid import uuid4

poll = Blueprint("poll", __name__)
polls = []

def _get_options(desc):
    options = []
    option = None
    print(desc)
    i = 0
    option = desc.get("option%d" % i)
    while option:
        options.append(option)
        i = i + 1
        option = desc.get("option%d" % i)
    print(options)
    return options

@poll.route("/poll", methods=["POST", "GET"])
@auth.login_required
def create_poll():
    owner = auth.current_user()
    desc = request.form if request.form else request.args
    title = desc.get("title")
    options = _get_options(desc)

    if owner == None or title == None:
        abort(400)

    data = {
        "id": str(uuid4()),
        "owner": owner,
        "title": title,
        "options": options
    }
    polls.append(data)
    return jsonify(data)

@poll.route("/poll/<poll_id>", methods=["POST", "GET"])
@auth.login_required
def update_poll(poll_id: str):
    print(poll_id, polls)
    desc = request.form if request.form else request.args
    title = desc.get("title")
    options = _get_options(desc)
    data = next((poll for poll in polls if poll["id"] == poll_id), None)

    if data == None:
        abort(400)

    data["title"] = title or data["title"]
    data["options"] = options or data["options"]
    
    return jsonify(data)



@poll.route("/polls", methods=["GET"])
@auth.login_required
def list_polls():
    owner = auth.current_user()
    return jsonify([poll for poll in polls if poll["owner"] == owner])
