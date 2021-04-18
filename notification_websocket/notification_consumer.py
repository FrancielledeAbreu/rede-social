from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import JsonWebsocketConsumer, AsyncWebsocketConsumer
from cache.timeline import TimelineCache
from accounts.models import User


class TimelineConsumer(JsonWebsocketConsumer):
    def connect(self):

        # current_user_id = int(
        #     self.scope['query_string'].decode("utf-8").split('=')[1])

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            'posts', self.channel_name)

        # user = User.objects.get(id=current_user_id)
        timeline_cache = TimelineCache()
        current_timeline = timeline_cache.get_timeline()

        self.send_json({'timeline': current_timeline})

    def disconnect(self, close_code):
        pass

    def posts_timeline(self, event):
        self.send_json({'timeline': event['timeline']})
