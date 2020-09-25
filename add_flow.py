from blip_session import BlipSession
import uuid
import json 
import time
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
    try:
        blipSession = BlipSession(key)
        res_flow = blipSession.process_command(get_working_flow())
        flow = res_flow['resource']
        print(f'requested flow with status: {res_flow["status"]}')
        return flow
    except Exception as ex:
        print(f'failed to request flow - Exception: {ex}')
    

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
        json_flow = json.dumps(flow, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        new_file.write(json_flow)
        new_file.close()
        print(f'created new json file: [{path}{file_name}]')
    except Exception as ex:
        print(f'failed to create new json file - Exception: {ex}')

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

def update_all_uuids(flow):
    try:
        new_flow = {}
        template_item, uuid_dict = update_value_uuids(flow)

        for k in template_item:
            if k in uuid_dict:
                new_flow[uuid_dict[k]] = template_item[k]

        print(f'replaced all UUIDs from the flow')
        return new_flow
        
    except Exception as ex:
        print(f'failed to replace UUID - Exception: {ex}')
    

if __name__ == "__main__":
    uuid_dict = {}
    template_item = get_item_flow(ITEM['key'])
    bot_flow = request_flow(BOT['key'])

    #create a backup JSON flow 
    dict_to_json_file(bot_flow, f'backup_{BOT["name"].replace(" ", "_")}', './json/backup/')

    template_flow = update_all_uuids(template_item)

    bot_flow.update(template_flow)

    result = update_flow(bot_flow, BOT['key'])

    print(f'inserted: {ITEM["name"]} into: {BOT["name"]} - update status: {result["status"]}')
