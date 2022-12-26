from django.urls import re_path
from .consumers import *

websocket_urlpatterns=[
    re_path(r"ws/stock/(?P<room_name>\w+)/$", StockConsumer.as_asgi()),
]