import os.path
from os import makedirs, stat
from appdirs import user_config_dir
from yaml import safe_load, safe_dump


CONFIG_DIR = user_config_dir('polybar-notifihub')
AUTH_PATH = os.path.join(CONFIG_DIR, 'auth.yaml')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.yaml')

auth = {}
config = {}


def load_config():
    """Load config files into memory, needs to be called before any other
    config call.
    """

    global auth
    global config

    try:
        auth = safe_load(open(AUTH_PATH))
    except FileNotFoundError:
        pass

    try:
        config = safe_load(open(CONFIG_PATH))
    except FileNotFoundError:
        pass


def list_auths():
    """Return pairs of connector names and authentication configs."""
    auths = []

    for (name, configs) in auth.items():
        for (label, config) in configs.items():
            auths.append((name, label, config))

    return auths


def has_auth(connector: str, label: str):
    return connector in auth and label in auth[connector]


def write_auth(connector: str, label: str, credentials):
    if connector not in auth:
        auth[connector] = {}

    auth[connector][label] = credentials

    _save_auth_config()


def remove_auth(connector: str, label: str):
    _assert_auth(connector, label)

    if len(auth[connector]) == 1:
        del auth[connector]
    else:
        del auth[connector][label]

    _save_auth_config()


def _save_auth_config():
    try:
        stat(CONFIG_DIR)
    except FileNotFoundError:
        makedirs(CONFIG_DIR)

    with open(AUTH_PATH, 'w') as fp:
        fp.write(safe_dump(auth))


def _assert_auth(connector: str, label: str):
    if not has_auth(connector, label):
        raise KeyError('No authentication data for %s (%s)' % (connector, label))
