#!python3

"""Notifihub Authenticate

Manage athentication details for given connector. Beware that resulting
credentials are then stored in plaintext in config directory.
Multiple connections can be created for the same connector by passing the label
option.

Usage:
    authenticate.py create <connector> [-l <connection_label>]
    authenticate.py delete <connector> [-l <connection_label>]
    authenticate.py (-h | --help)

Options:
    -l, --label=<connection_label>  Custom label for this connection [default: default]

"""
from docopt import docopt

from lib.manager import get_connector
from lib import config


def main(args):
    config.load_config()

    if (args['create']):
        con = get_connector(args['<connector>'])
        auth = con.authenticate()
        config.write_auth(args['<connector>'], args['--label'], auth)

    elif (args['delete']):
        config.remove_auth(args['<connector>'], args['--label'])


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
