from flask import Blueprint, request, abort, jsonify, url_for
from .auth import auth
from ..models.poll_model import db, Poll, PollOption

poll = Blueprint("poll", __name__)

def _poll_to_data(poll):
    return {
        "id": poll.id,
        "url": url_for("poll.read_poll", poll_id = poll.id),
        "title": poll.title,
        "owner": poll.owner,
        "options": [{
            "id": option.id,
            "url": url_for("poll.vote", option_id = option.id),
            "value": option.value,
            "count": option.count
        } for option in poll.options]
    }

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
    if poll == None:
        abort(404)

    poll.title = title or poll.title
    
    if options != None:
        option_dict = {option.id:option for option in poll.options}
        for option in options:
            if not isinstance(option, dict):
                abort(400)
        poll_options = [
            PollOption(value = option.get("value", ""), count = option.get("count", 0), poll=poll) if option.get("id") == None else option_dict[option["id"]] for option in options
        ]
        poll.options = poll_options
    db.session.commit()

    return jsonify(_poll_to_data(poll))

@poll.route("/poll/<poll_id>", methods=["GET"])
def read_poll(poll_id):
    poll = db.session.query(Poll).outerjoin(Poll.options).filter(Poll.id == poll_id).first()
    if poll == None:
        abort(404)

    return jsonify(_poll_to_data(poll))

@poll.route("/poll/<poll_id>", methods=["DELETE"])
@auth.login_required
def delete_poll(poll_id: str):
    poll = db.session.query(Poll).filter(Poll.id == poll_id).first()
    if poll == None:
        abort(404)

    db.session.delete(poll)
    db.session.commit()
    return jsonify({
        "id": poll_id
    })


@poll.route("/polls", methods=["GET"])
@auth.login_required
def list_polls():
    owner = auth.current_user()
    polls = db.session.query(Poll).filter(Poll.owner == owner).all()
    return jsonify([
        {
            "id": poll.id,
            "url": url_for("poll.read_poll", poll_id = poll.id),
            "title": poll.title,
        } for poll in polls
    ])

@poll.route("/vote/<option_id>", methods=["GET"])
def vote(option_id):
    option = db.session.query(PollOption).filter(PollOption.id == option_id).first()
    if option == None:
        abort(404)

    option.count = option.count + 1
    db.session.commit()
    return jsonify({
        "id": option.id,
        "value": option.value,
        "count": option.count
    })
