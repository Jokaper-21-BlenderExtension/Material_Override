import bpy

bl_info = {
    "name": "Material Pro Tools",
    "blender": (4, 2, 0),
    "category": "Object",
}

# Operator to override materials of selected objects
class OBJECT_OT_override_material(bpy.types.Operator):
    """Override materials of selected objects"""
    bl_idname = "object.override_material"
    bl_label = "Override Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    material_name: bpy.props.StringProperty(
        name="Override Material",
        description="Name of the material to override with",
        default=""
    )
    
    def execute(self, context):
        # Get the override material by name
        override_material = bpy.data.materials.get(self.material_name)
        
        if not override_material:
            self.report({'WARNING'}, f"Material '{self.material_name}' not found")
            return {'CANCELLED'}
        
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected.")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            if obj.type == 'MESH':
                # If no material slots, create a new one
                if len(obj.material_slots) == 0:
                    obj.data.materials.append(None)
                
                for i, mat_slot in enumerate(obj.material_slots):
                    # Override each material slot individually
                    obj.material_slots[i].material = override_material
        
        return {'FINISHED'}

# Operator to clear all materials but keep empty slots
class OBJECT_OT_clear_material_slots(bpy.types.Operator):
    """Clear all materials but keep empty slots"""
    bl_idname = "object.clear_material_slots"
    bl_label = "Clear Materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                for mat_slot in obj.material_slots:
                    # Clear material, but keep the empty slot
                    mat_slot.material = None
        
        return {'FINISHED'}

# Operator to remove all material slots
class OBJECT_OT_remove_material_slots(bpy.types.Operator):
    """Remove all material slots"""
    bl_idname = "object.remove_material_slots"
    bl_label = "Remove Material Slots"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Clear all material slots
                obj.data.materials.clear()
        
        return {'FINISHED'}

# Panel to hold all the buttons
class VIEW3D_PT_override_material_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Material Override"
    bl_idname = "VIEW3D_PT_override_material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AJO'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop_search(context.window_manager, "override_material_name", bpy.data, "materials", text="")
        
        # Apply operator with the selected material name
        operator = layout.operator("object.override_material", text="Apply", icon="PLAY")
        operator.material_name = context.window_manager.override_material_name
        
        # Create a row layout for side-by-side buttons
        row = layout.row()
        row.operator("object.clear_material_slots", text="Clear", icon="X")
        row.operator("object.remove_material_slots", text="Remove", icon="CANCEL")

def register():
    bpy.utils.register_class(OBJECT_OT_override_material)
    bpy.utils.register_class(OBJECT_OT_clear_material_slots)
    bpy.utils.register_class(OBJECT_OT_remove_material_slots)
    bpy.utils.register_class(VIEW3D_PT_override_material_panel)
    bpy.types.WindowManager.override_material_name = bpy.props.StringProperty(
        name="Override Material",
        description="Name of the material to override with",
        default=""
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_override_material)
    bpy.utils.unregister_class(OBJECT_OT_clear_material_slots)
    bpy.utils.unregister_class(OBJECT_OT_remove_material_slots)
    bpy.utils.unregister_class(VIEW3D_PT_override_material_panel)
    del bpy.types.WindowManager.override_material_name

if __name__ == "__main__":
    register()
