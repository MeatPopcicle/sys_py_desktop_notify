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
import time
from typing import Dict, List, Optional, Union
from functools import lru_cache

from .base import IconSet
from .system import SystemIconSet
from .material import MaterialIconSet
from .minimal import MinimalIconSet
from .material_complete import MaterialCompleteIconSet
from ..exceptions import IconError
from ..types import IconResolutionInfo, IconResolutionSource


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
        self._last_resolution: Optional[IconResolutionInfo] = None
        self._all_or_nothing_mode = True  # Enable all-or-nothing icon resolution
        self._required_icons: List[str] = []  # Icons required for all-or-nothing
        self._validation_cache: Dict[str, bool] = {}  # Cache validation results
        
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
            system_mode = config.system_mode
            system_mapping_file = config.system_mapping_file
        except:
            # Fallback if config not available
            system_theme = None
            system_size = 48
            system_prefer_scalable = False
            system_debug_logging = False
            system_mode = "auto"
            system_mapping_file = ""
        
        # Register icon sets with configuration
        icon_set_configs = [
            (SystemIconSet, {
                "theme_name": system_theme, 
                "icon_size": system_size,
                "prefer_scalable": system_prefer_scalable,
                "debug_logging": system_debug_logging,
                "mode": system_mode,
                "mapping_file": system_mapping_file if system_mapping_file else None
            }),
            (MaterialCompleteIconSet, {}),
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
        # Get required icons for validation
        self._required_icons = self._get_required_icons()
        
        if self.preferred_icon_set == "auto":
            # Automatically select the best available icon set
            available_sets = [(name, icon_set) for name, icon_set in self.icon_sets.items() 
                             if icon_set.is_available()]
            
            if available_sets:
                # Sort by priority (higher = better)
                available_sets.sort(key=lambda x: x[1].priority, reverse=True)
                
                # If all-or-nothing mode, validate icon sets
                if self._all_or_nothing_mode:
                    for set_name, icon_set in available_sets:
                        if self._validate_icon_set(set_name):
                            self.active_icon_set = set_name
                            self.logger.info(f"Auto-selected icon set: {self.active_icon_set} (all icons validated)")
                            return
                    
                    # No set has all required icons, use material-complete
                    if "material-complete" in self.icon_sets:
                        self.active_icon_set = "material-complete"
                        self.logger.info("Using material-complete icon set (all-or-nothing fallback)")
                    else:
                        # Fall back to highest priority
                        self.active_icon_set = available_sets[0][0]
                        self.logger.warning(f"No icon set has all required icons, using {self.active_icon_set}")
                else:
                    # Non all-or-nothing mode - use highest priority
                    self.active_icon_set = available_sets[0][0]
                    self.logger.info(f"Auto-selected icon set: {self.active_icon_set}")
            else:
                self.logger.warning("No icon sets available")
                
        else:
            # Use explicitly specified icon set
            if self.preferred_icon_set in self.icon_sets:
                icon_set = self.icon_sets[self.preferred_icon_set]
                if icon_set.is_available():
                    # Check if all-or-nothing validation passes
                    if self._all_or_nothing_mode and not self._validate_icon_set(self.preferred_icon_set):
                        self.logger.warning(f"Preferred icon set '{self.preferred_icon_set}' missing required icons")
                        if "material-complete" in self.icon_sets:
                            self.active_icon_set = "material-complete"
                            self.logger.info("Using material-complete icon set (all-or-nothing fallback)")
                        else:
                            self.active_icon_set = self.preferred_icon_set
                            self.logger.warning("Continuing with incomplete icon set")
                    else:
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
        # Try material-complete first for all-or-nothing mode
        if self._all_or_nothing_mode and "material-complete" in self.icon_sets:
            self.active_icon_set = "material-complete"
            self.logger.info("Using fallback icon set: material-complete")
        # Try minimal icon set as ultimate fallback
        elif "minimal" in self.icon_sets and self.icon_sets["minimal"].is_available():
            self.active_icon_set = "minimal"
            self.logger.info("Using fallback icon set: minimal")
        else:
            self.logger.error("No fallback icon set available")
    
    def _get_required_icons(self) -> List[str]:
        """Get list of required icons for all-or-nothing validation."""
        # Start with a base set of essential icons
        base_icons = [
            "info", "warning", "error", "success", "question",
            "save", "open", "close", "folder", "file",
            "settings", "user", "notification", "home"
        ]
        
        # Check if material-complete icon set has additional requirements
        if "material-complete" in self.icon_sets:
            material_set = self.icon_sets["material-complete"]
            if hasattr(material_set, 'get_required_icons'):
                return material_set.get_required_icons()
        
        return base_icons
    
    def _validate_icon_set(self, set_name: str) -> bool:
        """
        Validate if an icon set has all required icons.
        
        Args:
            set_name: Name of the icon set to validate
            
        Returns:
            True if all required icons are available, False otherwise
        """
        # Check cache first
        cache_key = f"{set_name}:{','.join(sorted(self._required_icons))}"
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]
        
        icon_set = self.icon_sets.get(set_name)
        if not icon_set or not icon_set.is_available():
            self._validation_cache[cache_key] = False
            return False
        
        # Special handling for system icon set with validate_icons method
        if hasattr(icon_set, 'validate_icons'):
            results = icon_set.validate_icons(self._required_icons)
            missing = [name for name, path in results.items() if path is None]
            is_valid = len(missing) == 0
            
            if not is_valid:
                self.logger.debug(f"Icon set '{set_name}' missing icons: {missing}")
        else:
            # For other icon sets, check each icon individually
            missing = []
            for icon_name in self._required_icons:
                if not icon_set.get_icon(icon_name):
                    missing.append(icon_name)
            
            is_valid = len(missing) == 0
            if not is_valid:
                self.logger.debug(f"Icon set '{set_name}' missing icons: {missing}")
        
        self._validation_cache[cache_key] = is_valid
        return is_valid
    
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
    
    def get_icon_detailed(self, name: str, fallback: bool = True) -> IconResolutionInfo:
        """
        Get icon with detailed resolution information.
        
        Args:
            name: Icon name to resolve
            fallback: Whether to use fallback resolution
            
        Returns:
            IconResolutionInfo with complete resolution details
        """
        start_time = time.time()
        
        # Initialize resolution info
        resolution_info = IconResolutionInfo(
            original_name=name,
            resolved_path=None,
            source=IconResolutionSource.NOT_FOUND,
            attempted_sources=[],
            fallback_chain=[],
            cached=False
        )
        
        # Check if it's a direct file path
        if name.startswith('/') or '.' in name:
            from pathlib import Path
            path = Path(name)
            if path.exists() and path.is_file():
                resolution_info.resolved_path = str(path)
                resolution_info.source = IconResolutionSource.FILE_PATH
                resolution_info.resolution_time_ms = (time.time() - start_time) * 1000
                self._last_resolution = resolution_info
                return resolution_info
        
        # Check if it's a unicode character/emoji
        if len(name) <= 4 and any(ord(c) > 127 for c in name):
            resolution_info.resolved_path = name
            resolution_info.source = IconResolutionSource.UNICODE
            resolution_info.resolution_time_ms = (time.time() - start_time) * 1000
            self._last_resolution = resolution_info
            return resolution_info
        
        # Try active icon set first
        if self.active_icon_set:
            active_set = self.icon_sets[self.active_icon_set]
            resolution_info.attempted_sources.append(self.active_icon_set)
            
            icon = active_set.get_icon(name)
            if icon is not None:
                resolution_info.resolved_path = icon
                resolution_info.source = self._get_source_for_set(self.active_icon_set)
                resolution_info.icon_set_used = self.active_icon_set
                
                # Get additional metadata from icon set
                if hasattr(active_set, 'get_theme_name'):
                    resolution_info.theme_name = getattr(active_set, 'get_theme_name')()
                if hasattr(active_set, 'get_icon_size'):
                    resolution_info.size = getattr(active_set, 'get_icon_size')()
                
                resolution_info.resolution_time_ms = (time.time() - start_time) * 1000
                self._last_resolution = resolution_info
                return resolution_info
        
        if not fallback:
            resolution_info.resolution_time_ms = (time.time() - start_time) * 1000
            self._last_resolution = resolution_info
            return resolution_info
        
        # Try fallback icon sets in priority order
        fallback_sets = [
            (set_name, icon_set) for set_name, icon_set in self.icon_sets.items()
            if set_name != self.active_icon_set and icon_set.is_available()
        ]
        
        # Sort by priority (higher = better)
        fallback_sets.sort(key=lambda x: x[1].priority, reverse=True)
        
        for set_name, icon_set in fallback_sets:
            resolution_info.attempted_sources.append(set_name)
            resolution_info.fallback_chain.append(set_name)
            
            icon = icon_set.get_icon(name)
            if icon is not None:
                resolution_info.resolved_path = icon
                resolution_info.source = self._get_source_for_set(set_name)
                resolution_info.icon_set_used = set_name
                resolution_info.is_fallback = True
                
                # Get additional metadata
                if hasattr(icon_set, 'get_theme_name'):
                    resolution_info.theme_name = getattr(icon_set, 'get_theme_name')()
                if hasattr(icon_set, 'get_icon_size'):
                    resolution_info.size = getattr(icon_set, 'get_icon_size')()
                
                self.logger.debug(f"Found '{name}' in fallback set: {set_name}")
                resolution_info.resolution_time_ms = (time.time() - start_time) * 1000
                self._last_resolution = resolution_info
                return resolution_info
        
        # Ultimate fallback - return unknown icon from minimal set
        if "minimal" in self.icon_sets:
            resolution_info.attempted_sources.append("minimal")
            resolution_info.fallback_chain.append("minimal")
            
            fallback_icon = self.icon_sets["minimal"].get_icon("question")
            if fallback_icon:
                resolution_info.resolved_path = fallback_icon
                resolution_info.source = IconResolutionSource.FALLBACK
                resolution_info.icon_set_used = "minimal"
                resolution_info.is_fallback = True
                resolution_info.original_name = name  # Keep original name
        
        resolution_info.resolution_time_ms = (time.time() - start_time) * 1000
        self._last_resolution = resolution_info
        return resolution_info
    
    def _get_source_for_set(self, set_name: str) -> IconResolutionSource:
        """Map icon set name to resolution source."""
        source_map = {
            "system": IconResolutionSource.SYSTEM_THEME,
            "material": IconResolutionSource.MATERIAL,
            "nerdfonts": IconResolutionSource.NERDFONTS,
            "minimal": IconResolutionSource.MINIMAL,
        }
        return source_map.get(set_name, IconResolutionSource.NOT_FOUND)
    
    def get_last_resolved_icon(self) -> Optional[IconResolutionInfo]:
        """
        Get details about the last icon resolution.
        
        Returns:
            IconResolutionInfo for the last resolved icon, or None if no resolution yet
        """
        return self._last_resolution
    
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
        self._validation_cache.clear()
        self.logger.debug("Cleared icon resolution cache")
    
    def set_all_or_nothing_mode(self, enabled: bool) -> None:
        """
        Enable or disable all-or-nothing icon resolution mode.
        
        Args:
            enabled: True to enable all-or-nothing mode, False to disable
        """
        if self._all_or_nothing_mode != enabled:
            self._all_or_nothing_mode = enabled
            self.logger.info(f"All-or-nothing mode: {'enabled' if enabled else 'disabled'}")
            
            # Re-select active icon set with new mode
            self._select_active_icon_set()
            
            # Clear caches as resolution behavior changed
            self.clear_cache()
    
    def get_all_or_nothing_mode(self) -> bool:
        """Get current all-or-nothing mode state."""
        return self._all_or_nothing_mode
    
    def set_required_icons(self, icon_names: List[str]) -> None:
        """
        Set custom list of required icons for all-or-nothing validation.
        
        Args:
            icon_names: List of icon names that must be present
        """
        self._required_icons = icon_names
        self._validation_cache.clear()
        
        # Re-validate current icon set
        if self._all_or_nothing_mode:
            self._select_active_icon_set()


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