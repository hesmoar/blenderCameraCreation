import bpy
from CameraShotCreation import parse_csv_file_to_dict, create_collection, set_timeline, create_markers, cam_creation, set_resolution   # Import your functions
from bpy_extras.io_utils import ImportHelper


# Define Scene Properties
bpy.types.Scene.csv_file_path = bpy.props.StringProperty(
    name="Add CSV File", 
    subtype='FILE_PATH'
)

bpy.types.Scene.render_mode = bpy.props.EnumProperty(
    name="Render Mode",
    description="Choose to create as a single file or multiple files",
    items=[
        ("SINGLE", "Single File", "Add all cameras to one file"),
        ("MULTIPLE", "Multiple Files", "Create a file for each camera"),
    ],
    default="SINGLE"
)

bpy.types.Scene.render_width = bpy.props.IntProperty(
    name="Render Width",
    description="Set the width of the render resolution",
    default=1920, min=1
)

bpy.types.Scene.render_height = bpy.props.IntProperty(
    name="Render Height",
    description="Set the height of the render resolution",
    default=1080, min=1
)



# Define Scene classes

class ShotToolsPanel(bpy.types.Panel):
    bl_label = "Shot Creation Tools"
    bl_idname = "PT_CameraPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "csv_file_path")
        #CSV File input button
        #layout.operator("object.parse_csv", text="Add CSV File")
        
        
        if hasattr(scene, "csv_data"):
            layout.label(text="CSV Loaded Succesfully")
       
       
        layout.prop(scene, "render_mode", text="Single/Multiple")
        layout.prop(scene, "render_width")
        layout.prop(scene, "render_height")



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
        scene.csv_file_path = self.filepath
        
        try:
            scene.csv_data = parse_csv_file_to_dict(self.filepath)
            self.report({'INFO'}, "CSV loaded succesfully")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load CSV: {e}")
                
        #csv_data = parse_csv_file_to_dict(self.filepath)
        print(csv_data)
        return {'FINISHED'}


class ApplyResolutionOperator(bpy.types.operator):
    bl_idname = "object.apply_resolution"
    bl_label = "Apply Render resolution"
    
    def execute(self, context):
        set_resolution(context)
        self.report({'INFO'}, "Resolution applied succesfully")
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(ShotToolsPanel)
    bpy.utils.register_class(ParseCSVOperator)
    bpy.utils.register_class(ApplyResolutionOperator)

def unregister():
    bpy.utils.unregister_class(ShotToolsPanel)
    bpy.utils.unregister_class(ParseCSVOperator)
    bpy.utils.unregister_class(ApplyResolutionOperator)
    del bpy.types.Scene.render_mode
    del bpy.types.Scene.render_width
    del bpy.types.Scene.render_height


if __name__== "__main__":
    register()