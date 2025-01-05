""" WarpNeRF Addon """

bl_info = {
    "name": "WarpNeRF",
    "description": "WarpNeRF is a Blender Addon for Neural Radiance Fields",
    "author": "James Perlman",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),  # Adjust to your target Blender version
    "location": "View3D > Sidebar > WarpNeRF",
    "category": "3D View",
}

import bpy
import importlib

from warpnerf.blender_utils import developer_utility
importlib.reload(developer_utility)
modules = developer_utility.setup_addon_modules(
    __path__, __name__, "bpy" in locals()
)

# The root dir is Blenders addon folder.
# Therefore, we need the "warpnerf" specifier for this addon
from warpnerf.blender_utils.logging_utility import log_report
from warpnerf.registration.registration import Registration

def register():
    """Register importers, exporters and panels."""
    Registration.register_addon()
    log_report("INFO", "Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    """Unregister importers, exporters and panels."""
    Registration.unregister_addon()
    log_report("INFO", "Unregistered {}".format(bl_info["name"]))

if __name__ == "__main__":
    log_report("INFO", "main called")
