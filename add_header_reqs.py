# coding=utf-8
import sys
import json

HEADER_NAME = 'x-api-key'
HEADER_VALUE = '{{config.claraApiKey}}'

if len(sys.argv) < 2:
    print('uso: python add_header_reqs.py <arquivo>')
    exit(-1)

arquivo_entrada = open(sys.argv[1], 'r', encoding='utf8')
fluxo = json.load(arquivo_entrada)
arquivo_entrada.close()

for bloco in fluxo:
    acoes = fluxo[bloco]['$enteringCustomActions'] + \
        fluxo[bloco]['$leavingCustomActions']
    for acao in acoes:
        if acao['type'] == 'ProcessHttp':
            if acao['settings']['uri'].find('{{config.api}}') != -1:
                acao['settings']['headers'][HEADER_NAME] = HEADER_VALUE

nome_saida = '%s ADDED.json' % (sys.argv[1].split('.')[0])
arquivo_saida = open(nome_saida, 'w', encoding='utf8')
arquivo_saida.write(json.dumps(fluxo))
arquivo_saida.close()

print('Feito! Salvo no arquivo %s' % nome_saida)
