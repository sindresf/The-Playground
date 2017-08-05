import json
from config_parse.config_structs import *

def parse_config(file):
    js_config = None
    with open(file) as json_data:
        js_config = json.load(json_data)
    config_structs = [Config(),Graphics_config(),LSTM_config(),Music_config()]
    for struct in config_structs:
        __register_settings_to(struct,js_config[struct.name])
    return config_structs

def __register_settings_to(struct, settings):
    for setting in settings:
        if setting == 'opt': struct.register_opt_config_settings(settings[setting])
        else:
            if(type(setting) is type({})):
                for s in setting:
                    __register_settings_to(struct,s)
            struct.register_config_setting(setting,settings[setting])