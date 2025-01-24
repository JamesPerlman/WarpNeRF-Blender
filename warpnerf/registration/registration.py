import importlib
import bpy

# Thank you https://github.com/SBCV/Blender-Addon-Photogrammetry-Importer


# from warpnerf.networking.warpnerf_client import WarpNeRFClient
from warpnerf.operators.import_dataset_operator import ImportNeRFDatasetOperator
from warpnerf.panels.main.training_panel import NeRFTrainingPanel
from warpnerf.preferences.addon_preferences import (register_addon_preferences, unregister_addon_preferences)
from warpnerf.renderers.remote_render_engine import (register_remote_render_engine, unregister_remote_render_engine)
from warpnerf.scene.scene_manager import WNSceneManager

# Definining the following import and export functions within the
# "Registration" class causes different errors when hovering over entries in
# "file/import" of the following form:
# "rna_uiItemO: operator missing srna 'import_scene.colmap_model'""

def _nerf_dataset_import_operator_fn(self, context):
    self.layout.operator(ImportNeRFDatasetOperator.bl_idname, text="NeRF Dataset")

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
        cls._register_importer(ImportNeRFDatasetOperator, _nerf_dataset_import_operator_fn)

    @classmethod
    def unregister_importers(cls):
        """Unregister all registered importers."""
        cls._unregister_importer(ImportNeRFDatasetOperator, _nerf_dataset_import_operator_fn)

    @classmethod
    def register_exporters(cls):
        """Register exporters."""
        pass

    @classmethod
    def unregister_exporters(cls):
        """Unregister all registered exporters."""
        pass

    @classmethod
    def register_panels(cls):
        """Register panels."""
        bpy.utils.register_class(NeRFTrainingPanel)

    @classmethod
    def unregister_panels(cls):
        """Unregister panels."""
        bpy.utils.unregister_class(NeRFTrainingPanel)

    @classmethod
    def register_addon(cls):
        register_remote_render_engine()
        register_addon_preferences()
        cls.register_importers()
        cls.register_panels()
        bpy._warpnerf_scene_manager = WNSceneManager()

    @classmethod
    def unregister_addon(cls):
        unregister_remote_render_engine()
        unregister_addon_preferences()
        cls.unregister_importers()
        cls.unregister_panels()
        del bpy._warpnerf_scene_manager
