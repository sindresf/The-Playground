import json
from config_parse.config_structs import Config_struct

def parse_config(file):
    js_config = None
    with open(file) as json_data:
        js_config = json.load(json_data)

    config_structs = [Config_struct("program"), #TODO could make this even better by
                      Config_struct("graphics"),# first passing name in to struct
                      Config_struct("lstm"),    # from the json config file
                      Config_struct("music")]   # and then doing the rest
                                                # instead of this other way round
    for struct in config_structs:               # since the return makes it so that the order has to be figured out anyways
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