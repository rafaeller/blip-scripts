from blip_session import BlipSession
import uuid
import json 
import csv
import os

try:
    print()
except Exception as ex:
    print(f'failed to request flow - Exception: {ex}')

key = {
    "template name": {
        "name": "template name",
        "key": "Key..."
    },
    "bot name": {
        "name": "bot name",
        "key": "Key..."
    }
}

#select the bot you want to insert the template item
BOT = key['bot name']

TEMPLATE = '%%template%%'

#verify if is a valid uuid
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

#blip json request to get working flow from bucket
def get_working_flow():
    return {
        "method": "get",
        "uri": "/buckets/blip_portal:builder_working_flow"
    }

#blip json request to set working flow from bucket
def set_working_flow(flow):
    return {  
        "method": "set",
        "uri": "/buckets/blip_portal:builder_working_flow",
        "type": "application/json",
        "resource": flow
    }

#blip json request to get working configuration from bucket
def get_working_configuration():
    return {
        "method": "get",
        "uri": "/buckets/blip_portal:builder_working_configuration"
    }

#blip json request to set working configuration from bucket
def set_working_configuration(config):
    return {  
        "method": "set",
        "uri": "/buckets/blip_portal:builder_working_configuration",
        "type": "application/json",
        "resource": config
    }

#blip command to get working flow from bucket 
#key (string) = blip bot authorization 
def request_flow(key):
    try:
        blipSession = BlipSession(key)
        res_flow = blipSession.process_command(get_working_flow())
        flow = res_flow['resource']
        print(f'requested flow with status: {res_flow["status"]}')
        return flow
    except Exception as ex:
        print(f'failed to request flow - Exception: {ex}')    

#blip command to get working configuration from bucket 
#key (string) = blip bot authorization 
def request_configuration(key):
    try:
        blipSession = BlipSession(key)
        res_config = blipSession.process_command(get_working_configuration())
        config = res_config['resource']
        print(f'requested configuration with status: {res_config["status"]}')
        return config
    except Exception as ex:
        print(f'failed to request configuration - Exception: {ex}')   

#blip command to update working flow of a blip bot 
#key (string) = blip bot autorization
#flow (dictionary) = blip bot json flow
def update_flow(flow, key):
    try:
        blipSession = BlipSession(key)
        res = blipSession.process_command(set_working_flow(flow))
        print(f'updated flow with status: {res["status"]}')
        return res
    except Exception as ex:
        print(f'failed to update flow - Exception: {ex}')

#blip command to update working configuration of a blip bot 
#key (string) = blip bot autorization
#config (dictionary) = blip bot configuration variables
def update_configuration(config, key):
    try:
        blipSession = BlipSession(key)
        res = blipSession.process_command(set_working_configuration(config))
        print(f'updated configuration with status: {res["status"]}')
        return res
    except Exception as ex:
        print(f'failed to update configuration - Exception: {ex}')

#chech if the template variables exist in the bot config, if not add them to the dictionary
#bot_config (dictionary) = blip bot configuration variables
#template_config (dictionary) = blip template bot configuration variables
def merge_configs(bot_config, template_config):
    try:
        for v in template_config:
            if v not in bot_config:
                bot_config[v] = template_config[v]
        print(f'merged configuration variables')
        return bot_config
    except Exception as ex:
        print(f'failed to merge configuration variables - Exception: {ex}')

#add configuration variables from template to blip bot
#bot_key (string) = blip bot authorization
#template_key (string) = blip template bot authorization
def add_template_configs(bot_key, template_key):
    try:
        bot_config = request_configuration(bot_key)
        template_config = request_configuration(template_key)

        config = merge_configs(bot_config, template_config)

        res = update_configuration(config, bot_key)

        return res
    except Exception as ex:
        print(f'failed to add configuration variables - Exception: {ex}')

#return template item flow and remove unnecessary states
#key (string) = blip bot authorization
def get_item_flow(key):
    try:
        flow = request_flow(key)
        del flow['onboarding']
        del flow['fallback']
        print(f'unnecessary states removed')
        return flow
    except Exception as ex:
        print(f'failed to remove unnecessary states - Exception: {ex}')

#check if directory path exists and create it if not
#path (string) = path of the directory
def create_directory_if_not_exists(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'created directory : {path}')
    except:
        print(f'failed to try to create the directory: {path}')

