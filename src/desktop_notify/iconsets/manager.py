# ────────────────────────────────────────────────────────────────────────────────
# Icon Set Manager
# ────────────────────────────────────────────────────────────────────────────────
"""
manager.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Icon set management system with automatic fallbacks and caching.
"""

import logging
from typing import Dict, List, Optional
from functools import lru_cache

from .base import IconSet
from .system import SystemIconSet
from .material import MaterialIconSet
from .minimal import MinimalIconSet
from ..exceptions import IconError


class IconSetManager:
    """
    ///////////////////////////////////////////////////////////////////
    ICON SET MANAGER
    ▄▄▄ ▄▄▄▄ ▄▄▄  ▄▄ ▄▄▄▄▄ ▄▄▄▄ ▄▄▄
    █   █    █▀▀  ██   █   █▄▄▄ █▀▀
    █▄▄ █▄▄▄ █▄▄  ██   █   █▄▄▄ █▄▄
    ///////////////////////////////////////////////////////////////////
    Manages multiple icon sets with intelligent fallback and caching.
    """
    
    def __init__(self, preferred_icon_set: str = "auto"):
        """
        Initialize icon set manager.
        
        Args:
            preferred_icon_set: Preferred icon set name or "auto"
        """
        self.preferred_icon_set = preferred_icon_set
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Initialize icon sets
        # ─────────────────────────────────────────────────────────────────
        self.icon_sets: Dict[str, IconSet] = {}
        self.active_icon_set: Optional[str] = None
        
        self._register_default_icon_sets()
        self._select_active_icon_set()
    
    def _register_default_icon_sets(self):
        """Register the default icon sets."""
        # Import here to avoid circular imports
        from ..config import get_config
        
        try:
            config = get_config()
            system_theme = config.system_icon_theme
            system_size = config.system_icon_size
            system_prefer_scalable = config.system_prefer_scalable
            system_debug_logging = config.system_debug_logging
        except:
            # Fallback if config not available
            system_theme = None
            system_size = 48
            system_prefer_scalable = False
            system_debug_logging = False
        
        # Register icon sets with configuration
        icon_set_configs = [
            (SystemIconSet, {
                "theme_name": system_theme, 
                "icon_size": system_size,
                "prefer_scalable": system_prefer_scalable,
                "debug_logging": system_debug_logging
            }),
            (MaterialIconSet, {}),
            (MinimalIconSet, {}),
        ]
        
        for icon_set_class, kwargs in icon_set_configs:
            try:
                icon_set = icon_set_class(**kwargs)
                self.icon_sets[icon_set.name] = icon_set
                self.logger.debug(f"Registered icon set: {icon_set.name}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize {icon_set_class.__name__}: {e}")
    
    def _select_active_icon_set(self):
        """Select the active icon set based on preferences and availability."""
        if self.preferred_icon_set == "auto":
            # Automatically select the best available icon set
            available_sets = [(name, icon_set) for name, icon_set in self.icon_sets.items() 
                             if icon_set.is_available()]
            
            if available_sets:
                # Sort by priority (higher = better)
                available_sets.sort(key=lambda x: x[1].priority, reverse=True)
                self.active_icon_set = available_sets[0][0]
                self.logger.info(f"Auto-selected icon set: {self.active_icon_set}")
            else:
                self.logger.warning("No icon sets available")
                
        else:
            # Use explicitly specified icon set
            if self.preferred_icon_set in self.icon_sets:
                icon_set = self.icon_sets[self.preferred_icon_set]
                if icon_set.is_available():
                    self.active_icon_set = self.preferred_icon_set
                    self.logger.info(f"Using preferred icon set: {self.active_icon_set}")
                else:
                    self.logger.warning(f"Preferred icon set '{self.preferred_icon_set}' not available")
                    self._select_active_icon_set_fallback()
            else:
                self.logger.warning(f"Unknown icon set: {self.preferred_icon_set}")
                self._select_active_icon_set_fallback()
    
    def _select_active_icon_set_fallback(self):
        """Select fallback icon set when preferred is unavailable."""
        # Try minimal icon set as ultimate fallback
        if "minimal" in self.icon_sets and self.icon_sets["minimal"].is_available():
            self.active_icon_set = "minimal"
            self.logger.info("Using fallback icon set: minimal")
        else:
            self.logger.error("No fallback icon set available")
    
    @lru_cache(maxsize=256)
    def get_icon(self, name: str, fallback: bool = True) -> Optional[str]:
        """
        ─────────────────────────────────────────────────────────────────
        Get icon with intelligent fallback
        ─────────────────────────────────────────────────────────────────
        """
        if not self.active_icon_set:
            if fallback and "minimal" in self.icon_sets:
                return self.icon_sets["minimal"].get_icon(name)
            return None
        
        # Try active icon set first
        active_set = self.icon_sets[self.active_icon_set]
        icon = active_set.get_icon(name)
        
        if icon is not None:
            return icon
        
        if not fallback:
            return None
        
        # ─────────────────────────────────────────────────────────────────
        # Try fallback icon sets in priority order
        # ─────────────────────────────────────────────────────────────────
        fallback_sets = [
            (name, icon_set) for name, icon_set in self.icon_sets.items()
            if name != self.active_icon_set and icon_set.is_available()
        ]
        
        # Sort by priority (higher = better)
        fallback_sets.sort(key=lambda x: x[1].priority, reverse=True)
        
        for set_name, icon_set in fallback_sets:
            icon = icon_set.get_icon(name)
            if icon is not None:
                self.logger.debug(f"Found '{name}' in fallback set: {set_name}")
                return icon
        
        # Ultimate fallback - return unknown icon from minimal set
        if "minimal" in self.icon_sets:
            return self.icon_sets["minimal"].get_icon("question")
        
        return None
    
    def set_active_icon_set(self, name: str) -> bool:
        """
        Set the active icon set.
        
        Args:
            name: Icon set name to activate
            
        Returns:
            True if successfully set, False otherwise
        """
        if name not in self.icon_sets:
            self.logger.error(f"Unknown icon set: {name}")
            return False
        
        icon_set = self.icon_sets[name]
        if not icon_set.is_available():
            self.logger.error(f"Icon set '{name}' is not available")
            return False
        
        self.active_icon_set = name
        self.preferred_icon_set = name
        
        # Clear cache when switching icon sets
        self.get_icon.cache_clear()
        
        self.logger.info(f"Switched to icon set: {name}")
        return True
    
    def get_active_icon_set(self) -> Optional[str]:
        """Get the name of the currently active icon set."""
        return self.active_icon_set
    
    def list_available_sets(self) -> List[str]:
        """List names of available icon sets."""
        return [name for name, icon_set in self.icon_sets.items() 
                if icon_set.is_available()]
    
    def list_all_sets(self) -> List[str]:
        """List names of all registered icon sets."""
        return list(self.icon_sets.keys())
    
    def get_icon_set_info(self, name: str) -> Optional[Dict[str, any]]:
        """
        Get information about a specific icon set.
        
        Args:
            name: Icon set name
            
        Returns:
            Dictionary with icon set information or None
        """
        if name not in self.icon_sets:
            return None
        
        icon_set = self.icon_sets[name]
        return {
            "name": icon_set.name,
            "priority": icon_set.priority,
            "available": icon_set.is_available(),
            "icon_count": len(icon_set.list_icons()),
        }
    
    def preview_icon_set(self, name: str, limit: int = 10) -> Dict[str, str]:
        """
        Get a preview of icons from a specific icon set.
        
        Args:
            name: Icon set name
            limit: Maximum number of icons to preview
            
        Returns:
            Dictionary mapping icon names to their resolved values
        """
        if name not in self.icon_sets:
            return {}
        
        icon_set = self.icon_sets[name]
        if not icon_set.is_available():
            return {}
        
        return icon_set.get_preview(limit)
    
    def register_icon_set(self, icon_set: IconSet) -> None:
        """
        Register a custom icon set.
        
        Args:
            icon_set: IconSet instance to register
        """
        self.icon_sets[icon_set.name] = icon_set
        self.logger.info(f"Registered custom icon set: {icon_set.name}")
        
        # Clear cache to include new icon set
        self.get_icon.cache_clear()
    
    def clear_cache(self) -> None:
        """Clear the icon resolution cache."""
        self.get_icon.cache_clear()
        self.logger.debug("Cleared icon resolution cache")


# ═══════════════════════════════════════════════════════════════════════════════
# Global icon set manager instance
# ═══════════════════════════════════════════════════════════════════════════════
_global_icon_manager: Optional[IconSetManager] = None


def get_icon_set_manager(preferred_icon_set: str = "auto") -> IconSetManager:
    """
    Get the global icon set manager instance.
    
    Args:
        preferred_icon_set: Preferred icon set for initial setup
        
    Returns:
        IconSetManager instance
    """
    global _global_icon_manager
    
    if _global_icon_manager is None:
        _global_icon_manager = IconSetManager(preferred_icon_set)
    
    return _global_icon_manager