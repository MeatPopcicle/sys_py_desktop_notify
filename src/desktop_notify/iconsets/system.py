# ────────────────────────────────────────────────────────────────────────────────
# System Icon Set with py_notify Integration
# ────────────────────────────────────────────────────────────────────────────────
"""
system.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

System icon set using py_notify.IconResolver from:
/home/gauol/Scratch/Projects - Code/py_nofify
"""

import logging
from typing import List, Optional
from pathlib import Path

from .base import IconSet
from ..exceptions import IconError

try:
    # ═══════════════════════════════════════════════════════════════════════════════
    # IMPORT py_notify.IconResolver
    # ═══════════════════════════════════════════════════════════════════════════════
    from py_notify import IconResolver
    PY_NOTIFY_AVAILABLE = True
except ImportError as e:
    PY_NOTIFY_AVAILABLE = False
    IconResolver = None


class SystemIconSet(IconSet):
    """
    ///////////////////////////////////////////////////////////////////
    SYSTEM ICON SET
    ▄▄▄▄▄ ▄▄▄ ▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄ ▄▄▄▄▄
    █▄▄▄▄ █▄▄ █▄▄▄   █   █▄▄▄ █▄▄▄▄
    ▄▄▄▄█ █▄▄ █▄▄▄   █   █▄▄▄ █▄▄▄▄
    ///////////////////////////////////////////////////////////////////
    System icon set using desktop theme icons via py_notify.IconResolver.
    
    INTEGRATION: Uses py_notify.IconResolver from:
    /home/gauol/Scratch/Projects - Code/py_nofify
    """
    
    def __init__(self, theme_name: Optional[str] = None, icon_size: int = 48):
        """
        Initialize system icon set.
        
        Args:
            theme_name: Icon theme name (None for auto-detection)
            icon_size: Preferred icon size in pixels
        """
        self.theme_name  = theme_name
        self.icon_size   = icon_size
        self.logger      = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Initialize py_notify IconResolver
        # ─────────────────────────────────────────────────────────────────
        self._resolver   = None
        self._cache      = {}  # Icon name -> resolved path cache
        
        if PY_NOTIFY_AVAILABLE:
            try:
                # Pass theme and size to IconResolver!
                self._resolver = IconResolver(
                    theme=self.theme_name,
                    size=self.icon_size
                )
                self.logger.debug(f"Initialized py_notify.IconResolver with theme='{self.theme_name}', size={self.icon_size}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize IconResolver: {e}")
                self._resolver = None
        else:
            self.logger.warning("py_notify not available - system icons disabled")
    
    @property
    def name(self) -> str:
        """Return the name of this icon set."""
        return "system"
    
    @property 
    def priority(self) -> int:
        """Return the priority of this icon set."""
        return 100  # Highest priority - prefer system icons
    
    def get_icon(self, name: str) -> Optional[str]:
        """
        ─────────────────────────────────────────────────────────────────
        Resolve icon name using py_notify.IconResolver
        ─────────────────────────────────────────────────────────────────
        """
        if not self.is_available():
            return None
        
        # Check cache first
        if name in self._cache:
            return self._cache[name]
        
        try:
            # Use py_notify.IconResolver to resolve icon
            result = self._resolver.resolve(name)
            
            if result:
                resolved_path = str(result)
                
                # Verify the file exists
                if Path(resolved_path).exists():
                    self._cache[name] = resolved_path
                    self.logger.debug(f"Resolved '{name}' -> '{resolved_path}'")
                    return resolved_path
                else:
                    self.logger.debug(f"Resolved path does not exist: {resolved_path}")
            
        except Exception as e:
            self.logger.debug(f"Failed to resolve icon '{name}': {e}")
        
        # Cache negative results to avoid repeated lookups
        self._cache[name] = None
        return None
    
    def list_icons(self) -> List[str]:
        """
        List available system icons.
        
        Note: This is a basic implementation. The py_notify.IconResolver
        may provide better methods for listing available icons.
        """
        # Common system icon names that are likely to be available
        common_icons = [
            # Status icons
            "info", "warning", "error", "question",
            "dialog-information", "dialog-warning", "dialog-error", "dialog-question",
            
            # Action icons  
            "save", "open", "close", "quit", "edit", "delete", "add", "remove",
            "copy", "cut", "paste", "undo", "redo", "find", "replace",
            
            # Device icons
            "computer", "monitor", "keyboard", "mouse", "printer", "scanner",
            "camera", "microphone", "speaker", "headphones",
            
            # Media icons
            "audio", "video", "image", "document", "text", "folder",
            "file", "archive", "music", "movie",
            
            # Network icons
            "network", "internet", "wifi", "bluetooth", "email", "web-browser",
            
            # System icons
            "preferences", "settings", "configure", "system", "user", "group",
            "security", "lock", "unlock", "key", "password",
            
            # Application icons
            "terminal", "calculator", "calendar", "clock", "games",
            "graphics", "office", "development", "multimedia",
        ]
        
        # Filter to only return icons that can actually be resolved
        available_icons = []
        for icon_name in common_icons:
            if self.get_icon(icon_name) is not None:
                available_icons.append(icon_name)
        
        return available_icons
    
    def is_available(self) -> bool:
        """Check if system icon set is available."""
        return (PY_NOTIFY_AVAILABLE and 
                self._resolver is not None)
    
    def clear_cache(self) -> None:
        """Clear the icon resolution cache."""
        self._cache.clear()
        self.logger.debug("Cleared icon cache")
    
    def update_configuration(self, theme_name: Optional[str] = None, icon_size: Optional[int] = None) -> None:
        """
        Update IconResolver configuration.
        
        Args:
            theme_name: New theme name (None to keep current)
            icon_size: New icon size (None to keep current)
        """
        if not PY_NOTIFY_AVAILABLE or not self._resolver:
            return
        
        # Update configuration if provided
        if theme_name is not None:
            self.theme_name = theme_name
            
        if icon_size is not None:
            self.icon_size = icon_size
        
        try:
            # Update IconResolver properties
            if theme_name is not None:
                self._resolver.theme = self.theme_name
                self.logger.debug(f"Updated IconResolver theme to: {self.theme_name}")
                
            if icon_size is not None:
                self._resolver.size = self.icon_size
                self.logger.debug(f"Updated IconResolver size to: {self.icon_size}")
            
            # Clear cache since resolution may change
            self.clear_cache()
            
        except Exception as e:
            self.logger.warning(f"Failed to update IconResolver configuration: {e}")