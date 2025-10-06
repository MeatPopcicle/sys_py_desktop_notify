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
from typing import Any, Dict, Optional, Callable, Union

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
        actions: Optional[Dict[str, str]] = None,
        action_callback: Optional[Callable[[str], None]] = None,
        **kwargs
    ) -> Union[bool, str]:
        """
        Send notification via dunstify.

        Args:
            icon: Icon name or path
            title: Notification title
            message: Notification message body
            notification_id: Optional ID for replacing/updating notifications
            urgency: Urgency level ('low', 'normal', 'critical')
            timeout: Timeout in milliseconds (None = default)
            actions: Dictionary of actions {key: label}
                    Special key "default": Triggered by LEFT-CLICK
                    Other keys: Appear in RIGHT-CLICK context menu
                    Example: {"default": "Accept", "decline": "Decline"}
            action_callback: Function to call with selected action key
            **kwargs: Additional dunst-specific options:
                     - category: Notification category
                     - desktop_entry: Desktop entry name
                     - sound: Whether to play sound

        Returns:
            If actions provided: Selected action key (str) or None if dismissed/timeout
            If no actions: True if sent successfully, False otherwise

        Mouse Click Behavior:
            - LEFT-CLICK: Triggers "default" action (if provided)
            - RIGHT-CLICK: Shows context menu with non-default actions
            - MIDDLE-CLICK: Dismisses notification

        See docs/Dunst_Action_Behavior.md for detailed documentation.
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
            # Add actions if provided
            # ─────────────────────────────────────────────────────────────────
            # ACTION BEHAVIOR:
            #   - "default" key: Triggers on LEFT-CLICK (direct click on notification)
            #   - Other keys: Appear in RIGHT-CLICK context menu
            #   - Middle-click: Always dismisses (built-in Dunst behavior)
            #
            # Example:
            #   actions = {
            #       "default": "Accept",  # Left-click triggers this
            #       "decline": "Decline", # Right-click menu option
            #       "later": "Later"      # Right-click menu option
            #   }
            #
            # See docs/Dunst_Action_Behavior.md for detailed documentation
            # ─────────────────────────────────────────────────────────────────
            if actions:
                # Add actions in consistent order: default first, then others
                if "default" in actions:
                    cmd.extend(["-A", f"default,{actions['default']}"])
                    self.logger.debug(f"Added default action (left-click): {actions['default']}")

                # Add non-default actions (right-click context menu)
                for action_id, label in actions.items():
                    if action_id != "default":
                        cmd.extend(["-A", f"{action_id},{label}"])
                        self.logger.debug(f"Added context menu action: {action_id}={label}")
            
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
                timeout=30 if actions else 10  # Longer timeout for interactive notifications
            )
            
            # ─────────────────────────────────────────────────────────────────
            # Handle actions response
            # ─────────────────────────────────────────────────────────────────
            if actions:
                if result.returncode == 0:
                    # Action was selected
                    selected_action = result.stdout.strip()
                    self.logger.debug(f"Action selected: {selected_action}")
                    
                    # Call callback if provided
                    if action_callback and selected_action:
                        try:
                            action_callback(selected_action)
                        except Exception as e:
                            self.logger.error(f"Action callback failed: {e}")
                    
                    return selected_action or None
                elif result.returncode == 1:
                    # Notification timed out
                    self.logger.debug(f"Notification timed out: {title}")
                    return None
                elif result.returncode == 2:
                    # Notification was dismissed
                    self.logger.debug(f"Notification dismissed: {title}")
                    return None
                else:
                    self.logger.warning(
                        f"dunstify failed (code {result.returncode}): {result.stderr}"
                    )
                    return None
            else:
                # Regular notification without actions
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
            return None if actions else False
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            return None if actions else False
    
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
                "actions",
                "callbacks",
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