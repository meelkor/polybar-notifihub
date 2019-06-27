from abc import abstractmethod, ABC
from lib.notification import Notification, NotificationSnapshot

class BaseConnection(ABC):

    label = None
    interval = 5

    @property
    @abstractmethod
    def name(self):
        ...

    @property
    @abstractmethod
    def icon(self):
        ...

    @property
    def id(self):
        return self.name + '#' + self.label

    def __init__(self, label: str):
        self.label = label

    @abstractmethod
    def update(self) -> NotificationSnapshot:
        ...

    @abstractmethod
    def dismiss(self, id: str):
        ...

    def _make_notification(self, id: str, title: str, detail: str):
        return Notification(self.id, id, title, detail)
