from django.urls import path
from .app_notification import MySyncConsumer, ASyncConsumer

ws_pattern = [
    path('ws/sc/<str:group_name>', MySyncConsumer.as_asgi()),
    path('ws/ac/<str:group_name>/', ASyncConsumer.as_asgi())
]