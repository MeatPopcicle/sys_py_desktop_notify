# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Exceptions
# ────────────────────────────────────────────────────────────────────────────────
"""
exceptions.py
AUTHOR: Desktop Notify Team  
DATE: 2024-01-15
VERSION: 1.0.0

Exception hierarchy for desktop notification system.
"""


class DesktopNotifyError(Exception):
    """Base exception for desktop notification system."""
    pass


class BackendError(DesktopNotifyError):
    """Exception raised for backend-related errors."""
    pass


class IconError(DesktopNotifyError):
    """Exception raised for icon resolution errors."""
    pass


class ConfigurationError(DesktopNotifyError):
    """Exception raised for configuration-related errors."""
    pass