from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from chat.models import Room

class ChatConsumer(JsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name =''
    
    def connect(self):
        user = self.scope["user"]
        # user가 인증되지 않았을 경우, 연결 요청을 거부(종료코드가 강제로 1006(비정상 종료)으로 지정)
        if not user.is_authenticated:
            self.close()
        else:
            room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
            self.group_name = Room.make_chat_group_name(room_pk=room_pk)
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()
        
    def disconnect(self, code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )
        
    
    def receive_json(self, content, **kwargs):
        _type = content["type"]
        if _type == "chat.message":
            message = content["message"]
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type":"chat.message",
                    "message":message
                }
            )
        else:
            print(f"Invalid message type : ${_type}")
        
    def chat_message(self,message_dict):
        self.send_json({
            "type":"chat.message",
            "message":message_dict["message"]
        })