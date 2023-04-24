
bl_info = {
    "name": "JewelSoft",
    "author": "Student of AIKTC SECO",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "View 3D > Sidebar",
    "description": "Jewelry design Plugin",
    "category": "3D VIEW",
}


if "bpy" in locals():
    _essential.reload_recursive(var.ADDON_DIR, locals())
else:
    import bpy
    from bpy.props import PointerProperty

    from . import var
    from .lib import _essential

    _essential.check(var.ICONS_DIR, bl_info["blender"])

    from . import (
        ui,
        preferences,
        op_gem_map,
        op_design_report,
        op_prongs,
        op_distribute,
        ops_gem,
        ops_measurement,
        ops_utils,
        ops_weighting,
    )
    from .lib import on_load, previewlib, data


classes = (
    preferences.MeasurementCollection,
    preferences.MaterialCollection,
    preferences.MaterialListCollection,
    preferences.AssetLibCollection,
    preferences.SizeCollection,
    preferences.MeasurementList,
    preferences.MaterialList,
    preferences.AssetLibList,
    preferences.SizeList,
    preferences.Preferences,
    preferences.WmProperties,
    preferences.SceneProperties,
    ui.VIEW3D_UL_jewelsoft_material_list,
    ui.VIEW3D_UL_jewelsoft_measurements,
    ui.VIEW3D_UL_jewelsoft_asset_libs,
    ui.VIEW3D_UL_jewelsoft_asset_libs_select,
    ui.VIEW3D_UL_jewelsoft_sizes,
    ui.VIEW3D_MT_jewelsoft,
    ui.VIEW3D_PT_jewelsoft_warning,
    ui.VIEW3D_PT_jewelsoft_gems,
    ui.VIEW3D_PT_jewelsoft_spacing_overlay,
    ui.VIEW3D_PT_jewelsoft_jeweling,
    ui.VIEW3D_PT_jewelsoft_measurement,
    ops_gem.OBJECT_OT_gem_add,
)


def register():
    for cls in classes:
        if cls is ui.VIEW3D_PT_jewelsoft_assets:
            prefs = bpy.context.preferences.addons[__package__].preferences
            cls.bl_ui_units_x = prefs.asset_popover_width
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.jewelsoft = PointerProperty(type=preferences.WmProperties)
    bpy.types.Scene.jewelsoft = PointerProperty(type=preferences.SceneProperties)

    bpy.types.VIEW3D_MT_object.append(ui.draw_jewelsoft_menu)


    on_load.handler_add()


    data.versioning_asset_favs()


def unregister():
    from .lib.view3d_lib import spacing_overlay

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.jewelsoft
    del bpy.types.Scene.jewelsoft

    bpy.types.VIEW3D_MT_object.remove(ui.draw_jewelsoft_menu)

    spacing_overlay.handler_del()
    on_load.handler_del()


    bpy.app.translations.unregister(__name__)

    previewlib.clear_previews()

    preferences._folder_cache.clear()


if __name__ == "__main__":
    register()
