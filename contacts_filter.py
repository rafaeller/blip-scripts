from uuid import uuid4
import requests

uri = '/contacts?$take={{take}}&$skip={{skip}}'


url = 'https://http.msging.net/commands'
uri = '/contacts?$take={{take}}&$skip={{skip}}'
take = 10000
skip = 0

body = {
    'id': str(uuid4()),
    'method': 'GET',
    'uri': uri.replace('{{take}}', str(take)).replace('{{skip}}', str(skip))
}
headers = {
    'Authorization': 'Key TOKEN'
}

response = requests.post(url, json=body, headers=headers)
response = response.json()

contacts = []
total = 0

while(len(response['resource']['items']) > 0):
    response = response['resource']['items']
    contact_batch = [
        {
            'nome': x['name'],
            'telefone': x['phoneNumber']
        }
        for x in response
        if 'group' not in x and 'name' in x and 'phoneNumber' in x
    ]
    contacts = contacts + contact_batch
    print(f'Got {len(contacts)} contacts')
    skip = skip + take
    body['uri'] = uri.replace('{{take}}', str(
        take)).replace('{{skip}}', str(skip))
    response = requests.post(url, json=body, headers=headers)
    response = response.json()

out_file = open('contatos.csv', 'w')

out_file.write('nome,telefone,\n')

lines = [f'{x["nome"]},{x["telefone"]},' for x in contacts]

out_file.writelines('\n'.join(lines))

out_file.close()
