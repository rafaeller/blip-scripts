from blip_session import BlipSession

# Fill with bot authorization key and user identity
BOT_AUTHORIZATION = 'Key Y2VsdWxhcGFwYTp6cE5sdVhYZ3g1VkZ5dlE3dGdwNQ=='
USER_IDENTITY = '553173591233@wa.gw.msging.net'

DELETE_METHOD = 'delete'
GET_METHOD = 'get'


if BOT_AUTHORIZATION == '' or USER_IDENTITY == '':
    print(
        '[ERROR] Reason: : must have a valid bot_authorization key and user_identity.'
    )
    exit(-1)


def create_all_context_request():
    return {
        'method': GET_METHOD,
        'to': 'postmaster@msging.net',
        'uri': f'/contexts/{USER_IDENTITY}'
    }


def delete_specific_context_variable(context_var):
    return {
        'method': DELETE_METHOD,
        'to': 'postmaster@msging.net',
        'uri': f'/contexts/{USER_IDENTITY}/{context_var}'
    }


if __name__ == "__main__":
    blipSession = BlipSession(BOT_AUTHORIZATION)
    res_context = blipSession.process_command(create_all_context_request())

    if (res_context.get('status') == 'success'):

        for context_var in res_context['resource']['items']:
            res__delete_context = blipSession.process_command(
                delete_specific_context_variable(context_var))
            if res__delete_context['status'] == 'success':
                print(f'Deleted context var :{context_var}')
            else:
                print(
                    f'[ERROR] Reason: {res__delete_context["reason"]["description"]}'
                )

        print('Finished')
        exit(-1)
    if (res_context.get('status') == 'failure'):
        print(
            f'[ERROR] Reason: {res_context["reason"]["description"]}\nFinished'
        )
    else:
        print(
            f'[ERROR] Reason: {res_context["description"]}\nFinished'
        )
