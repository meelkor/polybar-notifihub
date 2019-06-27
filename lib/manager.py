from lib.connectors.gmail import GmailConnection
from lib.connectors.connection import BaseConnection

CONNECTORS = {}

def _init():
    _register(GmailConnection)


def list_connectors():
    return list(CONNECTORS.keys)


def make_connection(name: str, label: str, auth) -> BaseConnection:
    Connector = get_connector(name)

    return Connector(label, auth)

def get_connector(name: str):
    if name not in CONNECTORS:
        raise KeyError('%s is not a known connector' % name)

    return CONNECTORS[name]


def _register(connector):
    CONNECTORS[connector.name] = connector


_init()
