# coding=utf-8
import sys
import json

if len(sys.argv) < 2:
    print('uso: python tag_input.py <arquivo>')
    exit(-1)

arquivo_entrada = open(sys.argv[1], 'r', encoding='utf8')
fluxo = json.load(arquivo_entrada)
arquivo_entrada.close()

ACTION_TAG = {
    'ProcessHttp': {
        "background": "#7762E3",
        "label": "ProcessHttp",
        "id": "blip-tag-7df1e1a9-87d1-c1a1-fd37-37331fa8a21d",
        "canChangeBackground": False
    },
    'TrackEvent': {
        "background": "#61D36F",
        "label": "TrackEvent",
        "id": "blip-tag-bc58ce94-4e76-4f66-a2c4-efb9b8ebb738",
        "canChangeBackground": False
    },
    'MergeContact': {
        "background": "#FF1E90",
        "label": "MergeContact",
        "id": "blip-tag-3ff93695-d2ae-dfc7-7fe5-f4e4b7a547a8",
        "canChangeBackground": False
    },
    'Redirect': {
        "background": "#1EA1FF",
        "label": "Redirect",
        "id": "blip-tag-e6dead9d-5a52-3901-7aa5-9ad0e275ae67",
        "canChangeBackground": False
    },
    'ManageList': {
        "background": "#1EDEFF",
        "label": "ManageList",
        "id": "blip-tag-9f66207a-45bb-76a7-3816-ddd9c6289f94",
        "canChangeBackground": False
    },
    'ExecuteScript': {
        "background": "#FF961E",
        "label": "ExecuteScript",
        "id": "blip-tag-d2974ed4-d8d9-0d87-6153-fbed3205d146",
        "canChangeBackground": False
    },
    'SetVariable': {
        "background": "#FF4A1E",
        "label": "SetVariable",
        "id": "blip-tag-f56c273b-ba00-ca1c-9342-0d4c15d33ac3",
        "canChangeBackground": False
    },
    'ProcessCommand': {
        "background": "#FC91AE",
        "label": "ProcessCommand",
        "id": "blip-tag-a691d5d5-f3c4-ef6b-b9c5-614d5de16169",
        "canChangeBackground": False
    },
    'UserInput': {
        'background': '#232d11',
        'label': 'User Input',
        'id': 'blip-tag-ba80e21e-7e32-11e9-8f9e-2a86e4085a59',
        'canChangeBackground': False
    }
}

for bloco in fluxo:
    tags_adicionadas = []
    fluxo[bloco]['$tags'] = []
    for acao in fluxo[bloco]['$enteringCustomActions'] + fluxo[bloco]['$leavingCustomActions']:
        if acao['type'] not in tags_adicionadas:
            try:
                fluxo[bloco]['$tags'].append(ACTION_TAG[acao['type']])
                tags_adicionadas.append(acao['type'])
            except:
                continue
    try:
        fluxo[bloco]['$contentActions'][-1]['input']['bypass']
    except:
        continue
    if not fluxo[bloco]['$contentActions'][-1]['input']['bypass']:
        fluxo[bloco]['$tags'].append(ACTION_TAG['UserInput'])

nome_saida = '%s FIXED.json' % (sys.argv[1].split('.')[0])
arquivo_saida = open(nome_saida, 'w', encoding='utf8')
arquivo_saida.write(json.dumps(fluxo))
arquivo_saida.close()

print('Feito! Salvo no arquivo %s' % nome_saida)
