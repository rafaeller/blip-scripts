from requests import Session
from uuid import uuid4

AUTH_KEY = '<BOT_KEY>'
LIST_NAME = 'list@broadcast.msging.net'

members = [
    'user@messenger.gw.msging.net'
]

session = Session()
session.headers = {
    'Authorization': AUTH_KEY
}

for m in members:
    command_body = {
        'id': str(uuid4()),
        'to': 'postmaster@broadcast.msging.net',
        'method': 'set',
        'uri': f'/lists/{LIST_NAME}/recipients',
        'type': 'application/vnd.lime.identity',
        'resource': m
    }

    try:
        command_res = session.post(
            'https://http.msging.net/commands', json=command_body)
        command_res = command_res.json()

        if command_res['status'] != 'success':
            print(m)
    except Exception as ex:
        print(m)
