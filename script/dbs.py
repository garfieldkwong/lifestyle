"""DBS checker script"""
import json
import os
from checker import dbs_checker
CREDES_FILENAME = os.path.join(
    os.path.dirname(__file__),
    'credentials.json'
)
CONFIG_FILE = os.path.join(
    os.path.dirname(__file__),
    'dbs_config.json'
)


def run():
    config_data = None
    with open(CONFIG_FILE) as file:
        config_data = json.load(file)
    checker = dbs_checker.Checker(CREDES_FILENAME, config_data)
    checker.check()


if __name__ == '__main__':
    run()
