from quick_poll.models import db
from quick_poll import create_app

app = create_app()
with app.app_context():
    db.create_all()