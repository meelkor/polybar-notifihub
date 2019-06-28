from lib.notification import NotificationSnapshot, Notification
from lib.connectors.connection import BaseConnection

class AppState:
    _focused_connection: str = None
    _focused_notification: int = None

    _connections = {}
    _snapshots = {}


    @property
    def connections(self):
        return (conn for conn in self._connections.values())


    def get_snapshot(self, conn_id: str) -> NotificationSnapshot:
        return self._snapshots[conn_id] if conn_id in self._snapshots else None


    def get_connection(self, conn_id: str):
        return self._connections[conn_id]


    def get_preview(self) -> Notification:
        if not self._focused_connection: return None

        snap = self._snapshots[self._focused_connection]

        return snap.notifications[self._focused_notification]


    def update_snapshot(self, conn_id: str, snap: NotificationSnapshot):
        self._snapshots[conn_id] = snap

        if not self._focused_connection and not snap.empty:
            self._focused_connection = conn_id
            self._focused_notification = 0

        elif self._focused_connection == conn_id:
            if snap.empty:
                snapshots = self._snapshots.items()
                id = next((id for (id, s) in snapshots if not s.empty), None)

                self._focused_connection = id
                self._focused_notification = 0

            elif len(snap.notifications) <= self._focused_notification:
                self._focused_notification = len(snap.notifications) - 1


    def add_connection(self, conn: BaseConnection):
        self._connections[conn.id] = conn


    def focus_notification(self, *args, step: int):
        if not self._focused_connection: return

        snap = self._snapshots[self._focused_connection]
        max = len(snap.notifications)

        self._focused_notification = (self._focused_notification + step) % max


    def focus_connection(self, *args, step: int):
        keys = [k for k in self._connections.keys() if not self._snapshots[k].empty]

        if (len(keys) == 0): return

        focused_index = keys.index(self._focused_connection)
        key = keys[(focused_index + step) % len(keys)]

        self._focused_connection = key
        self._focused_notification = 0

