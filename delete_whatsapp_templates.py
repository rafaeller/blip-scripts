from blip_session import BlipSession
import time

lista_templates = ["TEMPLATE_ID"]

my_auth_key = 'BOT_KEY'

contract_id = 'blip-cda'

bs = BlipSession(my_auth_key, contract_id)

def command(template):
  return {
    "method": "delete",
    "to": "postmaster@wa.gw.msging.net",
    "uri": f'/message-templates/{template}'
}

for template in lista_templates:
  result = bs.process_command(command(template))
  if result["status"] == "failure":
    print(f'{template} - failure')
  else:
    print(f'{template} - success')
  time.sleep(1)
  
