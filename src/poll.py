from flask import Blueprint, request, abort, jsonify
from auth import auth
from models.poll_model import db, Poll, PollOption

poll = Blueprint("poll", __name__)

@poll.route("/poll", methods=["POST"])
@auth.login_required
def create_poll():
    owner = auth.current_user()
    desc = request.json if request.json else request.form
    title = desc.get("title")
    options = desc.get("options")

    if owner == None or title == None:
        abort(400)

    poll = Poll(title = title, owner = owner)
    poll_options = [PollOption(value = option, poll=poll) for option in options]
    db.session.add(poll)
    db.session.commit()
    return jsonify({
        "id": poll.id
    })

@poll.route("/poll/<poll_id>", methods=["POST"])
@auth.login_required
def update_poll(poll_id: str):
    desc = request.json if request.json else request.form
    title = desc.get("title")
    options = desc.get("options")

    poll = db.session.query(Poll).outerjoin(Poll.options).filter(Poll.id == poll_id).first()
    poll.title = title or poll.title
    poll_options = [PollOption(value = option, poll=poll) for option in options]
    poll.options = poll_options
    db.session.commit()

    return jsonify({
        "id": poll.id,
        "title": poll.title,
        "owner": poll.owner,
        "options": [option.value for option in poll.options]
    })

@poll.route("/poll/<poll_id>", methods=["DELETE"])
@auth.login_required
def delete_poll(poll_id: str):
    poll = db.session.query(Poll).filter(Poll.id == poll_id).first()
    db.session.delete(poll)
    db.session.commit()
    return jsonify({
        "id": poll_id
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
            "options": [option.value for option in poll.options]
        } for poll in polls
    ])
