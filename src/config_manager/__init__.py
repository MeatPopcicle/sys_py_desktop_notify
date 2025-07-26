# ────────────────────────────────────────────────────────────────────────────────
# config_manager - Reusable TOML Configuration System
# ────────────────────────────────────────────────────────────────────────────────
"""
config_manager

A standalone, reusable configuration management system supporting:
- TOML configuration files with nested structures
- Environment variable overrides with dot notation
- Type validation and coercion
- Schema validation with defaults
- Multi-source configuration merging

This module can be extracted and used across multiple projects.
"""

from .core import ConfigManager
from .types import ConfigSchema, ConfigError
from .loaders import TOMLLoader, EnvLoader
from .validators import TypeValidator, SchemaValidator

__version__ = "1.0.0"
__all__ = [
    "ConfigManager",
    "ConfigSchema", 
    "ConfigError",
    "TOMLLoader",
    "EnvLoader",
    "TypeValidator",
    "SchemaValidator",
]