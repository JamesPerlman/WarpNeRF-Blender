from bpy.types import (
    AddonPreferences,
)
from bpy.props import (   
    StringProperty,
)
from bpy import utils
import bpy


# Thank you https://devtalk.blender.org/t/how-to-save-custom-user-preferences-for-an-addon/10362 

def fetch_pref(name: str):
    prefs = bpy.context.preferences.addons['warp_nerf'].preferences
    if prefs is None:
        return None
    return prefs[name]

class WarpNeRFPreferences(AddonPreferences):
    bl_idname = "warp_nerf"
    
    websocket_uri: StringProperty(
        name="Websocket URI",
        description = "URI of the websocket server",
        subtype='URL',
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, 'websocket_uri')


def register_addon_preferences():
    utils.register_class(WarpNeRFPreferences)


def unregister_addon_preferences():
    utils.unregister_class(WarpNeRFPreferences)
