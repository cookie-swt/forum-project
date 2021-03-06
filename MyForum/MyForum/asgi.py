"""
ASGI config for MyForum project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from .websocket import websocket_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyForum.settings')

async def application(scope,receive,send):
    
    if scope['type'] == 'http':
        await get_asgi_application(scope,receive,send)

    elif scope['type'] == 'websocket':
        await websocket_application(scope,receive,send)
    
    else:
        raise Exception('unknown scope type,'+scope['type'])