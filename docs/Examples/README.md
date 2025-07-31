# Desktop Notify Examples

Collection of practical examples demonstrating the Desktop Notify library.

## 📁 Examples Overview

| Example | Description | Features |
|---------|-------------|----------|
| [Basic Usage](basic_usage.py) | Simple notification examples | Core API, urgency levels, timeouts |
| [Interactive Actions](interactive_actions.py) | Action buttons and callbacks | User interaction, decision dialogs |
| [Application Integration](application_integration.py) | Real app integration patterns | Progress updates, error handling |
| [File Operations](file_operations.py) | File download/upload notifications | Action buttons, file operations |
| [System Monitoring](system_monitoring.py) | System alerts and monitoring | Resource monitoring, thresholds |
| [Build System](build_system.py) | CI/CD and build notifications | Build status, error reporting |
| [Voice Recording](voice_recording.py) | Audio recording workflow | State management, user controls |
| [Custom Backend](custom_backend.py) | Creating custom backends | Backend development, extensibility |
| [Icon Management](icon_management.py) | Icon set usage and management | Icon sets, resolution, fallbacks |
| [Configuration](configuration_examples.py) | Configuration examples | Runtime config, environment vars |

## 🚀 Running Examples

### Prerequisites

```bash
# Install desktop-notify
pip install desktop-notify

# Ensure notification daemon is running (Linux)
# For Dunst:
sudo apt install dunst  # Ubuntu/Debian
sudo pacman -S dunst    # Arch Linux
```

### Basic Example

```bash
python basic_usage.py
```

### Interactive Example

```bash
python interactive_actions.py
```

## 📖 Example Categories

### 🔔 Basic Notifications
- Simple notifications
- Urgency levels  
- Timeout control
- Icon usage

### 🎯 Interactive Features
- Action buttons
- User callbacks
- Decision dialogs
- Confirmation prompts

### 🔧 Application Integration
- Progress notifications
- Error handling
- State management
- Notification updates

### 🎨 Customization
- Icon management
- Backend selection
- Configuration
- Custom backends

## 💡 Usage Tips

1. **Start Simple**: Begin with `basic_usage.py` to understand core concepts
2. **Interactive Features**: Try `interactive_actions.py` for action button examples
3. **Real Applications**: Study `application_integration.py` for production patterns
4. **Customization**: Explore `custom_backend.py` for extending functionality

## 🔗 Quick Links

- **[API Reference](../API_Reference.md)** - Complete API documentation
- **[User Guide](../User_Guide.md)** - Installation and setup
- **[Configuration Guide](../Configuration_Guide.md)** - Configuration options

---

*Desktop Notify v1.0.0 - Examples Collection*