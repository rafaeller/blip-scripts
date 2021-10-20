from blip_session import BlipSession
from urllib.parse import quote
from json import load
import sys


if len(sys.argv) < 2:
    print('uso: python add_team_members.py <configs_json>')
    exit(-1)

config_json = load(open(sys.argv[1], 'r', encoding='utf8'))

if 'members' not in config_json or 'bots' not in config_json:
    print(
        'configs_json must have members (string list) and bots (obj [identity, name and authorization] list)'
    )
    exit(-1)

TEAM_MEMBERS = config_json['members']

BOTS = config_json['bots']

ADMIN_AUTH_PERMISSIONS = load(
    open('./admin_auth_permissions.json', 'r', encoding='utf8'))

ADMIN_USER_PERMISSIONS = load(
    open('./admin_user_permissions.json', 'r', encoding='utf8'))


def create_get_bot_account():
    return {
        'method': 'get',
        'uri': '/account'
    }


def create_set_auth_permissions(member_email, permissions, bot_identity, bot_name):
    short_name = bot_identity.split('@')[0]
    return {
        'to': 'postmaster@portal.blip.ai',
        'method': 'set',
        'uri': '/auth-permissions',
        'type': 'application/vnd.iris.portal.guest-user+json',
        'resource': {
            'applicationName': bot_name,
            'returnUrl': f'https://portal.blip.ai/application/detail/{short_name}/home',
            'shortName': short_name,
            'userCulture': 'pt-BR',
            'userEmail': member_email,
            'userFullName': member_email,
            'permissions': permissions
        },
        'metadata': {
            'server.shouldStore': 'true'
        }
    }


def create_set_user(member_email, bot_identity):
    return {
        'to': 'postmaster@portal.blip.ai',
        'method': 'set',
        'uri': f'/applications/{quote(bot_identity)}/users',
        'type': 'application/vnd.lime.identity',
        'resource': f'{quote(member_email)}@blip.ai',
        'metadata': {
            'server.shouldStore': 'true'
        }
    }


def create_set_user_permissions(member_email, permissions, bot_identity):
    return {
        'to': 'postmaster@portal.blip.ai',
        'method': 'set',
        'uri': f'/applications/{bot_identity}/permissions',
        'type': 'application/vnd.lime.collection+json',
        'resource': {
            'itemType': 'application/vnd.iris.portal.user-permission+json',
            'items': permissions
        },
        'metadata': {
            'server.shouldStore': 'true'
        }
    }


if __name__ == '__main__':
    print(f'Found {len(BOTS)} bots')
    for bot in BOTS:

        session = BlipSession(bot)
        bot_account = session.force_command(create_get_bot_account())
        bot_account = bot_account['resource']
        bot_identity = bot_account['identity']
        bot_name = bot_account['fullName']

        print(f'Starting to add on {bot_name}...')

        for member in TEAM_MEMBERS:
            print(f'Adding member {member} to {bot_name}')

            commands_to_exec = [
                create_set_auth_permissions(
                    member, ADMIN_AUTH_PERMISSIONS,
                    bot_identity, bot_name
                ),
                create_set_user(member, bot_identity),
                create_set_user_permissions(
                    member, ADMIN_USER_PERMISSIONS, bot_identity)
            ]

            commands_res = [session.force_command(c) for c in commands_to_exec]

            for cr in commands_res:
                if cr['status'] == 'success':
                    print(f'[SUCCESS] Added {member} to {bot_name}')
                else:
                    print(
                        f'[ERROR] Could not add {member} to {bot_name}')
                    print(
                        f'[ERROR {member} to {bot_name}] Reason: {cr["reason"]["description"]}'
                    )
            print(f'Done adding to {bot_name}')
    print('Done')
