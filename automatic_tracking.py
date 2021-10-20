# coding=utf-8
import sys
import json

CATEGORY = 'state.previous.name'
ACTION = 'state.name'

BASE_TRACKING = {
    'type': 'TrackEvent',
    '$title': 'TRACKING AUTOMATICO',
    '$invalid': False,
    'conditions': [
        {
            '$$hashKey': 'object:4353',
            'source': 'context',
            'comparison': 'exists',
            'values': [],
            'variable': CATEGORY
        },
        {
            '$$hashKey': 'object:4865',
            'source': 'context',
            'comparison': 'exists',
            'values': [],
            'variable': ACTION
        }
    ]
}

ROUTER_TRACKING = {
    **BASE_TRACKING,
    'settings': {
        'extras': {
            '#lastStateId': '{{state.previous.id}}',
            '#lastStateName': '{{state.previous.name}}',
            '#input': '{{input.content}}',
            '#contact': '{{contact.serialized}}',
            '#eventDatetime': '{{calendar.datetime}}',
            '#contactIdentity': '{{contact.identity}}',
            '#stateName': '{{state.name}}',
            '#stateId': '{{state.id}}',
            '#messageId': '{{input.message@id}}',
            '#tunnelOriginator': '{{tunnel.originator}}',
            '#tunnelOwner': '{{tunnel.owner}}',
            '#tunnelIdentity': '{{tunnel.identity}}'
        },
        'category': f'{{{{{CATEGORY}}}}}',
        'action': f'{{{{{ACTION}}}}}'
    }
}

TRACKING = {
    **BASE_TRACKING,
    'settings': {
        'extras': {
            '#lastStateId': '{{state.previous.id}}',
            '#lastStateName': '{{state.previous.name}}',
            '#input': '{{input.content}}',
            '#contact': '{{contact.serialized}}',
            '#eventDatetime': '{{calendar.datetime}}',
            '#contactIdentity': '{{contact.identity}}',
            '#stateName': '{{state.name}}',
            '#stateId': '{{state.id}}',
            '#messageId': '{{input.message@id}}'
        },
        'category': f'{{{{{CATEGORY}}}}}',
        'action': f'{{{{{ACTION}}}}}'
    }
}

ENTERING_ACTIONS_KEY = '$enteringCustomActions'
LEAVING_ACTIONS_KEY = '$leavingCustomActions'
ACTIONS_KEY = '$contentActions'
TITLE_KEY = '$title'
INPUT_KEY = 'input'
BYPASS_KEY = 'bypass'


def is_automatic_tracking(action):
    return action[TITLE_KEY] == BASE_TRACKING[TITLE_KEY]


def has_input_bypass(state):
    return ACTIONS_KEY in state and\
        INPUT_KEY in state[ACTIONS_KEY][-1] and\
        BYPASS_KEY in state[ACTIONS_KEY][-1][INPUT_KEY] and\
        state[ACTIONS_KEY][-1][INPUT_KEY][BYPASS_KEY]


if len(sys.argv) < 2:
    print('usage: python automatic_tracking.py <file> <is router? y|n>')
    exit(-1)

flow = []
filename = sys.argv[1]
is_router = len(sys.argv) > 2 and sys.argv[2] == 'y'

with open(filename, 'r', encoding='utf-8') as f:
    flow = json.load(f)

tracking = [ROUTER_TRACKING] if is_router else [TRACKING]

for state_id, state in flow.items():
    if not has_input_bypass(state):
        actions = [
            x for x in state[LEAVING_ACTIONS_KEY]
            if not is_automatic_tracking(x)
        ]
        state[LEAVING_ACTIONS_KEY] = actions + tracking
    else:
        actions = [
            x for x in state[ENTERING_ACTIONS_KEY]
            if not is_automatic_tracking(x)
        ]
        state[ENTERING_ACTIONS_KEY] = tracking + actions

output_filename = f'{filename.split(".")[0]}-TRACKED.json'

with open(output_filename, 'w') as f:
    json.dump(flow, f, ensure_ascii=False)

print(f'Done! Output file is {output_filename}')
