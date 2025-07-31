# Desktop Notify Documentation

Comprehensive documentation for the Python Desktop Notify library - a unified, backend-agnostic desktop notification system for Linux.

## 📚 Documentation Structure

### API References
- **[Desktop Notify API](Desktop_Notify_API.md)** - Complete API documentation for desktop notification system
- **[Config Manager API](Config_Manager_API.md)** - Complete API documentation for configuration management

### User Documentation
- **[User Guide](User_Guide.md)** - Getting started and common usage patterns  
- **[Configuration Guide](Configuration_Guide.md)** - Configuration options and customization

### Development Resources
- **[Backend Development](Backend_Development.md)** - Creating custom notification backends
- **[Icon Set Development](Icon_Set_Development.md)** - Building custom icon sets
- **[Examples](Examples/)** - Code examples and use cases

## 🚀 Quick Start

```python
from desktop_notify import send_notification

# Simple notification
send_notification("info", "Hello", "Desktop notifications working!")

# Interactive notification with actions
actions = {"yes": "Accept", "no": "Decline"}
result = send_notification(
    icon="question",
    title="Incoming Call", 
    message="John Doe is calling...",
    actions=actions
)

if result == "yes":
    print("Call accepted")
elif result == "no":
    print("Call declined")
else:
    print("No action taken")
```

## 🎯 Key Features

- **Backend Agnostic**: Supports Dunst, libnotify, console fallback
- **Rich Icon Support**: System icons, Material Design, NerdFonts, Unicode
- **Interactive Actions**: Clickable buttons with callback support
- **Smart Configuration**: TOML config with environment variable overrides
- **Zero Dependencies**: Works out of the box on most Linux systems

## 📖 Documentation Navigation

| Document | Description |
|----------|-------------|
| [Desktop Notify API](Desktop_Notify_API.md) | Complete desktop notification API documentation |
| [Config Manager API](Config_Manager_API.md) | Complete configuration management API documentation |
| [User Guide](User_Guide.md) | Installation, setup, and usage examples |
| [Configuration Guide](Configuration_Guide.md) | Configuration file format and options |
| [Backend Development](Backend_Development.md) | Creating custom notification backends |
| [Icon Set Development](Icon_Set_Development.md) | Building custom icon sets |

## 🔧 System Requirements

- **Python**: 3.8+
- **Linux Distribution**: Any modern Linux distro
- **Notification Daemon**: Dunst (recommended) or any freedesktop.org compatible daemon
- **Optional**: SystemIconSet requires `icon-mapper` library

## 💡 Support

- **Issues**: Report bugs on the GitHub issue tracker
- **Examples**: See the `Examples/` directory for working code samples
- **Configuration**: Check `Configuration_Guide.md` for setup help

---

*Generated with Desktop Notify v1.0.0*