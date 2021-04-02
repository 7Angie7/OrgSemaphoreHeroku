from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/control/(?P<pk_test>[\w.@+-]+)/$', consumers.SemaphoreConsumer.as_asgi()),
    re_path(r'ws/semaphore/(?P<semap_url>[\w.@+-]+)/$', consumers.IndexConsumer.as_asgi()),
]