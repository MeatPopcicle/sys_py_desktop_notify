# ────────────────────────────────────────────────────────────────────────────────
# desktop_notify - Unified Desktop Notification System
# ────────────────────────────────────────────────────────────────────────────────
"""
desktop_notify

A comprehensive, backend-agnostic Python interface for desktop notification 
systems on Linux. Provides unified API targeting multiple notification backends
with rich icon resolution and configuration management.

Basic Usage:
    from desktop_notify import send_notification
    
    send_notification("mic", "Recording Started", "Audio recording in progress")

Advanced Usage:
    from desktop_notify import NotificationManager
    
    manager = NotificationManager(backend="dunst", timeout=3000)
    manager.send("error", "Process Failed", "Could not complete operation")
"""

# Setup logging early
from . import logging_setup

from .api import send_notification, NotificationManager, is_notifications_available, get_notification_backend
from .exceptions import DesktopNotifyError, BackendError, IconError

__version__ = "1.0.0"
__all__ = [
    "send_notification",
    "NotificationManager", 
    "is_notifications_available",
    "get_notification_backend",
    "DesktopNotifyError",
    "BackendError",
    "IconError",
]