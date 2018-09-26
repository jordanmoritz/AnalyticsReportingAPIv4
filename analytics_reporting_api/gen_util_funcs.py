#gen_util_funcs.py
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

clean_operations = [str.strip, remove_ga_prefix, str.title]

def get_service_client(scopes, api_name, api_version, service_key_file=None, credentials=None):
    
    if credentials:
        service_client = build(api_name, api_version, credentials=credentials)
    
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(service_key_file, scopes=scopes)
        service_client = build(api_name, api_version, credentials=credentials)
    
    return service_client

def remove_ga_prefix(string):
    result = string.split(':')[1]
    return result

def clean_strings(strings, operations):
    results = []
    for string in strings:
        for operation in clean_operations:
            string = operation(string)
        results.append(string)
    return results