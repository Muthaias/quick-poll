from app import app
from poll import poll

app.register_blueprint(poll)

@app.route('/')
def api_root():
    return 'Welcome to the QuickPoll API root'