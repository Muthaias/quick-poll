from flask import Blueprint, request, abort, jsonify

poll = Blueprint("poll", __name__)
polls = []

@poll.route("/poll", methods=["POST", "GET"])
def create_poll():
    desc = request.form if request.form else request.args
    title = desc.get("title")
    owner = desc.get("owner")
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
    polls.append(owner)
    return jsonify(data)
