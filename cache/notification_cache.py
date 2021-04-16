from django.core.cache import cache
import ipdb
import json


class NotificationCache():
    def __init__(self, user):
        self.key = f'{user.id}:{user.username}'
        notification = cache.get(self.key)

        if notification == 'null' or notification == None:
            empty_array = json.dumps([])
            cache.set(self.key, empty_array, timeout=None)

            self.notification = []

        else:
            self.notification = json.loads(notification)

    def set_notification(self, notification):
        json_notification = json.dumps(notification)
        cache.set(self.key, json_notification, timeout=None)

    def get_notification(self):
        return self.notification

    def clear(self):
        self.notification = []
        empty_array = json.dumps([])
        cache.set(self.key, empty_array, timeout=None)
