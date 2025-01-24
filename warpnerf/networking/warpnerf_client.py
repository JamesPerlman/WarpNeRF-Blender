from typing import Callable
from warpnerf.networking.requests.render_request import RenderRequest
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
        if self.__initialized:
            return
        self.__initialized = True
    
    def __del__(self):
        self.runner.run(self.wsc.disconnect())
    
    # WebSocketClient
    @property
    def wsc(self):
        if not hasattr(self, "_wsc"):
            uri = fetch_pref("websocket_uri")
            self._wsc = WebSocketClient(uri)
        
        if not self._wsc.is_connected:
            self.runner.run(self._wsc.connect())

        return self._wsc
    
    def subscribe(self, topic, callback) -> Callable[[], None]:
        return self.wsc.subscribe(topic, callback)
    
    def unsubscribe(self, topic, callback):
        self.wsc.unsubscribe(topic, callback)
    
    def load_dataset(self, path: str):
        self.runner.run(self.wsc.send("load_dataset", {"path": str(path)}))

    def request_render(self, request: RenderRequest):
       self.runner.run(self.wsc.send("request_render", request.to_dict()))
    