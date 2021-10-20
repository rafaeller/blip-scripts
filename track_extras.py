import sys
import json

EXTRAS = {
    "userId": "{{contact.identity}}",
    "originatorMessageId": "{{input.message@id}}",
    "userEmail": "{{contact.email}}",
    "userName": "{{contact.name}}",
    "cnpj": "{{contact.extras.cnpj}}",
    "segmentName": "{{contact.extras.segmentName}}",
    "sessionId": "{{sessionId}}",
    "IdMessage": "{{input.message.id}}",
    "IdUser": "{{contact.identity}}",
    "username": "{{contact.extras.username}}",
    "Shortname": "{{contact.extras.shortname}}",
    "cpf": "{{contact.extras.cpf}}",
    "lastState": "{{state.previous.name}}",
    "score": "{{score}}",
    "clerk": "{{ticketAgentIdentity}}",
    "ticketId": "{{ticketId}}",
    "ticketOpenDatetime": "{{ticketOpenDate}}"
}

if len(sys.argv) < 2:
    print('uso: python track_extras.py <arquivo>')
    exit(-1)

arquivo_entrada = open(sys.argv[1], 'r', encoding='utf8')
fluxo = json.load(arquivo_entrada)
arquivo_entrada.close()

for bloco in fluxo:
    for acao in fluxo[bloco]['$enteringCustomActions'] + fluxo[bloco]['$leavingCustomActions']:
        if acao['type'] == 'TrackEvent':
            acao['settings']['extras'] = EXTRAS

nome_saida = '%s TRACKED.json' % (sys.argv[1].split('.')[0])
arquivo_saida = open(nome_saida, 'w', encoding='utf8')
arquivo_saida.write(json.dumps(fluxo))
arquivo_saida.close()

print('Feito! Salvo no arquivo %s' % nome_saida)