#create a json file using bot flow
#flow (dictionary) = blip bot json flow
#file_name (string) = name of the file to be created
#path (string) = path of the directory - leave empty to root directory
def dict_to_json_file(flow, file_name, path='./'):  
    try:
        create_directory_if_not_exists(path)
        new_file = open(f'{path}{file_name}.json', 'w')
        json_flow = json.dumps(flow, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ':'))
        new_file.write(json_flow)
        new_file.close()
        print(f'created new json file: [{path}{file_name}]')
    except Exception as ex:
        print(f'failed to create new json file - Exception: {ex}')
    
#recursive function that loops through the dictionary and generate new UUIDs for the flow
#flow (dictionary) = template item flow
def update_value_uuids(flow):
    try:
        for k, v in (flow.items() if isinstance(flow, dict) else enumerate(flow)):
            if isinstance(v, (dict, list)):
                update_value_uuids(v)
            else:
                if is_valid_uuid(v):
                    if v not in uuid_dict:
                        new_uuid = str(uuid.uuid4())
                        uuid_dict.update({flow[k]:new_uuid})

                        flow[k] = new_uuid
                    else:
                        flow[k] = uuid_dict[flow[k]]
        return flow, uuid_dict
    except Exception as ex:
        print(f'failed to generate new UUID - Exception: {ex}')

#update key and values UUIDs from the flow
#flow (dictionary) = template item flow
def update_all_uuids(flow):
    try:
        new_flow = {}
        flow, uuid_dict = update_value_uuids(flow)

        for k in flow:
            if k in uuid_dict:
                new_flow[uuid_dict[k]] = flow[k]

        print(f'replaced all UUIDs from the flow')
        return new_flow
    except Exception as ex:
        print(f'failed to replace UUID - Exception: {ex}')

#update all states position
#position (dictionary) = top and left values in pixel unit
def set_flow_position(flow, position):
    index = 0
    p = {}
    for k in flow:
        if index == 0:
            p['top'] = float(position['top'][:-2]) - float(flow[k]['$position']['top'][:-2])
            p['left'] = float(position['left'][:-2]) - float(flow[k]['$position']['left'][:-2])
            flow[k]['$position']['top'] = position['top']
            flow[k]['$position']['left'] = position['left']
        else:
            flow[k]['$position']['top'] = str(float(flow[k]['$position']['top'][:-2]) + p['top'])+'px'
            flow[k]['$position']['left'] = str(float(flow[k]['$position']['left'][:-2]) + p['left'])+'px'
        index += 1
    return flow

#find in blip bot flow all states with template tag in title
#bot_flow (dictionary) = blip bot json flow
def find_template_states(bot_flow):
    template_states = []
    for k in bot_flow:
        if TEMPLATE in bot_flow[k]['$title']:
            template_states.append(bot_flow[k])
    for i in template_states:
        del bot_flow[i['id']]
    return template_states,bot_flow

#for each template in template_states list update uuids and set flow position
#template_states (list) = list of template states
def set_new_template_flow(template_states):
    flow_to_add = {}
    for template_item in template_states:
        template_flow, template_key = select_template(template_item['$title'])
        if template_flow is not None:
            template_flow = update_all_uuids(template_flow)
            template_flow = set_flow_position(template_flow, template_item['$position'])
            
            flow_to_add.update(template_flow)
        
            add_template_configs(BOT['key'], template_key)
    return flow_to_add

#search for template in keys dict 
#template_name (string) = title od template state
def select_template(template_name):
    template_name = template_name.replace(TEMPLATE,'')
    template_flow = {}
    if template_name in key:
        template_flow = get_item_flow(key[template_name]['key'])
        return template_flow, key[template_name]['key']
    else:
        print(f'No templates was found with name: {template_name}')
        return None,None

if __name__ == "__main__":
    uuid_dict = {}
    
    #request blip bot flow
    bot_flow = request_flow(BOT['key'])

    #create a backup JSON flow 
    dict_to_json_file(bot_flow, f'backup_{BOT["name"].replace(" ", "_")}', './json/backup/')

    #search for templates states in blip bot flow
    template_states, bot_flow = find_template_states(bot_flow)

    #set flow with all templates
    flow_to_add = set_new_template_flow(template_states)

    #append flow templates in bot flow
    bot_flow.update(flow_to_add)
    
    #update blip bot flow with new templates
    result = update_flow(bot_flow, BOT['key']) 
    print(f'inserted:{BOT["name"]} - update status: {result["status"]}')
