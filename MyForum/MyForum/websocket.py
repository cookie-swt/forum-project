import json
import urllib


#全部的websocket sender
CONNECTIONS = {}

#判断用户是否已经连接
def check_connection(key):
    return key in CONNECTIONS

#发送消息结构体
def message(sender,msg_type,msg):
    text = json.dumps({
        'sender':sender,
        'contentType':msg_type,
        'content':msg,
    })
    return {
        'type':'websocket.send',
        'text':text
    }

async def websocket_application(scope, receive, send):
    while True:
        event = await receive()
        query_string = scope.get('query_string',b'').decode()
        qs = urllib.parse.parse_qs(query_string)
        auth = qs.get('auth',[''])[0]

        #收到建立连接的消息
        if event['type'] == 'websocket.connect':

            #验证用户名
            if not auth:
                break
            if auth in CONNECTIONS:
                break

            await send({'type':'websocket.accept'})
            
            #发送好友列表
            friends_list = list(CONNECTIONS.keys())
            await send(message('system','friendList',friends_list))

            #向其他人群发消息：有人加入群聊了
            for sender in CONNECTIONS.values():
                await sender(message('system','addUser',auth))

            #记录send对象
            CONNECTIONS[auth] = send

        #接收到断开连接的消息
        elif  event['type'] == 'websocket.disconnect':

            #移除记录
            if auth in CONNECTIONS:
                CONNECTIONS.pop(auth)
            
            #向其他人群发消息，有人离开聊天室了
            for sender in CONNECTIONS.values():
                await sender(message('system','removeUser',auth))
        
        elif event['type'] == 'websocket.receive':
            receive_msg = json.loads(event['text'])
            send_to = receive_msg.get('sendTo','')
            if send_to in CONNECTIONS:
                content_type = receive_msg.get('contentType','text')
                content = receive_msg.get('content','')
                msg = message(auth, content_type, content)
                await CONNECTIONS[send_to](msg)
            else:
                msg = message('system', 'text', '对方已经离开聊天室啦')
                await send(msg)
                
        else:
            pass

