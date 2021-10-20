from blip_session import BlipSession

bot_auth_key = 'source key'
router_auth_key = 'destination key'

bot_client = BlipSession(bot_auth_key)
router_client = BlipSession(router_auth_key)


def merge_contact(contact, client):
    contact['identity'] = contact['identity'].replace('prd', '')
    client.force_command({
        'method': 'merge',
        'uri': '/contacts',
        'type': 'application/vnd.lime.contact+json',
        'resource': contact
    })


def get_context_values(identity, client):
    command = client.force_command({
        'method': 'get',
        'uri': f'/contexts/{identity}?withContextValues=true&$take=99999'
    })
    command = command['resource']['items']
    command.append({
        'name': 'master-state',
        'type': 'text/plain',
        'value': 'prditauconsorcios@msging.net'
    })
    return command


def set_context_value(identity, name, value, mime_type, client):
    identity = identity.replace('prd', '')
    client.force_command({
        'method': 'set',
        'uri': f'/contexts/{identity}/{name}',
        'type': mime_type,
        'resource': value
    })


contacts = bot_client.process_command({
    'method': 'get',
    'uri': '/contacts?$take=9999'
})['resource']['items']
print(f'found {len(contacts)} contacts')

for contact in contacts:
    print(f'Merging with router contact {contact["identity"]}')
    merge_contact(contact, router_client)

contexts = bot_client.process_command({
    'method': 'get',
    'uri': '/contexts?$take=9999'
})['resource']['items']
print(f'fount {len(contexts)} contexts')

for user_context in contexts:
    print(f'Merging with router context {user_context}')
    context = get_context_values(user_context, bot_client)
    print(f'Got {len(context)} context variables')
    [
        set_context_value(
            user_context, c['name'], c['value'], c['type'], router_client)
        for c in context
    ]

print('Finish!')
