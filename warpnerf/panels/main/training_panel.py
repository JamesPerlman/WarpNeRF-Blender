import bpy
from warpnerf.operators.import_dataset_operator import ImportNeRFDatasetOperator

class NeRFTrainingPanel(bpy.types.Panel):
    """Class that defines the NeRF Training panel in the 3D View"""

    bl_label = "Training"
    bl_idname = "VIEW3D_PT_warpnerf_training_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "WarpNeRF"

    observers = []

    @classmethod
    def poll(cls, context):
        """Return the availability status of the panel."""
        
        return True
    
    def __init__(self):
        super().__init__()

    def draw(self, context):
        """Draw the panel with corresponding properties and operators."""

        layout = self.layout
        
        box = layout.box()
        box.label(text="Dataset")

        row = box.row()
        row.operator(ImportNeRFDatasetOperator.bl_idname, text="Load Dataset")
