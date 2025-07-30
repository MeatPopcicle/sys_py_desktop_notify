# ────────────────────────────────────────────────────────────────────────────────
# Console Notification Backend
# ────────────────────────────────────────────────────────────────────────────────
"""
console.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Console notification backend for headless environments and fallback.
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional, Callable, Union

from .base import NotificationBackend


class ConsoleBackend(NotificationBackend):
    """
    ///////////////////////////////////////////////////////////////////
    CONSOLE BACKEND
    ▄▄▄▄ ▄▄▄  ▄▄ ▄▄▄▄▄ ▄▄▄  ▄▄ ▄▄▄▄▄
    █    █▀▀  ██   █   █▀▀  ██   █  
    █▄▄▄ █▄▄  ██   █   █▄▄  ██   █  
    ///////////////////////////////////////////////////////////////////
    Console-based notification backend for headless environments.
    """
    
    def __init__(self, use_colors: bool = True, timestamp: bool = True):
        """
        Initialize Console backend.
        
        Args:
            use_colors: Whether to use ANSI colors in output
            timestamp: Whether to include timestamps
        """
        self.use_colors = use_colors
        self.timestamp = timestamp
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Color definitions
        # ─────────────────────────────────────────────────────────────────
        self.colors = {
            'reset':     '\033[0m',
            'bold':      '\033[1m',
            'dim':       '\033[2m',
            'red':       '\033[31m',
            'green':     '\033[32m',
            'yellow':    '\033[33m',
            'blue':      '\033[34m',
            'magenta':   '\033[35m',
            'cyan':      '\033[36m',
            'white':     '\033[37m',
        } if use_colors else {k: '' for k in [
            'reset', 'bold', 'dim', 'red', 'green', 
            'yellow', 'blue', 'magenta', 'cyan', 'white'
        ]}
        
        # ─────────────────────────────────────────────────────────────────
        # Urgency to color mapping
        # ─────────────────────────────────────────────────────────────────
        self.urgency_colors = {
            'low':      self.colors['dim'],
            'normal':   self.colors['blue'],
            'critical': self.colors['red'] + self.colors['bold'],
        }
    
    @property
    def name(self) -> str:
        """Return the name of this backend."""
        return "console"
    
    @property
    def priority(self) -> int:
        """Return the priority of this backend."""
        return 1  # Lowest priority - fallback only
    
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
        ─────────────────────────────────────────────────────────────────
        Send notification to console/terminal
        ─────────────────────────────────────────────────────────────────
        """
        try:
            # ─────────────────────────────────────────────────────────────────
            # Format notification components
            # ─────────────────────────────────────────────────────────────────
            timestamp_str = ""
            if self.timestamp:
                now = datetime.now()
                timestamp_str = f"[{now.strftime('%H:%M:%S')}] "
            
            # Format urgency indicator
            validated_urgency = self.validate_urgency(urgency)
            urgency_color = self.urgency_colors.get(validated_urgency, '')
            urgency_indicator = self._get_urgency_indicator(validated_urgency)
            
            # Format icon (convert to text representation)
            icon_str = self._format_icon(icon)
            
            # Format notification ID
            id_str = f" (ID: {notification_id})" if notification_id else ""
            
            # ─────────────────────────────────────────────────────────────────
            # Build notification output
            # ─────────────────────────────────────────────────────────────────
            header = (
                f"{timestamp_str}"
                f"{urgency_color}{urgency_indicator} "
                f"{icon_str} "
                f"{self.colors['bold']}{title}{self.colors['reset']}"
                f"{id_str}"
            )
            
            body = f"    {message}"
            
            # Add separator line for better visibility
            separator = "    " + "─" * min(50, len(message))
            
            # ─────────────────────────────────────────────────────────────────
            # Add actions if provided (console doesn't support interactive actions)
            # ─────────────────────────────────────────────────────────────────
            action_lines = []
            if actions:
                action_lines.append("    Available actions:")
                for action_id, label in actions.items():
                    action_lines.append(f"      - {label} ({action_id})")
                action_lines.append("    Note: Console backend does not support interactive actions")
            
            # ─────────────────────────────────────────────────────────────────
            # Output to stderr (to not interfere with script output)
            # ─────────────────────────────────────────────────────────────────
            output_lines = [header, body] + action_lines + [separator]
            
            for line in output_lines:
                print(line, file=sys.stderr)
            
            # Flush to ensure immediate output
            sys.stderr.flush()
            
            self.logger.debug(f"Sent console notification: {title}")
            
            # Console backend doesn't support interactive actions
            if actions:
                self.logger.debug(f"Console backend cannot handle actions: {list(actions.keys())}")
                return None  # No action can be selected
            else:
                return True
            
        except Exception as e:
            self.logger.error(f"Failed to send console notification: {e}")
            return None if actions else False
    
    def _get_urgency_indicator(self, urgency: str) -> str:
        """Get text indicator for urgency level."""
        indicators = {
            'low':      "[INFO]",
            'normal':   "[NOTIFY]", 
            'critical': "[ALERT]",
        }
        return indicators.get(urgency, "[NOTIFY]")
    
    def _format_icon(self, icon: str) -> str:
        """
        Format icon for console display.
        
        Args:
            icon: Icon name, path, or unicode character
            
        Returns:
            Formatted icon string
        """
        # If it's already a unicode character/emoji, use as-is
        if len(icon) <= 4 and any(ord(c) > 127 for c in icon):
            return icon
        
        # Convert common icon names to unicode/text
        icon_map = {
            # Status icons
            "info":        "ℹ️",
            "warning":     "⚠️",
            "error":       "❌",
            "success":     "✅",
            "question":    "❓",
            
            # Action icons
            "save":        "💾",
            "load":        "📥", 
            "open":        "📂",
            "close":       "❌",
            "edit":        "✏️",
            "delete":      "🗑️",
            
            # Device icons
            "mic":         "🎤",
            "camera":      "📷",
            "speaker":     "🔊",
            "headphones":  "🎧",
            
            # System icons
            "settings":    "⚙️",
            "user":        "👤",
            "lock":        "🔒",
            "unlock":      "🔓",
            
            # Fallback
            "notification": "🔔",
        }
        
        return icon_map.get(icon, "📢")  # Default notification icon
    
    def is_available(self) -> bool:
        """Check if Console backend is available."""
        return True  # Always available
    
    def get_backend_info(self) -> Dict[str, Any]:
        """Get information about the Console backend."""
        return {
            "name": self.name,
            "priority": self.priority,
            "available": self.is_available(),
            "use_colors": self.use_colors,
            "timestamp": self.timestamp,
            "features": [
                "urgency",
                "notification_id", 
                "icons",
                "colors",
                "timestamp",
            ],
            "urgency_levels": ["low", "normal", "critical"],
            "description": "Console/terminal output backend for headless environments",
        }
    
    def test_notification(self) -> bool:
        """
        Send a test notification to verify backend functionality.
        
        Returns:
            True if test notification sent successfully
        """
        return self.send_notification(
            icon="info",
            title="Desktop Notify Test",
            message="Console backend is working correctly",
            urgency="normal"
        )
    
    def set_colors_enabled(self, enabled: bool) -> None:
        """
        Enable or disable color output.
        
        Args:
            enabled: Whether to use colors
        """
        self.use_colors = enabled
        
        # Update color definitions
        if enabled:
            self.colors = {
                'reset':     '\033[0m',
                'bold':      '\033[1m', 
                'dim':       '\033[2m',
                'red':       '\033[31m',
                'green':     '\033[32m',
                'yellow':    '\033[33m',
                'blue':      '\033[34m',
                'magenta':   '\033[35m',
                'cyan':      '\033[36m',
                'white':     '\033[37m',
            }
        else:
            self.colors = {k: '' for k in self.colors.keys()}
        
        # Update urgency colors
        self.urgency_colors = {
            'low':      self.colors['dim'],
            'normal':   self.colors['blue'],
            'critical': self.colors['red'] + self.colors['bold'],
        }
    
    def set_timestamp_enabled(self, enabled: bool) -> None:
        """
        Enable or disable timestamp in output.
        
        Args:
            enabled: Whether to include timestamps
        """
        self.timestamp = enabled