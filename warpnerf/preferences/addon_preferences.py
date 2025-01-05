from bpy.types import (
    AddonPreferences,
)
from bpy.props import (   
    StringProperty,
)
import bpy


# Thank you https://devtalk.blender.org/t/how-to-save-custom-user-preferences-for-an-addon/10362 

def fetch_pref(name: str):
    prefs = bpy.context.preferences.addons['warpnerf'].preferences
    if prefs is None:
        return None
    return prefs[name]

class WarpNeRFPreferences(AddonPreferences):
    bl_idname = "warpnerf"
    
    websocket_uri: StringProperty(
        name="Websocket URI",
        description = "URI of the websocket server",
        subtype='BYTE_STRING'
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, 'websocket_uri')
