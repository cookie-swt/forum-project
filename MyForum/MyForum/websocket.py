CONNECTIONS = {}

async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event['type'] == 'websocket.connect':
            await send({'type':'websocket.accept'})
            
            #记录send对象
            CONNECTIONS['?'] = send

        elif  event['type'] == 'websocket.disconnect':
            break
        
        else :
            pass
