from flask import Flask
from poll import poll

app = Flask(__name__)
app.register_blueprint(poll)

@app.route('/')
def api_root():
    return 'Welcome to the QuickPoll API root'