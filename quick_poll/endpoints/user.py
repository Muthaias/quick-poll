from flask import Blueprint, request, jsonify, redirect
from uuid import uuid4

user = Blueprint("user", __name__)

@user.route("/user", methods=["GET"])
def get_user_id():
    desc = request.json if request.json else request.args
    url = desc.get("redirect")
    user_id = str(uuid4())
    if url == None:
        return jsonify({
            "user_id": user_id
        })
    arg_separator = "?" if url.find("?") == -1 else "&"
    return redirect(url + arg_separator + ("user_id=%s" % user_id))