#!python3

from asyncio import get_event_loop
from time import sleep
from functools import partial, partialmethod
import signal
from gi import require_version
require_version('Notify', '0.7')
from gi.repository import Notify
from os import getpid

from lib.config import load_config, list_auths
from lib.manager import make_connection
from lib.app_state import AppState

app = AppState()

def main():
    load_config()
    write_process_number()

    Notify.init('Notifyhub')

    signal.signal(signal.SIGRTMIN, on_prev_notification)
    signal.signal(signal.SIGRTMIN + 1, on_next_notification)
    signal.signal(signal.SIGRTMIN + 2, on_prev_connection)
    signal.signal(signal.SIGRTMIN + 3, on_next_connection)
    signal.signal(signal.SIGRTMIN + 4, on_mark_as_read)

    loop = get_event_loop()

    for (name, label, config) in list_auths():
        conn = make_connection(name, label, config)
        app.add_connection(conn)

        loop.run_in_executor(None, partial(start_update_loop, conn.id))

    loop.run_forever()


def start_update_loop(conn_id):
    while True:
        conn = app.get_connection(conn_id)
        update(conn_id)
        sleep(conn.interval)


def update(conn_id):
    conn = app.get_connection(conn_id)
    snapshot = conn.update()
    last_snap = app.get_snapshot(conn_id)

    if snapshot.has_new(last_snap):
        notification = snapshot.get_latest()
        title = '%s %s' % (conn.icon, notification.title)
        Notify.Notification.new(title, notification.detail).show()

    app.update_snapshot(conn_id, snapshot)

    render()


def render():
    out_buffer = ''

    for conn in app.connections:
        out_buffer += conn.icon

        snapshot = app.get_snapshot(conn.id)

        if snapshot and not snapshot.empty:
            out_buffer += '!'

        out_buffer += ','

    preview = app.get_preview()

    if preview:
        out_buffer += ' | ' + preview.title

    print(out_buffer)


def on_next_notification(*args):
    app.focus_notification(step=1)
    render()


def on_prev_notification(*args):
    app.focus_notification(step=-1)
    render()


def on_next_connection(*args):
    app.focus_connection(step=1)
    render()


def on_prev_connection(*args):
    app.focus_connection(step=-1)
    render()


def on_mark_as_read(*args):
    notif = app.get_preview()
    conn = app.get_connection(notif.connection)

    conn.dismiss(notif.id)
    update(conn.id)


def write_process_number():
    with open('/tmp/notifihub-pid', 'w') as fd:
        fd.write(str(getpid()))


if __name__ == '__main__':
    main()
