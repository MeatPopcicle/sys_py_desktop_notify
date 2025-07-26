# ────────────────────────────────────────────────────────────────────────────────
# Configuration Types and Exceptions
# ────────────────────────────────────────────────────────────────────────────────
"""
types.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Type definitions and exceptions for configuration management.
"""

from typing import Any, Dict, List, Type
from dataclasses import dataclass, field


class ConfigError(Exception):
    """Base exception for configuration-related errors."""
    pass


@dataclass
class ConfigSchema:
    """Schema definition for configuration validation."""
    
    # ─────────────────────────────────────────────────────────────────
    # Schema Definition
    # ─────────────────────────────────────────────────────────────────
    fields:          Dict[str, Type] = field(default_factory=dict)
    defaults:        Dict[str, Any] = field(default_factory=dict)
    required:        List[str] = field(default_factory=list)
    nested_schemas:  Dict[str, 'ConfigSchema'] = field(default_factory=dict)
    
    def add_field(self, name: str, field_type: Type, default: Any = None, required: bool = False):
        """Add a field to the schema."""
        self.fields[name] = field_type
        if default is not None:
            self.defaults[name] = default
        if required:
            self.required.append(name)
    
    def add_nested_schema(self, name: str, schema: 'ConfigSchema'):
        """Add a nested schema for complex configuration sections."""
        self.nested_schemas[name] = schema