# ────────────────────────────────────────────────────────────────────────────────
# Configuration Loaders
# ────────────────────────────────────────────────────────────────────────────────
"""
loaders.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Configuration loaders for TOML files and environment variables.
"""

import os
import toml
from pathlib import Path
from typing import Any, Dict, Optional


class TOMLLoader:
    """Loader for TOML configuration files."""
    
    def load(self, file_path: Path) -> Dict[str, Any]:
        """Load configuration from a TOML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        except toml.TomlDecodeError as e:
            raise ValueError(f"Invalid TOML syntax in {file_path}: {e}")
        except IOError as e:
            raise FileNotFoundError(f"Cannot read configuration file {file_path}: {e}")


class EnvLoader:
    """
    ///////////////////////////////////////////////////////////////////
    ENVIRONMENT VARIABLE LOADER
    ▄▄▄▄ ▄▄ ▄▄▄ ▄▄ ▄▄▄▄ ▄▄▄  ▄▄▄ ▄▄▄▄▄
    █▄▄▄ ██ █▀▀ ██ █▄▄▄ █▀▀  █▀▀   █  
    █▄▄▄ ██ █▄▄ ██ █▄▄▄ █▄▄  █▄▄   █  
    ///////////////////////////////////////////////////////////////////
    Load configuration from environment variables with prefix support.
    """
    
    def __init__(self, prefix: str = ""):
        """
        Initialize environment loader.
        
        Args:
            prefix: Environment variable prefix (e.g., "DESKTOP_NOTIFY_")
        """
        self.prefix = prefix.upper().rstrip('_')
        if self.prefix:
            self.prefix += '_'
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        Environment variables are converted to nested dictionaries using
        double underscore (__) as section separators.
        
        Examples:
            DESKTOP_NOTIFY_BACKEND=dunst -> {"backend": "dunst"}
            DESKTOP_NOTIFY_ICONS__ICON_SET=material -> {"icons": {"icon_set": "material"}}
        """
        config = {}
        
        for env_key, env_value in os.environ.items():
            if not env_key.startswith(self.prefix):
                continue
            
            # Remove prefix and convert to lowercase
            config_key = env_key[len(self.prefix):].lower()
            
            # Handle nested configuration with double underscores
            key_parts = config_key.split('__')
            
            # Navigate/create nested structure
            current_dict = config
            for part in key_parts[:-1]:
                if part not in current_dict:
                    current_dict[part] = {}
                current_dict = current_dict[part]
            
            # Set the final value with type coercion
            final_key = key_parts[-1]
            current_dict[final_key] = self._coerce_env_value(env_value)
        
        return config
    
    def _coerce_env_value(self, value: str) -> Any:
        """
        ─────────────────────────────────────────────────────────────────
        Coerce environment variable string to appropriate type
        ─────────────────────────────────────────────────────────────────
        """
        # Handle boolean values
        if value.lower() in ('true', '1', 'yes', 'on'):
            return True
        elif value.lower() in ('false', '0', 'no', 'off'):
            return False
        
        # Handle numeric values
        try:
            # Try integer first
            if '.' not in value:
                return int(value)
            else:
                return float(value)
        except ValueError:
            pass
        
        # Handle comma-separated lists
        if ',' in value:
            return [item.strip() for item in value.split(',')]
        
        # Return as string
        return value