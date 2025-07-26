# ────────────────────────────────────────────────────────────────────────────────
# Notification Backends
# ────────────────────────────────────────────────────────────────────────────────
"""
backends

Pluggable notification backend system supporting multiple notification daemons.
"""

from .base import NotificationBackend
from .dunst import DunstBackend
from .console import ConsoleBackend
from .discovery import BackendDiscovery

__all__ = [
    "NotificationBackend",
    "DunstBackend", 
    "ConsoleBackend",
    "BackendDiscovery",
]