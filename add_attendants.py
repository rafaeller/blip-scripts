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

ERROR_ATTENDANTS = []

if len(sys.argv) < 2:
    print('uso: python add_attendants.py <attendants.csv>')
    exit(-1)

attendants_csv = open(sys.argv[1], 'r', encoding='utf8')

csv_data = None

try:
    csv_data = attendants_csv.read().split('\n')[1:]
    attendants_csv.close()
except Exception as ex:
    print('Error while parsing csv')
    attendants_csv.close()
    exit(-1)


def create_set_attendant_command(email, teams):
    return {
        'id': str(uuid4()),
        'to': 'postmaster@desk.msging.net',
        'method': SET_METHOD,
        'uri': '/attendants',
        'type': 'application/vnd.iris.desk.attendant+json',
        'resource': {
            'identity': f'{quote(email)}@blip.ai',
            'teams': teams
        }
    }


def get_email_teams_from_line(line):
    splited_line = line.split(',')
    email = splited_line[0]
    teams = splited_line[1:]
    return email, teams


if __name__ == "__main__":
    print(f'Starting session for {IDENTIFIER}')
    session = Session()
    session.headers = {
        'Authorization': AUTHORIZATION
    }
    print(f'Found {len(csv_data)} attendants')
    for attendant in csv_data:
        email, teams = get_email_teams_from_line(attendant)
        command_body = create_set_attendant_command(email, teams)

        command_res = session.post(COMMANDS_URL, json=command_body)
        command_res = command_res.json()

        if command_res['status'] != 'success':
            print(f'Error adding {email}')
            ERROR_ATTENDANTS.append(attendant)
        else:
            print(f'Added {email}')
    if len(ERROR_ATTENDANTS) > 0:
        print(
            f'Saving {len(ERROR_ATTENDANTS)} not added attendants to error_{IDENTIFIER}.csv'
        )
        with open(f'error_{IDENTIFIER}.csv', 'w', encoding='utf8') as error_file:
            error_file.write('\n'.join(ERROR_ATTENDANTS))
            error_file.close()
    print('Done')
