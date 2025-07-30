# ────────────────────────────────────────────────────────────────────────────────
# System Icon Set with icon_mapper Integration
# ────────────────────────────────────────────────────────────────────────────────
"""
system.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

System icon set using icon_mapper.IconResolver from:
/home/gauol/Scratch/Projects - Code/icon-mapper
"""

import logging
from typing import List, Optional
from pathlib import Path

from .base import IconSet
from ..exceptions import IconError

try:
    # ═══════════════════════════════════════════════════════════════════════════════
    # IMPORT icon_mapper.IconResolver
    # ═══════════════════════════════════════════════════════════════════════════════
    import sys
    from pathlib import Path
    icon_mapper_path = Path("/home/gauol/Scratch/Projects - Code/icon-mapper/src")
    if icon_mapper_path.exists() and str(icon_mapper_path) not in sys.path:
        sys.path.insert(0, str(icon_mapper_path))
    
    from icon_mapper import IconResolver
    ICON_MAPPER_AVAILABLE = True
except ImportError as e:
    ICON_MAPPER_AVAILABLE = False
    IconResolver = None


class SystemIconSet(IconSet):
    """
    ///////////////////////////////////////////////////////////////////
    SYSTEM ICON SET
    ▄▄▄▄▄ ▄▄▄ ▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄ ▄▄▄▄▄
    █▄▄▄▄ █▄▄ █▄▄▄   █   █▄▄▄ █▄▄▄▄
    ▄▄▄▄█ █▄▄ █▄▄▄   █   █▄▄▄ █▄▄▄▄
    ///////////////////////////////////////////////////////////////////
    System icon set using desktop theme icons via icon_mapper.IconResolver.
    
    INTEGRATION: Uses icon_mapper.IconResolver from:
    /home/gauol/Scratch/Projects - Code/icon-mapper
    """
    
    def __init__(
        self, 
        theme_name: Optional[str] = None, 
        icon_size: int = 48,
        prefer_scalable: bool = False,
        debug_logging: bool = False,
        mode: str = "auto",
        mapping_file: Optional[str] = None
    ):
        """
        Initialize system icon set.
        
        Args:
            theme_name: Icon theme name (None for auto-detection)
            icon_size: Preferred icon size in pixels
            prefer_scalable: Whether to prioritize scalable icons over fixed-size
            debug_logging: Whether to enable detailed debug logging
            mode: Resolution mode ("auto", "explicit", "hybrid")
            mapping_file: Path to YAML mapping file (None for default)
        """
        self.theme_name      = theme_name
        self.icon_size       = icon_size
        self.prefer_scalable = prefer_scalable
        self.debug_logging   = debug_logging
        self.mode            = mode
        self.mapping_file    = mapping_file
        self.logger          = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Initialize icon_mapper IconResolver
        # ─────────────────────────────────────────────────────────────────
        self._resolver   = None
        self._cache      = {}  # Icon name -> resolved path cache
        
        if ICON_MAPPER_AVAILABLE:
            try:
                # icon_mapper uses simplified API - only theme name is needed
                # Default theme will be used if theme_name is None
                theme_to_use = self.theme_name if self.theme_name else "breeze"
                self._resolver = IconResolver(theme=theme_to_use)
                self.logger.debug(
                    f"Initialized icon_mapper.IconResolver with theme='{theme_to_use}'"
                )
            except Exception as e:
                self.logger.warning(f"Failed to initialize IconResolver: {e}")
                self._resolver = None
        else:
            self.logger.warning("icon_mapper not available - system icons disabled")
    
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
        Resolve icon name using icon_mapper.IconResolver
        ─────────────────────────────────────────────────────────────────
        """
        if not self.is_available():
            self.logger.debug(f"❌ SystemIconSet not available for '{name}'")
            return None
        
        # Check cache first
        if name in self._cache:
            cached_result = self._cache[name]
            if self._should_log_resolution():
                if cached_result:
                    self.logger.info(f"🔄 Icon '{name}' → '{cached_result}' (cached)")
                else:
                    self.logger.info(f"🔄 Icon '{name}' → None (cached miss)")
            return cached_result
        
        if self._should_log_resolution():
            self.logger.info(f"🔍 Resolving icon: '{name}'")
            self.logger.info(f"   Theme: {self.theme_name or 'auto'}, Size: {self.icon_size}, Scalable: {self.prefer_scalable}")
        
        try:
            # Use icon_mapper.IconResolver to resolve icon
            result = self._resolver.get_icon(name)
            
            if result:
                resolved_path = str(result)
                self._cache[name] = resolved_path
                
                if self._should_log_resolution():
                    self.logger.info(f"✅ Icon '{name}' → '{resolved_path}'")
                else:
                    self.logger.debug(f"Resolved '{name}' -> '{resolved_path}'")
                
                return resolved_path
            else:
                if self._should_log_resolution():
                    self.logger.info(f"❌ Icon '{name}' → None (not found)")
            
        except Exception as e:
            if self._should_log_resolution():
                self.logger.error(f"💥 Icon '{name}' resolution failed: {e}")
            else:
                self.logger.debug(f"Failed to resolve icon '{name}': {e}")
        
        # Cache negative results to avoid repeated lookups
        self._cache[name] = None
        return None
    
    def _should_log_resolution(self) -> bool:
        """Check if icon resolution should be logged based on config."""
        try:
            from ..config import get_config
            config = get_config()
            return config.log_icon_resolution
        except:
            return False
    
    def list_icons(self) -> List[str]:
        """
        List available system icons.
        
        Note: This uses the icon_mapper.IconResolver's list_icons() method
        to get all available icons in the current theme.
        """
        if not self.is_available():
            return []
        
        try:
            # Use icon_mapper's list_icons() method
            return self._resolver.list_icons()
        except Exception as e:
            self.logger.warning(f"Failed to list icons: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if system icon set is available."""
        return (ICON_MAPPER_AVAILABLE and 
                self._resolver is not None)
    
    def clear_cache(self) -> None:
        """Clear the icon resolution cache."""
        self._cache.clear()
        self.logger.debug("Cleared icon cache")
    
    def update_configuration(
        self, 
        theme_name: Optional[str] = None, 
        icon_size: Optional[int] = None,
        prefer_scalable: Optional[bool] = None,
        debug_logging: Optional[bool] = None,
        mode: Optional[str] = None,
        mapping_file: Optional[str] = None
    ) -> None:
        """
        Update IconResolver configuration.
        
        Args:
            theme_name: New theme name (None to keep current)
            icon_size: New icon size (None to keep current)
            prefer_scalable: New scalable preference (None to keep current)
            debug_logging: New debug logging setting (None to keep current)
            mode: New resolution mode (None to keep current)
            mapping_file: New mapping file path (None to keep current)
        """
        if not ICON_MAPPER_AVAILABLE or not self._resolver:
            return
        
        # Update configuration if provided
        if theme_name is not None:
            self.theme_name = theme_name
            
        # icon_mapper doesn't use these parameters, but keep them for compatibility
        if icon_size is not None:
            self.icon_size = icon_size
            
        if prefer_scalable is not None:
            self.prefer_scalable = prefer_scalable
            
        if debug_logging is not None:
            self.debug_logging = debug_logging
            
        if mode is not None:
            self.mode = mode
            
        if mapping_file is not None:
            self.mapping_file = mapping_file
        
        try:
            # Update IconResolver theme if changed
            if theme_name is not None:
                success = self._resolver.set_theme(self.theme_name)
                if success:
                    self.logger.debug(f"Updated IconResolver theme to: {self.theme_name}")
                else:
                    self.logger.warning(f"Failed to set theme to: {self.theme_name}")
            
            # Clear cache since resolution may change
            self.clear_cache()
            
        except Exception as e:
            self.logger.warning(f"Failed to update IconResolver configuration: {e}")