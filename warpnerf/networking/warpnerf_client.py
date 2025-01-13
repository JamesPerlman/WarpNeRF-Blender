from warpnerf.networking.websocket_client import WebSocketClient
from warpnerf.preferences.addon_preferences import fetch_pref
from warpnerf.utils.async_utils import AsyncRunner

class WarpNeRFClient:
    instance: 'WarpNeRFClient' = None
    runner: AsyncRunner = AsyncRunner()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(WarpNeRFClient, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance
    
    def __init__(self):
        if self.__initialized: return
        self.__initialized = True
    
    @property
    def client(self):
        if not hasattr(self, "_client"):
            uri = fetch_pref("websocket_uri")
            self._client = WebSocketClient(uri)
            self.runner.run(self._client.connect())
        
        return self._client
    
    def subscribe(self, topic, callback):
        return self.client.subscribe(topic, callback)
    
    def unsubscribe(self, topic, callback):
        self.client.unsubscribe(topic, callback)
    
    def load_dataset(self, path: str):
        self.runner.run(self.client.send("load_dataset", {"path": str(path)}))

#    def request_render(self, request: RenderRequest):
#        self.client.send("request_render", request.serialize())
    