
from pathlib import Path

ADDON_ID = __package__
ADDON_DIR = Path(__file__).parent
CONFIG_DIR = ADDON_DIR / ".config"

if not CONFIG_DIR.exists():
    import sys

    if sys.platform == "win32":
        CONFIG_DIR = Path.home() / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / "JewelSoft"
    elif sys.platform == "darwin":
        CONFIG_DIR = Path.home() / "Library" / "Application Support" / "Blender" / "JewelSoft"
    else:
        CONFIG_DIR = Path.home() / ".config" / "blender" / "JewelSoft"

GEM_ASSET_DIR = ADDON_DIR / "assets" / "gems"
GEM_ASSET_FILEPATH = GEM_ASSET_DIR / "gems.blend"
ICONS_DIR = ADDON_DIR / "assets" / "icons"

WEIGHTING_LIB_USER_DIR = CONFIG_DIR / "Weighting Library"
ASSET_LIBS_FILEPATH = CONFIG_DIR / "libraries.json"
ASSET_FAVS_FILEPATH = CONFIG_DIR / "favorites.json"
