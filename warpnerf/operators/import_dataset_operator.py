from pathlib import Path
import bpy
from warpnerf.networking.warpnerf_client import WarpNeRFClient

class ImportNeRFDatasetOperator(bpy.types.Operator):
    """An Operator to import a NeRF dataset from a directory or text input."""
    bl_idname = "warpnerf.import_nerf_dataset"
    bl_label = "Import Dataset"
    bl_description = "Import a dataset from a directory or specify a dataset name"

    input_mode: bpy.props.EnumProperty(
        name="Input Mode",
        description="Choose the input mode",
        items=[
            ('FILE', "File Select", "Select a JSON dataset file"),
            ('TEXT', "Text Input", "Enter dataset name directly")
        ],
        default='TEXT'
    ) # type: ignore

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')  # type: ignore
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default='*.json', options={'HIDDEN'}) # type: ignore

    text_input: bpy.props.StringProperty(  # For direct text input
        name="Dataset Name",
        description="Enter the name of the dataset",
        default="/home/luks/james/nerfs/pipe-thingy-makawao/transforms.json"
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if self.input_mode == 'FILE':
            print(f"Importing NeRF dataset from file: {self.filepath}")
            WarpNeRFClient().load_dataset(self.filepath)
        elif self.input_mode == 'TEXT':
            print(f"Importing NeRF dataset by name: {self.text_input}")
            path = Path(self.text_input)
            WarpNeRFClient().load_dataset(path)

        return {'FINISHED'}

    def invoke(self, context, event):
        if self.input_mode == 'FILE':
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "input_mode")
        if self.input_mode == 'TEXT':
            layout.prop(self, "text_input")

def menu_func_import(self, context):
    self.layout.operator(ImportNeRFDatasetOperator.bl_idname, text="Import NeRF Dataset")

def register():
    bpy.utils.register_class(ImportNeRFDatasetOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportNeRFDatasetOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
