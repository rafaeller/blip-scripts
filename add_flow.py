from blip_session import BlipSession
import uuid
import json 
import time
import csv
import os

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

#select the template item
ITEM = key['template name']

#select the bot you want to insert the template item
BOT = key['bot name']

#verify uuid
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

#blip command to get working flow from bucket 
#key (string) = blip bot authorization 
def request_flow(key):
    blipSession = BlipSession(key)
    res_flow = blipSession.process_command(get_working_flow())
    flow = res_flow['resource']
    return flow

#return template item flow and remove unnecessary states
#key (string) = blip bot authorization
def get_item_flow(key):
    flow = request_flow(key)
    del flow['onboarding']
    del flow['fallback']
    return flow

#create a json file using bot flow
#flow (dictionary) = blip bot json flow
#file_name (string) = name of the file to be created
#path (string) = path of the directory - leave empty to root directory
def dict_to_json_file(flow, file_name, path='./'):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print(f'failed to try to create the directory: {path}')
    backup_file = open(f'{path}{file_name}.json', 'w')
    json_flow = json.dumps(flow, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    backup_file.write(json_flow)
    backup_file.close()

#blip command to update working flow of a blip bot 
#key (string) = blip bot autorization
#flow (dictionary) = blip bot json flow
def update_flow(flow, key):
    blipSession = BlipSession(key)
    return blipSession.process_command(set_working_flow(flow))

#recursive function that loops through the dictionary and generate new UUIDs for the flow
#flow (dictionary) = template item flow
def update_uuids(flow):
    for k, v in (flow.items() if isinstance(flow, dict) else enumerate(flow)):
        if isinstance(v, (dict, list)):
            update_uuids(v)
        else:
            if is_valid_uuid(v):
                if v not in uuid_dict:
                    new_uuid = str(uuid.uuid4())
                    uuid_dict.update({flow[k]:new_uuid})

                    flow[k] = new_uuid
                else:
                    flow[k] = uuid_dict[flow[k]]
    return flow, uuid_dict

if __name__ == "__main__":
    #set auxiliary dictionaries
    uuid_dict = {}
    template_flow = {}

    template_item = get_item_flow(ITEM['key'])
    bot_flow = request_flow(BOT['key'])

    #create a backup JSON flow 
    dict_to_json_file(bot_flow, f'backup_{BOT["name"].replace(" ", "_")}', './json/backup/')

    template_item, uuid_dict = update_uuids(template_item)

    for k in template_item:
        if k in uuid_dict:
            template_flow[uuid_dict[k]] = template_item[k]

    bot_flow.update(template_flow)

    result = update_flow(bot_flow, BOT['key'])

    print(f'insert: {ITEM["name"]} into: {BOT["name"]} - update status:{result["status"]}')
