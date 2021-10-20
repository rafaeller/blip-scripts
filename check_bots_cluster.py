from blip_session import BlipSession
import os

bots = [
    {
        'key': 'BOT_KEY',
        'id': 'BOT_ID'
    }
]

def get_config(id):
    return {
    'method': 'get',
    'uri': f'lime://{id}@msging.net/configuration?caller=admin@msging.net'
}

for bot in bots:
    blipSession = BlipSession(bot["key"])

    res_context = blipSession.process_command(get_config(bot["id"]))

    obj = res_context

    if res_context.get('status') != 'success':
        print(f'{bot["id"]} - falha')
    else:
        result = obj["resource"]
        if('Cluster' in result): 
            cluster = result["Cluster"]
        else:
            cluster = 'Standard'
        print(f'{bot["id"]} - {cluster} - {result["PaymentAccount"]}')
   