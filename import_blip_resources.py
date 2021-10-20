from requests import post
from uuid import uuid4

commands_url = 'https://http.msging.net/commands'

source_authorization = 'src_key'
destination_authorizations = [
    'dest_key'
]


def getResourceValue(name):
    print(f'Getting value of {name}')
    r = post(
        commands_url,
        headers={
            'Authorization': source_authorization
        },
        json={
            'id': str(uuid4()),
            'method': 'get',
            'uri': f'/resources/{name}'
        }
    )
    r = r.json()
    return r['resource']


def setResourceValue(name, value):
    print(f'Setting {name} as {value}')
    r = post(
        commands_url,
        headers={
            'Authorization': destination_authorization
        },
        json={
            'id': str(uuid4()),
            'method': 'set',
            'uri': f'/resources/{name}',
            'type': 'text/plain',
            'resource': value
        }
    )


if __name__ == "__main__":
    for destination_authorization in destination_authorizations:

        print('Getting all resource names from source')
        resource_names_command = post(
            commands_url,
            headers={
                'Authorization': source_authorization
            },
            json={
                'id': str(uuid4()),
                'method': 'get',
                'uri': '/resources'
            }
        )

        resource_names_command = resource_names_command.json()
        resource_names = resource_names_command['resource']['items']

        print(f'Got {len(resource_names)} resource names: {str(resource_names)}')

        print('Getting values from resources...')
        resources = [
            {
                'resource': x,
                'value': getResourceValue(x)
            }
            for x in resource_names
        ]

        print(f'Got {len(resources)} values: {resources}')

        print('setting resources on destination')

        [setResourceValue(x['resource'], x['value']) for x in resources]

        print('Done...')

    print('All done...')
