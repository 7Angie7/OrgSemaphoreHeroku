from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/admin_page/', consumers.SemaphoreConsumer.as_asgi()),
    re_path(r'ws/', consumers.IndexConsumer.as_asgi()),
]