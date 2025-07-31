# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Type Definitions
# ────────────────────────────────────────────────────────────────────────────────
"""
types.py
AUTHOR: Desktop Notify Team  
DATE: 2024-01-15
VERSION: 1.0.0

Type definitions and data structures for desktop notification system.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
from enum import Enum


class IconResolutionSource(Enum):
    """Source of icon resolution."""
    SYSTEM_THEME = "system_theme"     # Resolved from system icon theme
    MATERIAL = "material"             # Material Design icon set
    NERDFONTS = "nerdfonts"          # Nerd Fonts icon set  
    MINIMAL = "minimal"              # Unicode/emoji fallback
    FILE_PATH = "file_path"          # Direct file path
    UNICODE = "unicode"              # Unicode character/emoji
    FALLBACK = "fallback"            # Final fallback icon
    NOT_FOUND = "not_found"          # Icon not resolved


@dataclass
class IconResolutionInfo:
    """
    Detailed information about icon resolution.
    
    Provides complete details about how an icon name was resolved,
    including the final path, source, and any fallback chain used.
    """
    
    # Basic resolution info
    original_name: str                    # Original icon name requested
    resolved_path: Optional[str]          # Final resolved path/glyph
    source: IconResolutionSource          # Where the icon came from
    
    # Resolution metadata  
    icon_set_used: Optional[str] = None   # Which icon set was used
    theme_name: Optional[str] = None      # System theme name (if applicable)
    size: Optional[int] = None            # Icon size (if applicable)
    is_fallback: bool = False             # Whether fallback was used
    
    # Fallback chain
    attempted_sources: list = None        # List of sources tried
    fallback_chain: list = None           # Chain of fallback attempts
    
    # Performance info
    resolution_time_ms: Optional[float] = None  # Time taken to resolve
    cached: bool = False                  # Whether result was cached
    
    def __post_init__(self):
        """Initialize default values."""
        if self.attempted_sources is None:
            self.attempted_sources = []
        if self.fallback_chain is None:
            self.fallback_chain = []
    
    @property
    def success(self) -> bool:
        """Whether icon resolution was successful."""
        return self.resolved_path is not None
    
    @property 
    def is_unicode(self) -> bool:
        """Whether the resolved icon is a unicode character."""
        return self.source in [IconResolutionSource.UNICODE, IconResolutionSource.MINIMAL]
    
    @property
    def is_file_path(self) -> bool:
        """Whether the resolved icon is a file path."""
        return self.source in [IconResolutionSource.SYSTEM_THEME, IconResolutionSource.MATERIAL, 
                              IconResolutionSource.NERDFONTS, IconResolutionSource.FILE_PATH]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "original_name": self.original_name,
            "resolved_path": self.resolved_path,
            "source": self.source.value,
            "icon_set_used": self.icon_set_used,
            "theme_name": self.theme_name,
            "size": self.size,
            "is_fallback": self.is_fallback,
            "attempted_sources": [s.value if hasattr(s, 'value') else str(s) for s in self.attempted_sources],
            "fallback_chain": self.fallback_chain,
            "resolution_time_ms": self.resolution_time_ms,
            "cached": self.cached,
            "success": self.success,
            "is_unicode": self.is_unicode,
            "is_file_path": self.is_file_path,
        }
    
    def __str__(self) -> str:
        """String representation for debugging."""
        status = "✅" if self.success else "❌"
        source_info = f"{self.source.value}"
        if self.icon_set_used:
            source_info += f" ({self.icon_set_used})"
        
        result = f"{status} '{self.original_name}' → {self.resolved_path or 'None'} [{source_info}]"
        
        if self.is_fallback:
            result += " (fallback)"
        if self.cached:
            result += " (cached)"
            
        return result


@dataclass
class NotificationResult:
    """
    Result of sending a notification with detailed information.
    
    Provides comprehensive feedback about notification sending,
    including action results and icon resolution details.
    """
    
    # Basic result
    success: bool                          # Whether notification was sent
    action_result: Optional[str] = None    # Selected action (for interactive notifications)
    
    # Icon resolution details
    icon_resolution: Optional[IconResolutionInfo] = None
    
    # Backend information
    backend_used: Optional[str] = None     # Which backend was used
    notification_id: Optional[str] = None  # ID used for the notification
    
    # Timing information
    send_time_ms: Optional[float] = None   # Time taken to send
    total_time_ms: Optional[float] = None  # Total time including resolution
    
    # Error information
    error_message: Optional[str] = None    # Error details if failed
    
    def __bool__(self) -> bool:
        """Boolean conversion for backward compatibility."""
        return self.success
    
    def __str__(self) -> str:
        """String representation returns action_result for interactive notifications."""
        if self.action_result is not None:
            return self.action_result
        return str(self.success)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "success": self.success,
            "action_result": self.action_result,
            "backend_used": self.backend_used,
            "notification_id": self.notification_id,
            "send_time_ms": self.send_time_ms,
            "total_time_ms": self.total_time_ms,
            "error_message": self.error_message,
        }
        
        if self.icon_resolution:
            result["icon_resolution"] = self.icon_resolution.to_dict()
        
        return result


# Type aliases for common use cases
NotificationResponse = Union[bool, str, NotificationResult]
IconResolutionResult = Union[str, IconResolutionInfo]