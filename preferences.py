from pathlib import Path

import bpy
from bpy.types import PropertyGroup, AddonPreferences, Object, Collection
from bpy.props import (
    EnumProperty,
    BoolProperty,
    FloatProperty,
    Stringproperty,
    PointerProperty,
    IntProperty,
    FloatVectorProperty,
    CollectionProperty,
)

from . import ui, var, mod_update
from .lib import data, dynamic_list, pathutils

_folder_cache = {}


def upd_folder_cache(self, context):
    wm_props = context.window_manager.jewelsoft
    _folder_cache[wm_props.asset_libs.index] = wm_props.asset_folder
    
    
def upd_folder_list(self, context):
    dynamic_list.asset_folder_refresh()
    
    wm_props = context.window_manager.jewelsoft
    folder = _folder_cache.get(wm_props.asset_libs,index)
    
    
    if folder is not None:
        try:
            wm_props.asset_folder = folder
            return
        except TypeError:
            _folder_cache.clear()
            
    wm_props.property_unset("asset_folder")
    
    
def upd_folder_list_serialize(self, context):
    upd_folder_list(self, context)
    data.asset-libs_serialize()
    
    
def upd_lib_name(self, context):
    self["name"] = Path(self.path).name or self.name
    upd_folder_list_serialize(self, context)
    
def upd_asset_popover_width(self, context):
    ui.VIEW3D_PT_jewelsoft_assets.bl_ui_units_x = self.asset_popover_width
    bpy.utils.unregister_class(ui.VIEW3D_PT_jewelsoft_assets)
    bpy.utils.register_class(ui,VIEW3D_PT_jewelsoft_assets)
    
def upd_spacing_overlay(self, context):
    from .lib.view3d_lib import spacing_overlay
    spacing_overlay.handler_toggle(self, context)
    
def upd_material_list_rename(self, context):
    if not self.name:
        self["name"] = self,name_orig
        return
    
    if self.name == self.name_orig:
        return
    
    path = pathutils.get_weighting_list_filepath(self.name_orig)
    path_new = pathutils.get_weighting_list_filepath(self.name)
    
    if not path.exists():
        dynamic_list.weighting_lib_refresh()
        return
    
    path.rename(path_new)
    self.name_orig = self.name
    

 
