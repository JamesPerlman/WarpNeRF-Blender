import importlib
import bpy
from warpnerf.blender_utils.scene_update_handler import register_depsgraph_updates, unregister_depsgraph_updates

# Thank you https://github.com/SBCV/Blender-Addon-Photogrammetry-Importer


from warpnerf.preferences.addon_preferences import (register_addon_preferences, unregister_addon_preferences)
from warpnerf.renderers.remote_render_engine import (register_remote_render_engine, unregister_remote_render_engine)

# Definining the following import and export functions within the
# "Registration" class causes different errors when hovering over entries in
# "file/import" of the following form:
# "rna_uiItemO: operator missing srna 'import_scene.colmap_model'""

class Registration:
    """Class to register import and export operators."""

    # Define register/unregister Functions
    
    @classmethod
    def _register_importer(cls, importer, append_function):
        """Register a single importer."""
        bpy.utils.register_class(importer)
        bpy.types.TOPBAR_MT_file_import.append(append_function)

    @classmethod
    def _unregister_importer(cls, importer, append_function):
        """Unregister a single importer."""
        bpy.utils.unregister_class(importer)
        bpy.types.TOPBAR_MT_file_import.remove(append_function)

    @classmethod
    def _register_exporter(cls, exporter, append_function):
        """Register a single exporter."""
        bpy.utils.register_class(exporter)
        bpy.types.TOPBAR_MT_file_export.append(append_function)

    @classmethod
    def _unregister_exporter(cls, exporter, append_function):
        """Unregister a single exporter."""
        bpy.utils.unregister_class(exporter)
        bpy.types.TOPBAR_MT_file_export.remove(append_function)

    @classmethod
    def register_importers(cls):
        """Register importers."""
        pass

    @classmethod
    def unregister_importers(cls):
        """Unregister all registered importers."""
        pass

    @classmethod
    def register_exporters(cls):
        """Register exporters."""
        pass

    @classmethod
    def unregister_exporters(cls):
        """Unregister all registered exporters."""
        pass

    @classmethod
    def register_misc_components(cls):
        register_remote_render_engine()
        register_addon_preferences()
        register_depsgraph_updates()

    @classmethod
    def unregister_misc_components(cls):
        unregister_remote_render_engine()
        unregister_addon_preferences()
        unregister_depsgraph_updates()

