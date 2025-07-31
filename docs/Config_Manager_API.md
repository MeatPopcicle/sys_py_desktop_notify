# Config Manager API Reference

Complete API documentation for the Config Manager library used by Desktop Notify.

## 📋 Table of Contents

- [Core Functions](#core-functions)
- [ConfigManager Class](#configmanager-class)
- [Configuration Loading](#configuration-loading)
- [Validation System](#validation-system)
- [Type Definitions](#type-definitions)
- [Exceptions](#exceptions)

## 🚀 Core Functions

### `get_config()`

Get the global configuration instance.

```python
def get_config(config_file: Optional[str] = None) -> ConfigManager
```

**Parameters:**
- `config_file` (Optional[str]): Path to specific config file, or None for automatic discovery

**Returns:** `ConfigManager` instance with loaded configuration

**Example:**
```python
from config_manager import get_config

config = get_config()
print(f"Backend: {config.backend}")
print(f"Timeout: {config.timeout}")
```

### `find_config_file()`

Find configuration file using standard search paths.

```python
def find_config_file(filename: str = "config.toml") -> Optional[str]
```

**Parameters:**
- `filename` (str): Configuration filename to search for

**Returns:** Path to found config file, or `None` if not found

**Search Order:**
1. `./config.toml` - Current directory
2. `~/.config/desktop-notify/config.toml` - User config directory  
3. `/etc/desktop-notify/config.toml` - System config directory

## ⚙️ ConfigManager Class

Main configuration management class with automatic loading, validation, and environment variable support.

### Constructor

```python
class ConfigManager:
    def __init__(
        self,
        config_file: Optional[str] = None,
        environment_prefix: str = "DESKTOP_NOTIFY_",
        auto_load: bool = True
    )
```

**Parameters:**
- `config_file` (Optional[str]): Path to config file, or None for auto-discovery
- `environment_prefix` (str): Prefix for environment variable overrides
- `auto_load` (bool): Whether to automatically load configuration on init

### Core Methods

#### `load_config()`

Load configuration from file and environment variables.

```python
def load_config(self, config_file: Optional[str] = None) -> None
```

**Parameters:**
- `config_file` (Optional[str]): Specific config file path, or None for auto-discovery

**Example:**
```python
config = ConfigManager(auto_load=False)
config.load_config("/path/to/custom/config.toml")
```

#### `reload_config()`

Reload configuration from the current source.

```python
def reload_config(self) -> None
```

**Example:**
```python
config = get_config()
# Config file was modified externally
config.reload_config()
```

#### `get()`

Get configuration value with support for nested keys.

```python
def get(self, key: str, default: Any = None) -> Any
```

**Parameters:**
- `key` (str): Configuration key (supports dot notation for nested keys)
- `default` (Any): Default value if key not found

**Example:**
```python
# Simple key
backend = config.get("backend", "auto")

# Nested key
dunst_command = config.get("backends.dunst.command", "dunstify")
```

#### `set()`

Set configuration value with support for nested keys.

```python
def set(self, key: str, value: Any) -> None
```

**Parameters:**
- `key` (str): Configuration key (supports dot notation)
- `value` (Any): Value to set

**Example:**
```python
config.set("backend", "dunst")
config.set("backends.dunst.command", "/usr/local/bin/dunstify")
```

#### `has()`

Check if configuration key exists.

```python
def has(self, key: str) -> bool
```

**Parameters:**
- `key` (str): Configuration key to check

**Example:**
```python
if config.has("backends.libnotify"):
    # Configure libnotify backend
    pass
```

### Validation Methods

#### `validate()`

Validate all configuration values against schema.

```python
def validate(self) -> List[str]
```

**Returns:** List of validation error messages (empty if valid)

**Example:**
```python
config = get_config()
errors = config.validate()

if errors:
    for error in errors:
        print(f"Config error: {error}")
else:
    print("Configuration is valid")
```

#### `validate_key()`

Validate a specific configuration key.

```python
def validate_key(self, key: str) -> Optional[str]
```

**Parameters:**
- `key` (str): Configuration key to validate

**Returns:** Error message if invalid, `None` if valid

### Environment Variable Support

#### `get_env_override()`

Get environment variable override for a config key.

```python
def get_env_override(self, key: str) -> Optional[str]
```

**Parameters:**
- `key` (str): Configuration key

**Returns:** Environment variable value if set, `None` otherwise

**Example:**
```python
# For key "backend", checks DESKTOP_NOTIFY_BACKEND
backend_override = config.get_env_override("backend")
```

#### `list_env_overrides()`

List all active environment variable overrides.

```python
def list_env_overrides(self) -> Dict[str, str]
```

**Returns:** Dictionary of key -> environment value mappings

### Configuration Properties

The ConfigManager provides direct property access to common configuration values:

#### Core Settings

```python
@property
def backend(self) -> str
    """Notification backend preference ('auto', 'dunst', 'console')"""

@property  
def timeout(self) -> int
    """Default notification timeout in milliseconds"""

@property
def urgency(self) -> str
    """Default urgency level ('low', 'normal', 'critical')"""

@property
def log_icon_resolution(self) -> bool
    """Whether to log icon resolution details"""
```

#### Icon Settings

```python
@property
def icon_set(self) -> str
    """Icon set preference ('auto', 'system', 'material', 'minimal')"""

@property
def system_icon_theme(self) -> Optional[str]
    """System icon theme name"""

@property
def system_icon_size(self) -> int
    """System icon size in pixels"""

@property
def system_prefer_scalable(self) -> bool
    """Whether to prefer scalable icons"""

@property
def system_debug_logging(self) -> bool
    """Whether to enable system icon debug logging"""

@property
def system_mode(self) -> str
    """System icon resolution mode"""

@property
def system_mapping_file(self) -> str
    """Path to custom icon mapping file"""
```

## 📄 Configuration Loading

### File Format

Configuration files use TOML format:

```toml
# Core notification settings
[notification]
backend = "auto"
timeout = 3000
urgency = "normal"
log_icon_resolution = false

# Icon configuration
[icons]
icon_set = "auto"
icon_system_theme = "Papirus"
icon_system_size = 48

# Backend-specific settings
[backends.dunst]
command = "dunstify"
supports_markup = true

[backends.console]
use_colors = true
timestamp = true
```

### Environment Variables

Override any configuration value using environment variables with the `DESKTOP_NOTIFY_` prefix:

```bash
# Override core settings
export DESKTOP_NOTIFY_BACKEND=dunst
export DESKTOP_NOTIFY_TIMEOUT=5000
export DESKTOP_NOTIFY_URGENCY=critical

# Override nested settings  
export DESKTOP_NOTIFY_BACKENDS_DUNST_COMMAND=/usr/local/bin/dunstify
export DESKTOP_NOTIFY_ICONS_ICON_SET=material
```

### Loading Priority

Configuration values are resolved in this order (highest to lowest priority):

1. **Environment variables** - `DESKTOP_NOTIFY_*` variables
2. **Configuration file** - TOML file values
3. **Default values** - Built-in defaults

## ✅ Validation System

### Built-in Validators

The config manager includes validators for common types:

#### String Validation

```python
from config_manager.validators import validate_string

# Validate with choices
validate_string("backend", "dunst", choices=["auto", "dunst", "console"])

# Validate with pattern
validate_string("theme", "Papirus", pattern=r"^[A-Za-z][A-Za-z0-9_-]*$")
```

#### Integer Validation

```python
from config_manager.validators import validate_int

# Validate with range
validate_int("timeout", 3000, min_value=0, max_value=60000)

# Validate with specific values
validate_int("size", 48, allowed=[16, 24, 32, 48, 64, 128])
```

#### Boolean Validation

```python
from config_manager.validators import validate_bool

validate_bool("log_icon_resolution", True)
```

#### Path Validation

```python
from config_manager.validators import validate_path

# Validate file exists
validate_path("config_file", "/path/to/config.toml", must_exist=True)

# Validate directory
validate_path("cache_dir", "/tmp/cache", is_directory=True)
```

### Custom Validators

```python
from config_manager.validators import register_validator

def validate_urgency(key: str, value: Any) -> Optional[str]:
    """Custom urgency validator."""
    valid_urgencies = ["low", "normal", "critical"]
    if value not in valid_urgencies:
        return f"Invalid urgency '{value}'. Must be one of: {valid_urgencies}"
    return None

# Register custom validator
register_validator("urgency", validate_urgency)
```

## 📝 Type Definitions

### ConfigValue

```python
ConfigValue = Union[str, int, bool, float, List[Any], Dict[str, Any]]
```

Represents any valid configuration value type.

### ConfigDict

```python
ConfigDict = Dict[str, ConfigValue]
```

Dictionary containing configuration key-value pairs.

### ValidationError

```python
@dataclass
class ValidationError:
    key: str                    # Configuration key that failed
    value: Any                  # Invalid value
    message: str                # Error description
    validator: str              # Validator that failed
```

## ⚠️ Exceptions

### ConfigError

Base exception for all configuration errors.

```python
class ConfigError(Exception):
    """Base configuration error."""
    pass
```

### ConfigFileError

Raised when configuration file cannot be loaded or parsed.

```python
class ConfigFileError(ConfigError):
    """Configuration file error."""
    
    def __init__(self, file_path: str, message: str):
        self.file_path = file_path
        super().__init__(f"Config file '{file_path}': {message}")
```

### ConfigValidationError

Raised when configuration validation fails.

```python
class ConfigValidationError(ConfigError):
    """Configuration validation error."""
    
    def __init__(self, errors: List[ValidationError]):
        self.errors = errors
        error_msgs = [f"{e.key}: {e.message}" for e in errors]
        super().__init__(f"Validation errors: {'; '.join(error_msgs)}")
```

---

## 📚 Usage Examples

### Basic Configuration

```python
from config_manager import get_config

# Get configuration
config = get_config()

# Access values
backend = config.backend
timeout = config.timeout
icon_set = config.icon_set

print(f"Using backend: {backend}")
print(f"Default timeout: {timeout}ms")
```

### Custom Configuration File

```python
from config_manager import ConfigManager

# Load specific config file
config = ConfigManager("/path/to/custom/config.toml")

# Validate configuration
errors = config.validate()
if errors:
    for error in errors:
        print(f"Error: {error}")
else:
    print("Configuration is valid")
```

### Environment Variable Overrides

```python
import os
from config_manager import get_config

# Set environment override
os.environ["DESKTOP_NOTIFY_BACKEND"] = "console"
os.environ["DESKTOP_NOTIFY_TIMEOUT"] = "5000"

# Load config (will use environment overrides)
config = get_config()

print(f"Backend: {config.backend}")  # Will be "console"
print(f"Timeout: {config.timeout}")  # Will be 5000

# List active overrides
overrides = config.list_env_overrides()
for key, value in overrides.items():
    print(f"Override: {key} = {value}")
```

### Dynamic Configuration

```python
from config_manager import ConfigManager

config = ConfigManager()

# Get with fallback
backend = config.get("backend", "auto")

# Set value
config.set("backend", "dunst")

# Check if key exists
if config.has("backends.dunst.command"):
    command = config.get("backends.dunst.command")
    print(f"Dunst command: {command}")

# Nested configuration
config.set("backends.libnotify.app_name", "MyApp")
app_name = config.get("backends.libnotify.app_name")
```

### Configuration Validation

```python
from config_manager import get_config, ConfigValidationError

try:
    config = get_config()
    
    # Validate all settings
    errors = config.validate()
    
    if errors:
        print("Configuration issues found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration is valid")
        
except ConfigValidationError as e:
    print(f"❌ Configuration validation failed:")
    for error in e.errors:
        print(f"  - {error.key}: {error.message}")
```

---

*Config Manager v1.0.0 - API Reference*