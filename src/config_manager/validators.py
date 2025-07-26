# ────────────────────────────────────────────────────────────────────────────────
# Configuration Validators
# ────────────────────────────────────────────────────────────────────────────────
"""
validators.py
AUTHOR: Desktop Notify Team
DATE: 2024-01-15
VERSION: 1.0.0

Configuration validation classes for type checking and schema validation.
"""

from typing import Any, Dict, List, Type, Union
from .types import ConfigSchema, ConfigError


class TypeValidator:
    """Validates and coerces configuration values to expected types."""
    
    def validate_type(self, value: Any, expected_type: Type) -> Any:
        """
        Validate and coerce a value to the expected type.
        
        Args:
            value: The value to validate
            expected_type: The expected type
            
        Returns:
            The coerced value
            
        Raises:
            ConfigError: If value cannot be coerced to expected type
        """
        if isinstance(value, expected_type):
            return value
        
        # Handle common type coercions
        try:
            if expected_type == bool:
                return self._coerce_bool(value)
            elif expected_type == int:
                return int(value)
            elif expected_type == float:
                return float(value)
            elif expected_type == str:
                return str(value)
            elif expected_type == list:
                return self._coerce_list(value)
            elif expected_type == dict:
                return self._coerce_dict(value)
            else:
                # For complex types, try direct conversion
                return expected_type(value)
        except (ValueError, TypeError) as e:
            raise ConfigError(
                f"Cannot convert '{value}' (type {type(value).__name__}) "
                f"to {expected_type.__name__}: {e}"
            )
    
    def _coerce_bool(self, value: Any) -> bool:
        """Coerce various types to boolean."""
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(value, (int, float)):
            return bool(value)
        else:
            raise ValueError(f"Cannot coerce {type(value).__name__} to bool")
    
    def _coerce_list(self, value: Any) -> List[Any]:
        """Coerce value to list."""
        if isinstance(value, list):
            return value
        elif isinstance(value, (tuple, set)):
            return list(value)
        elif isinstance(value, str):
            # Handle comma-separated strings
            return [item.strip() for item in value.split(',')]
        else:
            return [value]
    
    def _coerce_dict(self, value: Any) -> Dict[str, Any]:
        """Coerce value to dictionary."""
        if isinstance(value, dict):
            return value
        else:
            raise ValueError(f"Cannot coerce {type(value).__name__} to dict")


class SchemaValidator:
    """
    ///////////////////////////////////////////////////////////////////
    SCHEMA VALIDATOR
    ▄▄▄▄▄ ▄▄▄▄ ▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄
    █▄▄▄▄ █    ██ █▀▀   █   █▀▀
    ▄▄▄▄█ █▄▄▄ ██ █▄▄   █   █▄▄
    ///////////////////////////////////////////////////////////////////
    Validates configuration against a defined schema.
    """
    
    def __init__(self):
        self.type_validator = TypeValidator()
    
    def validate(self, config: Dict[str, Any], schema: ConfigSchema) -> Dict[str, Any]:
        """
        Validate configuration against schema.
        
        Args:
            config: Configuration dictionary to validate
            schema: Schema to validate against
            
        Returns:
            Validated and coerced configuration
            
        Raises:
            ConfigError: If validation fails
        """
        validated_config = {}
        
        # ─────────────────────────────────────────────────────────────────
        # Check required fields
        # ─────────────────────────────────────────────────────────────────
        for required_field in schema.required:
            if required_field not in config:
                raise ConfigError(f"Required configuration field missing: {required_field}")
        
        # ─────────────────────────────────────────────────────────────────
        # Validate and coerce field types
        # ─────────────────────────────────────────────────────────────────
        for field_name, field_type in schema.fields.items():
            if field_name in config:
                try:
                    validated_config[field_name] = self.type_validator.validate_type(
                        config[field_name], field_type
                    )
                except ConfigError as e:
                    raise ConfigError(f"Invalid value for '{field_name}': {e}")
        
        # ─────────────────────────────────────────────────────────────────
        # Validate nested schemas
        # ─────────────────────────────────────────────────────────────────
        for section_name, nested_schema in schema.nested_schemas.items():
            if section_name in config:
                if not isinstance(config[section_name], dict):
                    raise ConfigError(
                        f"Configuration section '{section_name}' must be a dictionary"
                    )
                
                validated_config[section_name] = self.validate(
                    config[section_name], nested_schema
                )
        
        # ─────────────────────────────────────────────────────────────────
        # Copy any additional fields not in schema
        # ─────────────────────────────────────────────────────────────────
        for key, value in config.items():
            if key not in validated_config:
                validated_config[key] = value
        
        return validated_config