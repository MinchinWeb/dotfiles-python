"""
Load this Python start up file (into Windows) by setting the appropriate
environmental variable.
"""

import os
import sys
import winreg
from enum import Enum
from pathlib import Path

import colorama

colorama.init()

STARTUP_FILE = Path.cwd() / 'home' / '.startup.py'
REGISTRY_PATH = 'Environment'
REGISTRY_KEY = 'PYTHONSTARTUP'


# modified from https://stackoverflow.com/a/35286642
def set_reg(registry_path, name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 
                                      0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

# https://stackoverflow.com/a/35286642
def get_reg(registry_path, name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path,
                                      0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

# from minchin.text
class Answers(Enum):
    '''
    Possibles answers to queries.
    YES and ALL are "Truth-y", while NO, QUIT, and NONE are "False-y".
    '''

    NO = 0
    YES = 1
    QUIT = 2
    ALL = 3
    NONE = 4

    def __bool__(self):
        if self.value in [0, 2, 4]:
            return False
        elif self.value in [1, 3]:
            return True

# from minchin.text
def query_yes_no(question, default="yes"):
    '''Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The return value is one of Answers.YES or Answers.NO.
    Copied (and modified) from
    http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    '''
    valid = {"yes": Answers.YES, "y": Answers.YES,  "ye": Answers.YES,
             "no": Answers.NO,   "n": Answers.NO}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if __name__ == "__main__":
    key_existing = get_reg(REGISTRY_PATH, REGISTRY_KEY)
    if key_existing is not None:
        print('[{}WARN{}] Registry Key already exists, and is set to "{}"'
              .format(colorama.Fore.YELLOW, colorama.Style.RESET_ALL,
                      key_existing))
        to_proceed = query_yes_no('Proceed anyway?', default="no")
        if to_proceed == Answers.NO:
            sys.exit(1)

    if not STARTUP_FILE.exists():
        print("[{}WARN{}] Startup file does not seem to exist..."
            .format(colorama.Fore.YELLOW, colorama.Style.RESET_ALL))
        sys.exit(2)

    results = set_reg(REGISTRY_PATH, REGISTRY_KEY, str(STARTUP_FILE))
    if results:
        print("[{}GOOD{}] Startup file loaded!"
              .format(colorama.Fore.GREEN, colorama.Style.RESET_ALL))
        print("You may need to re-open the console window for this to take "
              "effect.")
    else:
        print("[{}ERROR{}] Error writing to registry"
              .format(colorama.Fore.RED, colorama.Style.RESET_ALL))
