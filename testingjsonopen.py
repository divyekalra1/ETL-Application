from sqlalchemy import Column
import json

config_list = []

with open("config.txt", 'r') as config_file:
    config_list.append(json.load(config_file))
    for json_obj in config_file:
        temp_dict = json.loads(json_obj)
        config_list.append(temp_dict)


print(config_list[0])

# with open("config.txt", 'r') as config_file:
#     config = json.load(config_file)

# print(config)