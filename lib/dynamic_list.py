
from pathlib import Path
from functools import lru_cache
from typing import Optional, Union

import bpy
from bpy.app.translations import pgettext_iface as _

from .. import var
from . import pathutils, previewlib


EnumItems3 = tuple[tuple[str, str, str], ...]
EnumItems4 = tuple[tuple[str, str, str, int], ...]
EnumItems5 = tuple[tuple[str, str, str, Union[str, int], int], ...]
AssetItems = tuple[tuple[str, str, int, bool], ...]


def _iface_lang(context) -> str:
    view = context.preferences.view

    if view.use_translate_interface:
        return view.language

    return "en_US"


# Gems
# ---------------------------


def cuts(self, context) -> EnumItems5:
    lang = _iface_lang(context)
    color = context.preferences.themes[0].user_interface.wcol_menu_item.text.v

    return _cuts(lang, color)


def stones(self, context) -> EnumItems4:
    lang = _iface_lang(context)

    return _stones(lang)


@lru_cache(maxsize=1)
def _cuts(lang: str, color: float) -> EnumItems5:
    from . import gemlib

    pcoll = previewlib.scan_icons("cuts", var.GEM_ASSET_DIR)
    theme = "DARK" if color < 0.5 else "LIGHT"

    return tuple(
        (k, _(_(v.name, "Jewelry")), "", pcoll[theme + k].icon_id, i)  # _(_()) default return value workaround
        for i, (k, v) in enumerate(gemlib.CUTS.items())
    )


@lru_cache(maxsize=1)
def _stones(lang: str) -> EnumItems4:
    import operator
    from . import gemlib

    list_ = [
        (k, _(_(v.name, "Jewelry")), "", i)  # _(_()) default return value workaround
        for i, (k, v) in enumerate(gemlib.STONES.items())
    ]

    list_.sort(key=operator.itemgetter(1))

    return tuple(list_)




# Other
# ---------------------------


def abc(self, context) -> EnumItems3:
    return _abc()


@lru_cache(maxsize=1)
def _abc() -> EnumItems3:
    import string
    return tuple((str(i), char, "") for i, char in enumerate(string.ascii_uppercase))
