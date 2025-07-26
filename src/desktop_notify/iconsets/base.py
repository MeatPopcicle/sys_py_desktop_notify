# ────────────────────────────────────────────────────────────────────────────────
# Base Icon Set Interface
# ────────────────────────────────────────────────────────────────────────────────
"""
base.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Abstract base class for icon set implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class IconSet(ABC):
    """
    ///////////////////////////////////////////////////////////////////
    ICON SET BASE CLASS
    ▄▄▄ ▄▄▄▄ ▄▄▄  ▄▄ ▄▄
    █   █    █▀▀  ██ ██
    █▄▄ █▄▄▄ █▄▄  ██ ██
    ///////////////////////////////////////////////////////////////////
    Abstract base class for icon set implementations.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this icon set."""
        pass
    
    @property
    @abstractmethod
    def priority(self) -> int:
        """Return the priority of this icon set (higher = more preferred)."""
        pass
    
    @abstractmethod
    def get_icon(self, name: str) -> Optional[str]:
        """
        Resolve icon name to path/glyph/unicode.
        
        Args:
            name: Icon name to resolve
            
        Returns:
            Icon path, glyph, or unicode string, or None if not found
        """
        pass
    
    @abstractmethod
    def list_icons(self) -> List[str]:
        """
        List all available icons in this set.
        
        Returns:
            List of available icon names
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this icon set is available on the system.
        
        Returns:
            True if icon set can be used, False otherwise
        """
        pass
    
    def get_preview(self, limit: int = 10) -> Dict[str, str]:
        """
        Get a preview of icons in this set.
        
        Args:
            limit: Maximum number of icons to preview
            
        Returns:
            Dictionary mapping icon names to their resolved values
        """
        preview = {}
        icon_names = self.list_icons()[:limit]
        
        for name in icon_names:
            icon_value = self.get_icon(name)
            if icon_value:
                preview[name] = icon_value
        
        return preview