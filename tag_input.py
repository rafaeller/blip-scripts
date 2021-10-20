import sys
import json

if len(sys.argv) < 2:
    print('uso: python tag_input.py <arquivo>')
    exit(-1)

arquivo_entrada = open(sys.argv[1], 'r', encoding='utf8')
fluxo = json.load(arquivo_entrada)
arquivo_entrada.close()

for bloco in fluxo:
    try:
        fluxo[bloco]['$contentActions'][-1]['input']['bypass']
    except:
        continue
    if not fluxo[bloco]['$contentActions'][-1]['input']['bypass']:
        fluxo[bloco]['$tags'].append({
            'background': '#232d11',
            'label': 'User Input',
            'id': 'blip-tag-ba80e21e-7e32-11e9-8f9e-2a86e4085a59',
            'canChangeBackground': False
        })
nome_saida = '%s TAGGED.json' % (sys.argv[1].split('.')[0])
arquivo_saida = open(nome_saida, 'w', encoding='utf8')
arquivo_saida.write(json.dumps(fluxo))
arquivo_saida.close()

print('Feito! Salvo no arquivo %s' % nome_saida)
