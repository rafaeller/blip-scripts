from urllib.parse import quote
from requests import Session
from uuid import uuid4
import sys

# Modify

IDENTIFIER = 'bot_id'
AUTHORIZATION = 'bot_key'

# Do not modify

COMMANDS_URL = 'https://http.msging.net/commands'
SET_METHOD = 'set'

ERROR_RULES = []

if len(sys.argv) < 2:
    print('uso: python add_attendance_rules.py <lojas.csv>')
    exit(-1)

rules_csv = open(sys.argv[1], 'r', encoding='utf8')

rules_data = None

try:
    rules_data = rules_csv.read().split('\n')[1:]
    rules_csv.close()
except Exception as ex:
    print('Error while parsing csv')
    rules_csv.close()
    exit(-1)


def create_set_rule_command(values, team):
    return {
        'id': str(uuid4()),
        'to': 'postmaster@desk.msging.net',
        'method': SET_METHOD,
        'uri': '/rules',
        'type': 'application/vnd.iris.desk.rule+json',
        'resource': {
            'id': str(uuid4()),
            'title': team,
            'isActive': True,
            'ownerIdentity': f'{IDENTIFIER}@msging.net',
            'property': 'Contact.Extras.CDLOJA',
            'relation': 'Equals',
            'values': values,
            'team': team
        }
    }


if __name__ == "__main__":
    print(f'Starting session for {IDENTIFIER}')
    session = Session()
    session.headers = {
        'Authorization': AUTHORIZATION
    }
    print(f'Found {len(rules_data)} rules')
    for rule in rules_data:

        command_body = create_set_rule_command([rule], rule)

        command_res = session.post(COMMANDS_URL, json=command_body)
        command_res = command_res.json()

        if command_res['status'] != 'success':
            print(f'Error adding rule {rule}')
            ERROR_RULES.append(rule)
        else:
            print(f'Added rule {rule}')
    if len(ERROR_RULES) > 0:
        print(
            f'Saving {len(ERROR_RULES)} not added rules to error_rules_{IDENTIFIER}.csv'
        )
        with open(f'error_rules_{IDENTIFIER}.csv', 'w', encoding='utf8') as error_file:
            error_file.write('\n'.join(ERROR_RULES))
            error_file.close()
    print('Done')
