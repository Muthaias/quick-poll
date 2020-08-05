from flask import Blueprint, request, abort, jsonify
from auth import auth
from models.poll_model import db, Poll, PollOption

poll = Blueprint("poll", __name__)

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

    poll = Poll(title = title, owner = owner)
    poll_options = [PollOption(value = option, poll=poll) for option in options]
    db.session.add(poll)
    db.session.commit()
    return jsonify({
        "id": poll.id
    })

@poll.route("/poll/<poll_id>", methods=["POST", "GET"])
@auth.login_required
def update_poll(poll_id: str):
    desc = request.form if request.form else request.args
    title = desc.get("title")
    options = _get_options(desc)

    poll = db.session.query(Poll).outerjoin(Poll.options).filter(Poll.id == poll_id).first()
    poll.title = title or poll.title
    poll_options = [PollOption(value = option, poll=poll) for option in options]
    poll.options = poll_options
    db.session.commit()

    return jsonify({
        "id": poll.id,
        "title": poll.title,
        "owner": poll.owner,
        "option": [option.value for option in poll.options]
    })


@poll.route("/polls", methods=["GET"])
@auth.login_required
def list_polls():
    owner = auth.current_user()
    polls = db.session.query(Poll).outerjoin(Poll.options).filter(Poll.owner == owner).all()
    return jsonify([
        {
            "id": poll.id,
            "title": poll.title,
            "owner": poll.owner,
            "option": [option.value for option in poll.options]
        } for poll in polls
    ])
