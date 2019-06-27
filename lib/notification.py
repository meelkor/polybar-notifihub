class Notification:
    connection = None
    id = None
    title = None
    detail = None


    def __init__(self, connection, id, title, detail):
        self.connection = connection
        self.id = id
        self.title = title
        self.detail = detail


class NotificationSnapshot:
    count = None
    notifications = None

    def __init__(self, notifications: list, count = None):
        if (count == None):
            count = len(notifications)

        self.count = count
        self.notifications = notifications

    @property
    def empty(self):
        return len(self.notifications) == 0

    def get_latest(self) -> Notification:
        return self.notifications[0] if not self.empty else None

    def has_new(self, last) -> bool:
        """Check whether latest notification in this snapshot is new"""
        if self.empty:
            return False

        if not last:
            return True

        latest_id = self.notifications[0].id

        return len([n for n in last.notifications if n.id == latest_id]) == 0
