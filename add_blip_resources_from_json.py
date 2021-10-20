import sys
import json
from requests import post
from uuid import uuid4

bot_authorization = 'Key '

commands_url = 'https://msging.net/commands'

def setResourceValue(name, value):
    print(f'Setting {name} as {value}')
    res = post(
        commands_url,
        headers={
            'Authorization': bot_authorization
        },
        json={
            'id': str(uuid4()),
            'method': 'set',
            'uri': f'/resources/{name}',
            'type': 'text/plain',
            'resource': value
        }
    )
    return res

if __name__ == "__main__":
    if bot_authorization == '':
        print(f'add the Athorization Key in the file')
        exit(-1)

    if len(sys.argv) < 2:
        print(f'use: python {__file__} <resources json, key and value>')
        exit(-1)

    resources_file = open(sys.argv[1], 'r', encoding='utf8')
    resources = json.load(resources_file)
    resources_file.close()

    errors = []

    for key in resources:
        res = setResourceValue(key, resources[key])
        if not res.ok:
            errors.append(key)

    if errors:
        print('\x1b[6;30;41m' + 'The following resources couldn\'t be added:' + '\x1b[0m')
        print('\x1b[6;30;43m' + ', '.join(errors) + '\x1b[0m')
    else:
        print('\x1b[6;30;42m' + 'All the resources were added successfully' + '\x1b[0m')

