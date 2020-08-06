import requests
import pytest
import json
from uuid import uuid4

api_url = "http://localhost:5000"
headers = {
    'Content-Type': 'application/json'
}

@pytest.fixture
def poll_id():
    url = "%s/polls" % (api_url)
    resp = requests.get(url)
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) > 0
    poll_id = data[0]["id"]
    assert poll_id != None

    return poll_id

def test_create_poll():
    payload = {
        "title": "Hello world",
        "options": [
            "a",
            "b",
            "c"
        ]
    }
    
    url = "%s/poll" % api_url
    resp = requests.post(url, headers=headers, json=payload)

    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] != None

def test_update_poll(poll_id):
    payload = {
        "title": str(uuid4()),
        "options": [
            {
                "value": value,
                "count": 0
            } for value in [
                str(uuid4()),
                str(uuid4()),
                str(uuid4())
            ]
        ]
    }
    url = "%s/poll/%s" % (api_url, poll_id)
    resp = requests.post(url, headers=headers, json=payload)

    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == poll_id
    assert data["title"] == payload["title"]
    assert json.dumps([
        {
            "value": option["value"],
            "count": option["count"]
        } for option in data["options"]
    ]) == json.dumps(payload["options"])

def test_delete_poll(poll_id):
    url = "%s/poll/%s" % (api_url, poll_id)
    resp = requests.delete(url)

    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == poll_id

def test_polls():
    url = "%s/polls" % api_url
    resp = requests.get(url)

    assert resp.status_code == 200

    data = resp.json()
    for poll in data:
        assert poll["id"] != None
        assert poll["url"] != None
        assert poll["title"] != None

def test_vote(poll_id):
    url = "%s/poll/%s" % (api_url, poll_id)

    resp = requests.get(url)
    assert resp.status_code == 200

    poll_data = resp.json()
    assert poll_data["options"] != None
    assert len(poll_data["options"]) > 0

    option = poll_data["options"][0]
    vote_url = "%s/vote/%s" % (api_url, option["id"])

    vote_resp = requests.get(vote_url)
    assert vote_resp.status_code == 200

    vote_data = vote_resp.json()
    assert vote_data["count"] == option["count"] + 1