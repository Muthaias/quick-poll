from flask import Blueprint, request, abort, jsonify
from auth import auth

poll = Blueprint("poll", __name__)
polls = []

@poll.route("/poll", methods=["POST", "GET"])
@auth.login_required
def create_poll():
    owner = auth.current_user()
    desc = request.form if request.form else request.args
    title = desc.get("title")
    i = 0
    options = []
    option = None
    try:
        option = desc.get("option%d" % i)
    except:
        pass
    while option:
        options.append(option)
        i = i + 1
        try:
            option = desc.get("option%d" % i)
        except:
            pass
    if owner == None or title == None:
        abort(400)
    data = {
        "id": len(polls),
        "owner": owner,
        "title": title,
        "option": options
    }
    polls.append(data)
    return jsonify(data)

@poll.route("/poll", methods=["POST", "GET"])
@auth.login_required
def update_poll():


@poll.route("/polls", methods=["GET"])
@auth.login_required
def list_polls():
    owner = auth.current_user()
    return jsonify([poll for poll in polls if poll["owner"] == owner])
