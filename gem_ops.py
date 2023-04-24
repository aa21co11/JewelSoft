
import bpy
from bpy.props import EnumProperty, FloatProperty, BoolProperty
from bpy.types import Operator
from bpy.app.translations import pgettext_iface as _
from mathutils import Matrix

from .. import var
from ..lib import dynamic_list, unit


def upd_set_weight(self, context):
    if self.stone == "DIAMOND" and self.cut == "ROUND":
        self["weight"] = unit.convert_mm_ct(unit.Scale().from_scene(self.size))


def upd_weight(self, context):
    self["size"] = unit.Scale().to_scene(unit.convert_ct_mm(self.weight))


class OBJECT_OT_gem_add(Operator):
    bl_label = "Add Gem"
    bl_description = "Add gemstone to the scene"
    bl_idname = "object.jewelsoft_gem_add"
    bl_options = {"REGISTER", "UNDO"}

    cut: EnumProperty(name="Cut", items=dynamic_list.cuts, update=upd_set_weight)
    stone: EnumProperty(name="Stone", items=dynamic_list.stones, update=upd_set_weight)
    size: FloatProperty(
        name="Size",
        default=1.0,
        min=0.0001,
        step=5,
        precision=2,
        unit="LENGTH",
        update=upd_set_weight,
    )
    weight: FloatProperty(
        name="Carats",
        description="Round diamonds only",
        default=0.004,
        min=0.0001,
        step=0.1,
        precision=3,
        update=upd_weight,
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, "size")
        col = layout.column()
        col.enabled = self.stone == "DIAMOND" and self.cut == "ROUND"
        col.prop(self, "weight")
        layout.prop(self, "stone")
        split = layout.split(factor=0.4)
        row = split.row()
        row.alignment = "RIGHT"
        row.label(text="Cut", text_ctxt="Jewelry")
        split.template_icon_view(self, "cut", show_labels=True)

    def execute(self, context):
        from ..lib import asset, gemlib

        scene = context.scene
        view_layer = context.view_layer
        space_data = context.space_data
        cut_name = gemlib.CUTS[self.cut].name
        stone_name = gemlib.STONES[self.stone].name
        color = gemlib.STONES[self.stone].color or self.color

        for ob in context.selected_objects:
            ob.select_set(False)

        imported = asset.asset_import(var.GEM_ASSET_FILEPATH, ob_name=cut_name)
        ob = imported.objects[0]
        context.collection.objects.link(ob)

        if space_data.local_view:
            ob.local_view_set(space_data, True)

        ob.scale *= self.size
        ob.location = scene.cursor.location
        ob.select_set(True)
        ob["gem"] = {"cut": self.cut, "stone": self.stone}

        asset.add_material(ob, name=stone_name, color=color, is_gem=True)

        if context.mode == "EDIT_MESH":
            asset.ob_copy_to_faces(ob)
            bpy.ops.object.mode_set(mode="OBJECT")

        view_layer.objects.active = ob

        return {"FINISHED"}

    def invoke(self, context, event):
        from ..lib import asset

        self.color = asset.color_rnd()

        wm = context.window_manager
        return wm.invoke_props_dialog(self)


