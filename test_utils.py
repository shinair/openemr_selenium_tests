import json

def read_properties():
    properties = {}
    with open('secret.config', 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                key = key.strip()  # Strip spaces from key
                value = value.strip()  # Strip spaces from value
                properties[key] = value
    return properties

def get_user():
    return read_properties().get('username', None)

def get_pass():
    return read_properties().get('password', None)


def read_configurations_from_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    configurations = []

    for url, user_data in data.items():
        url_value = user_data['url']
        users = user_data['users']

        for user in users:
            username = user['username']
            password = user['password']
            configurations.append((url_value, username, password))

    return configurations


def read_urls_from_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    urls = [user_data['url'] for user_data in data.values()]
    return urls