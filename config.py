import json

config = {'repository': None}

config_path = 'config.json'

try:
    with open(config_path, 'r') as file:
        config = json.loads(file.read())
except:
    with open(config_path, 'w') as file:
        file.write(json.dumps(config))
