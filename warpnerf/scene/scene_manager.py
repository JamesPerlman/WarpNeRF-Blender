import bpy
from typing import Callable, List
from warpnerf.networking.warpnerf_client import WarpNeRFClient
from warpnerf.scene.objects.radiance_field import RadianceField

class WNSceneManager:
    instance: 'WNSceneManager' = None
    subscriptions: List[Callable[[], None]] = []

    def __init__(self):
        self.register_callbacks()

    def __del__(self):
        self.unregister_callbacks()

    def register_callbacks(self):
        self.unregister_callbacks()
        self.subscriptions.append(WarpNeRFClient().subscribe("add_radiance_field", self.on_add_radiance_field))

    def unregister_callbacks(self):
        for unsubscribe in self.subscriptions:
            unsubscribe()
        self.subscriptions = []

    def on_add_radiance_field(self, data: dict):
        wn_obj = RadianceField.from_dict(data)
        bl_obj = wn_obj.to_blender()
        bpy.context.scene.collection.objects.link(bl_obj)
        print("Added radiance field:", data)
