import yaml
import json
import pathlib


class Credentials:
    ROOT_DIR = str(pathlib.Path().resolve())

    def __init__(self):
        with open(Credentials.ROOT_DIR + '/assets/credentials.yaml', 'r') as stream:
            try:
                self.credentials = json.loads(json.dumps(yaml.safe_load(stream)))
            except yaml.YAMLError as exc:
                print(exc)

    def get_username(self):
        return self.credentials[0]['username']

    def get_password(self):
        return self.credentials[0]['password']


if __name__ == '__main__':
    credentials = Credentials()
    print(Credentials.ROOT_DIR)
    print(json.dumps(credentials.credentials, indent=4))
    print(credentials.get_username())
    print(credentials.get_password())
