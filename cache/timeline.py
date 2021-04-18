from django.core.cache import cache
import ipdb
import json


class TimelineCache():
    def __init__(self):
        # self.key = f'{user.id}:{user.username}'
        self.key = 'timeline_public'
        timeline = cache.get(self.key)

        if timeline == 'null' or timeline == None:
            empty_array = json.dumps([])
            cache.set(self.key, empty_array, timeout=None)

            self.timeline = []

        else:
            self.timeline = json.loads(timeline)

    def set_timeline(self, timeline):
        json_timeline = json.dumps(timeline)
        cache.set(self.key, json_timeline, timeout=None)

    def get_timeline(self):
        return self.timeline

    def clear(self):
        self.timeline = []
        empty_array = json.dumps([])
        cache.set(self.key, empty_array, timeout=None)
