# ────────────────────────────────────────────────────────────────────────────────
# Icon Resolution System
# ────────────────────────────────────────────────────────────────────────────────
"""
iconsets

Multi-format icon resolution system with automatic fallbacks and 
integration with py_notify.IconResolver for system icons.
"""

from .base import IconSet
from .manager import IconSetManager, get_icon_set_manager
from .system import SystemIconSet
from .material import MaterialIconSet
from .minimal import MinimalIconSet

__all__ = [
    "IconSet",
    "IconSetManager",
    "get_icon_set_manager",
    "SystemIconSet",
    "MaterialIconSet", 
    "MinimalIconSet",
]