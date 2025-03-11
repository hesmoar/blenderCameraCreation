import bpy
from CameraShotCreation import parse_csv_file_to_dict, create_collection, set_timeline, create_markers, cam_creation   # Import your functions
from bpy_extras.io_utils import ImportHelper


class ShotToolsPanel(bpy.types.Panel):
    bl_label = "Shot Creation Tools"
    bl_idname = "PT_CameraPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        #CSV File input button
        layout.operator("object.parse_csv", text="Add CSV File")
        
        layout.prop(scene, "setting_1")
        
        layout.prop(scene, "use_checkbox", text="Enable Feature X")
        
        layout.operator("object.execute_functions", text="Run Functions")


class ParseCSVOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "object.parse_csv"
    bl_label = "Parse CSV Operator"

    filter_glob: bpy.props.StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    def execute(self, context):
        scene = context.scene
        csv_data = parse_csv_file_to_dict(self.filepath)
        context.scene.csv_data = csv_data
        
        print(csv_data)
        return {'FINISHED'}

class ExecuteFunctionsOperator(bpy.types.Operator):
    bl_idname = "object.execute_functions"
    bl_label = "Execute Functions"

    def execute(self, context):
        scene = context.scene

        # Access the CSV data and selected settings here
        csv_data = scene.csv_data
        setting_1 = scene.setting_1
        setting_2 = scene.setting_2
        use_checkbox = scene.use_checkbox  # Get the checkbox value

        # Example of running functions based on the data
        print(f"CSV Data: {csv_data}")
        print(f"Setting 1: {setting_1}")
        print(f"Setting 2: {setting_2}")
        print(f"Checkbox selected: {use_checkbox}")

        # Here, you can call other functions to process the data, create cameras, etc.
        # create_cameras(csv_data, setting_1, setting_2, use_checkbox)

        return {'FINISHED'}
def add_properties():

    bpy.types.Scene.setting_1 = bpy.props.EnumProperty(
        items=[('OPTION_1', 'Option 1', 'Description of Option 1'),
               ('OPTION_2', 'Option 2', 'Description of Option 2')],
        name="Camera Type",
        default='OPTION_1'
    )

    bpy.types.Scene.setting_2 = bpy.props.IntProperty(
        name="Start Frame",
        default=1,
        min=1,
        max=2500
    )

    # Add a checkbox property
    bpy.types.Scene.use_checkbox = bpy.props.BoolProperty(
        name="Enable Feature X",
        description="Enable this feature to do something",
        default=False
    )

def register():
    add_properties()  # Add the properties for settings
    bpy.utils.register_class(ShotToolsPanel)
    bpy.utils.register_class(ParseCSVOperator)
    bpy.utils.register_class(ExecuteFunctionsOperator)

def unregister():
    bpy.utils.unregister_class(ShotToolsPanel)
    bpy.utils.unregister_class(ParseCSVOperator)
    bpy.utils.unregister_class(ExecuteFunctionsOperator)
    del bpy.types.Scene.setting_1  # Remove added properties
    del bpy.types.Scene.setting_2
    del bpy.types.Scene.use_checkbox

if __name__ == "__main__":
    register()
    
    
    