# ────────────────────────────────────────────────────────────────────────────────
# Core Configuration Management Classes
# ────────────────────────────────────────────────────────────────────────────────
"""
core.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Core configuration management classes providing TOML loading, environment
variable overrides, and type validation.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from .types import ConfigSchema, ConfigError
from .loaders import TOMLLoader, EnvLoader
from .validators import TypeValidator, SchemaValidator


class ConfigManager:
    """
    ///////////////////////////////////////////////////////////////////
    CONFIGURATION MANAGER
    ▄▄▄▄▄ ▄▄▄  ▄▄▄ ▄▄▄▄ ▄▄▄ ▄▄▄▄  
    █   █ █▀▀  █▀▀ █▄▄▄ █   █▄▄▄  
    █▄▄▄█ █▄▄  █▄▄ █▄▄▄ █▄▄ █▄▄▄  
    ///////////////////////////////////////////////////////////////////
    Unified configuration management with TOML files and env overrides.
    """
    
    def __init__(
        self,
        config_paths:    Optional[List[Union[str, Path]]] = None,
        env_prefix:      str = "",
        schema:          Optional[ConfigSchema] = None,
        auto_load:       bool = True
    ):
        # ─────────────────────────────────────────────────────────────────
        # Initialize core properties
        # ─────────────────────────────────────────────────────────────────
        self.config_paths    = [Path(p) for p in (config_paths or [])]
        self.env_prefix      = env_prefix
        self.schema          = schema
        self.logger          = logging.getLogger(__name__)
        
        # ─────────────────────────────────────────────────────────────────
        # Initialize loaders and validators
        # ─────────────────────────────────────────────────────────────────
        self.toml_loader     = TOMLLoader()
        self.env_loader      = EnvLoader(prefix=env_prefix)
        self.type_validator  = TypeValidator()
        self.schema_validator = SchemaValidator()
        
        # ─────────────────────────────────────────────────────────────────
        # Configuration storage
        # ─────────────────────────────────────────────────────────────────
        self._config_data:   Dict[str, Any] = {}
        self._source_map:    Dict[str, str] = {}  # Track where each value came from
        
        if auto_load:
            self.load()
    
    def add_config_path(self, path: Union[str, Path]) -> None:
        """Add a configuration file path to the search list."""
        config_path = Path(path)
        if config_path not in self.config_paths:
            self.config_paths.append(config_path)
    
    def load(self) -> Dict[str, Any]:
        """
        ─────────────────────────────────────────────────────────────────
        Load configuration from all sources
        ─────────────────────────────────────────────────────────────────
        Load and merge configuration from TOML files and environment variables.
        """
        merged_config = {}
        
        # ─────────────────────────────────────────────────────────────────
        # Load from TOML files (in order)
        # ─────────────────────────────────────────────────────────────────
        for config_path in self.config_paths:
            if config_path.exists():
                try:
                    toml_data = self.toml_loader.load(config_path)
                    self._merge_config(merged_config, toml_data, source=str(config_path))
                    self.logger.debug(f"Loaded configuration from: {config_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to load {config_path}: {e}")
            else:
                self.logger.debug(f"Configuration file not found: {config_path}")
        
        # ─────────────────────────────────────────────────────────────────
        # Apply environment variable overrides
        # ─────────────────────────────────────────────────────────────────
        env_overrides = self.env_loader.load()
        if env_overrides:
            self._merge_config(merged_config, env_overrides, source="environment")
            self.logger.debug(f"Applied {len(env_overrides)} environment overrides")
        
        # ─────────────────────────────────────────────────────────────────
        # Apply schema defaults and validate
        # ─────────────────────────────────────────────────────────────────
        if self.schema:
            merged_config = self._apply_schema_defaults(merged_config)
            self.schema_validator.validate(merged_config, self.schema)
        
        self._config_data = merged_config
        return self._config_data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'section.key')."""
        keys = key.split('.')
        current = self._config_data
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any, source: str = "runtime") -> None:
        """Set configuration value using dot notation."""
        keys = key.split('.')
        current = self._config_data
        
        # Navigate to parent of target key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the final value
        current[keys[-1]] = value
        self._source_map[key] = source
    
    def has(self, key: str) -> bool:
        """Check if configuration key exists."""
        return self.get(key) is not None
    
    def get_source(self, key: str) -> Optional[str]:
        """Get the source of a configuration value."""
        return self._source_map.get(key)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the complete configuration as a dictionary."""
        return self._config_data.copy()
    
    def _merge_config(self, target: Dict[str, Any], source: Dict[str, Any], source_name: str) -> None:
        """Merge source configuration into target, tracking sources."""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                # Recursively merge dictionaries
                self._merge_config(target[key], value, source_name)
            else:
                # Override with new value
                target[key] = value
                self._source_map[key] = source_name
    
    def _apply_schema_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values from schema."""
        if not self.schema:
            return config
        
        # Apply top-level defaults
        for key, default_value in self.schema.defaults.items():
            if key not in config:
                config[key] = default_value
                self._source_map[key] = "schema_default"
        
        # Apply nested schema defaults
        for section_name, nested_schema in self.schema.nested_schemas.items():
            if section_name not in config:
                config[section_name] = {}
            
            # Recursively apply nested defaults
            for key, default_value in nested_schema.defaults.items():
                if key not in config[section_name]:
                    config[section_name][key] = default_value
                    self._source_map[f"{section_name}.{key}"] = "schema_default"
        
        return config