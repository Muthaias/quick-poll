from app import db
from uuid import uuid4

def _uuid_str():
    return str(uuid4())

class Poll(db.Model):
    __tablename__ = 'poll'
    id = db.Column(db.String(80), primary_key=True, default=_uuid_str)
    title = db.Column(db.String(250), default="")
    owner = db.Column(db.String(80), nullable=False)

class PollOption(db.Model):
    __tablename__ = 'poll_option'
    id = db.Column(db.String(80), primary_key=True, default=_uuid_str)
    value = db.Column(db.String(80), nullable=False, default="")
    count = db.Column(db.Integer(), nullable=False, default=0)
    poll_id = db.Column(db.String(80), db.ForeignKey('poll.id'), nullable=False)
    poll = db.relationship('Poll', backref=db.backref('options', lazy=True, cascade="all, delete-orphan"))
