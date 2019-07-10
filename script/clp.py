"""HKBN checker script"""
import os
from checker import clp_checker
CREDES_FILENAME = os.path.join(
    os.path.dirname(__file__),
    'credentials.json'
)


def run():
    checker = clp_checker.Checker(CREDES_FILENAME)
    checker.check()


if __name__ == '__main__':
    run()
