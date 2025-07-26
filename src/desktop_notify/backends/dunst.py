# ────────────────────────────────────────────────────────────────────────────────
# Dunst Notification Backend
# ────────────────────────────────────────────────────────────────────────────────
"""
dunst.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Dunst notification backend using dunstify command integration.
"""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from .base import NotificationBackend
from ..exceptions import BackendError


class DunstBackend(NotificationBackend):
    """
    ///////////////////////////////////////////////////////////////////
    DUNST BACKEND
    ▄▄▄▄ ▄▄ ▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄
    █▄▄▄ ██ ██ █▀▀   █     █  
    █▄▄▄ ██ ██ █▄▄   █     █  
    ///////////////////////////////////////////////////////////////////
    Dunst notification backend using dunstify command.
    """
    
    def __init__(self, command: str = "dunstify"):
        """
        Initialize Dunst backend.
        
        Args:
            command: dunstify command name or path
        """
        self.command = command
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Validate command availability
        # ─────────────────────────────────────────────────────────────────
        self._command_path = self._find_command()
        
    def _find_command(self) -> Optional[str]:
        """Find the dunstify command on the system."""
        # Try the specified command first
        command_path = shutil.which(self.command)
        if command_path:
            return command_path
        
        # Try common alternatives
        alternatives = ["dunstify", "/usr/bin/dunstify", "/usr/local/bin/dunstify"]
        for alt in alternatives:
            alt_path = shutil.which(alt)
            if alt_path:
                self.logger.debug(f"Found dunstify at: {alt_path}")
                return alt_path
        
        return None
    
    @property
    def name(self) -> str:
        """Return the name of this backend."""
        return "dunst"
    
    @property
    def priority(self) -> int:
        """Return the priority of this backend."""
        return 90  # High priority for Linux desktop notifications
    
    def send_notification(
        self,
        icon: str,
        title: str,
        message: str,
        notification_id: Optional[str] = None,
        urgency: str = 'normal', 
        timeout: Optional[int] = None,
        **kwargs
    ) -> bool:
        """
        ─────────────────────────────────────────────────────────────────
        Send notification via dunstify
        ─────────────────────────────────────────────────────────────────
        """
        if not self.is_available():
            return False
        
        try:
            # Build dunstify command
            cmd = [self._command_path]
            
            # ─────────────────────────────────────────────────────────────────
            # Add notification ID for updates
            # ─────────────────────────────────────────────────────────────────
            if notification_id:
                cmd.extend(["-r", str(abs(hash(notification_id)) % 1000000)])
            
            # ─────────────────────────────────────────────────────────────────
            # Add urgency level
            # ─────────────────────────────────────────────────────────────────
            validated_urgency = self.validate_urgency(urgency)
            cmd.extend(["-u", validated_urgency])
            
            # ─────────────────────────────────────────────────────────────────
            # Add timeout
            # ─────────────────────────────────────────────────────────────────
            if timeout is not None:
                validated_timeout = self.validate_timeout(timeout)
                cmd.extend(["-t", str(validated_timeout)])
            
            # ─────────────────────────────────────────────────────────────────
            # Add icon if provided and exists
            # ─────────────────────────────────────────────────────────────────
            if icon:
                icon_path = self._resolve_icon_path(icon)
                if icon_path:
                    cmd.extend(["-i", icon_path])
            
            # ─────────────────────────────────────────────────────────────────
            # Handle additional dunst-specific options
            # ─────────────────────────────────────────────────────────────────
            if "category" in kwargs:
                cmd.extend(["-h", f"string:category:{kwargs['category']}"])
            
            if "desktop_entry" in kwargs:
                cmd.extend(["-h", f"string:desktop-entry:{kwargs['desktop_entry']}"])
            
            if "sound" in kwargs and kwargs["sound"]:
                cmd.extend(["-h", "int:suppress-sound:0"])
            
            # ─────────────────────────────────────────────────────────────────
            # Add title and message
            # ─────────────────────────────────────────────────────────────────
            cmd.append(title)
            cmd.append(message)
            
            # ─────────────────────────────────────────────────────────────────
            # Execute command
            # ─────────────────────────────────────────────────────────────────
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10  # Prevent hanging
            )
            
            if result.returncode == 0:
                self.logger.debug(f"Sent notification: {title}")
                return True
            else:
                self.logger.warning(
                    f"dunstify failed (code {result.returncode}): {result.stderr}"
                )
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("dunstify command timed out")
            return False
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            return False
    
    def _resolve_icon_path(self, icon: str) -> Optional[str]:
        """
        Resolve icon name/path for dunstify.
        
        Args:
            icon: Icon name, path, or unicode character
            
        Returns:
            Resolved icon path or None
        """
        # If it's already a file path and exists, use it
        icon_path = Path(icon)
        if icon_path.is_absolute() and icon_path.exists():
            return str(icon_path)
        
        # For unicode/emoji icons, don't pass to dunstify
        # (dunstify doesn't handle these well)
        if len(icon) <= 4 and any(ord(c) > 127 for c in icon):
            return None
        
        # For named icons, let dunstify resolve them
        # This works with system icon themes
        return icon
    
    def is_available(self) -> bool:
        """Check if Dunst backend is available."""
        return self._command_path is not None
    
    def get_backend_info(self) -> Dict[str, Any]:
        """Get information about the Dunst backend."""
        info = {
            "name": self.name,
            "priority": self.priority,
            "available": self.is_available(),
            "command": self.command,
            "command_path": self._command_path,
            "features": [
                "notification_id",
                "urgency", 
                "timeout",
                "markup",
                "icons",
                "categories",
                "desktop_entry",
                "sound",
            ],
            "urgency_levels": ["low", "normal", "critical"],
            "description": "Dunst notification daemon backend using dunstify",
        }
        
        # Add version information if available
        if self._command_path:
            try:
                result = subprocess.run(
                    [self._command_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    info["version"] = result.stdout.strip()
            except:
                pass
        
        return info
    
    def test_notification(self) -> bool:
        """
        Send a test notification to verify backend functionality.
        
        Returns:
            True if test notification sent successfully
        """
        return self.send_notification(
            icon="info",
            title="Desktop Notify Test",
            message="Dunst backend is working correctly",
            timeout=3000
        )