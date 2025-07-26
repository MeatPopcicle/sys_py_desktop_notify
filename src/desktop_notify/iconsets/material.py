# ────────────────────────────────────────────────────────────────────────────────
# Material Design Icon Set
# ────────────────────────────────────────────────────────────────────────────────
"""
material.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Material Design icon set using SVG icons with modern visual style.
"""

from typing import List, Optional
from pathlib import Path
import logging

from .base import IconSet


class MaterialIconSet(IconSet):
    """
    ///////////////////////////////////////////////////////////////////
    MATERIAL DESIGN ICONS
    ▄▄▄▄▄ ▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄ ▄▄▄  ▄▄▄ ▄▄▄▄ ▄▄
    █▄▄▄▄ █▄▄▄   █   █▄▄▄ █▀▀  █   █▄▄▄ ██
    █▄▄▄▄ █▄▄▄   █   █▄▄▄ █▄▄  █▄▄ █▄▄▄ ██
    ///////////////////////////////////////////////////////////////////
    Material Design icon set with modern SVG icons.
    """
    
    def __init__(self, icons_dir: Optional[Path] = None):
        """
        Initialize Material icon set.
        
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
        # Icon name mappings
        # ─────────────────────────────────────────────────────────────────
        self.icon_mappings = {
            # Status icons
            "info":        "info.svg",
            "warning":     "warning.svg", 
            "error":       "error.svg",
            "success":     "check_circle.svg",
            "question":    "help.svg",
            
            # Action icons
            "save":        "save.svg",
            "load":        "download.svg",
            "open":        "folder_open.svg",
            "close":       "close.svg",
            "edit":        "edit.svg",
            "delete":      "delete.svg",
            "add":         "add.svg",
            "remove":      "remove.svg",
            "valid":       "check.svg",
            "invalid":     "close.svg",
            
            # Device icons
            "mic":         "mic.svg",
            "camera":      "camera_alt.svg",
            "speaker":     "volume_up.svg",
            "headphones":  "headphones.svg",
            "keyboard":    "keyboard.svg",
            "mouse":       "mouse.svg",
            "monitor":     "desktop_windows.svg",
            "printer":     "print.svg",
            
            # Media icons
            "audio":       "audiotrack.svg",
            "video":       "videocam.svg",
            "image":       "image.svg",
            "document":    "description.svg",
            "folder":      "folder.svg",
            "file":        "insert_drive_file.svg",
            "music":       "music_note.svg",
            "movie":       "movie.svg",
            
            # Network icons
            "network":     "wifi.svg",
            "internet":    "language.svg",
            "email":       "email.svg",
            "download":    "download.svg",
            "upload":      "upload.svg",
            "sync":        "sync.svg",
            
            # System icons
            "settings":    "settings.svg",
            "preferences": "tune.svg",
            "user":        "person.svg",
            "group":       "group.svg",
            "security":    "security.svg",
            "lock":        "lock.svg",
            "unlock":      "lock_open.svg",
            "key":         "vpn_key.svg",
            
            # Application icons
            "terminal":    "terminal.svg",
            "calculator":  "calculate.svg",
            "calendar":    "calendar_today.svg",
            "clock":       "schedule.svg",
            "search":      "search.svg",
            "notification": "notifications.svg",
            "home":        "home.svg",
            "work":        "work.svg",
            
            # Process states
            "running":     "play_arrow.svg",
            "stopped":     "stop.svg",
            "paused":      "pause.svg",
            "waiting":     "hourglass_empty.svg",
            "complete":    "done.svg",
            "failed":      "error_outline.svg",
        }
    
    @property
    def name(self) -> str:
        """Return the name of this icon set."""
        return "material"
    
    @property
    def priority(self) -> int:
        """Return the priority of this icon set."""
        return 80  # High priority for modern look
    
    def get_icon(self, name: str) -> Optional[str]:
        """
        ─────────────────────────────────────────────────────────────────
        Resolve Material Design icon name to SVG file path
        ─────────────────────────────────────────────────────────────────
        """
        if not self.is_available():
            return None
        
        # Check if we have a mapping for this icon
        if name in self.icon_mappings:
            icon_filename = self.icon_mappings[name]
            icon_path = self.icons_dir / icon_filename
            
            if icon_path.exists():
                return str(icon_path)
            else:
                self.logger.debug(f"Material icon file not found: {icon_path}")
        
        # Try direct filename lookup
        direct_path = self.icons_dir / f"{name}.svg"
        if direct_path.exists():
            return str(direct_path)
        
        return None
    
    def list_icons(self) -> List[str]:
        """List all available Material Design icons."""
        available_icons = []
        
        # Add mapped icons that exist
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
        return self.icons_dir.exists() and any(self.icons_dir.glob("*.svg"))
    
    def create_icon_directory(self) -> None:
        """Create the icons directory if it doesn't exist."""
        self.icons_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created Material icons directory: {self.icons_dir}")
    
    def download_icons(self) -> bool:
        """
        Download Material Design icons (placeholder for future implementation).
        
        Returns:
            True if download successful, False otherwise
        """
        # This would be implemented to download Material Design icons
        # from https://fonts.google.com/icons or similar source
        self.logger.warning("Material icon download not yet implemented")
        return False