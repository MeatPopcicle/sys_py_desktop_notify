# Desktop Notify Configuration Guide

Complete guide to configuring the Python Desktop Notify library.

## 📋 Table of Contents

- [Configuration Overview](#configuration-overview)
- [Configuration File](#configuration-file)
- [Environment Variables](#environment-variables)
- [Runtime Configuration](#runtime-configuration)
- [Backend Configuration](#backend-configuration)
- [Icon Configuration](#icon-configuration)
- [Advanced Settings](#advanced-settings)
- [Configuration Examples](#configuration-examples)

## 🔧 Configuration Overview

Desktop Notify supports multiple configuration methods with the following priority (highest to lowest):

1. **Runtime parameters** - Direct function/class arguments
2. **Environment variables** - OS environment settings
3. **Configuration file** - TOML config file
4. **Default values** - Built-in defaults

### Configuration Locations

The library searches for configuration files in this order:

1. `./config.toml` - Current directory
2. `~/.config/desktop-notify/config.toml` - User config directory
3. `/etc/desktop-notify/config.toml` - System config directory

## 📄 Configuration File

### Basic Configuration

Create `~/.config/desktop-notify/config.toml`:

```toml
# ────────────────────────────────────────────────────────────────────────────────
# Desktop Notify Configuration
# ────────────────────────────────────────────────────────────────────────────────

[notification]
# Backend preference ("auto", "dunst", "console", "libnotify")
backend = "auto"

# Default timeout in milliseconds (None = backend default, 0 = persistent)
timeout = 3000

# Default urgency level ("low", "normal", "critical")
urgency = "normal"

# Enable icon resolution logging
log_icon_resolution = false

[icons]
# Icon set preference ("auto", "system", "material", "minimal", "nerdfonts")
icon_set = "auto"

# System icon theme (for SystemIconSet)
icon_system_theme = "Papirus"

# System icon size in pixels
icon_system_size = 48

# Icon cache TTL in seconds
icon_cache_ttl = 3600

[backends.dunst]
# Dunstify command path/name
command = "dunstify"

# Enable markup support
supports_markup = true

# Maximum action timeout (milliseconds)
max_action_timeout = 30000

[backends.console]
# Use ANSI colors in output
use_colors = true

# Include timestamps in output
timestamp = true

# Output destination ("stderr", "stdout")
output = "stderr"

[backends.libnotify]
# Application name for notifications
app_name = "desktop-notify"

# Enable sound notifications
enable_sound = false

[logging]
# Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
level = "WARNING"

# Log file path (None = no file logging)
file = null

# Log format string
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Minimal Configuration

```toml
[notification]
backend = "dunst"
timeout = 5000

[icons]
icon_set = "material"
```

## 🌍 Environment Variables

Override any configuration setting using environment variables with the `DESKTOP_NOTIFY_` prefix:

### Core Settings

```bash
# Backend preference
export DESKTOP_NOTIFY_BACKEND=dunst

# Icon set preference  
export DESKTOP_NOTIFY_ICON_SET=material

# Default timeout (milliseconds)
export DESKTOP_NOTIFY_TIMEOUT=4000

# Default urgency
export DESKTOP_NOTIFY_URGENCY=normal

# Enable icon resolution logging
export DESKTOP_NOTIFY_LOG_ICON_RESOLUTION=true
```

### Backend-Specific Settings

```bash
# Dunst backend
export DESKTOP_NOTIFY_DUNST_COMMAND=dunstify
export DESKTOP_NOTIFY_DUNST_SUPPORTS_MARKUP=true

# Console backend
export DESKTOP_NOTIFY_CONSOLE_USE_COLORS=false
export DESKTOP_NOTIFY_CONSOLE_TIMESTAMP=true

# Logging
export DESKTOP_NOTIFY_LOGGING_LEVEL=DEBUG
```

### Complete Environment Example

```bash
#!/bin/bash
# Desktop Notify Environment Configuration

# Core notification settings
export DESKTOP_NOTIFY_BACKEND=dunst
export DESKTOP_NOTIFY_TIMEOUT=5000
export DESKTOP_NOTIFY_URGENCY=normal

# Icon settings
export DESKTOP_NOTIFY_ICON_SET=material
export DESKTOP_NOTIFY_ICON_SYSTEM_THEME=Papirus
export DESKTOP_NOTIFY_ICON_SYSTEM_SIZE=64

# Backend customization
export DESKTOP_NOTIFY_DUNST_COMMAND=/usr/local/bin/dunstify
export DESKTOP_NOTIFY_CONSOLE_USE_COLORS=true

# Debug settings
export DESKTOP_NOTIFY_LOG_ICON_RESOLUTION=true
export DESKTOP_NOTIFY_LOGGING_LEVEL=INFO

echo "Desktop Notify environment configured"
```

## ⚡ Runtime Configuration

### NotificationManager Configuration

```python
from desktop_notify import NotificationManager

# Basic runtime configuration
manager = NotificationManager(
    backend="dunst",
    icon_set="material",
    timeout=4000,
    urgency="normal"
)

# Advanced configuration with backend options
manager = NotificationManager(
    backend="dunst",
    icon_set="system",
    timeout=5000,
    urgency="low",
    # Backend-specific options
    dunst_command="dunstify",
    console_use_colors=True,
    icon_system_theme="Papirus",
    icon_system_size=64
)
```

### Dynamic Configuration Changes

```python
# Create manager with defaults
manager = NotificationManager()

# Check current configuration
info = manager.get_backend_info()
print(f"Current backend: {info['name']}")

# Switch backends at runtime
if manager.switch_backend("console"):
    print("Switched to console backend")

# Switch icon sets at runtime
if manager.switch_icon_set("minimal"):
    print("Switched to minimal icons")

# Send with custom settings
manager.send(
    icon="save",
    title="Custom Settings",
    message="Using runtime configuration",
    timeout=8000,
    urgency="critical"
)
```

## 🔌 Backend Configuration

### Dunst Backend

```toml
[backends.dunst]
# Command to run (dunstify path)
command = "dunstify"

# Enable Pango markup support
supports_markup = true

# Maximum timeout for action notifications (ms)
max_action_timeout = 30000

# Default hints to add
default_hints = [
    "string:category:desktop-notify",
    "string:desktop-entry:desktop-notify"
]
```

**Runtime Configuration:**
```python
from desktop_notify.backends.dunst import DunstBackend

backend = DunstBackend(command="/usr/local/bin/dunstify")
manager = NotificationManager(backend=backend)
```

### Console Backend

```toml
[backends.console]
# Use ANSI color codes
use_colors = true

# Include timestamps
timestamp = true

# Output destination
output = "stderr"  # or "stdout"

# Custom color scheme
[backends.console.colors]
reset = "\033[0m"
bold = "\033[1m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
```

**Runtime Configuration:**
```python
from desktop_notify.backends.console import ConsoleBackend

backend = ConsoleBackend(
    use_colors=True,
    timestamp=True
)
manager = NotificationManager(backend=backend)

# Dynamic color control
backend.set_colors_enabled(False)  # Disable colors
backend.set_timestamp_enabled(False)  # Disable timestamps
```

### Custom Backend Configuration

```python
# Custom backend with configuration
class EmailBackend(NotificationBackend):
    def __init__(self, smtp_server, email, password):
        self.smtp_server = smtp_server
        self.email = email
        self.password = password
    
    # Implementation...

# Use custom backend
email_backend = EmailBackend(
    smtp_server="smtp.gmail.com",
    email="alerts@myapp.com", 
    password="app_password"
)

manager = NotificationManager(backend=email_backend)
```

## 🎨 Icon Configuration

### System Icon Set

```toml
[icons]
icon_set = "system"

# Icon theme name (must be installed)
icon_system_theme = "Papirus"

# Icon size in pixels
icon_system_size = 48

# Search paths for icons
icon_system_paths = [
    "/usr/share/icons",
    "~/.local/share/icons",
    "~/.icons"
]

# Fallback themes if primary not found
icon_system_fallbacks = ["hicolor", "Adwaita"]
```

### Material Icon Set

```toml
[icons]
icon_set = "material"

# Material icon variant
material_variant = "filled"  # filled, outlined, round, sharp, two-tone

# Material icon size
material_size = "24dp"  # 18dp, 24dp, 36dp, 48dp

# Custom material icons directory
material_icons_dir = "~/.local/share/desktop-notify/material-icons"
```

### Icon Cache Configuration

```toml
[icons]
# Enable icon caching
enable_cache = true

# Cache TTL in seconds
cache_ttl = 3600

# Maximum cache size (number of icons)
cache_max_size = 1000

# Cache directory
cache_dir = "~/.cache/desktop-notify/icons"
```

### Runtime Icon Configuration

```python
from desktop_notify.iconsets.manager import get_icon_set_manager

# Get icon manager
icon_manager = get_icon_set_manager()

# Configure system icon set
icon_manager.configure_system_icons(
    theme="Papirus",
    size=64,
    search_paths=["/usr/share/icons", "~/.icons"]
)

# List available themes
themes = icon_manager.list_system_themes()
print(f"Available themes: {themes}")

# Preview icon set
preview = icon_manager.preview_icon_set("material")
for name, path in preview.items():
    print(f"{name}: {path}")
```

## ⚙️ Advanced Settings

### Logging Configuration

```toml
[logging]
# Global logging level
level = "WARNING"

# Log to file
file = "~/.local/share/desktop-notify/desktop-notify.log"

# Log rotation
max_bytes = 1048576  # 1MB
backup_count = 3

# Log format
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Module-specific levels
[logging.modules]
"desktop_notify.backends" = "INFO"
"desktop_notify.iconsets" = "DEBUG"
```

### Performance Settings

```toml
[performance]
# Icon resolution cache
icon_cache_enabled = true
icon_cache_size = 500
icon_cache_ttl = 1800

# Backend discovery cache
backend_cache_enabled = true
backend_cache_ttl = 300

# Async notification sending
async_enabled = false
max_concurrent_notifications = 5

# Timeout settings
default_timeout = 3000
max_timeout = 60000
min_timeout = 100
```

### Security Settings

```toml
[security]
# Allowed commands for backends
allowed_commands = [
    "dunstify",
    "/usr/bin/dunstify",
    "/usr/local/bin/dunstify"
]

# Allowed icon paths
allowed_icon_paths = [
    "/usr/share/icons",
    "~/.local/share/icons",
    "~/.icons"
]

# Disable shell command execution
disable_shell_commands = false

# Maximum message length
max_message_length = 1000
max_title_length = 100
```

## 📚 Configuration Examples

### Development Environment

```toml
# config.toml for development
[notification]
backend = "console"
timeout = 2000
urgency = "normal"
log_icon_resolution = true

[icons]
icon_set = "minimal"

[backends.console]
use_colors = true
timestamp = true

[logging]
level = "DEBUG"
format = "%(name)s:%(lineno)d - %(levelname)s - %(message)s"
```

### Production Server

```toml
# config.toml for headless server
[notification]
backend = "console"
timeout = 5000
urgency = "normal"

[icons]
icon_set = "minimal"

[backends.console]
use_colors = false
timestamp = true
output = "stdout"

[logging]
level = "ERROR"
file = "/var/log/desktop-notify.log"
```

### Desktop Application

```toml
# config.toml for desktop app
[notification]
backend = "auto"
timeout = 4000
urgency = "normal"

[icons]
icon_set = "system"
icon_system_theme = "Papirus"
icon_system_size = 48

[backends.dunst]
command = "dunstify"
supports_markup = true

[performance]
icon_cache_enabled = true
icon_cache_size = 200
```

### Multi-Backend Setup

```toml
# config.toml with backend preferences
[notification]
backend = "auto"

# Backend priority order
backend_priority = ["dunst", "libnotify", "console"]

[backends.dunst]
command = "dunstify"
priority = 90

[backends.libnotify] 
app_name = "MyApplication"
priority = 80

[backends.console]
use_colors = true
priority = 10
```

### Environment-Specific Configs

#### Development (config-dev.toml)
```toml
[notification]
backend = "console"
log_icon_resolution = true

[logging]
level = "DEBUG"
```

#### Testing (config-test.toml)
```toml
[notification]
backend = "console"
timeout = 1000

[backends.console]
use_colors = false
```

#### Production (config-prod.toml)
```toml
[notification]
backend = "auto"
timeout = 3000

[logging]
level = "WARNING"
file = "/var/log/myapp-notifications.log"
```

**Usage:**
```python
import os
from desktop_notify import NotificationManager

# Load environment-specific config
env = os.getenv("APP_ENV", "dev")
config_file = f"config-{env}.toml"

manager = NotificationManager(config_file=config_file)
```

### Configuration Validation

```python
from desktop_notify.config import validate_config, ConfigError

try:
    config = validate_config("config.toml")
    print("✅ Configuration valid")
except ConfigError as e:
    print(f"❌ Configuration error: {e}")
```

### Configuration Schema

```python
# Get configuration schema
from desktop_notify.config import get_config_schema

schema = get_config_schema()
print("Configuration options:")
for section, options in schema.items():
    print(f"[{section}]")
    for option, details in options.items():
        print(f"  {option} = {details['default']} # {details['description']}")
```

---

## 🔍 Configuration Debugging

### Check Current Configuration

```python
from desktop_notify.config import get_config

config = get_config()
print(f"Backend: {config.backend}")
print(f"Icon set: {config.icon_set}")
print(f"Timeout: {config.timeout}")
print(f"Config file: {config.config_file}")
```

### Environment Variable Check

```bash
# List all desktop-notify environment variables
env | grep DESKTOP_NOTIFY

# Check specific variable
echo $DESKTOP_NOTIFY_BACKEND
```

### Configuration File Location

```python
from desktop_notify.config import find_config_file

config_path = find_config_file()
if config_path:
    print(f"Using config file: {config_path}")
else:
    print("No config file found, using defaults")
```

---

*Desktop Notify v1.0.0 - Configuration Guide*