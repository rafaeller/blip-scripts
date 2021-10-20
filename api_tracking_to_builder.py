import sys
import json

if len(sys.argv) < 2:
    print('uso: python tag_input.py <arquivo>')
    exit(-1)

arquivo_entrada = open(sys.argv[1], 'r', encoding='utf8')
fluxo = json.load(arquivo_entrada)
arquivo_entrada.close()


for bloco in fluxo:
    for action_moment in ['$enteringCustomActions', '$leavingCustomActions']:
        for i, acao in enumerate(fluxo[bloco][action_moment]):
            try:
                acao['type']
            except:
                print(json.dumps(acao, indent=4))
                continue

            if acao['type'] == 'ProcessHttp' and acao['settings']['uri'] == '{{config.api}}/blip/tracking':
                body = json.loads(acao['settings']['body'])
                for track in body:
                    fluxo[bloco][action_moment].append(
                        {
                            'type': 'TrackEvent',
                            '$title': acao['$title'],
                            '$invalid': False,
                            'settings': {
                                    'category': track['category'],
                                    'action': track['action'],
                                    'extras': track['extras']
                            }
                        }
                    )
                fluxo[bloco][action_moment].pop(i)

nome_saida = '%s MIGRATED.json' % (sys.argv[1].split('.')[0])
arquivo_saida = open(nome_saida, 'w', encoding='utf8')
arquivo_saida.write(json.dumps(fluxo))
arquivo_saida.close()

print('Feito! Salvo no arquivo %s' % nome_saida)
