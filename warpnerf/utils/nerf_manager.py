from warpnerf.networking.requests.render_request import RenderRequest
from warpnerf.networking.websocket_client import WebSocketClient

class NeRFManager:
    instance: 'NeRFManager' = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(NeRFManager, cls).__new__(cls)
        return cls.instance
    
    def __init__(self, uri):
        if self.__initialized: return
        self.__initialized = True
        self.client = WebSocketClient(uri)
    
    def subscribe(self, topic, callback):
        return self.client.subscribe(topic, callback)
    
    def unsubscribe(self, topic, callback):
        self.client.unsubscribe(topic, callback)
    
    def request_render(self, request: RenderRequest):
        self.client.send("request_render", request)
    