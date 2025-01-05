from warpnerf.networking.websocket_client import WebSocketClient

class WarpNeRFClient:
    instance: 'WarpNeRFClient' = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(WarpNeRFClient, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance
    
    def __init__(self, uri):
        if self.__initialized: return
        self.__initialized = True
        self.client = WebSocketClient(uri)
    
    def subscribe(self, topic, callback):
        return self.client.subscribe(topic, callback)
    
    def unsubscribe(self, topic, callback):
        self.client.unsubscribe(topic, callback)
    
    def load_dataset(self, path: str):
        self.client.send("load_dataset", {"path": path})

#    def request_render(self, request: RenderRequest):
#        self.client.send("request_render", request.serialize())
    