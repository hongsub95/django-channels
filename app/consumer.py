import json

from channels.generic.websocket import WebsocketConsumer,JsonWebsocketConsumer
'''
class LiveblogConsumer(WebsocketConsumer):
    groups=["liveblog"]
    
    def liveblog_post_created(self,event_dict):
        self.send(json.dumps(event_dict))

    def liveblog_post_updated(self,event_dict):
        self.send(json.dumps(event_dict))
    
    def liveblog_post_deleted(self,event_dict):
        self.send(json.dumps(event_dict))

class EchoConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        obj = json.loads(text_data)
        print("수신:",obj)
        
        json_string = json.dumps({
            "content":obj["content"],
            "user":obj["user"]
        })
        self.send(json_string)
'''
class LiveblogConsumer(JsonWebsocketConsumer):
    groups=["liveblog"]
    
    def liveblog_post_created(self,event_dict):
        self.send_json(event_dict)

    def liveblog_post_updated(self,event_dict):
        self.send_json(event_dict)
    
    def liveblog_post_deleted(self,event_dict):
        self.send_json(event_dict)

class EchoConsumer(JsonWebsocketConsumer):
    def receive_json(self, content, **kwargs):
        print("수신:",content)
        
        self.send_json({
            "content":content["content"],
            "user":content["user"]
        })