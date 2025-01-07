from bpy.types import (
    AddonPreferences,
)
from bpy.props import (   
    StringProperty,
)
import bpy

DEFAULT_PREFS = {
    "websocket_uri": "ws://localhost:8765",
}

# Thank you https://devtalk.blender.org/t/how-to-save-custom-user-preferences-for-an-addon/10362 

def fetch_pref(name: str):
    prefs = bpy.context.preferences.addons['warpnerf'].preferences
    
    if prefs is None or not name in prefs:
        return DEFAULT_PREFS[name]
    
    return prefs[name]

class WarpNeRFPreferences(AddonPreferences):
    bl_idname = "warpnerf"
    
    websocket_uri: StringProperty(
        name="Websocket URI",
        description = "URI of the websocket server",
        subtype='BYTE_STRING',
        default=DEFAULT_PREFS["websocket_uri"]
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, 'websocket_uri')

def register_addon_preferences():
    bpy.utils.register_class(WarpNeRFPreferences)

def unregister_addon_preferences():
    bpy.utils.unregister_class(WarpNeRFPreferences)
