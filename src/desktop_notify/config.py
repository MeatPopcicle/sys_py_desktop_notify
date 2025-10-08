# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Configuration
# ────────────────────────────────────────────────────────────────────────────────
"""
config.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Configuration system for desktop notification library using the reusable
config_manager module.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from config_manager import ConfigManager, ConfigSchema
from .exceptions import ConfigurationError


def create_desktop_notify_schema() -> ConfigSchema:
    """
    Create the configuration schema for desktop notify.
    
    Returns:
        ConfigSchema instance with desktop notify validation rules
    """
    # ═══════════════════════════════════════════════════════════════════════════════
    # Main configuration schema
    # ═══════════════════════════════════════════════════════════════════════════════
    main_schema = ConfigSchema()
    
    # ─────────────────────────────────────────────────────────────────
    # Notification settings
    # ─────────────────────────────────────────────────────────────────
    main_schema.add_field("backend", str, default="auto")
    main_schema.add_field("timeout", int, default=3000) 
    main_schema.add_field("urgency", str, default="normal")
    main_schema.add_field("enable_sound", bool, default=True)
    main_schema.add_field("log_level", str, default="INFO")
    main_schema.add_field("log_icon_resolution", bool, default=False)
    
    # ─────────────────────────────────────────────────────────────────
    # Icon settings
    # ─────────────────────────────────────────────────────────────────
    icon_schema = ConfigSchema()
    icon_schema.add_field("icon_set", str, default="auto")
    icon_schema.add_field("system_theme", str, default="")
    icon_schema.add_field("system_size", int, default=48)
    icon_schema.add_field("system_prefer_scalable", bool, default=False)
    icon_schema.add_field("system_debug_logging", bool, default=False)
    icon_schema.add_field("system_mode", str, default="auto")
    icon_schema.add_field("system_mapping_file", str, default="")
    icon_schema.add_field("fallback_enabled", bool, default=True)
    
    main_schema.add_nested_schema("icons", icon_schema)
    
    # ─────────────────────────────────────────────────────────────────
    # Backend-specific settings
    # ─────────────────────────────────────────────────────────────────
    backends_schema = ConfigSchema()
    
    # Dunst backend settings
    dunst_schema = ConfigSchema()
    dunst_schema.add_field("command", str, default="dunstify")
    dunst_schema.add_field("supports_markup", bool, default=True)
    dunst_schema.add_field("max_timeout", int, default=60000)
    dunst_schema.add_field("rofi_theme", str, default="")
    
    backends_schema.add_nested_schema("dunst", dunst_schema)
    
    # Console backend settings
    console_schema = ConfigSchema()
    console_schema.add_field("use_colors", bool, default=True)
    console_schema.add_field("timestamp", bool, default=True)
    
    backends_schema.add_nested_schema("console", console_schema)
    
    main_schema.add_nested_schema("backends", backends_schema)
    
    return main_schema


class DesktopNotifyConfig:
    """
    ///////////////////////////////////////////////////////////////////
    DESKTOP NOTIFY CONFIGURATION
    ▄▄▄▄ ▄▄▄  ▄▄ ▄▄▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄
    █    █▀▀  ██ █▄▄▄ █   █   █   █▄▄▄
    █▄▄▄ █▄▄  ██ █▄▄▄ █▄▄ █   █   █▄▄▄
    ///////////////////////////////////////////////////////////////////
    Configuration management for desktop notification system.
    """
    
    def __init__(
        self,
        config_paths: Optional[list] = None,
        auto_load: bool = True
    ):
        """
        Initialize desktop notify configuration.
        
        Args:
            config_paths: List of configuration file paths to load
            auto_load: Whether to automatically load configuration
        """
        self.logger = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Setup default configuration paths
        # ─────────────────────────────────────────────────────────────────
        if config_paths is None:
            config_paths = self._get_default_config_paths()
        
        # ─────────────────────────────────────────────────────────────────
        # Initialize configuration manager
        # ─────────────────────────────────────────────────────────────────
        self.schema = create_desktop_notify_schema()
        self.config_manager = ConfigManager(
            config_paths=config_paths,
            env_prefix="DESKTOP_NOTIFY",
            schema=self.schema,
            auto_load=auto_load
        )
        
        if auto_load:
            self.logger.debug("Configuration loaded successfully")
    
    def _get_default_config_paths(self) -> list:
        """Get default configuration file paths."""
        paths = []
        
        # System-wide configuration
        system_config = Path("/etc/desktop-notify/config.toml")
        if system_config.exists():
            paths.append(system_config)
        
        # User configuration
        user_config_dir = Path.home() / ".config" / "desktop-notify"
        user_config = user_config_dir / "config.toml"
        paths.append(user_config)
        
        # Local project configuration
        local_config = Path.cwd() / "desktop-notify.toml"
        if local_config.exists():
            paths.append(local_config)
        
        return paths
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key using dot notation
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config_manager.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key using dot notation
            value: Value to set
        """
        self.config_manager.set(key, value, source="runtime")
    
    def reload(self) -> None:
        """Reload configuration from files."""
        self.config_manager.load()
        self.logger.debug("Configuration reloaded")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get complete configuration as dictionary."""
        return self.config_manager.to_dict()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Convenience methods for common configuration access
    # ═══════════════════════════════════════════════════════════════════════════════
    
    @property
    def backend(self) -> str:
        """Get preferred backend name."""
        return self.get("backend", "auto")
    
    @backend.setter
    def backend(self, value: str) -> None:
        """Set preferred backend name."""
        self.set("backend", value)
    
    @property 
    def timeout(self) -> int:
        """Get default notification timeout."""
        return self.get("timeout", 3000)
    
    @timeout.setter
    def timeout(self, value: int) -> None:
        """Set default notification timeout."""
        self.set("timeout", value)
    
    @property
    def urgency(self) -> str:
        """Get default notification urgency."""
        return self.get("urgency", "normal")
    
    @urgency.setter
    def urgency(self, value: str) -> None:
        """Set default notification urgency."""
        self.set("urgency", value)
    
    @property
    def icon_set(self) -> str:
        """Get preferred icon set."""
        return self.get("icons.icon_set", "auto")
    
    @icon_set.setter
    def icon_set(self, value: str) -> None:
        """Set preferred icon set."""
        self.set("icons.icon_set", value)
    
    @property
    def system_icon_theme(self) -> str:
        """Get system icon theme name."""
        return self.get("icons.system_theme", "")
    
    @system_icon_theme.setter 
    def system_icon_theme(self, value: str) -> None:
        """Set system icon theme name."""
        self.set("icons.system_theme", value)
    
    @property
    def system_icon_size(self) -> int:
        """Get system icon size."""
        return self.get("icons.system_size", 48)
    
    @system_icon_size.setter
    def system_icon_size(self, value: int) -> None:
        """Set system icon size."""
        self.set("icons.system_size", value)
    
    @property
    def system_prefer_scalable(self) -> bool:
        """Get system icon scalable preference."""
        return self.get("icons.system_prefer_scalable", False)
    
    @system_prefer_scalable.setter
    def system_prefer_scalable(self, value: bool) -> None:
        """Set system icon scalable preference."""
        self.set("icons.system_prefer_scalable", value)
    
    @property
    def system_debug_logging(self) -> bool:
        """Get system icon debug logging setting."""
        return self.get("icons.system_debug_logging", False)
    
    @system_debug_logging.setter
    def system_debug_logging(self, value: bool) -> None:
        """Set system icon debug logging setting."""
        self.set("icons.system_debug_logging", value)
    
    @property
    def system_mode(self) -> str:
        """Get system icon resolution mode."""
        return self.get("icons.system_mode", "auto")
    
    @system_mode.setter
    def system_mode(self, value: str) -> None:
        """Set system icon resolution mode."""
        self.set("icons.system_mode", value)
    
    @property
    def system_mapping_file(self) -> str:
        """Get system icon mapping file path."""
        return self.get("icons.system_mapping_file", "")
    
    @system_mapping_file.setter
    def system_mapping_file(self, value: str) -> None:
        """Set system icon mapping file path."""
        self.set("icons.system_mapping_file", value)
    
    @property 
    def enable_sound(self) -> bool:
        """Get sound enablement status."""
        return self.get("enable_sound", True)
    
    @enable_sound.setter
    def enable_sound(self, value: bool) -> None:
        """Set sound enablement status."""
        self.set("enable_sound", value)
    
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get("notification.log_level", "INFO")
    
    @log_level.setter
    def log_level(self, value: str) -> None:
        """Set logging level."""
        self.set("notification.log_level", value)
    
    @property
    def log_icon_resolution(self) -> bool:
        """Get icon resolution logging setting."""
        result = self.get("notification.log_icon_resolution", False)
        return result
    
    @log_icon_resolution.setter
    def log_icon_resolution(self, value: bool) -> None:
        """Set icon resolution logging setting."""
        self.set("notification.log_icon_resolution", value)
    
    # ─────────────────────────────────────────────────────────────────
    # Backend-specific configuration
    # ─────────────────────────────────────────────────────────────────
    
    def get_backend_config(self, backend_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific backend.
        
        Args:
            backend_name: Name of the backend
            
        Returns:
            Backend configuration dictionary
        """
        return self.get(f"backends.{backend_name}", {})
    
    def get_dunst_command(self) -> str:
        """Get dunstify command path."""
        return self.get("backends.dunst.command", "dunstify")
    
    def get_console_use_colors(self) -> bool:
        """Get console backend color usage setting."""
        return self.get("backends.console.use_colors", True)
    
    def get_console_timestamp(self) -> bool:
        """Get console backend timestamp setting."""
        return self.get("backends.console.timestamp", True)


# ═══════════════════════════════════════════════════════════════════════════════
# Global configuration instance
# ═══════════════════════════════════════════════════════════════════════════════
_global_config: Optional[DesktopNotifyConfig] = None


def get_config(reload: bool = False) -> DesktopNotifyConfig:
    """
    Get the global configuration instance.
    
    Args:
        reload: Whether to force reload the configuration
        
    Returns:
        DesktopNotifyConfig instance
    """
    global _global_config
    
    if _global_config is None or reload:
        _global_config = DesktopNotifyConfig()
    
    if reload and _global_config:
        _global_config.reload()
    
    return _global_config