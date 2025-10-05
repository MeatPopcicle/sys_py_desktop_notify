# ────────────────────────────────────────────────────────────────────────────────
# Complete Material Design Icon Set
# ────────────────────────────────────────────────────────────────────────────────
"""
material_complete.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 2.0.0

Complete Material Design icon set with comprehensive mappings for all common
desktop notification scenarios. Used as the default fallback when system icons
are incomplete.
"""

from typing import List, Optional, Dict
from pathlib import Path
import logging

from .base import IconSet


class MaterialCompleteIconSet(IconSet):
    """
    ///////////////////////////////////////////////////////////////////
    COMPLETE MATERIAL DESIGN ICONS
    ▄▄▄▄▄ ▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄ ▄▄▄  ▄▄▄ ▄▄▄▄ ▄▄
    █▄▄▄▄ █▄▄▄   █   █▄▄▄ █▀▀  █   █▄▄▄ ██
    █▄▄▄▄ █▄▄▄   █   █▄▄▄ █▄▄  █▄▄ █▄▄▄ ██
    ///////////////////////////////////////////////////////////////////
    Complete Material Design icon set with extensive mappings.
    """
    
    def __init__(self, icons_dir: Optional[Path] = None):
        """
        Initialize complete Material icon set.
        
        Args:
            icons_dir: Directory containing Material Design SVG icons
        """
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Icon directory setup
        # ─────────────────────────────────────────────────────────────────
        if icons_dir:
            self.icons_dir = Path(icons_dir)
        else:
            # Default to a subdirectory in the package
            self.icons_dir = Path(__file__).parent / "assets" / "material"
        
        # ─────────────────────────────────────────────────────────────────
        # Complete icon mappings for all 70 standard icons (based on breeze.yaml)
        # ─────────────────────────────────────────────────────────────────
        self.icon_mappings = {
            # Status/Dialog icons (8)
            "info":             "info.svg",
            "warning":          "warning.svg", 
            "error":            "error.svg",
            "success":          "check_circle.svg",
            "question":         "help.svg",
            "alert":            "warning.svg",
            "ok":               "check_circle.svg",
            "valid":            "check_circle.svg",
            
            # Actions (20)
            "save":             "save.svg",
            "open":             "folder_open.svg",
            "new":              "new.svg",
            "copy":             "copy.svg",
            "cut":              "cut.svg", 
            "paste":            "paste.svg",
            "undo":             "undo.svg",
            "redo":             "redo.svg",
            "find":             "find.svg",
            "delete":           "delete.svg",
            "clear":            "clear.svg",
            "back":             "back.svg",
            "forward":          "forward.svg",
            "up":               "up.svg",
            "down":             "down.svg",
            "home":             "home.svg",
            "refresh":          "refresh.svg",
            "edit":             "edit.svg",
            "close":            "close.svg",
            "add":              "add.svg",
            
            # Media (8)
            "play":             "play.svg",
            "pause":            "pause.svg",
            "stop":             "stop.svg",
            "next":             "next.svg",
            "previous":         "previous.svg",
            "record":           "record.svg",
            "music":            "music.svg",
            "video":            "video.svg",
            
            # Devices (8 + aliases)
            "microphone":       "microphone.svg",
            "mic":              "microphone.svg",
            "camera":           "camera.svg",
            "printer":          "printer.svg",
            "scanner":          "scanner.svg",
            "speaker":          "speaker.svg",
            "headphones":       "headphones.svg",
            "battery":          "battery.svg",
            
            # System (11)
            "settings":         "settings.svg",
            "config":           "settings.svg",
            "preferences":      "settings.svg",
            "user":             "person.svg",
            "users":            "users.svg",
            "network":          "network.svg",
            "wifi":             "wifi.svg",
            "bluetooth":        "bluetooth.svg",
            "power":            "power.svg",
            "logout":           "logout.svg",
            "lock":             "lock.svg",
            
            # Applications (10)
            "browser":          "browser.svg",
            "mail":             "mail.svg",
            "editor":           "editor.svg",
            "terminal":         "terminal.svg",
            "calculator":       "calculator.svg",
            "folder":           "folder.svg",
            "file":             "insert_drive_file.svg",
            "document":         "document.svg",
            "image":            "image.svg",
            "archive":          "archive.svg",
            
            # Status/Loading (5)
            "load":             "load.svg",
            "loading":          "loading.svg",
            "process":          "process.svg",
            "working":          "working.svg",
            "busy":             "busy.svg",
            
            # Additional common mappings
            "notification":     "notifications.svg",
            "check":            "check.svg",
            "cross":            "close.svg",
        }
        
        # ─────────────────────────────────────────────────────────────────
        # Category-based fallbacks for intelligent icon resolution
        # ─────────────────────────────────────────────────────────────────
        self.category_patterns = {
            "app-": "apps.svg",
            "device-": "devices.svg",
            "action-": "touch_app.svg",
            "status-": "info.svg",
            "folder-": "folder.svg",
            "file-": "insert_drive_file.svg",
            "audio-": "audiotrack.svg",
            "video-": "videocam.svg",
            "image-": "image.svg",
            "network-": "wifi.svg",
            "system-": "settings.svg",
            "user-": "person.svg",
            "notification-": "notifications.svg",
        }
    
    @property
    def name(self) -> str:
        """Return the name of this icon set."""
        return "material-complete"
    
    @property
    def priority(self) -> int:
        """Return the priority of this icon set."""
        return 70  # Lower than system icons but higher than minimal
    
    def get_icon(self, name: str) -> Optional[str]:
        """
        ─────────────────────────────────────────────────────────────────
        Resolve icon name to Material Design SVG path
        ─────────────────────────────────────────────────────────────────
        """
        if not self.is_available():
            return None
        
        # Normalize icon name
        normalized_name = name.lower().replace('_', '-')
        
        # Check direct mapping first
        if normalized_name in self.icon_mappings:
            icon_filename = self.icon_mappings[normalized_name]
            icon_path = self.icons_dir / icon_filename
            
            if icon_path.exists():
                return str(icon_path)
            else:
                self.logger.debug(f"Material icon file not found: {icon_path}")
        
        # Try common alternatives/aliases
        aliases = {
            "information": "info",
            "alert": "warning", 
            "fail": "error",
            "failed": "error",
            "ok": "success",
            "complete": "success",
            "directory": "folder",
            "config": "settings",
            "configure": "settings",
            "person": "user",
            "bell": "notification",
            "house": "home",
            "cross": "close",
        }
        
        if normalized_name in aliases:
            return self.get_icon(aliases[normalized_name])
        
        # Try direct file lookup
        direct_path = self.icons_dir / f"{normalized_name}.svg"
        if direct_path.exists():
            return str(direct_path)
        
        # Try category-based fallback
        for prefix, fallback_icon in self.category_patterns.items():
            if normalized_name.startswith(prefix):
                fallback_path = self.icons_dir / fallback_icon
                if fallback_path.exists():
                    self.logger.debug(f"Using category fallback for '{name}': {fallback_icon}")
                    return str(fallback_path)
        
        # Ultimate fallback - help outline icon
        help_path = self.icons_dir / "help_outline.svg"
        if help_path.exists():
            self.logger.debug(f"Using help_outline fallback for '{name}'")
            return str(help_path)
        
        return None
    
    def list_icons(self) -> List[str]:
        """List all available Material Design icons."""
        available_icons = []
        
        # Add mapped icons that exist as SVG files
        for icon_name, filename in self.icon_mappings.items():
            icon_path = self.icons_dir / filename
            if icon_path.exists():
                available_icons.append(icon_name)
        
        # Add any additional SVG files in the directory
        if self.icons_dir.exists():
            for svg_file in self.icons_dir.glob("*.svg"):
                icon_name = svg_file.stem
                if icon_name not in available_icons:
                    available_icons.append(icon_name)
        
        return sorted(available_icons)
    
    def is_available(self) -> bool:
        """Check if Material icon set is available."""
        # Check if icon directory exists and has SVG files
        if not self.icons_dir.exists():
            return False
        
        # Check if we have at least some essential icons
        essential_icons = ['info.svg', 'warning.svg', 'error.svg', 'help_outline.svg']
        for icon in essential_icons:
            if not (self.icons_dir / icon).exists():
                return False
        
        return True
    
    def get_required_icons(self) -> List[str]:
        """
        Get list of icon names that should be validated for all-or-nothing.
        
        Returns:
            List of essential icon names for desktop notifications
        """
        return [
            "info", "warning", "error", "success", "question",
            "save", "open", "close", "folder", "file",
            "settings", "user", "notification", "home",
            "check", "cross", "help"
        ]