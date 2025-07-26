# ────────────────────────────────────────────────────────────────────────────────
# Minimal Unicode Icon Set
# ────────────────────────────────────────────────────────────────────────────────
"""
minimal.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15  
VERSION: 1.0.0

Minimal icon set using Unicode characters and emojis as fallback icons.
"""

from typing import List, Optional
import logging

from .base import IconSet


class MinimalIconSet(IconSet):
    """
    ///////////////////////////////////////////////////////////////////
    MINIMAL UNICODE ICONS
    ▄▄▄▄▄ ▄▄▄ ▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄▄ ▄▄
    █▄▄▄▄ █   ██ █▀▀   █   █▄▄▄ ██
    █▄▄▄▄ █▄▄ ██ █▄▄   █   █▄▄▄ ██
    ///////////////////////////////////////////////////////////////////
    Minimal icon set using Unicode characters and emojis as fallbacks.
    Always available and works in any environment.
    """
    
    def __init__(self):
        """Initialize minimal icon set."""
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Unicode character mappings
        # ─────────────────────────────────────────────────────────────────
        self.icon_mappings = {
            # Status icons
            "info":        "ℹ️",
            "warning":     "⚠️",
            "error":       "❌",
            "success":     "✅",
            "question":    "❓",
            "valid":       "✓",
            "invalid":     "✗",
            
            # Action icons
            "save":        "💾",
            "load":        "📥",
            "open":        "📂",
            "close":       "❌",
            "edit":        "✏️",
            "delete":      "🗑️",
            "add":         "➕",
            "remove":      "➖",
            "copy":        "📋",
            "cut":         "✂️",
            "paste":       "📌",
            
            # Device icons
            "mic":         "🎤",
            "camera":      "📷",
            "speaker":     "🔊",
            "headphones":  "🎧",
            "keyboard":    "⌨️",
            "mouse":       "🖱️",
            "monitor":     "🖥️",
            "printer":     "🖨️",
            "computer":    "💻",
            
            # Media icons
            "audio":       "🔊",
            "video":       "📹",
            "image":       "🖼️",
            "document":    "📄",
            "folder":      "📁",
            "file":        "📄",
            "music":       "🎵",
            "movie":       "🎬",
            "archive":     "📦",
            
            # Network icons
            "network":     "🌐",
            "internet":    "🌍",
            "wifi":        "📶",
            "bluetooth":   "📘",
            "email":       "✉️",
            "download":    "⬇️",
            "upload":      "⬆️",
            "sync":        "🔄",
            
            # System icons
            "settings":    "⚙️",
            "preferences": "🔧",
            "user":        "👤",
            "group":       "👥",
            "security":    "🔒",
            "lock":        "🔒",
            "unlock":      "🔓",
            "key":         "🔑",
            "password":    "🔐",
            
            # Application icons
            "terminal":    "💻",
            "calculator":  "🧮",
            "calendar":    "📅",
            "clock":       "🕐",
            "search":      "🔍",
            "notification": "🔔",
            "home":        "🏠",
            "work":        "💼",
            "games":       "🎮",
            
            # Process states
            "running":     "▶️",
            "stopped":     "⏹️",
            "paused":      "⏸️",
            "waiting":     "⏳",
            "complete":    "✅",
            "failed":      "❌",
            "loading":     "⏳",
            
            # Arrows and navigation
            "up":          "⬆️",
            "down":        "⬇️",
            "left":        "⬅️",
            "right":       "➡️",
            "next":        "⏭️",
            "previous":    "⏮️",
            "forward":     "⏩",
            "backward":    "⏪",
            
            # Common symbols
            "star":        "⭐",
            "heart":       "❤️",
            "check":       "✓",
            "cross":       "✗",
            "plus":        "+",
            "minus":       "-",
            "equals":      "=",
            "percent":     "%",
            "at":          "@",
            "hash":        "#",
            "dollar":      "$",
            
            # Technical symbols
            "code":        "💻",
            "bug":         "🐛",
            "gear":        "⚙️",
            "wrench":      "🔧",
            "hammer":      "🔨",
            "electric":    "⚡",
            "battery":     "🔋",
            "signal":      "📶",
            "antenna":     "📡",
        }
    
    @property
    def name(self) -> str:
        """Return the name of this icon set."""
        return "minimal"
    
    @property
    def priority(self) -> int:
        """Return the priority of this icon set."""
        return 10  # Lowest priority - fallback only
    
    def get_icon(self, name: str) -> Optional[str]:
        """
        ─────────────────────────────────────────────────────────────────
        Resolve icon name to Unicode character/emoji
        ─────────────────────────────────────────────────────────────────
        """
        # Direct mapping lookup
        if name in self.icon_mappings:
            return self.icon_mappings[name]
        
        # Try common alternative names
        alternatives = {
            "information": "info",
            "alert": "warning",
            "fail": "error",
            "ok": "success",
            "help": "question",
            "microphone": "mic",
            "volume": "speaker",
            "screen": "monitor",
            "config": "settings",
            "configure": "settings",
            "person": "user",
            "people": "group",
            "locked": "lock",
            "unlocked": "unlock",
            "cmd": "terminal",
            "shell": "terminal",
            "find": "search",
            "bell": "notification",
            "house": "home",
            "office": "work",
            "play": "running",
            "stop": "stopped",
            "pause": "paused",
            "done": "complete",
            "finish": "complete",
            "broken": "failed",
        }
        
        if name in alternatives:
            return self.get_icon(alternatives[name])
        
        # Fallback for unknown icons
        return "❓"
    
    def list_icons(self) -> List[str]:
        """List all available minimal icons."""
        return sorted(self.icon_mappings.keys())
    
    def is_available(self) -> bool:
        """Check if minimal icon set is available."""
        return True  # Always available - uses Unicode/emoji
    
    def get_fallback_icon(self, category: str = "general") -> str:
        """
        Get a fallback icon for a category.
        
        Args:
            category: Icon category (status, action, device, media, etc.)
            
        Returns:
            Unicode character for the category
        """
        category_fallbacks = {
            "status":      "ℹ️",
            "action":      "⚙️", 
            "device":      "💻",
            "media":       "📄",
            "network":     "🌐",
            "system":      "⚙️",
            "application": "💻",
            "process":     "⚙️",
            "navigation":  "➡️",
            "symbol":      "❓",
            "technical":   "⚙️",
        }
        
        return category_fallbacks.get(category, "❓")