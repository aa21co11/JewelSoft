

from bpy.types import Panel, Menu, UIList

from . import mod_update
from .lib import dynamic_list, pathutils, unit
from .lib.previewlib import icon, icon_menu


# Lists
# ---------------------------


class VIEW3D_UL_jewelsoft_material_list(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        props = context.scene.jewelsoft
        mainrow = layout.row(align=True)

        row = mainrow.row(align=True)
        row.scale_x = 0.8
        row.prop(item, "enabled", text="")

        row = mainrow.row(align=True)
        row.active = item.enabled
        row.prop(item, "name", text="", emboss=False)

        if props.weighting_show_composition:
            sub = mainrow.row(align=True)
            sub.scale_x = 1.5
            sub.prop(item, "composition", text="", emboss=False)

        if props.weighting_show_density:
            sub = mainrow.row(align=True)
            sub.scale_x = 0.7
            sub.prop(item, "density", text="", emboss=False)


class VIEW3D_UL_jewelsoft_measurements(UIList):
    icons = {
        "DIMENSIONS": "SHADING_BBOX",
        "WEIGHT": "FILE_3D",
        "RING_SIZE": "MESH_CIRCLE",
    }

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.alert = item.collection is None and item.object is None
        layout.prop(item, "name", text="", emboss=False, icon=self.icons.get(item.type, "BLANK1"))


class VIEW3D_UL_jewelsoft_asset_libs(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.split(factor=0.25, align=True)
        row.prop(item, "name", text="", emboss=False)
        row.prop(item, "path", text="", emboss=False)

class VIEW3D_UL_jewelsoft_asset_libs_select(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.label(text=item.name, translate=False)
        row.operator("wm.path_open", text="", icon="FILE_FOLDER", emboss=False).filepath = item.path


class VIEW3D_UL_jewelsoft_sizes(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.active = False
        sub.label(text="Qty")
        row.prop(item, "qty", text="", emboss=False)

        row = layout.row(align=True)
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.active = False
        sub.label(text="Size")
        row.prop(item, "size", text="", emboss=False)


# Menus
# ---------------------------


def draw_jewelsoft_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("VIEW3D_MT_jewelsoft")


class VIEW3D_MT_jewelsoft(Menu):
    bl_label = "jewelsoft"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("object.jewelsoft_gem_add", icon_value=icon_menu("GEM_ADD"))
        layout.operator("object.jewelsoft_gem_edit", icon_value=icon_menu("GEM_EDIT"))
        layout.operator("object.jewelsoft_gem_recover", icon_value=icon_menu("GEM_RECOVER"))
        layout.menu("VIEW3D_MT_jewelsoft_select_gem_by")
        layout.operator("wm.call_panel", text="Spacing Overlay", text_ctxt="*", icon="WINDOW").name = "VIEW3D_PT_jewelsoft_spacing_overlay"
        layout.separator()
        layout.operator("wm.call_panel", text="Assets", text_ctxt="*", icon="WINDOW").name = "VIEW3D_PT_jewelsoft_assets"
        layout.separator()
        layout.operator("object.jewelsoft_prongs_add", icon_value=icon_menu("PRONGS"))
        layout.operator("object.jewelsoft_cutter_add", icon_value=icon_menu("CUTTER"))
        layout.separator()
        layout.operator("object.jewelsoft_mirror", icon_value=icon_menu("MIRROR"))
        layout.operator("object.jewelsoft_radial_instance", icon_value=icon_menu("RADIAL"))
        layout.operator("object.jewelsoft_make_instance_face", icon_value=icon_menu("INSTANCE_FACE"))
        layout.operator("object.jewelsoft_resize", icon_value=icon_menu("RESIZE"))
        layout.operator("object.jewelsoft_lattice_project", icon_value=icon_menu("LATTICE_PROJECT"))
        layout.operator("object.jewelsoft_lattice_profile", icon_value=icon_menu("LATTICE_PROFILE"))
        layout.separator()
        layout.operator("curve.jewelsoft_size_curve_add", icon_value=icon_menu("SIZE_CURVE"))
        layout.operator("object.jewelsoft_stretch_along_curve", icon_value=icon_menu("STRETCH"))
        layout.operator("object.jewelsoft_move_over_under", text="Move Over", icon_value=icon_menu("OVER"))
        layout.operator("object.jewelsoft_move_over_under", text="Move Under", icon_value=icon_menu("UNDER")).under = True
        layout.operator("curve.jewelsoft_length_display", icon_value=icon_menu("CURVE_LENGTH"))
        layout.separator()
        layout.operator("wm.call_panel", text="Weighting", text_ctxt="*", icon="WINDOW").name = "VIEW3D_PT_jewelsoft_weighting"
        layout.separator()
        layout.operator("wm.jewelsoft_design_report", text="Design Report")
        layout.operator("view3d.jewelsoft_gem_map")
        layout.operator("wm.call_panel", text="Measurement", text_ctxt="*", icon="WINDOW").name = "VIEW3D_PT_jewelsoft_measurement"








# Panels
# ---------------------------


class SidebarSetup:
    bl_category = "jewelsoft"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"



class VIEW3D_PT_jewelsoft_warning(SidebarSetup, Panel):
    bl_label = "Warning"

    @classmethod
    def poll(cls, context):
        return unit.check() is not unit.WARN_NONE

    def draw_header(self, context):
        self.layout.alert = True
        self.layout.label(icon="ERROR")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.alignment = "CENTER"

        warning = unit.check()

        if warning is unit.WARN_SCALE:
            row.label(text="Scene scale is not optimal")
        elif warning is unit.WARN_SYSTEM:
            row.label(text="Unsupported unit system")

        row = layout.row()
        row.alignment = "CENTER"
        row.scale_y = 1.5
        row.operator("scene.jewelsoft_scene_units_set")


class VIEW3D_PT_jewelsoft_gems(SidebarSetup, Panel):
    bl_label = "Gems"

    @classmethod
    def poll(cls, context):
        return context.mode in {"OBJECT", "EDIT_MESH"}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator("object.jewelsoft_gem_add", icon_value=icon("GEM_ADD"))
        row.operator("object.jewelsoft_gem_edit", text="", icon_value=icon("GEM_EDIT"))
        row.operator("object.jewelsoft_gem_recover", text="", icon_value=icon("GEM_RECOVER"))

        layout.menu("VIEW3D_MT_jewelsoft_select_gem_by")


class VIEW3D_PT_jewelsoft_spacing_overlay(SidebarSetup, Panel):
    bl_label = "Spacing Overlay"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_jewelsoft_gems"

    def draw_header(self, context):
        wm_props = context.window_manager.jewelsoft
        self.layout.prop(wm_props, "show_spacing", text="")

    def draw(self, context):
        props = context.scene.jewelsoft
        wm_props = context.window_manager.jewelsoft

        layout = self.layout

        if self.is_popover:
            row = layout.row(align=True)
            row.prop(wm_props, "show_spacing", text="")
            row.label(text="Spacing Overlay")

        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.active = wm_props.show_spacing
        col.prop(props, "overlay_show_all")
        col.prop(props, "overlay_show_in_front")
        col.prop(props, "overlay_use_overrides")
        col.prop(props, "overlay_spacing", text="Spacing", text_ctxt="Jewelry")

        col.separator()

        row = col.row(align=True)
        row.operator("object.jewelsoft_overlay_override_add")
        row.operator("object.jewelsoft_overlay_override_del")


c

    


class VIEW3D_PT_jewelsoft_jeweling(SidebarSetup, Panel):
    bl_label = "Jeweling"
    bl_context = "objectmode"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("object.jewelsoft_prongs_add", text="Prongs", icon_value=icon("PRONGS"))
       
        row = layout.row(align=True)
        


class VIEW3D_PT_jewelsoft_measurement(SidebarSetup, Panel):
    bl_label = "Measurement"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "VIEW3D_PT_jewelsoft_design_report"

    def draw(self, context):
        measures_list = context.scene.jewelsoft.measurements

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        if self.is_popover:
            layout.label(text="Measurement")
            layout.separator()

        row = layout.row()

        col = row.column()
        col.template_list(
            "VIEW3D_UL_jewelsoft_measurements",
            "",
            measures_list,
            "coll",
            measures_list,
            "index",
            rows=3,
        )

        col = row.column(align=True)
        col.operator("wm.jewelsoft_ul_measurements_add", text="", icon="ADD")
        col.operator("scene.jewelsoft_ul_del", text="", icon="REMOVE").prop = "measurements"
        col.separator()
        op = col.operator("scene.jewelsoft_ul_move", text="", icon="TRIA_UP")
        op.prop = "measurements"
        op.move_up = True
        col.operator("scene.jewelsoft_ul_move", text="", icon="TRIA_DOWN").prop = "measurements"

        if measures_list.coll:
            item = measures_list.coll[measures_list.index]

            col = layout.column()

            if item.type == "RING_SIZE":
                col.alert = item.object is None
                col.prop(item, "object")
            else:
                col.alert = item.collection is None
                col.prop(item, "collection")

            if item.type == "WEIGHT":
                box = layout.box()
                row = box.row()
                row.label(text=item.material_name, translate=False)
                row.operator("wm.jewelsoft_ul_measurements_material_select", text="", icon="DOWNARROW_HLT", emboss=False)
            elif item.type == "DIMENSIONS":
                col = layout.column(heading="Dimensions", align=True)
                col.prop(item, "x")
                col.prop(item, "y")
                col.prop(item, "z")
            elif item.type == "RING_SIZE":
                layout.prop(item, "ring_size")
                layout.prop(item, "axis", expand=True)


# Preferences
# ---------------------------


def prefs_ui(self, context):
    wm_props = context.window_manager.jewelsoft
    active_tab = wm_props.prefs_active_tab

    layout = self.layout
    layout.use_property_split = True
    layout.use_property_decorate = False

    split = layout.split(factor=0.25)
    col = split.column()
    col.use_property_split = False
    col.scale_y = 1.3
    col.prop(wm_props, "prefs_active_tab", expand=True)

    box = split.box()

    if active_tab == "ASSET_MANAGER":
        box.label(text="Libraries")
        col = box.column()
        row = col.row()

        col = row.column()
        col.template_list(
            "VIEW3D_UL_jewelsoft_asset_libs",
            "",
            wm_props.asset_libs,
            "coll",
            wm_props.asset_libs,
            "index",
            rows=4,
        )

        col = row.column(align=True)
        col.operator("wm.jewelsoft_ul_add", text="", icon="ADD").prop = "asset_libs"
        col.operator("wm.jewelsoft_ul_del", text="", icon="REMOVE").prop = "asset_libs"
        col.separator()
        op = col.operator("wm.jewelsoft_ul_move", text="", icon="TRIA_UP")
        op.prop = "asset_libs"
        op.move_up = True
        col.operator("wm.jewelsoft_ul_move", text="", icon="TRIA_DOWN").prop = "asset_libs"


    elif active_tab == "DESIGN_REPORT":
        col = box.column()
        col.prop(self, "report_lang")

        box.label(text="Gem Map Font Size")
        col = box.column()
        col.prop(self, "gem_map_fontsize_table")
        col.prop(self, "gem_map_fontsize_gem_size")

    elif active_tab == "THEMES":
        box.label(text="Spacing Overlay")
        col = box.column()
        col.prop(self, "overlay_color")
        col.prop(self, "overlay_linewidth")
        col.prop(self, "overlay_fontsize_distance")

    elif active_tab == "UPDATES":
        mod_update.prefs_ui(self, box)
